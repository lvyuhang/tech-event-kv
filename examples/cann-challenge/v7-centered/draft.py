import math, random
from pathlib import Path

OUT = Path("/home/claude/gen/v7/out"); OUT.mkdir(parents=True, exist_ok=True)
REFS = Path("/home/claude/tech-event-kv/examples/cann-challenge/v7-centered/refs")
W, H = 1920, 1080
CX, CY = 960, 600
SIX = [("#2F6BFF", "电光蓝"), ("#FF3D9A", "品红"), ("#B6F23A", "青柠"), ("#FF8A00", "橙"), ("#8B5CFF", "紫"), ("#00D4FF", "青")]
# wedge centre angles (deg, maths convention, y up); top (90) kept dark for the title, bottom (270) for the hands
ANG = [8, 48, 132, 172, 222, 318]
HALF = 17
FONT = "'Noto Sans CJK SC',sans-serif"


def f(v): return f"{v:.1f}"


def P(r, a, cx=CX, cy=CY):
    t = math.radians(a)
    return cx + r * math.cos(t), cy - r * math.sin(t)


def wedge(a, half=HALF, r=2600):
    x1, y1 = P(r, a - half); x2, y2 = P(r, a + half)
    return f"M{CX} {CY} L{f(x1)} {f(y1)} L{f(x2)} {f(y2)} Z"


def channel(k):
    a = ANG[k]; col = SIX[k][0]
    gx, gy = P(1300, a)
    o = [f'<linearGradient id="g{k}" gradientUnits="userSpaceOnUse" x1="{CX}" y1="{CY}" x2="{f(gx)}" y2="{f(gy)}">'
         f'<stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset=".12" stop-color="{col}" stop-opacity=".85"/>'
         f'<stop offset=".55" stop-color="{col}" stop-opacity=".3"/><stop offset="1" stop-color="{col}" stop-opacity=".05"/></linearGradient>',
         f'<clipPath id="w{k}"><path d="{wedge(a)}"/></clipPath>']
    body = [f'<path d="{wedge(a)}" fill="url(#g{k})"/>']
    g = []
    for d in (-HALF, -HALF / 2, 0, HALF / 2, HALF):  # perspective rays
        x, y = P(2600, a + d); g.append(f'<line x1="{CX}" y1="{CY}" x2="{f(x)}" y2="{f(y)}"/>')
    r = 60
    while r < 2400:  # depth rings, spacing grows outward
        g.append(f'<circle cx="{CX}" cy="{CY}" r="{f(r)}" fill="none"/>')
        r *= 1.32
    body.append(f'<g clip-path="url(#w{k})" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="1.2">{"".join(g)}</g>')
    return "".join(o), "".join(body)


