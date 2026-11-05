"""Computation-body KV sample (direction A '计算力场'), FORCE-style flat graphic.
Renders SVG + HTML text, screenshots with playwright.
"""
import math, random, sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/gen/force/out")
OUT.mkdir(parents=True, exist_ok=True)

C = dict(bg="#07070B", dot="#DADDE8", line="#7E859E", rim="#9AA0B4",
         p1="#8B6CFF", p2="#4B2FC9", p0="#2A1C7A", org="#FF5A1F", org2="#FF8A3D",
         blue="#2F6BFF", white="#E9EBF2", grey="#8C93A8", lime="#C6FF3D", ink="#F3F4F8")


def f(v):
    return f"{v:.1f}"


class Body:
    """A complete sphere with a stepped opening on its lower right."""

    def __init__(self, cx, cy, R, light=(0.55, -0.55, 0.63), pitch=8.0,
                 top_off=-70, x_start=170, step_w=58, step_h=60, t=26, focus=(130, 200), mirror=False):
        self.m = mirror
        self.cx, self.cy, self.R = cx, cy, R
        n = math.sqrt(sum(v * v for v in light))
        self.L = tuple(v / n for v in light)
        self.pitch = pitch
        s = R / 430.0
        self.s = s
        self.y_top = cy + top_off * s
        self.x0 = cx + x_start * s
        self.sw, self.sh, self.t = step_w * s, step_h * s, t * s
        self.F = (cx + focus[0] * s, cy + focus[1] * s)

    def stair_x(self, y):
        if y < self.y_top:
            return 1e9
        k = int((y - self.y_top) // self.sh)
        return self.x0 - k * self.sw

    def in_open(self, x, y, pad=0):
        if self.m:
            x = 2 * self.cx - x
        return y >= self.y_top - pad and x >= self.stair_x(y) - pad

    def stair_poly(self, dx=0, dy=0, far=4000):
        pts = [(far, self.y_top), (self.x0, self.y_top)]
        y, x = self.y_top, self.x0
        while y < self.cy + self.R + self.sh:
            y += self.sh
            pts.append((x, y))
            x -= self.sw
            pts.append((x, y))
        pts.append((x, far)); pts.append((far, far))
        return " ".join(f"{f(px+dx)},{f(py+dy)}" for px, py in pts)

    def svg(self, uid="b", dots=True, opening=True, outline=True):
        cx, cy, R, p = self.cx, self.cy, self.R, self.pitch
        o = [f'<defs><clipPath id="c{uid}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R-1)}"/></clipPath>'
             f'<clipPath id="d{uid}"><polygon points="{self.stair_poly(self.t, self.t)}"/></clipPath>'
             f'<radialGradient id="deep{uid}" cx="{f(self.F[0])}" cy="{f(self.F[1])}" r="{f(R*.9)}" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0" stop-color="#1A0E3A"/><stop offset=".55" stop-color="#05040A"/><stop offset="1" stop-color="#000"/></radialGradient>'
             f'<radialGradient id="core{uid}" cx="{f(self.F[0]-20*self.s)}" cy="{f(self.F[1]-30*self.s)}" r="{f(170*self.s)}" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0" stop-color="{C["org2"]}"/><stop offset=".7" stop-color="{C["org"]}"/><stop offset="1" stop-color="#C2300A"/></radialGradient></defs>']
        # body fill: very dark so the dots read as volume
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="#0B0B12"/>')
        lx, ly, lz = self.L
        dot_parts, line_parts = [], []
        if dots:
            y = cy - R + p / 2
            while y < cy + R:
                x = cx - R + p / 2
                run_start = None
                row = int((y - cy + R) // p)
                xo = (p / 2) if row % 2 else 0
                xs = cx - R + p / 2 + xo
                x = xs
                while x < cx + R:
                    dx, dy = (x - cx) / R, (y - cy) / R
                    d2 = dx * dx + dy * dy
                    if d2 < 1 and not (opening and self.in_open(x, y, pad=p * .2)):
                        nz = math.sqrt(1 - d2)
                        lam = max(0.0, dx * lx + dy * ly + nz * lz)
                        rim = (1 - nz) ** 3
                        v = max(0.0, (lam - 0.22) / 0.78)
                        if v > 0.02:
                            r = 0.5 * p * (0.18 + 0.78 * v ** 0.75)
                            op = 0.55 + 0.45 * v
                            dot_parts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r:.2f}" fill-opacity="{op:.2f}"/>')
                        elif rim > 0.08:
                            dot_parts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{0.9+1.4*rim:.2f}" fill-opacity="{0.25+0.5*rim:.2f}"/>')
                    x += p
                y += p * 0.866
            # line raster on the shadow side (线栅)
            yy = cy - R + 3
            while yy < cy + R:
                x = cx - R
                seg = None
                while x <= cx + R:
                    dx, dy = (x - cx) / R, (yy - cy) / R
                    d2 = dx * dx + dy * dy
                    ok = False
                    if d2 < 1 and not (opening and self.in_open(x, yy)):
                        nz = math.sqrt(1 - d2)
                        lam = max(0.0, dx * lx + dy * ly + nz * lz)
                        ok = lam < 0.30
                    if ok and seg is None:
                        seg = x
                    if (not ok) and seg is not None:
                        if x - seg > 6:
                            line_parts.append(f"M{f(seg)} {f(yy)}H{f(x)}")
                        seg = None
                    x += 3
                if seg is not None:
                    line_parts.append(f"M{f(seg)} {f(yy)}H{f(x)}")
                yy += 5.5 * self.s
        o.append(f'<path d="{"".join(line_parts)}" stroke="{C["line"]}" stroke-opacity=".42" stroke-width="{1.1*self.s:.2f}" fill="none"/>')
        o.append(f'<g fill="{C["dot"]}">{"".join(dot_parts)}</g>')
        if opening:
            t = self.t
            mt = f'transform="translate({f(2*cx)} 0) scale(-1 1)"' if self.m else ''
            o.append(f'<g clip-path="url(#c{uid})"><g {mt}>')
            o.append(f'<polygon points="{self.stair_poly()}" fill="{C["p1"]}"/>')          # top faces
            o.append(f'<polygon points="{self.stair_poly(0, t)}" fill="{C["p2"]}"/>')       # side faces
            o.append(f'<polygon points="{self.stair_poly(t, t)}" fill="url(#deep{uid})"/>')  # depth
            o.append(f'<g clip-path="url(#d{uid})">')
            o.append(f'<circle cx="{f(self.F[0])}" cy="{f(self.F[1])}" r="{f(135*self.s)}" fill="url(#core{uid})"/>')
            o.append(self.tiles())
            o.append('</g></g></g>')
            # stair edge hairline + lime node
            o.append(f'<polygon points="{self.stair_poly()}" fill="none" stroke="{C["p1"]}" stroke-opacity=".0"/>')
        if outline:
            o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="none" stroke="{C["rim"]}" stroke-opacity=".55" stroke-width="{1.4*self.s:.2f}"/>')
        return "\n".join(o)

    def tiles(self, seed=7):
        rnd = random.Random(seed)
        s = self.s
        pitch = 38 * s
        size = 32 * s
        Fx, Fy = self.F
        o = []
        cols = []
        gx0 = Fx - 9 * pitch
        gy0 = Fy - 9 * pitch
        lime_left = 2
        for i in range(19):
            for j in range(19):
                x = gx0 + i * pitch
                y = gy0 + j * pitch
                cxm, cym = x + size / 2, y + size / 2
                if not self.in_open((2*self.cx-(cxm-self.t)) if self.m else (cxm-self.t), cym - self.t):
                    continue
                if (cxm - self.cx) ** 2 + (cym - self.cy) ** 2 > (self.R - 6) ** 2:
                    continue
                d = math.hypot(cxm - Fx, cym - Fy) / s
                # ordered core: whole aligned tiles in a stepped block
                if d < 118:
                    if rnd.random() < 0.12:
                        continue
                    r = rnd.random()
                    col = C["org2"] if (d < 50 and r < .5) else (C["blue"] if r < .32 else (C["white"] if r < .85 else C["grey"]))
                    if lime_left and rnd.random() < 0.05:
                        col = C["lime"]; lime_left -= 1
                    o.append(self.tile(x, y, size, col))
                else:
                    if d > 300:
                        continue
                    n = 2 if d < 215 else 3
                    drop = 0.45 if n == 2 else 0.78
                    sub = pitch / n
                    ss = sub * 0.82
                    jit = (d - 125) / 300 * 7 * s
                    for a in range(n):
                        for b in range(n):
                            if rnd.random() < drop:
                                continue
                            sx = x + a * sub + rnd.uniform(-jit, jit)
                            sy = y + b * sub + rnd.uniform(-jit, jit)
                            r = rnd.random()
                            col = C["blue"] if r < .3 else (C["white"] if r < .62 else (C["grey"] if r < .9 else C["org"]))
                            o.append(self.tile(sx, sy, ss, col, flat=n == 3))
        return "".join(o)

    def tile(self, x, y, size, col, flat=False):
        if flat:
            return f'<rect x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size)}" fill="{col}"/>'
        e = max(1.5, size * 0.12)
        return (f'<rect x="{f(x+e)}" y="{f(y+e)}" width="{f(size)}" height="{f(size)}" fill="#000" fill-opacity=".55"/>'
                f'<rect x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size)}" fill="{col}"/>'
                f'<rect x="{f(x)}" y="{f(y)}" width="{f(size)}" height="{f(size*.18)}" fill="#fff" fill-opacity=".22"/>')


FONT = "'Noto Sans CJK SC','Noto Sans SC',sans-serif"
MONO = "'DejaVu Sans Mono',monospace"


def html(body, w, h):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;background:{C["bg"]};}} .wrap{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{C["bg"]};font-family:{FONT};color:{C["ink"]}}}
.abs{{position:absolute}}
</style></head><body><div class="wrap">{body}</div></body></html>'''


def kv_final():
    b = Body(1300, 545, 440, top_off=60, x_start=150, focus=(90, 255), mirror=True)
    svg = f'<svg class="abs" style="left:0;top:0" width="1920" height="1080">{b.svg("m")}' \
          f'<rect x="{f(2*b.cx-b.x0-6)}" y="{f(b.y_top-6)}" width="12" height="12" fill="{C["lime"]}"/></svg>'
    txt = f'''
