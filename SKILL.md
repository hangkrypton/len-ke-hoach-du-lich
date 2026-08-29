---
name: len-ke-hoach-du-lich
description: Lên kế hoạch du lịch cá nhân hoàn chỉnh cho một điểm đến đã chọn — checklist xác định mục tiêu/thời gian/ngân sách/số người; đặc trưng điểm đến (lịch sử, văn hoá, kinh tế, an ninh); chọn thời điểm theo mục tiêu (Milky Way, chụp ảnh, biển, trekking...); chọn khách sạn theo trục trung tâm + rating + giá; lịch trình theo tuyến hướng Đông–Tây–Nam–Bắc, mỗi tuyến có lúc nên đi, kèm gợi ý ghép tuyến; quán ăn theo rating Google. Dùng skill này bất cứ khi nào người dùng nói về một chuyến đi sắp tới, hỏi "nên đi tháng mấy", "ở khách sạn nào", "lịch trình mấy ngày", "ăn gì ở đâu", hoặc nhắc một địa danh kèm ý định đi chơi — kể cả khi chỉ hỏi một phần và không dùng từ "kế hoạch". Đầu ra là file kế hoạch Markdown có nguồn, CSV/KML cho Google My Maps, và trang lịch trình di động đăng thành Artifact.
---

# Lên kế hoạch du lịch

Skill này mã hoá cách người dùng tự lên kế hoạch cho một chuyến đi **sau khi đã chọn điểm đến**. Nguyên tắc xuyên suốt: mọi quyết định (đi lúc nào, ở đâu, đi đâu trước, ăn gì) đều xuất phát từ **mục tiêu của chuyến đi** và **đặc trưng của điểm đến**, và mọi con số (giá, rating, khoảng cách, giờ mở cửa) đều phải có nguồn hoặc được gắn cờ `[CẦN XÁC MINH]`. Kế hoạch tốt là kế hoạch mà chủ nhân có thể mở trên điện thoại giữa chuyến đi và tin được.

## Bước 0 — Checklist câu hỏi trước khi lên kế hoạch

Trước khi tra cứu bất cứ thứ gì, đọc `references/checklist-cau-hoi.md` và chạy checklist 12 câu trong đó. Lý do: một kế hoạch làm với sai giả định (nhóm 5 người mà tìm phòng đôi, ngân sách 800k mà người ta có 2 triệu, đã đặt vé rồi mà còn gợi ý đổi ngày) phải làm lại từ đầu — tốn hơn nhiều so với một lượt hỏi.

Cách hỏi: **một tin nhắn duy nhất**, liệt kê 12 mục đã **điền sẵn** những gì người dùng đã nói và **giá trị mặc định** cho phần còn thiếu, để họ chỉ cần sửa dòng sai. Ba mục bắt buộc là điểm đến, mục tiêu chính, thời gian/số ngày — thiếu một trong ba thì phải hỏi. Các mục còn lại có mặc định (1–2 người, ~800.000 đ/đêm cho cả phòng, thuê xe máy, không kiêng ăn...) và người dùng có thể ghi đè bất cứ lúc nào.

Nếu người dùng nói "cứ làm đi", đã trả lời đủ trong yêu cầu, hoặc không có mặt (chạy tự động), thì không hỏi nữa — dùng mặc định và ghi rõ tất cả giả định vào mục **Giả định** ở đầu file kế hoạch để họ thấy ngay cái gì là đoán.

## Bước 1 — Hiểu đặc trưng điểm đến

Trước khi tính ngày hay tìm phòng, dành một lượt tra cứu ngắn để hiểu **nơi này là gì** — vì đặc trưng của điểm đến quyết định mọi bước sau (mùa nào có gì, khu nào nên ở, điểm nào đáng đi, món nào phải thử, chỗ nào không được chụp). Tìm hiểu năm mặt:

