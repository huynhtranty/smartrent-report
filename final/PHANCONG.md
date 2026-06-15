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
| `Chapter1/chapter1.tex` | Đặt vấn đề, Mục tiêu đề tài, Phạm vi của đề tài | Chung / nhóm trưởng | **Vũ** |
| `Chapter2/chapter2.tex` | Batdongsan, Phongtro123, NhaTot, Zillow, so sánh, khoảng trống AI, kết luận chương | Khảo sát thị trường | **Vy** (khoảng trống AI), **Phát** hỗ trợ phần web |
| `Chapter3/chapter3.tex` §3.1 | Kiến trúc tổng quan, mô hình, các thành phần | Chung / nhóm trưởng | **Vũ** |
| `Chapter3/chapter3.tex` §3.2 | Nền tảng Web (tổ chức mã nguồn, kết nối, đa ngôn ngữ, ưu điểm) | Web | **Phát** (webapp) + **Hùng** (admin) |
| `Chapter3/chapter3.tex` §3.3 | Backend Modular Monolith, module nghiệp vụ, phân tầng, luồng dữ liệu, ưu điểm | Backend | **Ty** + **Tường** (Vũ review) |
| `Chapter3/chapter3.tex` §3.4 | AI Agent, đánh giá giá BĐS, gợi ý cá nhân hóa, tạo/kiểm duyệt nội dung, kiến trúc tích hợp AI | AI | **Vy** + **Vũ** (Ty review) |
| `Chapter3/chapter3.tex` §3.5 | Hạ tầng: R2, MySQL, LiteLLM & Langfuse, cổng thanh toán, CI/CD, triển khai | Hạ tầng / DevOps | **Ty** |
| `Chapter3/chapter3.tex` §3.6 | Cơ sở dữ liệu: tổng quan, sơ đồ thiết kế, mô tả các bảng | CSDL | **Tường** |
| `Chapter4/chapter4.tex` | §4.1 khái quát, §4.2 các giai đoạn, §4.3.1 phân công vai trò, §4.4 khó khăn | Nhóm trưởng | **Vũ** |
| `Chapter5/chapter5.tex` §5.1 | Kết quả hệ thống Người thuê | Web | **Phát** |
| `Chapter5/chapter5.tex` §5.2 | Kết quả hệ thống Quản trị viên | Web / Backend | **Hùng** |
| `Chapter5/chapter5.tex` §5.3 | Kết quả triển khai các tính năng AI | AI | **Vy** + **Vũ** |
| `Chapter6/chapter6.tex` | Ý nghĩa, kinh nghiệm, vấn đề tồn đọng, hướng phát triển | Chung | **Vũ** (tổng hợp ý kiến cả nhóm) |
| `Appendix/summary.tex` | Tóm tắt toàn đồ án | Nhóm trưởng | **Vũ** |
| `Appendix/appendix1.tex` | Bổ sung từ viết tắt / thuật ngữ khi viết bài | Tất cả | **Tất cả** |
| `References/references.bib` | Thêm tài liệu tham khảo (nhớ cập nhật `resetnumbers` trong `main.tex`) | Người trích dẫn | **Người trích dẫn tự thêm** |

## Tóm tắt theo người

| Người | Vai trò trong hệ thống | Phần báo cáo phụ trách |
|---|---|---|
| **Trường Vũ** | Nhóm trưởng – Backend + AI | Ch1, Ch3.1 (kiến trúc), Ch3.4 (AI, cùng Vy), Ch4 (quản lý dự án), Ch5.3 (kết quả AI, cùng Vy), Ch6, `summary.tex`, review backend |
| **Ty** | Backend + AI / DevOps | Ch3.3 (backend, cùng Tường), Ch3.4 (review AI), Ch3.5 (hạ tầng) |
| **Tường** | Backend | Ch3.3 (backend, cùng Ty), Ch3.6 (CSDL) |
| **Vy** | AI | Ch2 (khoảng trống AI), Ch3.4 (AI, cùng Vũ), Ch5.3 (kết quả AI, cùng Vũ) |
| **Phát** | Web – Webapp người thuê | Ch2 (hỗ trợ phần web), Ch3.2 (web, cùng Hùng), Ch5.1 (kết quả người thuê) |
| **Hùng** | Web – Frontend Admin | Ch3.2 (web, cùng Phát), Ch5.2 (kết quả quản trị viên), tổng hợp bảng từ viết tắt |

Nguyên tắc chia: mỗi người viết phần báo cáo đúng với phần mình đã code, để mô tả chính xác và tránh giẫm chân. Trường Vũ (nhóm trưởng) ôm các chương chung/quản lý + tổng hợp; backend do Ty + Tường viết chính (Vũ review), CSDL giao Tường; AI gồm Vy, Vũ, Ty (Vy + Vũ viết chính, Ty review).

## Phụ lục

| File | Nội dung | Trạng thái | Người |
|---|---|---|---|
| `Appendix/thanks.tex` | Lời cảm ơn | ✅ Đã có | — |
| `Appendix/commitment.tex` | Lời cam đoan | ✅ Đã có | — |
| `Appendix/summary.tex` | Tóm tắt toàn đồ án | ⏳ Cần viết | **Vũ** |
| `Appendix/appendix1.tex` | Bảng từ viết tắt / thuật ngữ | ⏳ Bổ sung dần khi viết | **Tất cả** (Hùng tổng hợp, rà cuối) |
| `Appendix/advisor.tex` | Nhận xét GVHD | 📄 Chờ PDF giáo vụ | bỏ comment khi có PDF |
| `Appendix/reviewer.tex` | Nhận xét GVPB | 📄 Chờ PDF giáo vụ | bỏ comment khi có PDF |
| `Appendix/proposal.tex` | Đề cương chi tiết | 📄 Chờ PDF | chèn `proposal.pdf` khi có |

## Hình ảnh / sơ đồ (thư mục `images/`)

Nguyên tắc: ai phụ trách mục nào thì tự chụp/vẽ hình cho mục đó. **Hùng + Phát điều phối** khâu hình ảnh (thu gom, đặt tên theo `chXX-tên-hình.png`, đánh số, thống nhất kích thước & caption).

| Hình cần có | Mục | Người |
|---|---|---|
| Sơ đồ kiến trúc tổng quan | Ch3.1 | **Vũ** |
| Sơ đồ tổ chức mã nguồn web, ảnh đa ngôn ngữ | Ch3.2 | **Phát** + **Hùng** |
| Sơ đồ Modular Monolith, phân tầng, luồng dữ liệu | Ch3.3 | **Ty** + **Tường** |
| Sơ đồ kiến trúc tích hợp AI, luồng AI Agent | Ch3.4 | **Vy** + **Vũ** |
| Sơ đồ hạ tầng / triển khai, CI/CD | Ch3.5 | **Ty** |
| Sơ đồ ERD cơ sở dữ liệu | Ch3.6 | **Tường** |
| Ảnh chụp giao diện webapp người thuê | Ch5.1 | **Phát** |
| Ảnh chụp giao diện trang quản trị | Ch5.2 | **Hùng** |
| Ảnh chụp các tính năng AI | Ch5.3 | **Vy** |

## Còn để trống / cần file ngoài

- `Appendix/proposal.tex`: chèn `proposal.pdf` khi có (bỏ comment dòng `\includepdf`).
- Nhận xét GVHD/GVPB trong `main.tex`: đang comment, bỏ comment khi có PDF từ giáo vụ.
- `Chapter3` §3.4 có 2 mục trùng tên "Hệ thống gợi ý cá nhân hóa" (theo file gốc) — cần rà lại.
