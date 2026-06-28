# CLAUDE.md — Quy ước làm báo cáo SmartRent

Hướng dẫn cho Claude khi chỉnh sửa báo cáo khóa luận trong thư mục này.
Mục tiêu: báo cáo học thuật **sạch, nhất quán, tự nhiên** — không màu mè.

## Cấu trúc dự án

- `final/` — nguồn LaTeX (`main.tex` include các `ChapterX/chapterX.tex` và `Appendix/*.tex`).
- `diagrams/` — sơ đồ Mermaid: `*/src/*.mmd` là nguồn, render ra `*/pdf/` (nhúng LaTeX) và `*/png/` (xem nhanh).
- Build LaTeX: `cd final && latexmk -g -pdf -interaction=nonstopmode main.tex` (engine pdfTeX, bib qua biber).
- Render sơ đồ: `cd diagrams && bash render.sh` (hoặc `fe` / `be`). **Không** sửa tay file PDF/PNG — sửa `.mmd` rồi render lại.

## Quy tắc trình bày (BẮT BUỘC)

### 0. Tuyệt đối KHÔNG dùng icon/emoji — ở bất kỳ đâu
- Không thêm emoji/icon (📱 🌐 🧠 🤖 ✅ 🔥 …) vào **bất kỳ chỗ nào**: sơ đồ Mermaid, nội dung LaTeX, bảng, caption, lẫn các file Markdown (README, CLAUDE.md, ghi chú). Chỉ dùng chữ.
- Khi tạo hoặc sửa nội dung mới, mặc định **không chèn icon**. Nếu phát hiện icon có sẵn thì gỡ bỏ.

### 1. In đậm — chỉ dùng cho tiêu đề
- **Được** in đậm (`\textbf`): tiêu đề mục/chương (do template lo), **tiêu đề cột/hàng trong bảng**, và **nhãn dẫn đầu mỗi mục liệt kê** (`\item \textbf{Nhãn:} ...` hoặc `\item \textbf{Câu tiêu đề.} ...`).
- **Cấm** in đậm rải rác giữa câu để nhấn mạnh thuật ngữ, tên công nghệ, tên thư viện (Next.js, React, TanStack Query, shadcn/ui…). Để **chữ thường**.
- Cần làm nổi thuật ngữ/khái niệm thì dùng `\textit{...}`; tên file/định danh mã/biến thì dùng `\texttt{...}`. Không dùng `\textbf` cho hai việc này.

### 2. Sơ đồ — nhìn tự nhiên, một màu thống nhất
- Không icon (xem mục 0).
- **Chỉ dùng một màu** cho toàn bộ sơ đồ; **không** tô màu bừa bãi (mỗi node một màu đỏ/xanh/vàng/tím). Một tông màu (indigo) áp dụng nhất quán cho **mọi** sơ đồ fe lẫn be.
- **Không** đặt màu trong file `.mmd`: không viết `classDef` / `class` / `style ... fill/stroke`. Để node thừa hưởng màu chung khai báo tập trung ở `diagrams/mermaid.config.json` (`themeVariables`). Muốn đổi màu thì sửa đúng một chỗ là config này, rồi render lại — không sửa từng sơ đồ.
- Đường nối/mũi tên để màu xám trung tính; ưu tiên rõ ràng hơn trang trí.

### 3. Nội dung phải khớp hệ thống thật
- **Không** thêm tích hợp không tồn tại. Hệ thống **không** dùng kênh nhắn tin SMS/Zalo (ZNS) để thông báo — đừng vẽ/viết các node "otp · sms", "Zalo OTP/ZNS". Cổng thanh toán **ZaloPay/SePay** thì **giữ** (là nghiệp vụ thật).
- **webapp (FE) và trang quản trị (admin) dùng chung kiến trúc kỹ thuật** -- admin được fork từ webapp rồi điều chỉnh nội dung và phong cách giao diện. Được phép viết rằng chúng "dùng chung kiến trúc". **Không** viết rằng chúng hoàn toàn độc lập về cơ sở mã hoặc quy ước kỹ thuật.

### 4. Văn phong & nhất quán
- Tiếng Việt học thuật, ngôi trung lập; thuật ngữ kỹ thuật kèm bản gốc trong ngoặc lần đầu xuất hiện: "kết xuất phía máy chủ (Server-Side Rendering -- SSR)".
- Hình/Bảng luôn có `\caption` và `\label`, tham chiếu bằng `Hình~\ref{...}` / `Bảng~\ref{...}` (có `~` chống xuống dòng).
- Dùng `--` cho dấu gạch ngang câu, `\ldots` cho dấu ba chấm.

## Trước khi kết thúc
- Render lại sơ đồ nếu đã sửa `.mmd`, rồi build LaTeX, đảm bảo `exit=0` và không có `!`/Undefined reference trong log.
- Soát lại: còn `\textbf` giữa câu không? còn icon trong `.mmd` không? còn nhắc SMS/Zalo messaging không?
