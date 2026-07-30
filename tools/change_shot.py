#!/usr/bin/env python3
"""Chup anh truoc/sau cho mot thay doi trong bao cao, co highlight vung khac biet.

Chi phu thuoc pdftotext + pdftoppm (poppler) va thu vien chuan Python.

Vi du:
    python3 tools/change_shot.py \
        --before /tmp/before.pdf --after final/main.pdf \
        --text-before "quan ly phong tro cho thue" \
        --text-after  "quan ly bai dang cho thue phong tro" \
        --label ch6-quan-ly-bai-dang \
        --outdir .change-shots

Moi lan sua duoc ghi vao mot thu muc rieng, danh so tang dan:

    .change-shots/01-ch6-quan-ly-bai-dang/{before,after,compare}.png
"""

import argparse
import os
import re
import struct
import subprocess
import sys
import tempfile
import unicodedata
import zlib

DPI = 130
TINT = (255, 226, 66)      # vang highlight
TINT_ALPHA = 0.30
BORDER = (222, 96, 26)     # cam vien
BORDER_W = 3
PAD = 8                    # padding quanh bbox (px)
CROP_PAD = 46              # padding doc khi cat vung quan tam
ROW_GAP = 24               # khoang trong toi da de gop 2 dai thay doi
MIN_PIXELS_PER_ROW = 3     # loc nhieu khu vien chu
DIFF_THRESHOLD = 40        # tong chenh lech 3 kenh mau


# ---------------------------------------------------------------- PPM / PNG

class Image:
    __slots__ = ("w", "h", "px")

    def __init__(self, w, h, px):
        self.w, self.h, self.px = w, h, px  # px: bytearray RGB

    @classmethod
    def read_ppm(cls, path):
        with open(path, "rb") as fh:
            data = fh.read()
        if not data.startswith(b"P6"):
            raise ValueError(f"{path}: khong phai PPM P6")
        pos, fields = 2, []
        while len(fields) < 3:
            while pos < len(data) and data[pos : pos + 1].isspace():
                pos += 1
            if data[pos : pos + 1] == b"#":
                while data[pos : pos + 1] not in (b"\n", b""):
                    pos += 1
                continue
            start = pos
            while pos < len(data) and not data[pos : pos + 1].isspace():
                pos += 1
            fields.append(int(data[start:pos]))
        pos += 1  # mot ky tu trang sau maxval
        w, h, _ = fields
        return cls(w, h, bytearray(data[pos : pos + w * h * 3]))

    def crop(self, top, bottom):
        top = max(0, top)
        bottom = min(self.h, bottom)
        return Image(self.w, bottom - top,
                     self.px[top * self.w * 3 : bottom * self.w * 3])

    def write_png(self, path):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * stride : (y + 1) * stride]

        def chunk(tag, payload):
            return (struct.pack(">I", len(payload)) + tag + payload
                    + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF))

        with open(path, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n")
            fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)))
            fh.write(chunk(b"IDAT", zlib.compress(bytes(raw), 6)))
            fh.write(chunk(b"IEND", b""))


def stack(images, gap=18, bg=(228, 228, 232)):
    w = max(im.w for im in images)
    h = sum(im.h for im in images) + gap * (len(images) - 1)
    out = Image(w, h, bytearray(bytes(bg) * (w * h)))
    y = 0
    for i, im in enumerate(images):
        for row in range(im.h):
            off = ((y + row) * w) * 3
            out.px[off : off + im.w * 3] = im.px[row * im.w * 3 : (row + 1) * im.w * 3]
        y += im.h + (gap if i < len(images) - 1 else 0)
    return out


# ---------------------------------------------------------------- highlight

def tint_box(img, x0, y0, x1, y1):
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.w, x1), min(img.h, y1)
    a = TINT_ALPHA
    for y in range(y0, y1):
        base = (y * img.w + x0) * 3
        for i in range(base, base + (x1 - x0) * 3, 3):
            for c in range(3):
                img.px[i + c] = int(img.px[i + c] * (1 - a) + TINT[c] * a)
    for t in range(BORDER_W):
        for x in range(x0, x1):
            for y in (y0 + t, y1 - 1 - t):
                if 0 <= y < img.h:
                    o = (y * img.w + x) * 3
                    img.px[o : o + 3] = bytes(BORDER)
        for y in range(y0, y1):
            for x in (x0 + t, x1 - 1 - t):
                if 0 <= x < img.w:
                    o = (y * img.w + x) * 3
                    img.px[o : o + 3] = bytes(BORDER)