<div class="abs" style="left:110px;top:64px;display:flex;gap:18px">{''.join('<div style="width:132px;height:40px;border:1.5px dashed rgba(255,255,255,.28);border-radius:4px;font:500 13px '+MONO+';color:rgba(255,255,255,.5);display:flex;align-items:center;justify-content:center;letter-spacing:2px">LOGO</div>' for _ in range(3))}</div>
<div class="abs" style="left:110px;top:332px">
 <div style="font-weight:700;font-size:54px;letter-spacing:3px;line-height:1">CANN 挑战赛</div>
 <div style="font-weight:900;font-size:176px;letter-spacing:-4px;line-height:1.08;margin-top:14px;white-space:nowrap">全国总决赛</div>
 <div style="font-weight:500;font-size:50px;letter-spacing:10px;line-height:1;margin-top:26px;color:#E3E5EE">以算为锋，奔赴金陵</div>
 <div style="display:flex;align-items:center;gap:14px;margin-top:40px;font-weight:500;font-size:28px;letter-spacing:3px;color:#A8AEC2">
  <span style="width:12px;height:12px;background:{C["lime"]};display:inline-block"></span>12 月 5 日｜中国·南京</div>
</div>'''
    return html(svg + txt, 1920, 1080)


def sheet():
    W, H = 1920, 1080
    parts = []
    # 1 stepped outline -> info frame
    s1 = Body(0, 0, 430)
    def stair_frame(x, y, w, h, step=34, n=3, col=C["p1"]):
        pts = [(x, y), (x + w - n * step, y)]
        cx, cy = x + w - n * step, y
        for k in range(n):
            cy += step * .9; pts.append((cx, cy)); cx += step; pts.append((cx, cy))
        pts += [(x + w, y + h), (x, y + h)]
        pp = " ".join(f"{f(a)},{f(b)}" for a, b in pts)
        return f'<polygon points="{pp}" fill="none" stroke="{col}" stroke-width="2"/>'
    a1 = stair_frame(70, 250, 520, 150)
    a1b = stair_frame(70, 430, 250, 92, step=22)
    # 2 tile core -> numeral "5" built from tiles (aligned core + fragmented edge)
    five = ["11111", "10000", "11110", "00001", "00001", "10001", "01110"]
    rnd = random.Random(3)
    t2 = []
    ox, oy, pc = 770, 236, 40
    for j, row in enumerate(five):
        for i, ch in enumerate(row):
            if ch != "1":
                continue
            x, y = ox + i * pc, oy + j * pc
            edge = (i == 0 and j >= 5)
            col = C["org2"] if (i, j) in [(1, 2), (2, 2), (3, 2)] else (C["blue"] if (i + j) % 3 == 0 else C["white"])
            if (i, j) == (4, 4):
                col = C["lime"]
            if edge:
                for a in range(2):
                    for b in range(2):
                        if rnd.random() < .3:
                            continue
                        t2.append(s1.tile(x + a * pc / 2 + rnd.uniform(-2, 2), y + b * pc / 2 + rnd.uniform(-2, 2), pc / 2 * .8, rnd.choice([C["white"], C["grey"], C["blue"]]), flat=True))
            else:
                t2.append(s1.tile(x, y, pc * .84, col))
    # 3 halftone texture -> background patch (partial body)
    tex = Body(1520, 600, 300, pitch=7.0)
    texsvg = f'<g clip-path="url(#texclip)">{tex.svg("t", opening=False, outline=False)}</g>'
    swatches = [("#07070B", "近黑 · 背景 / 安静区"), ("#DADDE8", "灰白网点 · 外层体积"), ("#8B6CFF", "紫 · 剖面顶面"),
                ("#4B2FC9", "深紫 · 剖面侧面"), ("#FF5A1F", "橙 · 内核暖"), ("#2F6BFF", "蓝 · 内核冷"), ("#C6FF3D", "黄绿 · 激活节点（极少）")]
    sw = "".join(f'<div style="display:flex;align-items:center;gap:14px"><div style="width:46px;height:46px;background:{c};border:1px solid rgba(255,255,255,.15)"></div>'
                 f'<div style="font-size:19px;color:#C9CDD9">{n}<span style="font:14px {MONO};color:#7E859E;margin-left:10px">{c}</span></div></div>' for c, n in swatches)
    svg = (f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}"><defs><clipPath id="texclip"><rect x="1300" y="236" width="520" height="290"/></clipPath></defs>'
           f'{a1}{a1b}{"".join(t2)}{texsvg}<rect x="1300" y="236" width="520" height="290" fill="none" stroke="rgba(255,255,255,.12)"/></svg>')
    lab = lambda x, y, t, sub: f'<div class="abs" style="left:{x}px;top:{y}px"><div style="font-weight:700;font-size:24px">{t}</div><div style="font-size:17px;color:#8C93A8;margin-top:6px">{sub}</div></div>'
    txt = (lab(70, 140, "① 阶梯开口 → 信息框 / 导视端部", "主体开口的台阶轮廓，切成框的一角")
           + lab(770, 140, "② 分块内核 → 编号 / 局部构字", "整齐归位的整块 + 边缘碎裂的小块")
           + lab(1300, 140, "③ 外层网点 → 背景 / 局部体积", "同一套网点与线栅，只取局部")
           + f'<div class="abs" style="left:96px;top:282px;font-weight:500;font-size:30px;letter-spacing:3px">12 月 5 日｜中国·南京</div>'
           + f'<div class="abs" style="left:92px;top:456px;font-weight:700;font-size:26px;letter-spacing:2px">签到处 →</div>'
           + f'<div class="abs" style="left:770px;top:530px;font:15px {MONO};color:#7E859E">倒计时 05 DAYS（示意）</div>'
           + '<div class="abs" style="left:70px;top:46px;font-weight:900;font-size:34px">计算力场 · 风格校准</div>'
           + '<div class="abs" style="left:430px;top:58px;font-size:18px;color:#8C93A8">从主样本里取出的三类同源资产、色彩角色和标题字样；色值与比例未锁定</div>'
           + f'<div class="abs" style="left:70px;top:640px;font-weight:700;font-size:24px">色彩角色</div><div class="abs" style="left:70px;top:690px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 40px;width:760px">{sw}</div>'
           + f'<div class="abs" style="left:1000px;top:640px;font-weight:700;font-size:24px">标题字样 · 思源黑体（Noto Sans CJK，SIL OFL 可商用）</div>'
           + f'<div class="abs" style="left:1000px;top:690px;font-weight:900;font-size:120px;letter-spacing:-3px;line-height:1">全国总决赛</div>'
           + f'<div class="abs" style="left:1000px;top:836px;font-weight:500;font-size:40px;letter-spacing:8px">以算为锋，奔赴金陵</div>'
           + f'<div class="abs" style="left:1000px;top:906px;font-size:17px;color:#8C93A8">Black 900 · 字距 -2% ／ Medium 500 · 字距 +16% ／ 字身直立，不加发光、描边、斜体</div>')
    return html(svg + txt, W, H)


def shoot(name, content, w, h):
    p = OUT / f"{name}.html"
    p.write_text(content, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": w, "height": h})
        pg.goto(p.as_uri()); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"{name}.png"))
        br.close()


if __name__ == "__main__":
    shoot("kv1_sample", kv_final(), 1920, 1080)
    shoot("calibration_sheet", sheet(), 1920, 1080)
    print("done", OUT)