def panel(kind, x, y, w, h, col, rot, rnd):
    o = [f'<g transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})">',
         f'<rect x="{f(x+6)}" y="{f(y+8)}" width="{f(w)}" height="{f(h)}" rx="6" fill="#000" fill-opacity=".45"/>']
    if kind == "code":
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="#141027" stroke="{col}" stroke-width="2"/>')
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h*.13)}" rx="6" fill="{col}" fill-opacity=".85"/>')
        yy = y + h * .24
        for i in range(6):
            xx = x + w * .08 + (i % 3) * w * .05
            for seg in range(rnd.randint(1, 3)):
                ln = w * rnd.uniform(.12, .3)
                c = rnd.choice(["#FF3D9A", "#00D4FF", "#B6F23A", "#FF8A00", "#C9C3E8"])
                o.append(f'<rect x="{f(xx)}" y="{f(yy)}" width="{f(ln)}" height="{f(h*.045)}" rx="2" fill="{c}"/>')
                xx += ln + w * .03
            yy += h * .11
    elif kind == "checker":
        n = 8; c = w / n
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="#F2F0FA"/>')
        for i in range(n):
            for j in range(int(h / c)):
                if (i + j) % 2:
                    o.append(f'<rect x="{f(x+i*c)}" y="{f(y+j*c)}" width="{f(c)}" height="{f(c)}" fill="#120C2A"/>')
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="{col}" stroke-width="3"/>')
    elif kind == "chart":
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="4" fill="#2A1C7A" stroke="#FFFFFF" stroke-opacity=".6"/>')
        for i in range(1, 6):
            o.append(f'<line x1="{f(x+w*i/6)}" y1="{f(y)}" x2="{f(x+w*i/6)}" y2="{f(y+h)}" stroke="#fff" stroke-opacity=".18"/>')
        pts = []
        for i in range(13):
            pts.append(f"{f(x+w*i/12)},{f(y+h*(.85 - .6*(i/12)**1.6 + rnd.uniform(-.06,.06)))}")
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="3"/>')
    elif kind == "term":
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="#07050F" stroke="#FFFFFF" stroke-opacity=".5"/>')
        for i in range(3):
            o.append(f'<circle cx="{f(x+14+i*14)}" cy="{f(y+14)}" r="4" fill="{["#FF5F57","#FEBC2E","#28C840"][i]}"/>')
        o.append(f'<rect x="{f(x+w*.08)}" y="{f(y+h*.45)}" width="{f(w*.06)}" height="{f(h*.12)}" fill="{col}"/>')
        o.append(f'<rect x="{f(x+w*.18)}" y="{f(y+h*.45)}" width="{f(w*.5)}" height="{f(h*.12)}" fill="#C9C3E8" fill-opacity=".7"/>')
        o.append(f'<rect x="{f(x+w*.08)}" y="{f(y+h*.68)}" width="{f(w*.05)}" height="{f(h*.12)}" fill="{col}"/>')
    elif kind == "prism":
        o = [f'<g transform="rotate({rot} {f(x+w/2)} {f(y+h/2)})">',
             f'<polygon points="{f(x)},{f(y+h*.3)} {f(x+w*.75)},{f(y)} {f(x+w)},{f(y+h*.25)} {f(x+w*.25)},{f(y+h*.55)}" fill="{col}"/>',
             f'<polygon points="{f(x)},{f(y+h*.3)} {f(x+w*.25)},{f(y+h*.55)} {f(x+w*.25)},{f(y+h)} {f(x)},{f(y+h*.75)}" fill="#1B1240"/>',
             f'<polygon points="{f(x+w*.25)},{f(y+h*.55)} {f(x+w)},{f(y+h*.25)} {f(x+w)},{f(y+h*.7)} {f(x+w*.25)},{f(y+h)}" fill="{col}" fill-opacity=".55"/>']
    o.append("</g>")
    return "".join(o)


def cube(cx, cy, s):
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    top = (cx, cy - s); right = (cx + s * c30, cy - s * s30); left = (cx - s * c30, cy - s * s30)
    mid = (cx, cy); br = (cx + s * c30, cy + s * s30); bl = (cx - s * c30, cy + s * s30); bot = (cx, cy + s)
    def poly(pts, fill, op=1):
        return f'<polygon points="{" ".join(f"{f(a)},{f(b)}" for a, b in pts)}" fill="{fill}" fill-opacity="{op}"/>'
    o = [f'<circle cx="{cx}" cy="{cy}" r="{s*2.2:.0f}" fill="url(#halo)"/>',
         poly([top, right, mid, left], "#FFFFFF"), poly([left, mid, bot, bl], "#D9D2FF"), poly([mid, right, br, bot], "#B4A8FF")]
    def grid(p00, p10, p01, p11, n=4, col="#6B4CF6"):
        g = []
        for i in range(n):
            for j in range(n):
                def bil(u, v):
                    return ((1-u)*(1-v)*p00[0]+u*(1-v)*p10[0]+(1-u)*v*p01[0]+u*v*p11[0], (1-u)*(1-v)*p00[1]+u*(1-v)*p10[1]+(1-u)*v*p01[1]+u*v*p11[1])
                q = .1
                pts = [bil((i+q)/n, (j+q)/n), bil((i+1-q)/n, (j+q)/n), bil((i+1-q)/n, (j+1-q)/n), bil((i+q)/n, (j+1-q)/n)]
                lit = (i, j) in [(1, 2), (2, 1)]
                g.append(poly(pts, ("#FF8A00" if (i + j) % 2 else "#C6FF3D") if lit else "#FFFFFF", .95 if lit else .55))
        return g
    o += grid(left, mid, bl, bot) + grid(mid, right, bot, br) + grid(left, top, mid, right, col="#8B5CFF")
    return "".join(o)


