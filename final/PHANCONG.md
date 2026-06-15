# Phân công viết báo cáo LaTeX

Bộ LaTeX đã được dựng đủ khung 6 chương theo mục lục của Báo Cáo Cuối Kỳ.
Mỗi mục cần viết đều có sẵn dòng `% TODO: Nội dung` — gõ nội dung ngay bên dưới
và **xóa dòng TODO** khi viết xong.

## Quy ước chung (mọi người đọc trước)

- Chỉ sửa file thuộc mục mình phụ trách để tránh xung đột git.
- Chèn hình vào thư mục `images/` rồi dùng `\includegraphics{tên-file}`.
- Thêm tài liệu tham khảo vào `References/references.bib` rồi trích dẫn bằng `\cite{key}`.
- Gặp thuật ngữ/viết tắt mới thì thêm một dòng vào `Appendix/appendix1.tex`.
- Build lại theo thứ tự: `pdflatex` -> `biber` -> `pdflatex` -> `pdflatex`.
- Phần 4.3.2 và 4.3.3 (quy trình làm việc nhóm) ĐÃ có nội dung — không cần viết lại.

## Bảng phân công

| File | Mục cần viết | Mảng phụ trách | Người |
|---|---|---|---|
| `Chapter1/chapter1.tex` | Đặt vấn đề, Mục tiêu đề tài, Phạm vi của đề tài | Chung / nhóm trưởng | |
| `Chapter2/chapter2.tex` | Batdongsan, Phongtro123, NhaTot, Zillow, so sánh, khoảng trống AI, kết luận chương | Khảo sát thị trường | |
| `Chapter3/chapter3.tex` §3.1 | Kiến trúc tổng quan, mô hình, các thành phần | Chung / nhóm trưởng | |
| `Chapter3/chapter3.tex` §3.2 | Nền tảng Web (tổ chức mã nguồn, kết nối, đa ngôn ngữ, ưu điểm) | Web | |
| `Chapter3/chapter3.tex` §3.3 | Backend Modular Monolith, module nghiệp vụ, phân tầng, luồng dữ liệu, ưu điểm | Backend | |
| `Chapter3/chapter3.tex` §3.4 | AI Agent, đánh giá giá BĐS, gợi ý cá nhân hóa, tạo/kiểm duyệt nội dung, kiến trúc tích hợp AI | AI | |
| `Chapter3/chapter3.tex` §3.5 | Hạ tầng: R2, MySQL, LiteLLM & Langfuse, cổng thanh toán, CI/CD, triển khai | Hạ tầng / DevOps | |
| `Chapter3/chapter3.tex` §3.6 | Cơ sở dữ liệu: tổng quan, sơ đồ thiết kế, mô tả các bảng | CSDL | |
| `Chapter4/chapter4.tex` | §4.1 khái quát, §4.2 các giai đoạn, §4.3.1 phân công vai trò, §4.4 khó khăn | Nhóm trưởng | |
| `Chapter5/chapter5.tex` §5.1–5.2 | Kết quả hệ thống Người thuê + Quản trị viên | Web / Backend | |
| `Chapter5/chapter5.tex` §5.3 | Kết quả triển khai các tính năng AI | AI | |
| `Chapter6/chapter6.tex` | Ý nghĩa, kinh nghiệm, vấn đề tồn đọng, hướng phát triển | Chung | |
| `Appendix/summary.tex` | Tóm tắt toàn đồ án | Nhóm trưởng | |
| `Appendix/appendix1.tex` | Bổ sung từ viết tắt / thuật ngữ khi viết bài | Tất cả | |
| `References/references.bib` | Thêm tài liệu tham khảo (nhớ cập nhật `resetnumbers` trong `main.tex`) | Người trích dẫn | |

## Còn để trống / cần file ngoài

- `Appendix/proposal.tex`: chèn `proposal.pdf` khi có (bỏ comment dòng `\includepdf`).
- Nhận xét GVHD/GVPB trong `main.tex`: đang comment, bỏ comment khi có PDF từ giáo vụ.
- `Chapter3` §3.4 có 2 mục trùng tên "Hệ thống gợi ý cá nhân hóa" (theo file gốc) — cần rà lại.
