# Lên kế hoạch du lịch — Claude Skill

Một [Claude Skill](https://docs.claude.com/en/docs/claude-code/skills) giúp Claude lên **kế hoạch du lịch cá nhân hoàn chỉnh** cho một điểm đến đã chọn — theo đúng cách một người tự lên kế hoạch cho chuyến đi của mình, không phải một bài viết quảng cáo du lịch.

## Skill này làm gì

Sau khi bạn đã chọn điểm đến, skill dẫn Claude đi qua 6 bước, mỗi bước xuất phát từ **mục tiêu chuyến đi** và **đặc trưng điểm đến**, với mọi con số đều có nguồn hoặc gắn cờ `[CẦN XÁC MINH]`:

1. **Checklist trước khi lên kế hoạch** — 12 câu hỏi (điểm đến, mục tiêu, thời gian, số người, ngân sách...), hỏi một lần với giá trị điền sẵn/mặc định để bạn chỉ cần sửa dòng sai.
2. **Đặc trưng điểm đến** — lịch sử, văn hoá, kinh tế, địa vị hành chính/an ninh, tính chất du lịch — và hệ quả của từng điều đó lên kế hoạch.
3. **Chọn thời điểm đi** — theo mục tiêu cụ thể (ngắm dải Ngân hà, nhiếp ảnh, biển/lặn, trekking...), không suy diễn cảm tính.
4. **Chọn khách sạn** — khoanh trục trung tâm trước, xếp hạng theo khoảng cách + rating (kèm số lượt đánh giá) + giá, rồi lọc theo mục tiêu; trình bày bảng shortlist và top 3.
5. **Lịch trình theo tuyến hướng Đông – Tây – Nam – Bắc** — mỗi tuyến là một vòng đi–về tự đủ (khoảng cách, thời gian nên đi, thứ tự điểm dừng, ăn dọc tuyến, phương án khi mưa/biển động), kèm gợi ý ghép tuyến theo số ngày — thay vì một lịch cứng theo từng ngày dễ vỡ khi có gì đó thay đổi.
6. **Ăn uống** theo rating Google, và **đóng gói thành trang lịch trình di động** (mở một chạm trên điện thoại, có nút mở Google Maps, checklist tick được) cùng file CSV/KML để nhập vào Google My Maps.

## Cấu trúc thư mục

```
len-ke-hoach-du-lich/
├── SKILL.md                       # Nội dung skill chính (quy trình 6 bước)
├── references/
│   ├── checklist-cau-hoi.md       # 12 câu hỏi trước khi lên kế hoạch
│   ├── goi-y-theo-muc-tieu.md     # Quy tắc chọn thời điểm theo từng mục tiêu
│   └── mau-ke-hoach.md            # Mẫu file kế hoạch Markdown đầu ra
└── scripts/
    ├── tao_kml.py                 # CSV điểm dừng → file KML cho Google My Maps
    └── tao_trang_html.py          # Markdown + CSV → trang lịch trình di động (HTML/Artifact)
```

## Đầu ra

- File kế hoạch Markdown (`ke-hoach-<điểm đến>-<tháng>.md`) theo mẫu trong `references/mau-ke-hoach.md`, có mục Giả định, Đặc trưng điểm đến, Thời điểm, Khách sạn, Lịch trình theo tuyến, Ăn uống, Nguồn.
- File `ban-do-<điểm đến>.csv` (và `.kml` nếu có toạ độ) để nhập vào [Google My Maps](https://www.google.com/maps/d/).
- Trang lịch trình di động một file (HTML), đăng được thành Artifact khi có công cụ Artifact — mở trên điện thoại giữa chuyến đi, có tab theo từng tuyến, nút mở Google Maps cho mỗi điểm dừng, và checklist việc cần làm.

## Cách dùng

Cài skill này vào Claude (Claude Code hoặc Cowork), sau đó chỉ cần nhắc đến một chuyến đi sắp tới — hỏi "nên đi tháng mấy", "ở khách sạn nào", "lịch trình mấy ngày", "ăn gì ở đâu", hoặc nhắc một địa danh kèm ý định đi chơi. Skill tự kích hoạt kể cả khi bạn chỉ hỏi một phần, không cần dùng đúng từ "kế hoạch".

Xem chi tiết cách cài skill trong [tài liệu Claude Skills](https://docs.claude.com/en/docs/claude-code/skills).

## Nguyên tắc

- Mọi quyết định (đi lúc nào, ở đâu, đi đâu trước, ăn gì) xuất phát từ mục tiêu chuyến đi và đặc trưng điểm đến, không phải liệt kê máy móc.
- Mọi con số (giá, rating, khoảng cách, giờ mở cửa) có nguồn và ngày tra cứu, hoặc gắn cờ `[CẦN XÁC MINH]` — không bịa tên khách sạn, quán ăn, rating.
- Ngôn ngữ: tiếng Việt, gọn, thực dụng — viết như ghi chú cho chính mình, không phải văn quảng cáo.

## Giấy phép

Chia sẻ tự do để dùng và tuỳ chỉnh cho nhu cầu lên kế hoạch du lịch của riêng bạn.