def hand(cx, base_y, mirror):
    # simplified wireframe hand: palm + four fingers + thumb, outline + contour lines
    sx = -1 if mirror else 1
    def tr(x, y): return f"{f(cx + sx*x)},{f(base_y + y)}"
    palm = [(-70, 120), (-80, 10), (-40, -40), (60, -60), (90, 0), (80, 120)]
    fingers = [[(-40, -40), (-30, -170), (-10, -175), (0, -48)], [(0, -48), (15, -210), (38, -212), (32, -55)],
               [(32, -55), (55, -195), (78, -190), (62, -56)], [(62, -56), (95, -150), (113, -142), (90, -2)],
               [(-80, 10), (-170, -50), (-160, -70), (-62, -26)]]
    o = []
    st = 'fill="#3A1F9A" fill-opacity=".35" stroke="#B9A6FF" stroke-width="2"'
    o.append(f'<polygon points="{" ".join(tr(*p) for p in palm)}" {st}/>')
    for fg in fingers:
        o.append(f'<polygon points="{" ".join(tr(*p) for p in fg)}" {st}/>')
    for k in range(1, 6):
        y = 120 - k * 30
        o.append(f'<line x1="{tr(-75, y).split(",")[0]}" y1="{f(base_y+y)}" x2="{tr(85, y).split(",")[0]}" y2="{f(base_y+y)}" stroke="#B9A6FF" stroke-opacity=".5"/>')
    return "".join(o)


def nanjing_wall(cx, cy, w):
    o = []
    x = cx - w / 2
    o.append(f'<rect x="{f(cx-w/2)}" y="{f(cy)}" width="{f(w)}" height="16" fill="#3A2A70"/>')
    while x < cx + w / 2:
        o.append(f'<rect x="{f(x)}" y="{f(cy-9)}" width="10" height="9" fill="#3A2A70"/>'); x += 18
    return "".join(o)


def draft():
    rnd = random.Random(5)
    defs, body = [], []
    for k in range(6):
        d, b = channel(k); defs.append(d); body.append(b)
    for a in [90 + 25, 90 - 25, 270 + 30, 270 - 30, 0 + 90 + 50, 90 - 50]:
        x, y = P(2400, a)
        body.append(f'<line x1="{CX}" y1="{CY}" x2="{f(x)}" y2="{f(y)}" stroke="#FFFFFF" stroke-opacity=".22" stroke-width="1"/>')
    body.append(nanjing_wall(CX, CY + 2, 150))
    # panels along channels: (channel, radius, kind, size)
    plan = [(0, 330, "code", 150), (0, 640, "chart", 260), (1, 700, "prism", 110), (1, 900, "checker", 200),
            (2, 680, "code", 220), (3, 330, "checker", 140), (3, 640, "chart", 250),
            (4, 360, "prism", 150), (4, 640, "term", 260), (5, 380, "code", 170), (5, 650, "checker", 240)]
    for k, r, kind, s in plan:
        x, y = P(r, ANG[k] + rnd.uniform(-4, 4))
        w, h = s, s * (0.62 if kind in ("code", "term", "chart") else 1)
        body.append(panel(kind, x - w / 2, y - h / 2, w, h, SIX[k][0], rnd.uniform(-12, 12), rnd))
    body.append(cube(CX, CY - 10, 70))

    defs.append('<radialGradient id="halo"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset=".4" stop-color="#C9B8FF" stop-opacity=".35"/><stop offset="1" stop-color="#8B5CFF" stop-opacity="0"/></radialGradient>'
                '<radialGradient id="vig" cx=".5" cy=".55" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
                '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .6 0"/></filter>')
    svg = (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0"><defs>{"".join(defs)}</defs>'
           f'<rect width="{W}" height="{H}" fill="#0A0618"/>{"".join(body)}'
           f'<rect width="{W}" height="{H}" fill="url(#vig)"/><rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16"/></svg>')
    txt = f'''<div style="position:absolute;left:0;top:70px;width:{W}px;text-align:center;color:#fff;font-family:{FONT}">
<div style="font-weight:700;font-size:40px;letter-spacing:6px">CANN 挑战赛</div>
<div style="font-weight:900;font-size:132px;letter-spacing:-2px;line-height:1.1">全国总决赛</div>
<div style="font-weight:500;font-size:38px;letter-spacing:10px;margin-top:4px">以算为锋，奔赴金陵</div></div>
<div style="position:absolute;left:0;bottom:36px;width:{W}px;text-align:center;color:#fff;font-family:{FONT};font-weight:500;font-size:24px;letter-spacing:4px">12 月 5 日｜中国·南京</div>
<div style="position:absolute;left:60px;top:44px;display:flex;gap:14px">{''.join('<div style="width:110px;height:34px;border:1.5px dashed rgba(255,255,255,.35);border-radius:4px"></div>' for _ in range(3))}</div>'''
    return svg + txt


