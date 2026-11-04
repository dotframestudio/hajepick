# 이 문서로 알 수 있는 것: 하제픽 링크 페이지 만들기 — links.json 을 읽어 index.html 을 다시 만든다.
# 쓰는 법: python build.py  (links.json 에 상품을 이어 붙인 뒤) → git commit → git push
# links.json 한 줄 = {"no": 1, "name": "상품 이름", "shop": "쿠팡" 또는 "카카오", "url": "제휴 링크", "note": "한 줄 추천", "added": "2026-11-05"}
# 왜: 쇼츠 자막 "프로필 링크 N번" → 이 페이지 N번. 공정위 수수료 문구 · AI 가상 인물 표시는 맨 위에 늘 고정(지우지 않기).
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
links = json.loads((HERE / "links.json").read_text(encoding="utf-8"))
nos = [x["no"] for x in links]
if len(nos) != len(set(nos)):
    raise SystemExit("links.json 번호가 겹쳐요 — 번호는 한 번 쓰면 바꾸지 않아요")
for x in links:
    if not x.get("url", "").startswith("https://"):
        raise SystemExit(f"{x.get('no')}번 링크가 https 가 아니에요")

def card(x):
    e = html.escape
    shop = e(x.get("shop", ""))
    note = f'<p class="note">{e(x["note"])}</p>' if x.get("note") else ""
    return (f'<a class="card" id="n{x["no"]}" href="{e(x["url"])}" target="_blank" rel="sponsored noopener">'
            f'<span class="no">{x["no"]}</span><span class="body"><span class="name">{e(x["name"])}</span>{note}'
            f'<span class="shop shop-{shop}">{shop}</span></span></a>')

cards = "\n".join(card(x) for x in sorted(links, key=lambda x: -x["no"]))
if not cards:
    cards = '<p class="empty">첫 추천 상품이 곧 올라와요 ✨</p>'

page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HAJE PICK 하제픽 · 추천 링크</title>
<meta name="description" content="하제가 리뷰를 다 읽고 고른 추천 상품 링크 모음">
<meta name="robots" content="noindex">
<style>
:root{{--bg:#fff6f2;--ink:#1d1a24;--soft:#6b6475;--pink:#ff4f8b;--violet:#7b5cff;--card:#fff}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Pretendard,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:linear-gradient(160deg,#ffe3ec,#efe8ff 60%,#e6f6ff);color:var(--ink);min-height:100vh}}
main{{max-width:480px;margin:0 auto;padding:28px 18px 48px}}
.top{{text-align:center}}.top img{{width:104px;height:104px;border-radius:50%;border:3px solid #fff;box-shadow:0 6px 20px #7b5cff33}}
h1{{font-size:22px;margin:12px 0 2px;letter-spacing:.5px}}.sub{{color:var(--soft);font-size:14px;margin:0}}
.notice{{background:#ffffffcc;border-radius:14px;padding:12px 14px;font-size:12.5px;line-height:1.55;color:#4a4453;margin:18px 0}}
.notice b{{color:var(--ink)}}
.find{{display:flex;gap:8px;margin:0 0 14px}}.find input{{flex:1;border:0;border-radius:12px;padding:12px 14px;font-size:16px;background:#fff}}
.card{{display:flex;gap:14px;align-items:center;background:var(--card);border-radius:16px;padding:14px 16px;margin:10px 0;color:inherit;text-decoration:none;box-shadow:0 3px 12px #1d1a2410;transition:transform .12s}}
.card:active{{transform:scale(.98)}}.card:target{{outline:3px solid var(--pink)}}
.no{{min-width:46px;height:46px;border-radius:12px;background:linear-gradient(135deg,var(--pink),var(--violet));color:#fff;font-weight:800;font-size:20px;display:flex;align-items:center;justify-content:center}}
.body{{display:flex;flex-direction:column;gap:3px}}.name{{font-weight:700;font-size:15px}}.note{{margin:0;font-size:13px;color:var(--soft)}}
.shop{{font-size:11px;font-weight:700;color:var(--violet)}}.shop-쿠팡{{color:#e4443a}}.shop-카카오{{color:#c79a00}}
.empty{{text-align:center;color:var(--soft);padding:30px 0}}
.sns{{display:flex;justify-content:center;gap:10px;margin:22px 0 6px}}.sns a{{background:#fff;border-radius:999px;padding:9px 16px;font-size:13px;font-weight:700;color:var(--ink);text-decoration:none}}
footer{{text-align:center;font-size:11.5px;color:var(--soft);margin-top:16px}}footer a{{color:inherit}}
</style></head><body><main>
<div class="top"><img src="haje.jpg" alt="하제 프로필"><h1>HAJE PICK 하제픽</h1><p class="sub">리뷰 다 읽고 골라 주는 하제의 추천 🛍️</p></div>
<div class="notice">
<b>쇼츠에서 본 번호를 찾아 눌러 주세요.</b><br>
이 페이지의 링크는 쿠팡 파트너스 · 카카오 선물하기 큐레이터 활동의 일환으로, 구매하시면 이에 따른 일정액의 수수료를 제공받습니다. 가격은 바뀔 수 있으니 구매 전 상품 페이지에서 확인해 주세요.<br>
<b>하제는 AI로 만든 가상 인물이에요.</b> 직접 써 본 후기가 아니라, 리뷰와 정보를 보고 고른 추천이에요.
</div>
<div class="find"><input id="q" inputmode="numeric" placeholder="번호로 찾기 (예: 3)" aria-label="번호로 찾기"></div>
<div id="list">
{cards}
</div>
<div class="sns"><a href="https://www.youtube.com/@hajepick" target="_blank" rel="noopener">YouTube</a><a href="https://www.instagram.com/hajepick/" target="_blank" rel="noopener">Instagram</a></div>
<footer>문의 <a href="mailto:studiodotframe@gmail.com">studiodotframe@gmail.com</a> · © 닷프레임 스튜디오</footer>
</main>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{{const v=q.value.trim();document.querySelectorAll('.card').forEach(c=>{{c.style.display=(!v||c.id==='n'+v)?'':'none'}})}});
</script>
</body></html>
"""
(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"index.html 만듦 - 상품 {len(links)}개")