1. **Lịch sử**: nơi này từng là gì, có dấu tích/di tích nào đáng kể, có câu chuyện nào làm thay đổi cách nhìn khi đứng ở đó (ví dụ Côn Đảo không chỉ là đảo đẹp mà là hệ thống nhà tù hơn 100 năm — điều này đổi cả nhịp và thái độ của chuyến đi).
2. **Văn hoá**: cộng đồng dân cư, tín ngưỡng, lễ hội, tập quán cần tôn trọng (trang phục ở đền chùa, giờ giấc, điều kiêng kỵ), ngôn ngữ/phương ngữ, đặc sản và cách ăn của người địa phương.
3. **Kinh tế**: người dân sống bằng gì (đánh cá, nông nghiệp, du lịch, công nghiệp), mặt bằng giá so với đất liền/thành phố lớn, có dùng chuyển khoản/thẻ rộng rãi hay chủ yếu tiền mặt, có ATM không, hàng hoá gì khan hiếm hoặc đắt (đảo xa thường đắt gấp rưỡi và hết hàng khi biển động). Điều này quyết định mang bao nhiêu tiền mặt và ngân sách ăn uống thực tế.
4. **Địa vị hành chính, an ninh và các đặc trưng riêng**: là đặc khu, vùng biên giới, khu vực có yếu tố quân sự hay quốc phòng (nhiều đảo tiền tiêu có khu vực cấm vào, cấm chụp ảnh, cấm bay drone; có thể cần giấy tờ tuỳ thân khi ra vào), vườn quốc gia/khu bảo tồn (phí, giấy phép, giờ đóng cửa), địa hình đặc biệt (đèo, đường độc đạo, không có đèn đường), khí hậu vi mô. Ghi rõ những gì **không được làm** ở đây — tránh một vi phạm vô ý phá hỏng cả chuyến đi.
5. **Tính chất du lịch**: điểm đến này phục vụ kiểu khách nào (nghỉ dưỡng cao cấp, phượt, tâm linh, gia đình, khách quốc tế), đã phát triển đến đâu (còn hoang sơ hay đã thương mại hoá), hạ tầng ra sao (đường, xe, tàu bay, mạng, ATM), mật độ khách theo mùa, và những gì người đi trước hay phàn nàn hoặc tiếc vì đã bỏ lỡ.

Đầu ra là mục **"Đặc trưng điểm đến"** dài khoảng 200–350 chữ ở đầu file kế hoạch, kết thúc bằng 2–4 gạch đầu dòng **"Điều này ảnh hưởng gì đến kế hoạch"** — ví dụ: "đảo có mùa dừng tàu → chọn bay", "đa số khách đi tour nhà tù buổi sáng → đi buổi chiều cho vắng", "dân đảo nghỉ trưa dài → quán đóng 13–16h". Nếu không rút ra được hệ quả nào cho kế hoạch thì mục này đang viết như bách khoa toàn thư, cần cắt lại.

## Bước 2 — Chọn thời điểm đi

Mục tiêu chuyến đi quyết định thời điểm, không phải ngược lại. Với mỗi mục tiêu, liệt kê các **điều kiện tự nhiên và xã hội** cần thoả mãn rồi giao chúng lại để tìm cửa sổ thời gian tốt nhất:

1. **Mùa / thời tiết** của vùng đó (mùa mưa, gió mùa, biển động, sương mù, nhiệt độ). Việt Nam có ít nhất 3 chế độ khí hậu khác nhau — Bắc, Trung, Nam — nên không suy từ Hà Nội ra Phú Quốc.
2. **Điều kiện đặc thù của mục tiêu**: pha trăng và độ cao dải Ngân hà (ngắm sao), giờ vàng và hướng mặt trời (chụp ảnh), thuỷ triều (lặn, chụp bãi đá), mùa hoa/mùa lúa chín (phong cảnh), lịch lễ hội.
3. **Yếu tố con người**: mùa cao điểm (giá phòng gấp đôi, đông), lễ tết, ngày cuối tuần, có tàu/máy bay hay không (nhiều đảo dừng tàu khi biển động).

Đầu ra của bước này là **một cửa sổ thời gian đề xuất + 1–2 phương án dự phòng**, kèm lý do ngắn cho từng ràng buộc. Nếu người dùng đã chốt ngày, bước này chuyển thành **kiểm tra rủi ro** cho ngày đó (trăng tròn? mùa mưa? lễ?) và gợi ý điều chỉnh mục tiêu nếu cần.

Đọc `references/goi-y-theo-muc-tieu.md` khi mục tiêu thuộc nhóm thiên văn, nhiếp ảnh, biển/lặn, núi/trekking — file đó có các quy tắc cụ thể (ví dụ tránh ±4 ngày quanh trăng tròn, kiểm tra tỷ lệ mây, tra lịch tàu).

## Bước 3 — Chọn khách sạn

Cách làm là **khoanh vùng trước, xếp hạng sau, rồi mới lọc theo mục tiêu**:

