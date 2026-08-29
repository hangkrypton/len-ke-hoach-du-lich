#!/usr/bin/env python3
"""
Tạo trang HTML một file, tối ưu cho điện thoại, từ file kế hoạch Markdown (theo mẫu
references/mau-ke-hoach.md) và file CSV bản đồ (ban-do-<diem-den>.csv).

Cách dùng:
    python3 tao_trang_html.py ke-hoach-con-dao-thang-5-2027.md ban-do-con-dao.csv
    python3 tao_trang_html.py ke-hoach.md ban-do.csv --out chuyen-di-con-dao.html --artifact

--artifact : bỏ <!doctype>/<html>/<head>/<body> để đăng bằng công cụ Artifact (Artifact tự bọc khung).
             Không có cờ này thì tạo file HTML hoàn chỉnh, mở trực tiếp trên điện thoại/trình duyệt được.

Trang gồm các tab: Tổng quan · từng Tuyến (Bắc/Nam/Đông/Tây/Trung tâm) · Ghép tuyến · Ăn uống · Chỗ ở · Việc cần làm · Nguồn.
Mỗi điểm dừng trong CSV có nút mở Google Maps theo cột dia_chi (hoặc toạ độ nếu có).
Checklist "Việc cần làm" nhớ trạng thái tick trong trình duyệt (localStorage, có try/catch).
"""
import argparse
import csv
import html
import json
import re
import sys
from collections import OrderedDict
from urllib.parse import quote_plus

# ---------- Markdown → HTML (dùng thư viện nếu có, không thì bộ chuyển tối giản) ----------
try:
    import markdown as _md

    def md_to_html(text):
        return _md.markdown(text, extensions=["tables", "sane_lists"])
