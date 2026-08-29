#!/usr/bin/env python3
"""
Chuyển bảng điểm dừng (CSV) của lịch trình thành file KML để nhập vào Google My Maps.

Cách dùng:
    python3 tao_kml.py ban-do-con-dao.csv            # tạo ban-do-con-dao.kml
    python3 tao_kml.py ban-do-con-dao.csv --ten "Côn Đảo 4–7/5/2027"

CSV cần các cột (không phân biệt hoa thường, thứ tự tuỳ ý):
    ten        - tên điểm (bắt buộc)
    tuyen      - "Tuyến Bắc", "Tuyến Nam"... hoặc "Chỗ ở" → mỗi giá trị thành một lớp (layer). (Cột cũ `ngay` vẫn đọc được.)
    thu_tu     - số thứ tự điểm dừng trên tuyến (tuỳ chọn)
    lat, lng   - toạ độ (tuỳ chọn; nếu thiếu, dòng đó bị bỏ qua trong KML và được liệt kê ra để nhập bằng CSV)
    dia_chi    - địa chỉ hoặc chuỗi tìm kiếm Google Maps (tuỳ chọn, đưa vào mô tả)
    gio        - giờ dự kiến (tuỳ chọn)
    ghi_chu    - ghi chú (tuỳ chọn)
    loai       - "tham quan" | "an" | "o" | "chup" (tuỳ chọn, đổi màu ghim)

My Maps giới hạn 10 lớp / bản đồ và 2.000 điểm / lớp — với một chuyến đi cá nhân thì thoải mái.
"""
import csv
import sys
import argparse
from xml.sax.saxutils import escape
from collections import OrderedDict

MAU = {  # màu KML dạng aabbggrr
    "tham quan": "ff0000ff",  # đỏ
    "chup": "ffff00ff",       # tím
    "an": "ff00a5ff",         # cam
    "o": "ff00ff00",          # xanh lá
    "khac": "ffff0000",       # xanh dương
}


def doc_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("CSV rỗng.")
    # chuẩn hoá tên cột
    out = []
    for r in rows:
        out.append({(k or "").strip().lower(): (v or "").strip() for k, v in r.items()})
    return out


def toa_do(r):
    try:
        return float(r.get("lat", "")), float(r.get("lng", ""))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--ten", default=None, help="Tên bản đồ")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rows = doc_csv(a.csv)
    ten_ban_do = a.ten or a.csv.rsplit(".", 1)[0]
    out = a.out or a.csv.rsplit(".", 1)[0] + ".kml"

    lop = OrderedDict()
    thieu = []
    for r in rows:
        if not r.get("ten"):
            continue
        td = toa_do(r)
        if td is None:
            thieu.append(r["ten"])
            continue
        lop.setdefault(r.get("tuyen") or r.get("ngay") or "Khác", []).append((r, td))

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>',
             f"<name>{escape(ten_ban_do)}</name>"]
    for k, mau in MAU.items():
        parts.append(f'<Style id="{k.replace(" ", "_")}"><IconStyle><color>{mau}</color>'
                     '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon></IconStyle></Style>')
    def _tt(x):
        try:
            return int(float(x[0].get("thu_tu", "")))
        except ValueError:
            return 10**6

    for ten_lop, items in lop.items():
        items = sorted(items, key=_tt)
        parts.append(f"<Folder><name>{escape(ten_lop)}</name>")
        for r, (lat, lng) in items:
            loai = (r.get("loai") or "khac").lower()
            if loai not in MAU:
                loai = "khac"
            mo_ta = []
            if r.get("gio"):
                mo_ta.append(f"Giờ: {r['gio']}")
            if r.get("dia_chi"):
                mo_ta.append(f"Địa chỉ: {r['dia_chi']}")
            if r.get("ghi_chu"):
                mo_ta.append(r["ghi_chu"])
            tt = r.get("thu_tu")
            ten = (f"{tt}. " if tt else "") + (f"{r['gio']} " if r.get("gio") else "") + r["ten"]
            parts.append(
                f"<Placemark><name>{escape(ten)}</name>"
                f"<description>{escape(' | '.join(mo_ta))}</description>"
                f'<styleUrl>#{loai.replace(" ", "_")}</styleUrl>'
                f"<Point><coordinates>{lng},{lat},0</coordinates></Point></Placemark>")
        parts.append("</Folder>")
    parts.append("</Document></kml>")

    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"Đã tạo {out}: {sum(len(v) for v in lop.values())} điểm, {len(lop)} lớp ({', '.join(lop)}).")
    if thieu:
        print(f"{len(thieu)} điểm thiếu toạ độ, không vào KML — nhập bằng CSV (My Maps tự định vị theo cột dia_chi):")
        for t in thieu:
            print("  -", t)


if __name__ == "__main__":
    main()