1. **Khoanh trục trung tâm.** Xác định 1–3 trục đường/khu vực mà mọi thứ xoay quanh (chợ, bến tàu, khu ăn uống, điểm thuê xe). Với chuyến đi có mục tiêu đặc biệt, "trung tâm" có thể lệch khỏi trung tâm hành chính — ví dụ chuyến ngắm sao thì nên ở gần bãi tối thay vì khu phố sáng đèn; chuyến chụp bình minh thì ở gần điểm chụp để không phải chạy xe 30 phút lúc 4h sáng. Ghi rõ "trung tâm" của kế hoạch này là đâu.
2. **Quét và xếp hạng** các khách sạn/homestay theo ba tiêu chí, theo thứ tự ưu tiên:
   - Khoảng cách tới trục trung tâm (gần → xa; ghi bằng km hoặc phút đi xe máy)
   - Rating Google Review **kèm số lượt đánh giá** — 4.8 với 12 review kém tin cậy hơn 4.5 với 600 review; đọc lướt vài review 1–2 sao gần nhất để bắt lỗi hệ thống (ồn, nước yếu, thái độ). Công cụ tìm kiếm thường không đọc được trực tiếp Google Maps và các trang đặt phòng lớn hay chặn; khi đó lấy rating từ nguồn tổng hợp còn đọc được (Wanderlog, Expedia, mia.vn, vntrip, trang của khách sạn, bài review có ảnh chụp màn hình rating) và ghi rõ **"4,6 (215) — theo Wanderlog"** thay vì bỏ trống cả cột. Chỉ gắn `[CẦN XÁC MINH]` khi thật sự không có nguồn nào; một bảng toàn cờ thì không giúp người đọc chọn được gì.
   - Giá/đêm so với ngân sách (mặc định ~800.000 đ; ghi giá đúng mùa đi, vì giá cao điểm và thấp điểm khác nhau nhiều)
3. **Lọc theo mục tiêu và yêu cầu đặc biệt**: hướng núi hay hướng biển, có sân thượng, có bếp, nhận phòng muộn, cho thuê xe máy tại chỗ, có chỗ để đồ chụp ảnh...

Trình bày thành **bảng shortlist 5–7 chỗ**, rồi **chọn ra top 3** với một câu lý do mỗi chỗ và một câu "điểm trừ" nếu có. Người dùng muốn thấy quá trình so sánh, không chỉ kết luận.

## Bước 4 — Lịch trình theo tuyến hướng (Đông – Tây – Nam – Bắc)

Đơn vị của lịch trình là **tuyến theo hướng**, không phải ngày. Lý do: một lịch theo ngày giả định quá nhiều thứ (giờ máy bay đến, thời tiết hôm đó, sức khoẻ, hứng thú) và sai một mắt xích là phải xếp lại toàn bộ; còn một tuyến "đi về phía Nam, mất nửa ngày, nên đi buổi chiều" thì vẫn đúng dù người dùng đảo thứ tự các ngày. Người dùng sẽ tự ghép tuyến vào ngày khi đến nơi — skill chỉ gợi ý cách ghép.

1. **Liệt kê điểm tham quan** phù hợp mục tiêu (lọc theo sở thích và số ngày; không liệt kê mọi thứ trên bản đồ).
2. **Chia thành tuyến theo hướng** tính từ chỗ ở: Bắc, Nam, Đông, Tây, và "Trung tâm" (đi bộ được). Nếu địa hình không vuông vắn (đảo dài, thung lũng, một trục đường độc đạo), chia theo trục đường hoặc theo "đi ra – quay về" nhưng vẫn đặt tên theo hướng để dễ hình dung. Mỗi tuyến là **một vòng đi–về từ chỗ ở**, thường 3–4 tuyến cho một chuyến 3–5 ngày.
3. **Với mỗi tuyến, viết thành một mục tự đủ**, gồm:
   - **Khoảng cách và thời lượng**: tổng km, thời gian di chuyển, thời gian tham quan → xếp vào loại *nửa ngày* hay *cả ngày*.
   - **Thời gian nên đi**: buổi nào trong ngày và vì sao (bãi hướng Đông chụp bình minh; đèo phía Tây chụp hoàng hôn; nhà tù/bảo tàng đi giữa trưa nắng; bãi tối ngắm sao sau 21h; chợ chỉ họp sáng). Nếu tuyến có **mỏ neo** (bình minh, thuỷ triều, giờ ngân hà lên, giờ mở cửa), ghi rõ giờ mỏ neo và xếp thứ tự điểm quanh nó.
   - **Thứ tự điểm dừng** trên tuyến: điểm, thời gian nên đến / thời gian ở lại, lý do đi (nhất là khi phục vụ mục tiêu chính), lưu ý (vé, đường xấu, cần đặt trước, cấm chụp).
   - **Ăn dọc tuyến**: 1–2 quán nằm trên đường (lấy từ Bước 5), để không phải quay về trung tâm ăn trưa.
   - **Điều kiện huỷ/thay thế**: tuyến này bỏ khi nào (mưa, biển động, sương mù) và thay bằng gì.