def moodboard():
    imgs = [("ref_a_purple_corridor.png", "借：近黑紫底、一点透视网格墙、悬浮平面面板、线框手、颗粒"),
            ("ref_b_orange_burst.png", "借：喷枪颗粒渐变、物件沿放射方向飞、跳跃配色"),
            ("ref_c_vanke_collage.png", "借：平面与立体拼贴、虹彩边、漂浮物的超现实感")]
    cards = "".join(f'<div style="display:flex;flex-direction:column;gap:10px"><img src="{(REFS/n).as_uri()}" style="width:580px;height:326px;object-fit:cover;border-radius:6px"/>'
                    f'<div style="font-size:20px;color:#D8D3F0">{t}</div></div>' for n, t in imgs)
    sw = "".join(f'<div style="display:flex;flex-direction:column;gap:8px;align-items:flex-start"><div style="width:120px;height:72px;background:{c}"></div>'
                 f'<div style="font-size:18px;color:#D8D3F0">{n} <span style="font-family:monospace;color:#8C86A8">{c}</span></div></div>' for c, n in SIX)
    rules = ["构图和概念按 brief：严格居中、一点透视、六路汇聚到中心（南京 · 总决赛）",
             "六条通道各一种赛区色，中心白热；其余是近黑紫 #0A0618",
             "物件是开发者的东西：代码窗（只有抽象色线）、矩阵分块、性能曲线、终端、数据棱柱；≤ 14 件",
             "平面为主、少量 3D；全画面颗粒；不做发光玻璃和光轨",
             "不要 &lt;/&gt;、{}、0/1、复古电脑、地球、电竞人物"]
    rl = "".join(f'<div style="font-size:20px;color:#EDEAF8;line-height:1.6">· {r}</div>' for r in rules)
    return f'''<div style="position:absolute;inset:0;background:#0A0618;font-family:{FONT};padding:56px 60px;box-sizing:border-box">
<div style="display:flex;align-items:baseline;gap:20px"><div style="font-size:40px;font-weight:900;color:#fff">情绪版 · 居中汇聚 × 数字拼贴</div>
<div style="font-size:20px;color:#8C86A8">参考图只借风格；构图与概念来自 brief</div></div>
<div style="display:flex;gap:30px;margin-top:36px">{cards}</div>
<div style="display:flex;gap:60px;margin-top:44px"><div><div style="font-size:24px;font-weight:700;color:#fff;margin-bottom:16px">六赛区色</div><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px 26px">{sw}</div></div>
<div style="flex:1"><div style="font-size:24px;font-weight:700;color:#fff;margin-bottom:12px">规则</div>{rl}</div></div></div>'''


def shoot(name, inner):
    p = OUT / f"{name}.html"
    p.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0}}</style></head><body><div style="position:relative;width:{W}px;height:{H}px;overflow:hidden">{inner}</div></body></html>', encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width": W, "height": H}); pg.goto(p.as_uri()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT / f"{name}.png")); b.close()


shoot("v7_layout_draft", draft())
shoot("v7_moodboard", moodboard())
print("ok")
