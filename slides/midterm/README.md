# Thuyết trình giữa kỳ KOA

- `KOA_Midterm_Presentation_TDTU.pptx`: 15 slide 16:9, text, sơ đồ và 5 bảng native chỉnh sửa được.
- `KOA_Midterm_Presentation_TDTU.pdf`: bản xuất trực tiếp bằng PowerPoint.
- `speaker-notes.md`: kịch bản tiếng Việt cho từng slide; notes cũng có trong PowerPoint, khoảng 18 phút 35 giây.
- `build_presentation.py`: mã dựng và xuất trên Windows bằng PowerPoint COM; ảnh QA và dữ liệu hình học được lưu trong `_build/`.

Theme là **TDTU-inspired academic theme**. Logo giữ màu/tỷ lệ từ website chính thức TDTU; URL và SHA-256 có trong `assets/tdtu-logo-provenance.json`. Chưa xác minh được một slide master hay bộ mã màu chính thức; các màu bố cục là lựa chọn thiết kế, không được gọi là template chính thức hoặc university endorsement.

Các sơ đồ native được rút gọn từ `assets/diagrams/01–05`, giữ vòng correction/revision có giới hạn, PRE recheck, POST mới và control plane xác định. Full SVG/Mermaid gốc vẫn được giữ trong repository. Nội dung dùng chung baseline `ac4ade7` và `docs/midterm/content-contract.md`; các pass count là qualification kỹ thuật, không phải medical accuracy.

Dựng lại trong môi trường Windows đã có Microsoft PowerPoint, Python và `pywin32`:

```powershell
python -X utf8 slides/midterm/build_presentation.py
```

Lệnh ghi lại PPTX/PDF cùng tên, xuất ảnh của 15 slide, ghi notes, rồi mở lại PPTX bằng PowerPoint để kiểm tra. Không cài dependency, không gọi mạng/provider, không chạy thí nghiệm. Builder chỉ đóng presentation do nó mở; không đóng tài liệu khác của người dùng.

Nhật ký kiểm tra cấu trúc, hình học, mở bằng PowerPoint và hash đầu ra nằm trong `docs/midterm/production-receipt.json`. Rà soát khoa học độc lập và visual QA được ghi riêng cùng thư mục.
