# Báo cáo giữa kỳ KOA

- `KOA_Midterm_Report_TDTU.docx`: bản Word chỉnh sửa được, có mục lục cập nhật bằng field.
- `KOA_Midterm_Report_TDTU.pdf`: bản xuất bằng Microsoft Word, 42 trang; nội dung chính 31 trang (Chương 1–8), ngoài ra có bìa, front matter, tài liệu tham khảo và phụ lục.
- `report-content.md`: nguồn nội dung tiếng Việt, có cấu trúc bảng và chỉ dẫn hình.
- `build_report.py`, `export_report.py`: dựng DOCX, cập nhật mục lục, xuất PDF và dựng ảnh QA vào `_build/`.

Baseline khoa học: `ac4ade796e56377882b8069d0fb7a14809e8180b`; quy ước dùng chung tại `docs/midterm/content-contract.md`. Không diễn giải ngày tạo tệp thành ngày cập nhật kết quả nghiên cứu.

Đã xem trực tiếp PDF tham khảo do người dùng cung cấp: bố cục bìa, A4, Times New Roman 13 pt, tiêu đề đậm, lề trái 3,5 cm/phải 2 cm và số trang trên giữa được áp dụng. PDF tham khảo không có quy cách mục lục/bibliography để sao chép; các phần này được bổ sung theo nhu cầu báo cáo. Trang ngang và các vùng phóng to giúp đọc sơ đồ. Không thêm khoa, giảng viên hướng dẫn, mã sinh viên, môn học hay niên khóa chưa được xác minh. Đây là bản thích ứng theo mẫu đã quan sát, không phải chứng nhận tuân thủ một bộ quy định đầy đủ của trường.

Để dựng lại trên môi trường Windows đã có Microsoft Word, Edge, Python cùng `python-docx`, `PyMuPDF`, `Pillow`, `pywin32`:

```powershell
python -X utf8 report/midterm/build_report.py
python -X utf8 report/midterm/export_report.py
```

Các lệnh ghi lại hai artifact cùng tên. Nguồn hình là `assets/diagrams/` và logo chính thức đã lưu cùng provenance trong `slides/midterm/assets/`. Không cần gọi mô hình, provider, tải benchmark hoặc chạy lại thí nghiệm. Bộ xuất dùng một phiên Word ẩn riêng và đóng tài liệu của phiên đó.

Kiểm tra đã thực hiện, giới hạn và hash đầu ra nằm tại `docs/midterm/production-receipt.json`, `visual-qa.md` và `science-review.md`.