def diff_bands(a, b):
    """Tra ve danh sach (y0, y1, x0, x1) cac dai pixel khac nhau."""
    if (a.w, a.h) != (b.w, b.h):
        return [(0, min(a.h, b.h), 0, min(a.w, b.w))]
    rows = {}
    stride = a.w * 3
    for y in range(a.h):
        ra = a.px[y * stride : (y + 1) * stride]
        rb = b.px[y * stride : (y + 1) * stride]
        if ra == rb:
            continue
        xs = [x for x in range(a.w)
              if abs(ra[x * 3] - rb[x * 3]) + abs(ra[x * 3 + 1] - rb[x * 3 + 1])
                 + abs(ra[x * 3 + 2] - rb[x * 3 + 2]) > DIFF_THRESHOLD]
        if len(xs) >= MIN_PIXELS_PER_ROW:
            rows[y] = (xs[0], xs[-1] + 1)
    if not rows:
        return []
    bands, ys = [], sorted(rows)
    start = prev = ys[0]
    for y in ys[1:]:
        if y - prev > ROW_GAP:
            bands.append((start, prev + 1))
            start = y
        prev = y
    bands.append((start, prev + 1))
    out = []
    for y0, y1 in bands:
        xs = [rows[y] for y in range(y0, y1) if y in rows]
        out.append((y0, y1, min(x[0] for x in xs), max(x[1] for x in xs)))
    return out


# ---------------------------------------------------------------- pdf utils

def norm(s):
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def find_page(pdf, needle):
    txt = subprocess.run(["pdftotext", "-q", pdf, "-"], capture_output=True).stdout.decode("utf-8", "replace")
    target = norm(needle)
    for i, page in enumerate(txt.split("\f"), start=1):
        if target in norm(page):
            return i
    return None


def folder_name(outdir, label, no_index):
    """Moi lan sua co mot thu mac rieng, danh so tang dan de giu dung thu tu."""
    if no_index:
        return label
    used = 0
    if os.path.isdir(outdir):
        for entry in os.listdir(outdir):
            m = re.match(r"(\d+)-", entry)
            if m and os.path.isdir(os.path.join(outdir, entry)):
                used = max(used, int(m.group(1)))
    return f"{used + 1:02d}-{label}"


def render(pdf, page, workdir, tag):
    prefix = os.path.join(workdir, tag)
    subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), pdf, prefix],
                   check=True, capture_output=True)
    files = sorted(f for f in os.listdir(workdir) if f.startswith(tag) and f.endswith(".ppm"))
    if not files:
        raise RuntimeError(f"pdftoppm khong tao anh cho trang {page} cua {pdf}")
    return Image.read_ppm(os.path.join(workdir, files[0]))


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--text-before", required=True, help="chuoi dinh vi trang o ban truoc")
    ap.add_argument("--text-after", required=True, help="chuoi dinh vi trang o ban sau")
    ap.add_argument("--label", required=True)
    ap.add_argument("--outdir", default=".change-shots", help="thu muc goc chua cac lan sua")
    ap.add_argument("--full-page", action="store_true", help="xuat ca trang thay vi cat vung thay doi")
    ap.add_argument("--no-index", action="store_true", help="khong them so thu tu vao ten thu muc")
    ap.add_argument("--folder", help="dung dung thu muc nay (cho lan sua dung nhieu cho)")
    ap.add_argument("--part", help="tien to ten file khi mot lan sua co nhieu vi tri")
    args = ap.parse_args()

    p_before = find_page(args.before, args.text_before)
    p_after = find_page(args.after, args.text_after)
    if not p_before or not p_after:
        sys.exit(f"Khong tim thay trang (before={p_before}, after={p_after})")
    print(f"trang truoc={p_before} trang sau={p_after}")

    change_dir = args.folder or os.path.join(
        args.outdir, folder_name(args.outdir, args.label, args.no_index))
    os.makedirs(change_dir, exist_ok=True)
    prefix = f"{args.part}-" if args.part else ""
    with tempfile.TemporaryDirectory() as tmp:
        img_b = render(args.before, p_before, tmp, "b")
        img_a = render(args.after, p_after, tmp, "a")

    bands = diff_bands(img_b, img_a)
    if not bands:
        print("canh bao: khong phat hien khac biet pixel tren trang nay")
    for y0, y1, x0, x1 in bands:
        tint_box(img_b, x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD)
        tint_box(img_a, x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD)

    if bands and not args.full_page:
        top = min(b[0] for b in bands) - CROP_PAD
        bot = max(b[1] for b in bands) + CROP_PAD
        img_b, img_a = img_b.crop(top, bot), img_a.crop(top, bot)

    outputs = (("before.png", img_b), ("after.png", img_a),
               ("compare.png", stack([img_b, img_a])))
    for name, img in outputs:
        p = os.path.join(change_dir, prefix + name)
        img.write_png(p)
        print(p)


if __name__ == "__main__":
    main()
