# Diagrams — Sơ đồ kiến trúc SmartRent

Sơ đồ tổ chức mã nguồn hệ thống SmartRent viết bằng **Mermaid**, render sẵn ra **PDF vector** để nhúng vào báo cáo LaTeX. Chia theo 2 thành phần:

```
diagrams/
├── fe/                 # Frontend — smartrent-fe (Next.js)
│   ├── src/  pdf/  png/
├── be/                 # Backend — smartrent-backend (Spring Boot)
│   ├── src/  pdf/  png/
├── mermaid.config.json # cấu hình theme/font dùng chung
├── render.sh           # render lại toàn bộ (hoặc fe / be)
└── README.md
```

Mỗi phần: `src/` = nguồn `.mmd` (sửa ở đây) · `pdf/` = vector cho LaTeX · `png/` = xem nhanh / chèn Word.

## Frontend — `fe/` (Next.js 15 · React 19 · TanStack Query · Zustand)

| File | Nội dung |
|------|----------|
| `01-architecture-layers` | Phân lớp: Routing → UI → Logic → Data → Infra → Backend |
| `02-folder-structure` | Cây thư mục `src/` |
| `03-atomic-design` | atoms → molecules → organisms → templates → pages |
| `04-data-flow` | Component → Hook → TanStack Query → Service → Axios → API |
| `05-providers` | Cây Provider trong `_app.tsx` |
| `06-routing` | Bản đồ route (Pages Router) |
| `07-state-management` | TanStack Query / Zustand / Context |

## Backend — `be/` (Spring Boot 3.4 · JPA · MySQL · Redis)

| File | Nội dung |
|------|----------|
| `01-architecture-layers` | Phân lớp: Controller → Service → Mapper → Repository → MySQL + cross-cutting |
| `02-package-structure` | Cây package `com.smartrent` |
| `03-request-flow` | Luồng xử lý 1 request: JWT → Controller → Service → Repo → DB (+ Redis cache) |
| `04-domain-modules` | 40 nhóm domain service (listing, auth, payment, ai…) |
| `05-external-integrations` | Tích hợp ngoài: MySQL, Redis, S3, Google, Brevo, ZaloPay/SePay, AI |

## Render lại (sau khi sửa `.mmd`)

```bash
bash render.sh          # cả fe + be ; cần Node.js (mermaid-cli qua npx)
bash render.sh fe       # chỉ frontend
bash render.sh be       # chỉ backend
```

## Nhúng vào LaTeX

> **LaTeX không render Mermaid trực tiếp** — ta nhúng file PDF đã render sẵn (vector, sắc nét khi in).

**Cách 1 — thêm đường dẫn vào `graphicspath`** (trong `final/main.tex`, dòng 39):

```latex
\graphicspath{ {Images/} {../diagrams/fe/pdf/} {../diagrams/be/pdf/} }
```

rồi trong chapter chỉ cần tên file (không trùng tên giữa fe/be vì khác thư mục — nếu trùng, dùng Cách 2):

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=\textwidth]{01-architecture-layers}
  \caption{Kiến trúc phân lớp của backend SmartRent}
  \label{fig:be-architecture}
\end{figure}
```

**Cách 2 — đường dẫn tương đối trực tiếp** (rõ ràng, tránh trùng tên — khuyến nghị):

```latex
\includegraphics[width=\textwidth]{../diagrams/be/pdf/01-architecture-layers.pdf}
\includegraphics[width=\textwidth]{../diagrams/fe/pdf/01-architecture-layers.pdf}
```

> Đường dẫn `../diagrams/...` tính từ `final/` (nơi chứa `main.tex`).
> Cần `\usepackage{float}` để dùng `[H]` (ghim vị trí hình) — kiểm tra preamble nếu báo lỗi.

## Lưu ý

- Sửa nội dung ở `*/src/*.mmd` rồi chạy `render.sh` — **không** sửa tay file PDF/PNG.
- File FE và BE có cùng số thứ tự (`01-architecture-layers`) nên khi nhúng nên dùng Cách 2 hoặc đặt label/caption rõ FE/BE.
- PDF vector zoom/in không vỡ; ưu tiên PDF cho LaTeX, PNG chỉ xem nhanh hoặc chèn Word.
