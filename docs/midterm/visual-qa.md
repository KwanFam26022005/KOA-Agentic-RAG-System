# Kiểm tra trình bày bộ tài liệu giữa kỳ

Rà soát ngày 21–22/10/2026. Phạm vi: hiện vật tài liệu; không thẩm định y khoa và không chạy lại thí nghiệm. Hash bản bàn giao nằm trong `production-receipt.json` và `science-review.md`.

## Báo cáo Word và PDF

- DOCX đã mở bằng Microsoft Word trong phiên ẩn riêng, cập nhật field/mục lục, repaginate, lưu và xuất PDF trực tiếp. Kết quả **42 trang**, gồm **31 trang nội dung chính** của tám chương (PDF 7–37), năm trang front matter, bìa và năm trang references/phụ lục.
- Đã dựng ảnh **toàn bộ 42 trang** bằng PyMuPDF; xem contact sheets toàn bộ trang và xem lớn bìa, mục lục/danh mục, trang thân bài, bảng kết quả, bibliography và các trang hình trọng yếu. Các chương có tiêu đề và phân trang riêng; không còn trang trắng hoặc đoạn văn tràn thành trang lẻ như bản đầu.
- Khổ PDF: A4 dọc 595,3×841,9 pt; các trang hình ngang 841,9×595,3 pt. Thân bài Times New Roman 13 pt, heading 16/14 pt; bảng/chú thích được định cỡ riêng. PDF chứa Times New Roman thường/đậm; không có ký tự thay thế U+FFFD trong văn bản trích xuất.
- Bìa giữ trật tự cơ quan/trường, logo, tác giả, loại báo cáo, tên đề tài và địa điểm. Không dùng tên môn, khoa, giảng viên, mã sinh viên hoặc niên khóa chưa xác minh. Đã bỏ đường kẻ mặc định của Word Title và đổi caption về màu đen.
- Mục lục Word có field cập nhật và số trang hiện hành; danh mục đủ tám hình và tám bảng được đánh số. Có chín bảng native tính cả danh mục viết tắt. Các trích dẫn và cross-reference xuất hiện trong thân bài; 17 mục [1–13], [P1–P4] nằm trong bibliography.
- Năm SVG nghiên cứu được render bằng Chromium cục bộ để giữ font và arrowheads rồi nhúng vào DOCX. Các trang ngang giữ hình tổng quan; chi tiết PRE, POST/revision và guard có vùng phóng to riêng. Khi dựng ảnh chi tiết, chỉ bỏ các header container ngoài vùng focus để tránh cắt chữ; không bỏ node, condition hoặc connector khoa học. SVG/Mermaid đầy đủ vẫn có trong repository.

## Đối chiếu mẫu trường

Đã đọc và xem trực tiếp PDF tham khảo 18 trang do người dùng chỉ định. Bản mới áp dụng A4, Times New Roman, cấp tiêu đề đậm, lề thân dọc trái 3,5 cm/phải 2 cm, số trang trên giữa và trật tự bìa đã quan sát. Lề trang ngang được điều chỉnh để đặt sơ đồ. Mẫu không có quy ước mục lục/bibliography để đối chiếu; các phần đó được bổ sung cho báo cáo nghiên cứu, dùng front matter La Mã và nội dung số Ả Rập. Không coi các lựa chọn bổ sung này là quy định chính thức đã xác minh. PDF tham khảo gốc không được sửa hoặc đưa vào bộ công bố.

## PowerPoint và PDF slide

- Đã xuất và xem ảnh native **15/15 slide** ở 1600×900. PPTX đã mở lại bằng Microsoft PowerPoint; canvas 960×540 pt (16:9), PDF 15 trang.
- Text, box, connector và năm bảng là native editable; chỉ logo là ảnh. Có 15 notes nhúng và file script tiếng Việt riêng, tổng thời lượng gợi ý 18:35.
- Các trang kiến trúc/PRE/POST dùng hình giản lược native từ SVG 02/03, giữ các vòng phản hồi bắt buộc. Không đặt toàn bộ SVG nhãn nhỏ lên slide. Đã xem lại riêng slide 8–11 và 13 sau các sửa connector, nhãn và công thức.
- Logo từ website chính thức giữ nguyên tỷ lệ/màu, có URL và SHA-256. Nền trắng, Arial, xanh/đỏ dùng tiết chế. Theme được ghi **TDTU-inspired**, không gọi là slide master hoặc mã màu chính thức đã xác nhận.
- Hai helper kiểm tra package và hình học PowerPoint kết thúc exit 0: **0 findings, 0 warnings** ở bản cuối. Chúng kiểm tra cấu trúc/biên và heading fit; kết luận về connector, nhãn và tính dễ đọc còn dựa trên việc xem ảnh thực tế.
- Bản cuối không thấy text bị cắt, nằm ngoài slide hoặc connector đi xuyên các nhãn đã sửa. Font thường 18–25 pt, title khoảng 32 pt, phần dẫn nguồn nhỏ hơn. Tên đề tài, tác giả và scientific snapshot hiện rõ.

## Vấn đề cụ thể đã sửa

1. Báo cáo đầu có trang tràn sau hình/bảng: tách line spacing cho ảnh, dùng page-break-before, nén bảng viết tắt bằng bề rộng cột phù hợp và bỏ diễn giải lặp trên trang hình; giữ font thân 13 pt.
2. Các danh mục được cập nhật sau phân trang; bổ sung Hình 4.3, 4.4 và C.1.
3. Slide 8–10: làm rõ PolicyGuard, PRE recheck/ABSTAIN sau recheck và condition của correction; dời nhãn khỏi connector. Slide 11: tách hai đẳng thức 16×3=48 và 48×3=144.
4. SVG 01/04: phân biệt release manifest SHA `eda0e26c...` với source identity `5aa87228b...`; SVG/MMD 04 thống nhất terminal status. Đây là correction khoa học về nhãn, đã được reviewer xác minh.
5. SVG 02: dời tag Fresh Decomposition/POST Recheck khỏi thân Reviser. SVG 04: sửa tọa độ của chữ xoay Air-gap, đặt trong wall và tránh tag READ-ONLY. Không đổi luồng hoặc phương pháp.

## Công cụ và giới hạn

Renderer DOCX đóng gói sẵn không chạy được do thiếu `pdf2image`; không cài dependency mới. Thay bằng xuất Word native và raster PDF bằng PyMuPDF đã cài sẵn. Kết quả render/kiểm tra thực tế được ghi ở trên; không coi renderer bị thiếu là một check đã PASS.

Ảnh QA, cache trình duyệt và các bản nháp được giữ ở `_build/` và không stage. Không chạy lại runtime tests, full regression, bootstrap, provider hoặc clinical scoring. Không xác nhận clinical accuracy, safety, cost saving, quyền tái phân phối guideline hay endorsement của TDTU.