4. **Gợi ý ghép tuyến theo số ngày** — một bảng ngắn, trình bày là *gợi ý*, không phải lịch: ngày đến/đi thường chỉ còn nửa ngày nên ghép tuyến Trung tâm hoặc tuyến nửa ngày gần nhất; tuyến cả ngày xa nhất đặt vào ngày trọn vẹn; tuyến có mỏ neo đêm (ngắm sao) nên ghép với tuyến nhẹ ngày hôm sau. Nêu 1–2 cách ghép khác nhau nếu chuyến có tuỳ chọn (ví dụ có đi tour đảo hay không).
5. **Kế hoạch B** cho ngày mưa/biển động (bảo tàng, quán cà phê, chợ, spa) — đặc biệt khi mục tiêu chính phụ thuộc thời tiết.

### Đưa lịch trình lên Google My Maps

Một lịch trình trong file Markdown khó dùng khi đang chạy xe; bản đồ có ghim theo tuyến thì mở trên điện thoại là thấy ngay điểm tiếp theo cách bao xa. Vì không thể tạo My Maps thay người dùng (cần tài khoản Google của họ), skill tạo sẵn **file nhập** để họ tự nhập trong 2 phút:

1. Tạo file `ban-do-<diem-den>.csv` với các cột `ten, tuyen, thu_tu, lat, lng, dia_chi, gio, ghi_chu, loai` — mỗi dòng là một điểm dừng: điểm tham quan, bãi chụp, chỗ ở (top 1) và quán ăn đã chọn. Cột `tuyen` là "Tuyến Bắc", "Tuyến Nam"... hoặc "Chỗ ở" — mỗi giá trị thành một lớp riêng trên bản đồ, bật/tắt được; `thu_tu` là số thứ tự trên tuyến; `gio` là giờ nên đến (tuỳ chọn). Cột `dia_chi` là tên/địa chỉ đúng như trên Google Maps để My Maps tự định vị; toạ độ chỉ điền khi tra được từ nguồn tin cậy (ghi toạ độ đoán mò còn hại hơn để trống, vì ghim lệch 2 km trên đảo là lạc đường).
2. Nếu có toạ độ cho phần lớn điểm, chạy `python3 scripts/tao_kml.py ban-do-<diem-den>.csv --ten "<tên chuyến đi>"` để tạo file KML có sẵn lớp theo tuyến và màu ghim theo loại (đỏ tham quan, tím bãi chụp, cam ăn, xanh lá chỗ ở). Script sẽ liệt kê những điểm thiếu toạ độ để nhập bằng CSV.
3. Ghi vào cuối mục Lịch trình hướng dẫn 4 dòng: mở [Google My Maps](https://www.google.com/maps/d/) → Tạo bản đồ mới → Nhập (Import) → chọn file KML, hoặc CSV rồi chọn cột `dia_chi` làm vị trí và `ten` làm tiêu đề → nhập mỗi tuyến thành một lớp nếu dùng CSV. Nhắc họ kiểm tra lại ghim nào bị định vị sai (My Maps đôi khi ghim nhầm quán trùng tên ở tỉnh khác).

Gửi file CSV (và KML nếu có) cùng file kế hoạch.

## Bước 5 — Ăn uống

Quét quán ăn **quanh chỗ ở** (bán kính ~1–2 km hoặc 10 phút xe) và **quanh từng cụm tham quan** (để ăn trưa không phải quay về), rồi xếp hạng theo rating Google kèm số review. Bổ sung 2–3 **món đặc sản địa phương** với quán được nhắc đến nhiều nhất — rating cao nhưng toàn khách du lịch nước ngoài đánh giá không phải lúc nào cũng là quán ngon nhất theo khẩu vị Việt.

Ghép quán vào lịch trình từng ngày (ăn sáng gần khách sạn, ăn trưa gần cụm đang đi, ăn tối về trung tâm). Ghi giờ mở cửa vì nhiều quán địa phương nghỉ chiều hoặc đóng sớm.

## Bước 6 — Đóng gói để theo dõi trong chuyến đi

File Markdown là **bản gốc** để cân nhắc và sửa trước chuyến đi; nhưng khi đang ngoài đường, người dùng cần một thứ mở bằng một chạm trên điện thoại và cho biết ngay "điểm tiếp theo là gì, ở đâu". Vì vậy sau khi có file kế hoạch và file CSV, luôn tạo thêm **trang lịch trình di động**:

1. Chạy `python3 scripts/tao_trang_html.py <ke-hoach>.md <ban-do>.csv --artifact --out <ten>.artifact.html` — script tự dựng trang một file từ hai file kia: tab Tổng quan · từng Tuyến (Bắc/Nam/Đông/Tây/Trung tâm) · Ghép tuyến · Ăn uống · Chỗ ở · Việc cần làm · Nguồn; mỗi điểm dừng có nút mở Google Maps theo địa chỉ; checklist tick được và nhớ trạng thái; cờ `[CẦN XÁC MINH]` được tô vàng. Không viết HTML thủ công — script bảo đảm mọi chuyến đi cùng một giao diện đã thử trên màn hình điện thoại.
2. **Nếu có công cụ Artifact** (Cowork/Claude Code có Artifact): đăng file `.artifact.html` đó thành Artifact, favicon 🧭, mô tả một câu. Người dùng nhận được link mở trên điện thoại, chia sẻ cho người đi cùng, và khi kế hoạch đổi thì chạy lại script và đăng lại **cùng đường dẫn file** để giữ link.
3. **Nếu không có Artifact**: chạy script không có `--artifact` để ra file HTML hoàn chỉnh và gửi file đó — mở được trực tiếp trên điện thoại (kể cả offline).

Thứ tự bàn giao: link/trang di động trước (đó là thứ họ sẽ dùng nhiều nhất), rồi file Markdown, rồi CSV/KML. Lịch trình thay đổi thì sửa Markdown/CSV trước rồi chạy lại script — không sửa tay trong HTML, vì lần sau tạo lại sẽ mất.

## Tra cứu và độ tin cậy

Kế hoạch này dùng để đi thật, nên số liệu sai gây tốn tiền hoặc lỡ mục tiêu. Vì vậy:

- **Tra cứu web** cho giá phòng, rating/số review, thời tiết theo mùa, lịch trăng, lịch tàu/bay, giờ mở cửa. Ưu tiên nguồn gốc (Google Maps, trang đặt phòng, trang thời tiết, lịch thiên văn) hơn bài blog.
- Mọi con số ghi kèm **nguồn và ngày tra cứu**. Số liệu chỉ có từ nguồn thứ cấp hoặc không tra được thì gắn `[CẦN XÁC MINH]` ngay cạnh — không được bỏ trống và cũng không được bịa.
- Tuyệt đối không bịa tên khách sạn, quán ăn, rating. Nếu công cụ tìm kiếm không có, ghi rõ "chưa tra được, cần kiểm tra trên Google Maps" thay vì đoán.
- Cuối file có mục **Nguồn** liệt kê link đã dùng.

## Đầu ra

Tạo một file Markdown tên `ke-hoach-<diem-den>-<thang>.md` theo mẫu trong `references/mau-ke-hoach.md`. Đọc file mẫu trước khi viết. Nếu người dùng chỉ hỏi **một bước** (ví dụ chỉ hỏi nên đi tháng mấy), trả lời phần đó thôi, vẫn theo cách làm của bước tương ứng, không chạy checklist đầy đủ và không tạo file trừ khi họ yêu cầu. Câu hỏi nhanh xứng đáng câu trả lời nhanh: kết luận trước, 2–3 lý do, đánh đổi nếu có, nguồn gom vào một dòng — khoảng 150–300 chữ. Mẹo phụ và phần mở rộng để dành khi họ hỏi tiếp.

Ngôn ngữ: tiếng Việt, gọn, thực dụng. Không viết văn quảng cáo du lịch ("thiên đường nghỉ dưỡng"); viết như ghi chú cho chính mình.

