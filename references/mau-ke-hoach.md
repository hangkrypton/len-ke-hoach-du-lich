# Mẫu file kế hoạch

Dùng cấu trúc này cho file `ke-hoach-<diem-den>-<thang>.md`. Giữ nguyên thứ tự mục; bỏ mục không áp dụng thay vì để trống. Bảng ngắn gọn, mỗi ô một dòng.

```markdown
# Kế hoạch [Điểm đến] — [khoảng thời gian]

**Mục tiêu chuyến đi:** [1 câu]
**Giả định:** [số người, ngân sách phòng, phương tiện, số ngày — ghi rõ cái nào là mặc định do chưa được cho biết]
**Ngày lập:** [ngày tra cứu]

## 1. Đặc trưng điểm đến

[200–350 chữ: lịch sử, văn hoá, kinh tế, địa vị hành chính/an ninh & đặc trưng riêng (đặc khu, quân sự, vườn quốc gia...), tính chất du lịch — chỉ những gì ảnh hưởng đến chuyến đi]

**Lưu ý / không được làm ở đây:** [vd. cấm drone, khu quân sự cấm chụp, mang tiền mặt vì ít ATM]

**Điều này ảnh hưởng gì đến kế hoạch:**
- ...
- ...

## 2. Thời điểm

| Ràng buộc | Điều kiện tốt | Nguồn |
|---|---|---|
| Thời tiết / mùa | ... | ... |
| [Điều kiện theo mục tiêu, vd. pha trăng] | ... | ... |
| Cao điểm / lễ / phương tiện | ... | ... |

**Đề xuất:** [cửa sổ ngày cụ thể] — [lý do 1 câu]
**Dự phòng:** [cửa sổ khác] — [đánh đổi gì]
**Rủi ro cần theo dõi:** [vd. dự báo mây 3 ngày trước khi đi]

## 3. Chỗ ở

**Trục trung tâm của kế hoạch này:** [tên đường/khu + vì sao]

| # | Tên | Cách trung tâm | Rating (số review) | Giá/đêm (mùa đi) | Hướng / đặc điểm | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | ... | 0,3 km | 4,6 (412) | 750k | hướng biển | ... |

**Chọn top 3:**
1. **[Tên]** — [lý do]. Điểm trừ: [...]
2. ...
3. ...

## 4. Lịch trình theo tuyến

**Chỗ ở làm gốc:** [tên/khu]. Các tuyến tính từ đây.

| Tuyến | Km / thời gian | Loại | Nên đi lúc | Mỏ neo |
|---|---|---|---|---|
| Bắc | ~18 km / 4h | nửa ngày | sáng sớm | bình minh 05:40 |
| Nam | ... | cả ngày | chiều → tối | ngân hà lên 21:30 |

### Tuyến Bắc — [tên gợi nhớ, vd. Đầm Trầu & mũi Tàu Bể]
**Nên đi:** [buổi + vì sao]. **Thời lượng:** [x giờ]. **Bỏ khi:** [mưa/biển động] → thay bằng [...].

| # | Điểm | Đến lúc / ở lại | Vì sao đi | Lưu ý |
|---|---|---|---|---|
| 1 | ... | 05:30 / 45 phút | mỏ neo bình minh | đường tối, đèn pin |

**Ăn dọc tuyến:** [quán] ([rating], giờ mở).

### Tuyến Nam — ...

### Tuyến Trung tâm — [đi bộ]

**Gợi ý ghép tuyến theo số ngày (chỉ là gợi ý):**

| Ngày | Ghép | Lý do |
|---|---|---|
| Ngày 1 (đến trưa) | Trung tâm + khảo sát tuyến Nam | nửa ngày, gần |
| Ngày 2 | Bắc (sáng) + nghỉ + Nam (tối, ngắm sao) | ... |
| Ngày 3 | Đông (cả ngày) | ... |
| Ngày 4 (về chiều) | tuỳ: lặp lại tuyến thích nhất | ... |

**Kế hoạch B (mưa / biển động):** ...

**Bản đồ Google My Maps:** file `ban-do-<diem-den>.csv` (+ `.kml` nếu có toạ độ) đính kèm.
Nhập: [Google My Maps](https://www.google.com/maps/d/) → Tạo bản đồ mới → Nhập → chọn file → (CSV) cột vị trí = `dia_chi`, tiêu đề = `ten` → kiểm tra ghim lệch.

## 5. Ăn uống

| Quán | Món nổi bật | Rating (số review) | Cách chỗ ở / cụm | Giờ mở cửa | Ghi chú |
|---|---|---|---|---|---|

**Đặc sản nên thử:** ...

## 6. Việc cần làm trước khi đi
- [ ] Đặt phòng [tên] trước ngày ...
- [ ] Đặt vé tàu/bay ...
- [ ] Kiểm tra dự báo mây/thời tiết ngày ...
- [ ] ...

## Nguồn
- [tên nguồn](link) — tra ngày ...
```

## File đi kèm

- `ban-do-<diem-den>.csv` — cột `ten, tuyen, thu_tu, lat, lng, dia_chi, gio, ghi_chu, loai`; một dòng mỗi điểm dừng; `tuyen` = "Tuyến Bắc"/"Tuyến Nam"/.../"Chỗ ở".
- `ban-do-<diem-den>.kml` — tạo bằng `scripts/tao_kml.py` khi có toạ độ.
- `<ten>.artifact.html` — trang lịch trình di động, tạo bằng `scripts/tao_trang_html.py` từ hai file trên; đăng thành Artifact. Script đọc theo đúng các tiêu đề `## 1.`–`## 6.`, `### Tuyến X`, đoạn `**Gợi ý ghép tuyến` và bảng `- [ ]` của mẫu này, nên giữ nguyên cấu trúc tiêu đề.

## Quy ước để script đọc được

- Để một dòng trống trước mỗi danh sách, bảng và giữa các dòng `**Nhãn:**` liên tiếp.
- Trong CSV, quán ăn để trong lớp tuyến (`tuyen` = "Tuyến Nam") với `loai=an` — trang di động tự gom vào tab Ăn uống; chỗ ở dùng `tuyen` = "Chỗ ở", `loai=o`. Tên lớp CSV phải trùng chữ hướng trong tiêu đề `### Tuyến X` (Bắc/Nam/Đông/Tây/Trung tâm).

## Cách gắn cờ

- `[CẦN XÁC MINH]` đặt ngay sau con số/thông tin chưa tra được từ nguồn gốc. Ví dụ: `Giá 650k/đêm [CẦN XÁC MINH — chỉ thấy trên blog 2024]`.
- Không tổng hợp thành một câu "mọi thông tin cần kiểm tra lại" ở cuối — cờ phải ở đúng chỗ để người đọc biết tin cái gì.