except ImportError:  # bộ chuyển tối giản: heading, bảng, list, bold, link, checkbox
    def _inline(s):
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s

    def md_to_html(text):
        out, lines, i = [], text.splitlines(), 0
        while i < len(lines):
            ln = lines[i]
            if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-", lines[i + 1]):
                hdr = [c.strip() for c in ln.strip("|").split("|")]
                rows, i = [], i + 2
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
                out.append("<table><thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in hdr) + "</tr></thead><tbody>")
                for r in rows:
                    out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
                out.append("</tbody></table>"); continue
            m = re.match(r"^(#{1,6})\s+(.*)", ln)
            if m:
                out.append(f"<h{len(m.group(1))}>{_inline(m.group(2))}</h{len(m.group(1))}>"); i += 1; continue
            if re.match(r"^\s*[-*]\s+", ln):
                out.append("<ul>")
                while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                    item = re.sub(r'^\s*[-*]\s+', '', lines[i]); out.append(f"<li>{_inline(item)}</li>"); i += 1
                out.append("</ul>"); continue
            if re.match(r"^\s*\d+\.\s+", ln):
                out.append("<ol>")
                while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                    item = re.sub(r'^\s*\d+\.\s+', '', lines[i]); out.append(f"<li>{_inline(item)}</li>"); i += 1
                out.append("</ol>"); continue
            if ln.strip():
                out.append(f"<p>{_inline(ln)}</p>")
            i += 1
        return "\n".join(out)


def tien_xu_ly(md):
    """Chèn dòng trống trước danh sách hoặc dòng '**Nhãn:**' đi ngay sau text thường,
    vì bộ chuyển Markdown sẽ nhồi chúng vào cùng một đoạn nếu thiếu dòng trống."""
    out, prev = [], ""
    for ln in md.splitlines():
        bat_dau_khoi = re.match(r"^\s*([-*]\s+|\d+\.\s+|\*\*[^*]+:\*\*|#{1,6}\s|\|)", ln)
        prev_la_text = prev.strip() and not re.match(r"^\s*([-*]\s+|\d+\.\s+|\|)", prev) and not prev.startswith("#")
        if bat_dau_khoi and prev_la_text:
            out.append("")
        out.append(ln); prev = ln
    return "\n".join(out)


# ---------- Đọc kế hoạch ----------
def tach_muc(md):
    """Trả về (tiêu đề, phần mở đầu, OrderedDict {tên mục '## ' → nội dung})."""
    title, intro, sections, cur = "", [], OrderedDict(), None
    for ln in md.splitlines():
        if ln.startswith("# ") and not title:
            title = ln[2:].strip(); continue
        m = re.match(r"^##\s+(.*)", ln)
        if m and not ln.startswith("###"):
            cur = m.group(1).strip(); sections[cur] = []; continue
        (sections[cur] if cur else intro).append(ln)
    return title, "\n".join(intro), OrderedDict((k, "\n".join(v)) for k, v in sections.items())


def tim_muc(sections, *tu_khoa):
    for k, v in sections.items():
        kl = k.lower()
        if any(t in kl for t in tu_khoa):
            return k, v
    return None, ""


def tach_tuyen(lich_trinh_md):
    """Từ mục Lịch trình: (phần đầu trước ###, [(tiêu đề tuyến, nội dung)], phần sau — gợi ý ghép tuyến, kế hoạch B, bản đồ)."""
    dau, tuyen, cur, sau = [], [], None, []
    for ln in lich_trinh_md.splitlines():
        m = re.match(r"^###\s+(.*)", ln)
        if m and cur != "SAU":
            cur = [m.group(1).strip(), []]; tuyen.append(cur); continue
        if cur is None:
            dau.append(ln)
        elif cur == "SAU":
            sau.append(ln)
        elif re.match(r"^\*\*(Gợi ý ghép|Kế hoạch B|Bản đồ)", ln):
            sau.append(ln); cur = "SAU"
        else:
            cur[1].append(ln)
    return "\n".join(dau), [(t, "\n".join(b)) for t, b in tuyen], "\n".join(sau)


def doc_csv(path):
    if not path:
        return OrderedDict()
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    lop = OrderedDict()
    for r in rows:
        if r.get("ten"):
            lop.setdefault(r.get("tuyen") or r.get("ngay") or "Khác", []).append(r)
    return lop


def link_maps(r):
    try:
        lat, lng = float(r.get("lat", "")), float(r.get("lng", ""))
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    except ValueError:
        return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(r.get("dia_chi") or r["ten"])


FLAG_RE = re.compile(r"\[CẦN XÁC MINH[^\]]*\]")


def the_diem(r):
    loai = (r.get("loai") or "khac").lower().replace(" ", "-")
    gio = f'<span class="gio">{html.escape(r["gio"])}</span>' if r.get("gio") else ""
    ghi_txt = FLAG_RE.sub(lambda m: '<span class="flag">' + m.group(0) + '</span>', html.escape(r.get("ghi_chu", "")))
    ghi = f'<div class="ghi">{ghi_txt}</div>' if r.get("ghi_chu") else ""
    return (f'<div class="diem {loai}">{gio}<div class="than"><div class="ten">{html.escape(r["ten"])}</div>{ghi}</div>'
            f'<a class="maps" href="{link_maps(r)}" target="_blank" rel="noopener" aria-label="Mở Google Maps">Maps ↗</a></div>')


HUONG = ["trung tâm", "đông bắc", "đông nam", "tây bắc", "tây nam", "bắc", "nam", "đông", "tây"]


def huong_cua(tieu_de):
    """Lấy chữ hướng trong 'Tuyến Bắc — ...' / 'Tuyến Trung tâm' / 'Ngày 2'."""
    t = tieu_de.lower()
    for h in HUONG:
        if re.search(r"\b" + h + r"\b", t):
            return h
    m = re.match(r"(ngày\s*\d+)", t)
    return m.group(1).replace(" ", "") if m else t.strip()


def khop_tuyen(tieu_de_tuyen, lop):
    """Ghép '### Tuyến Bắc — ...' với lớp CSV 'Tuyến Bắc' (so theo chữ hướng)."""
    key = huong_cua(tieu_de_tuyen)
    for k, v in lop.items():
        if huong_cua(k) == key:
            def _t(r):  # thứ tự trên tuyến; nếu thiếu thì theo giờ; nếu thiếu nốt thì giữ nguyên
                try:
                    return (0, int(float(r.get("thu_tu", ""))))
                except ValueError:
                    m2 = re.match(r"(\d{1,2})[:h](\d{2})?", r.get("gio", ""))
                    return (1, int(m2.group(1)) * 60 + int(m2.group(2) or 0)) if m2 else (2, 0)
            return sorted(v, key=_t)
    return []


def checklist_html(md):
    items, rest = [], []
    for ln in md.splitlines():
        m = re.match(r"^\s*-\s*\[( |x|X)\]\s*(.*)", ln)
        if m:
            items.append((m.group(1).lower() == "x", m.group(2)))
        else:
            rest.append(ln)
    out = ['<ul class="checklist">']
    for i, (done, txt) in enumerate(items):
        out.append(f'<li><label><input type="checkbox" data-i="{i}" {"checked" if done else ""}> <span>{md_to_html(txt).replace("<p>", "").replace("</p>", "")}</span></label></li>')
    out.append("</ul>")
    return "\n".join(out) + md_to_html("\n".join(rest))


CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#1e1e1c;--muted:#6b6a66;--line:#e4e2dc;--acc:#0b6e4f;--acc-ink:#fff;
--tham-quan:#c0392b;--chup:#8e44ad;--an:#e67e22;--o:#27ae60;--khac:#2f6fb3}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#141513;--card:#1e201d;--ink:#ecebe6;--muted:#a3a29c;--line:#31342f;--acc:#3fbf8f;--acc-ink:#0c1a14}}
:root[data-theme="dark"]{--bg:#141513;--card:#1e201d;--ink:#ecebe6;--muted:#a3a29c;--line:#31342f;--acc:#3fbf8f;--acc-ink:#0c1a14}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
header{padding:16px 16px 8px}header h1{font-size:1.25rem;margin:0 0 4px}header .sub{color:var(--muted);font-size:.9rem}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:6px;overflow-x:auto;padding:8px 12px;-webkit-overflow-scrolling:touch}
nav button{flex:0 0 auto;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:6px 12px;font-size:.9rem;white-space:nowrap}
nav button.on{background:var(--acc);color:var(--acc-ink);border-color:var(--acc)}
main{padding:12px 12px 48px;max-width:720px;margin:0 auto}section{display:none}section.on{display:block}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 12px}
.card h2,.card h3{font-size:1.05rem;margin:0 0 8px}.card h4{margin:12px 0 4px}
.diem{display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-top:1px solid var(--line)}.diem:first-of-type{border-top:0}
.nen-di{background:var(--bg);border-radius:8px;padding:8px 10px;margin:0 0 8px;font-size:.95rem}
.diem .gio{flex:0 0 52px;font-variant-numeric:tabular-nums;color:var(--muted);font-size:.9rem;padding-top:2px}
.diem .than{flex:1;min-width:0}.diem .ten{font-weight:600}.diem .ghi{color:var(--muted);font-size:.9rem}
.diem::before{content:"";flex:0 0 4px;align-self:stretch;border-radius:2px;background:var(--khac)}
.diem.tham-quan::before{background:var(--tham-quan)}.diem.chup::before{background:var(--chup)}.diem.an::before{background:var(--an)}.diem.o::before{background:var(--o)}
a.maps{flex:0 0 auto;font-size:.85rem;text-decoration:none;color:var(--acc);border:1px solid var(--acc);border-radius:8px;padding:4px 8px;align-self:center}
details{margin:8px 0}summary{cursor:pointer;color:var(--acc);font-weight:600}
table{border-collapse:collapse;width:100%;font-size:.9rem;display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;background:linear-gradient(to right,var(--card) 30%,rgba(0,0,0,0)),linear-gradient(to left,var(--card) 30%,rgba(0,0,0,0)),linear-gradient(to right,rgba(0,0,0,.12),rgba(0,0,0,0)),linear-gradient(to left,rgba(0,0,0,.12),rgba(0,0,0,0));background-position:left,right,left,right;background-repeat:no-repeat;background-size:40px 100%,40px 100%,14px 100%,14px 100%;background-attachment:local,local,scroll,scroll}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--bg)}.checklist{list-style:none;padding:0;margin:0}.checklist li{padding:8px 0;border-top:1px solid var(--line)}.checklist li:first-child{border-top:0}
.checklist label{display:flex;gap:10px;align-items:flex-start}.checklist input{width:20px;height:20px;margin-top:2px;flex:0 0 auto}
a{color:var(--acc)}code{font-size:.9em}.flag{background:#fff3cd;color:#6b4e00;border-radius:4px;padding:0 4px}
"""

JS = """
const tabs=[...document.querySelectorAll('nav button')],secs=[...document.querySelectorAll('main section')];
function show(id){tabs.forEach(b=>b.classList.toggle('on',b.dataset.t===id));secs.forEach(s=>s.classList.toggle('on',s.id===id));
 try{localStorage.setItem('kh_tab',id)}catch(e){}}
tabs.forEach(b=>b.addEventListener('click',()=>show(b.dataset.t)));
let first=secs[0]&&secs[0].id;try{const s=localStorage.getItem('kh_tab');if(s&&document.getElementById(s))first=s}catch(e){}
if(first)show(first);
const KEY='kh_check_'+(document.body.dataset.key||'');
document.querySelectorAll('.checklist input').forEach(cb=>{
 try{const st=JSON.parse(localStorage.getItem(KEY)||'{}');if(cb.dataset.i in st)cb.checked=st[cb.dataset.i]}catch(e){}
 cb.addEventListener('change',()=>{try{const st=JSON.parse(localStorage.getItem(KEY)||'{}');st[cb.dataset.i]=cb.checked;localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}})});
"""


def build(md_path, csv_path, out, artifact):
    md = tien_xu_ly(open(md_path, encoding="utf-8").read())
    title, intro, sec = tach_muc(md)
    lop = doc_csv(csv_path)

    def flag(h):
        return FLAG_RE.sub(r'<span class="flag">\g<0></span>', h)

    tabs, panels = [], []

    def add(tid, label, inner):
        tabs.append(f'<button data-t="{tid}">{html.escape(label)}</button>')
        panels.append(f'<section id="{tid}">{inner}</section>')

    # Tổng quan
    k1, v1 = tim_muc(sec, "đặc trưng")
    k2, v2 = tim_muc(sec, "thời điểm")
    tq = f'<div class="card">{flag(md_to_html(intro))}</div>'
    if v2:
        tq += f'<div class="card"><h2>{html.escape(k2)}</h2>{flag(md_to_html(v2))}</div>'
    if v1:
        tq += f'<div class="card"><h2>{html.escape(k1)}</h2>{flag(md_to_html(v1))}</div>'
    add("tongquan", "Tổng quan", tq)

    # Tuyến theo hướng
    klt, vlt = tim_muc(sec, "lịch trình")
    dau, tuyen, sau = tach_tuyen(vlt) if vlt else ("", [], "")
    for i, (td, body) in enumerate(tuyen, 1):
        stops = khop_tuyen(td, lop)
        # dòng "**Nên đi:** ..." đưa lên đầu thẻ để thấy ngay lúc nào nên đi tuyến này
        nen_di = re.search(r"^\*\*Nên đi:\*\*.*$", body, re.M)
        inner = f'<div class="card"><h2>{html.escape(td)}</h2>'
        if nen_di:
            inner += f'<p class="nen-di">{flag(md_to_html(nen_di.group(0)))[3:-4]}</p>'
        if stops:
            inner += "".join(the_diem(r) for r in stops)
            inner += f"<details><summary>Chi tiết tuyến</summary>{flag(md_to_html(body))}</details>"
        else:
            inner += flag(md_to_html(body))
        inner += "</div>"
        if i == 1 and dau.strip():
            inner += f"<details class=\"card\"><summary>Tổng quan các tuyến</summary>{flag(md_to_html(dau))}</details>"
        label = huong_cua(td)
        label = label[0].upper() + label[1:] if label else f"Tuyến {i}"
        add(f"tuyen{i}", label, inner)
    if sau.strip():
        add("ghep", "Ghép tuyến", f'<div class="card">{flag(md_to_html(sau))}</div>')

    # Ăn uống
    ka, va = tim_muc(sec, "ăn uống")
    an = ""
    an_rows, seen = [], set()
    for k, v in lop.items():
        for r in v:
            if ("ăn" in k.lower() or (r.get("loai") or "").lower() == "an") and r["ten"] not in seen:
                seen.add(r["ten"]); an_rows.append(r)
    if an_rows:
        an += '<div class="card"><h2>Quán đã chọn</h2>' + "".join(the_diem(r) for r in an_rows) + "</div>"
    if va:
        an += f'<div class="card"><h2>{html.escape(ka)}</h2>{flag(md_to_html(va))}</div>'
    if an:
        add("an", "Ăn uống", an)

    # Chỗ ở
    ko, vo = tim_muc(sec, "chỗ ở", "khách sạn")
    o = ""
    o_rows, seen_o = [], set()
    for k, v in lop.items():
        for r in v:
            if ("chỗ ở" in k.lower() or (r.get("loai") or "").lower() == "o") and r["ten"] not in seen_o:
                seen_o.add(r["ten"]); o_rows.append(r)
    if o_rows:
        o += '<div class="card"><h2>Nơi ở</h2>' + "".join(the_diem(r) for r in o_rows) + "</div>"
    if vo:
        o += f'<div class="card"><h2>{html.escape(ko)}</h2>{flag(md_to_html(vo))}</div>'
    if o:
        add("o", "Chỗ ở", o)

    # Việc cần làm
    kv, vv = tim_muc(sec, "việc cần làm", "checklist")
    if vv:
        add("viec", "Việc cần làm", f'<div class="card"><h2>{html.escape(kv)}</h2>{flag(checklist_html(vv))}</div>')

    # Nguồn + các mục còn lại
    kn, vn = tim_muc(sec, "nguồn")
    if vn:
        add("nguon", "Nguồn", f'<div class="card"><h2>{html.escape(kn)}</h2>{md_to_html(vn)}</div>')

    key = re.sub(r"[^a-z0-9]+", "-", title.lower())[:60]
    body = (f"<header><h1>{html.escape(title)}</h1><div class=\"sub\">Chọn tuyến theo hướng · mỗi tuyến ghi lúc nào nên đi · nút Maps dẫn thẳng tới địa chỉ</div></header>"
            f"<nav>{''.join(tabs)}</nav><main>{''.join(panels)}</main>")
    if artifact:
        page = f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n<div data-key=\"{key}\" id=\"app\">{body}</div>\n<script>document.body.dataset.key='{key}';{JS}</script>"
    else:
        page = (f"<!doctype html><html lang=\"vi\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
                f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body data-key=\"{key}\">{body}<script>{JS}</script></body></html>")
    open(out, "w", encoding="utf-8").write(page)
    print(f"Đã tạo {out} ({len(page)//1024} KB): {len(tuyen)} tuyến, {sum(len(v) for v in lop.values())} điểm có nút Maps.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ke_hoach_md")
    ap.add_argument("ban_do_csv", nargs="?", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--artifact", action="store_true", help="xuất nội dung không có khung html/head/body để đăng Artifact")
    a = ap.parse_args()
    out = a.out or re.sub(r"\.md$", "", a.ke_hoach_md) + (".artifact.html" if a.artifact else ".html")
    build(a.ke_hoach_md, a.ban_do_csv, out, a.artifact)
