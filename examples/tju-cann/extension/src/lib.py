"""CANN 开发者俱乐部 · 设计语言组件库 v2
从定稿 KV 提炼的规则：
  1. 一切落在网格单元 u 上；黑色描边 = 0.035u，只描卡片，不描背景格
  2. 背景 = 浅灰 + 白色网格；约 20–30% 的格子留空
  3. 标志画面 hero_field：蓝底 + 台阶编号 + 黄橙绿三色斜条 + 彩色玻璃，按画幅重新生成
  4. 像素风景要出血（顶部蓝色雪山向右散成像素点 / 底部绿色像素山压边）
  5. 标题卡可以带台阶缺口，与周围格子咬合
  6. 数字、编号、标签用像素字；标题用超粗黑体
"""
import random, math
import numpy as np
from scipy.spatial import Voronoi
from PIL import ImageFont

BLUE, YEL, GRN, ORG, CYAN, BLK, WHT, BG = '#0057FF', '#FFC100', '#0CC736', '#FF6A00', '#00CEFF', '#050505', '#FCFBFC', '#EAEAEA'
LBLUE, GRID_B, GLASS_LINE, HILL = '#009EFF', '#1A66FF', '#07394E', '#26BB45'
HEAVY = 'Noto Sans CJK SC'
PIXEL = 'FusionPixel'
_heavy = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
_pixel = '/home/claude/work/v2/fonts/fusion-pixel-12px-proportional-zh_hans.ttf'
_fcache = {}


def measure(txt, size, font=HEAVY, ls=0):
    path = _pixel if font == PIXEL else _heavy
    key = (path, 200)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, 200, index=2 if path == _heavy else 0)  # index 2 = SC
    return _fcache[key].getlength(txt) * size / 200 + ls * size * max(len(txt) - 1, 0)


def fit(txt, w, font=HEAVY, maxsize=999, ls=0):
    return min(maxsize, w / (measure(txt, 1, font) + ls * max(len(txt) - 1, 0)))



PIXFONT = {
 '0': ["01110","10001","10011","10101","11001","10001","01110"],
 '1': ["00100","01100","00100","00100","00100","00100","01110"],
 '2': ["01110","10001","00001","00110","01000","10000","11111"],
 '3': ["11110","00001","00001","01110","00001","00001","11110"],
 '4': ["00010","00110","01010","10010","11111","00010","00010"],
 '5': ["11111","10000","11110","00001","00001","10001","01110"],
 '6': ["00110","01000","10000","11110","10001","10001","01110"],
 '7': ["11111","00001","00010","00100","01000","01000","01000"],
 '8': ["01110","10001","10001","01110","10001","10001","01110"],
 '9': ["01110","10001","10001","01111","00001","00010","01100"],
 'X': ["10001","10001","01010","00100","01010","10001","10001"],
 ':': ["0","1","1","0","1","1","0"],
 '.': ["0","0","0","0","0","1","1"],
 '-': ["000","000","000","111","000","000","000"],
 ' ': ["00","00","00","00","00","00","00"],
 '/': ["00001","00010","00010","00100","01000","01000","10000"],
}


def _pix_rects(x, y, txt, h, color):
    p = h / 7
    out, cx = [], x
    for ch in txt:
        g = PIXFONT[ch]
        for j, row in enumerate(g):
            run = None
            for i, c in enumerate(row + '0'):
                if c == '1' and run is None:
                    run = i
                elif c != '1' and run is not None:
                    out.append(f'<rect x="{cx+run*p:.2f}" y="{y+j*p:.2f}" width="{(i-run)*p+0.3:.2f}" height="{p+0.3:.2f}"/>')
                    run = None
        cx += (len(g[0]) + 1) * p
    return f'<g fill="{color}">{"".join(out)}</g>', cx - x - p


def pix_width(txt, h):
    p = h / 7
    return sum((len(PIXFONT[c][0]) + 1) * p for c in txt) - p


class Doc:
    def __init__(self, W, H, u):
        self.W, self.H, self.u = W, H, u
        self.sw = u * 0.035
        self.parts = []
        self.defs = []
        self._id = 0

    def nid(self):
        self._id += 1
        return f'i{self._id}'

    def add(self, s):
        self.parts.append(s)

    # ------------------------------------------------------------- 基础
    def grid_bg(self, x=0, y=0, w=None, h=None, fill=BG, line=WHT, step=None, lw=None):
        w = self.W if w is None else w
        h = self.H if h is None else h
        step = step or self.u
        lw = lw or self.u * 0.03
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
        xs = np.arange(x, x + w + 0.1, step)
        ys = np.arange(y, y + h + 0.1, step)
        s += f'<path d="{"".join(f"M{v:.2f} {y}V{y+h}" for v in xs)}{"".join(f"M{x} {v:.2f}H{x+w}" for v in ys)}" stroke="{line}" stroke-width="{lw}"/>'
        self.add(s)

    def card(self, x, y, w, h, fill=WHT, notch=None, stroke=True, rx=0):
        """notch=(corner, nw, nh)，corner ∈ tl tr bl br：切掉一角形成台阶"""
        if notch:
            c, nw, nh = notch
            pts = {'tr': [(x, y), (x + w - nw, y), (x + w - nw, y + nh), (x + w, y + nh), (x + w, y + h), (x, y + h)],
                   'tl': [(x + nw, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y + nh), (x + nw, y + nh)],
                   'br': [(x, y), (x + w, y), (x + w, y + h - nh), (x + w - nw, y + h - nh), (x + w - nw, y + h), (x, y + h)],
                   'bl': [(x, y), (x + w, y), (x + w, y + h), (x + nw, y + h), (x + nw, y + h - nh), (x, y + h - nh)]}[c]
            d = 'M' + 'L'.join(f'{a:.2f} {b:.2f}' for a, b in pts) + 'Z'
            self.add(f'<path d="{d}" fill="{fill}" stroke="{BLK if stroke else "none"}" stroke-width="{self.sw}" stroke-linejoin="miter"/>')
        else:
            self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{BLK if stroke else "none"}" stroke-width="{self.sw}"/>')

    def text(self, x, y, txt, size, fill=BLK, font=HEAVY, anchor='start', ls=0, weight=900, baseline='central'):
        fam = f"'{font}'"
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-weight="{weight}" font-size="{size:.2f}" fill="{fill}" '
                 f'text-anchor="{anchor}" dominant-baseline="{baseline}" letter-spacing="{ls*size:.2f}">{txt}</text>')

    def ftext(self, x, y, w, h, txt, fill=BLK, font=HEAVY, anchor='middle', maxsize=999, ls=0, pad=0):
        """在盒子里按宽度撑满（不超过高度限制）"""
        size = min(fit(txt, w - 2 * pad, font, maxsize, ls), h)
        tx = {'start': x + pad, 'middle': x + w / 2, 'end': x + w - pad}[anchor]
        self.text(tx, y + h / 2 + (size * 0.04 if font == HEAVY else 0), txt, size, fill, font, anchor, ls)
        return size

    def crop(self, vb, x, y, w, h, par='xMidYMid meet', black=False):
        cx, cy, cw, ch = vb
        cid = self.nid()
        self.add(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{cx} {cy} {cw} {ch}" preserveAspectRatio="{par}" overflow="hidden">'
                 f'<clipPath id="{cid}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath>'
                 + (f'<filter id="{cid}f" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -0.8 -0.8 -0.8 0 2.35"/></filter>' if black else '')
                 + f'<image href="kv.svg" width="1408" height="784" clip-path="url(#{cid})"' + (f' filter="url(#{cid}f)"' if black else '') + '/></svg>')

    # ------------------------------------------------------------- KV 像素图标（只裁图形本身，不带格子边框）
    ICONS = {
        'npu': ((36, 132, 165, 175), BLUE), 'mug': ((722, 402, 110, 128), WHT), 'flower': ((872, 400, 140, 130), '#00C2FF'),
        'plus': ((712, 10, 88, 95), BLUE), 'times': ((820, 10, 92, 95), WHT), 'sigma': ((930, 10, 90, 95), YEL),
        'matrix': ((712, 133, 310, 82), BG), 'member': ((720, 240, 270, 143), None), 'spark': ((862, 545, 165, 80), WHT),
        'cal': ((10, 418, 220, 128), WHT), 'hello': ((14, 337, 205, 46), BLK), 'logos': ((1060, 16, 290, 50), BLUE),
        'cann': ((257, 210, 426, 124), WHT), 'avatar': ((739, 272, 76, 94), '#D9D9D9'), 'club': ((247, 352, 446, 88), WHT),
    }

    def icon(self, name, x, y, w, h, pad=0.12, cell=True, fill=None, stroke=True):
        vb, f = self.ICONS[name]
        if cell:
            self.card(x, y, w, h, fill or f or BG, stroke=stroke)
        p = min(w, h) * pad
        self.crop(vb, x + p, y + p, w - 2 * p, h - 2 * p)

    def tju(self, x, y, w, h):
        cw = w / 4
        for i, (t, c) in enumerate([('T', BLUE), ('J', ORG), ('U', GRN), ('+1', WHT)]):
            self.card(x + i * cw, y, cw, h, c)
            self.ftext(x + i * cw, y, cw, h, t, BLK if c == WHT else WHT, HEAVY, maxsize=h * 0.5)

    def pixtext(self, x, y, txt, h, color=WHT, anchor='start', ret=False):
        """KV 风格粗像素数字（5×7 点阵），y 为顶边"""
        txt = txt.replace('–', '-').replace('—', '-')
        w = pix_width(txt, h)
        if anchor == 'middle':
            x -= w / 2
        elif anchor == 'end':
            x -= w
        s, _ = _pix_rects(x, y, txt, h, color)
        if ret:
            return s
        self.add(s)
        return w

    def sparkle(self, cx, cy, r, fill=YEL):
        k = r * 0.16
        d = f'M{cx} {cy-r}Q{cx+k} {cy-k} {cx+r} {cy}Q{cx+k} {cy+k} {cx} {cy+r}Q{cx-k} {cy+k} {cx-r} {cy}Q{cx-k} {cy-k} {cx} {cy-r}Z'
        self.add(f'<path d="{d}" fill="{fill}"/>')

    # ------------------------------------------------------------- 标志画面
    def hero_field(self, x, y, w, h, seed=3, steps=('01', '02', '03'), angle=62, logos=False, glass_top=0.48,
                   stripe_at=0.0, cell=None, step_run=None, flip=False, logo_w=None):
        """台阶 + 三色斜条 + 彩色玻璃。stripe_at：斜条在底边的起点（占 w 的比例）"""
        u = cell or self.u
        rnd = random.Random(seed)
        cid = self.nid()
        g = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">']
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}"/>')
        xs = np.arange(x, x + w, u)
        ys = np.arange(y, y + h, u)
        g.append(f'<path d="{"".join(f"M{v:.1f} {y}V{y+h}" for v in xs)}{"".join(f"M{x} {v:.1f}H{x+w}" for v in ys)}" stroke="{GRID_B}" stroke-width="{u*0.03}"/>')
        a = math.radians(angle)
        dx, dy = math.cos(a), -math.sin(a)          # 斜条方向（向右上）
        nx, ny = math.sin(a), math.cos(a)           # 法线（指向右下，玻璃一侧）
        sb = u * 0.27                                # 每条宽
        x0, y0 = x + w * stripe_at, y + h           # 黄条外沿经过的点
        L = (w + h) * 3

        def band(o1, o2, col):
            p = [(x0 + nx * o1 - dx * L, y0 + ny * o1 - dy * L), (x0 + nx * o1 + dx * L, y0 + ny * o1 + dy * L),
                 (x0 + nx * o2 + dx * L, y0 + ny * o2 + dy * L), (x0 + nx * o2 - dx * L, y0 + ny * o2 - dy * L)]
            return f'<path d="M{"L".join(f"{a_:.1f} {b_:.1f}" for a_, b_ in p)}Z" fill="{col}"/>'

        # 台阶（KV：每级 1u，编号隔级出现，编号下一级放浅蓝条）
        def sx(yy):  # 黄条外沿在高度 yy 处的 x
            return x0 + dx * ((yy - y0) / dy)
        st = step_run or u
        ytop = y + u * (2.3 if logos else 1.3)
        y_in = y0 + ((x + w - u * 0.5) - x0) * dy / dx      # 斜条在画面右缘内的最高点
        ytop = max(ytop, y_in)
        xtop = sx(ytop) - st * 1.7
        nsteps = 2 * len(steps) + 1
        path = f'M{sx(ytop)+u:.1f} {ytop:.1f}'
        if not steps:
            nsteps = 0
        for i in range(nsteps):
            xi, yi = xtop - i * st, ytop + i * st
            path += f'L{xi:.1f} {yi:.1f}L{xi:.1f} {yi+st:.1f}'
        for k, lab in enumerate(steps):
            i = 2 * k
            xi, yi = xtop - i * st, ytop + i * st
            y1, y2 = yi + st, yi + 2 * st
            if y2 > y + h * glass_top + st * 0.2:
                break
            g.append(f'<path d="M{xi:.1f} {y1+st*0.04:.1f}L{sx(y1):.1f} {y1+st*0.04:.1f}L{sx(y2):.1f} {y2-st*0.04:.1f}L{xi:.1f} {y2-st*0.04:.1f}Z" fill="{LBLUE}"/>')
            g.append(self.pixtext(xi + st * 0.22, yi + st * 0.2, lab, st * 0.6, WHT, ret=True))
        if steps:
            g.append(f'<path d="{path}" fill="none" stroke="{BLK}" stroke-width="{u*0.035}"/>')
        # 玻璃（斜条右下侧，且在 glass_top 以下）
        gy = y + h * glass_top
        gid = self.nid()
        off = sb * 5 + u * 0.05
        # 半平面 n·(p - p0) > off  ∩  y > gy
        far = (w + h) * 3
        hp = [(x0 + nx * off - dx * far, y0 + ny * off - dy * far), (x0 + nx * off + dx * far, y0 + ny * off + dy * far),
              (x0 + nx * far + dx * far, y0 + ny * far + dy * far), (x0 + nx * far - dx * far, y0 + ny * far - dy * far)]
        g.append(f'<clipPath id="{gid}"><path d="M{"L".join(f"{a_:.1f} {b_:.1f}" for a_, b_ in hp)}Z"/></clipPath>')
        g2 = self.nid()
        g.append(f'<clipPath id="{g2}"><rect x="{x-5}" y="{gy}" width="{w+10}" height="{h}"/></clipPath>')
        pts = []
        sp = u * 1.25
        for gx in np.arange(x - sp, x + w + sp, sp):
            for gyy in np.arange(gy - sp, y + h + sp, sp * 0.9):
                pts.append((gx + rnd.uniform(-0.42, 0.42) * sp, gyy + rnd.uniform(-0.42, 0.42) * sp))
        vor = Voronoi(np.array(pts))
        cols = [BLUE] * 30 + [CYAN] * 24 + [YEL] * 22 + ['#00A6FF'] * 12 + [ORG] * 13
        cells = []
        for ri in vor.point_region:
            reg = vor.regions[ri]
            if not reg or -1 in reg:
                continue
            poly = vor.vertices[reg]
            cells.append(f'<path d="M{"L".join(f"{a_:.1f} {b_:.1f}" for a_, b_ in poly)}Z" fill="{rnd.choice(cols)}"/>')
        g.append(f'<g clip-path="url(#{gid})"><g clip-path="url(#{g2})"><rect x="{x}" y="{gy}" width="{w}" height="{h}" fill="{GLASS_LINE}"/>'
                 f'<g stroke="{GLASS_LINE}" stroke-width="{u*0.09}" stroke-linejoin="round">{"".join(cells)}</g>'
                 f'<rect x="{x}" y="{gy}" width="{w}" height="{h}" fill="none" stroke="{GLASS_LINE}" stroke-width="{u*0.12}"/></g></g>')
        # 斜条
        g.append(band(0, sb, YEL) + band(sb * 2, sb * 3, ORG) + band(sb * 4, sb * 5, GRN))
        g.append('</g>')
        self.add(''.join(g))
        if logos:
            lw = logo_w or min(w * 0.82, u * 5.2)
            self.crop(self.ICONS['logos'][0], x + u * 0.35, y + u * 0.3, lw, lw * 50 / 290)

    # ------------------------------------------------------------- 像素风景
    def pixel_hill(self, x, y, w, h, b=None, color=HILL, seed=1, base=0.25, peak=0.95, dissolve=True, holes=True, flip=False):
        """底部出血的像素山：从 y+h 往上长"""
        b = b or self.u * 0.2
        rnd = random.Random(seed)
        n = int(w // b) + 1
        hts, v = [], 0
        for i in range(n):
            t = i / max(n - 1, 1)
            v = 0.7 * v + 0.3 * rnd.uniform(-0.18, 0.18)
            hts.append(min(max(base + (peak - base) * t ** 0.8 + v, 0.06), 1.0))
        hts = list(np.convolve(hts, np.ones(3) / 3, mode='same'))
        if flip: hts = hts[::-1]
        s = []
        for i, hv in enumerate(hts):
            k = int(hv * h / b)
            for j in range(k):
                if holes and j > 1 and rnd.random() < 0.03:
                    continue
                s.append(f'<rect x="{x+i*b:.1f}" y="{y+h-(j+1)*b:.1f}" width="{b*0.86:.1f}" height="{b*0.86:.1f}"/>')
            if dissolve and rnd.random() < 0.35:
                jj = k + rnd.randint(1, 3)
                if jj * b < h:
                    s.append(f'<rect x="{x+i*b:.1f}" y="{y+h-(jj+1)*b:.1f}" width="{b*0.86:.1f}" height="{b*0.86:.1f}"/>')
        cid = self.nid()
        self.add(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})" fill="{color}">{"".join(s)}</g>')

    def snow_peak(self, x, y, w, h, b=None, seed=2, dissolve_w=0.42):
        """顶部出血的蓝色块 + 白色阶梯雪山，右侧散成像素点（KV 左上角）"""
        b = b or self.u * 0.14
        rnd = random.Random(seed)
        solid_w = round(w * (1 - dissolve_w) / b) * b
        s = [f'<rect x="{x}" y="{y}" width="{solid_w}" height="{h}" fill="{BLUE}"/>']
        cols, rows = int(w * dissolve_w // b), int(h // b)
        for c in range(cols):
            p = (1 - c / cols)
            for r in range(rows):
                q = p ** 1.4 * (0.75 if r < rows * 0.75 else 0.45)
                if rnd.random() < q * (0.9 if c < 2 else 0.55):
                    s.append(f'<rect x="{x+solid_w+c*b:.1f}" y="{y+r*b:.1f}" width="{b*0.92:.1f}" height="{b*0.92:.1f}" fill="{BLUE}"/>')
        n = int(solid_w // b)
        hs = []
        for i in range(n):
            t = i / n
            hv = (0.18 + 0.62 * (t / 0.42)) if t < 0.42 else (0.80 - 0.75 * ((t - 0.42) / 0.58) ** 0.8)
            hs.append(max(0.0, hv))
        d = f'M{x} {y+h}'
        for i, hv in enumerate(hs):
            hh = round(hv * h / b) * b
            d += f'L{x+i*b:.1f} {y+h-hh:.1f}L{x+(i+1)*b:.1f} {y+h-hh:.1f}'
        d += f'L{x+solid_w} {y+h}Z'
        s.append(f'<path d="{d}" fill="{WHT}"/>')
        cid = self.nid()
        self.add(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})">{"".join(s)}</g>')

    def contrib_mountain(self, x, y, w, h, b, seed=3, start=0.12, end=0.92, hi=None):
        """贡献山：GitHub 贡献图的方块，从左到右越来越高、越来越绿（从第一个算子到第一份贡献）"""
        rnd = random.Random(seed)
        shades = ['#CFEFD6', '#9BE0A8', '#5DCB72', '#26BB45', '#0C9A2F']
        n = int(w // b)
        out = []
        v = 0
        tops = []
        for i in range(n):
            t = i / max(n - 1, 1)
            v = 0.65 * v + 0.35 * rnd.uniform(-0.12, 0.12)
            hh = max(1, int((start + (end - start) * t ** 1.15 + v) * h / b))
            tops.append(hh)
            for j in range(hh):
                depth = j / max(hh, 1)
                lvl = min(4, max(0, int(t * 3.2 + (1 - depth) * 0.8 + rnd.uniform(-0.9, 0.9))))
                if j == hh - 1 and rnd.random() < 0.25:
                    continue
                out.append(f'<rect x="{x+i*b+b*0.07:.1f}" y="{y+h-(j+1)*b+b*0.07:.1f}" width="{b*0.86:.1f}" height="{b*0.86:.1f}" rx="{b*0.08:.1f}" fill="{shades[lvl]}"/>')
            if rnd.random() < 0.18 and t > 0.25:
                jj = hh + rnd.randint(1, 3)
                out.append(f'<rect x="{x+i*b+b*0.07:.1f}" y="{y+h-(jj+1)*b+b*0.07:.1f}" width="{b*0.86:.1f}" height="{b*0.86:.1f}" rx="{b*0.08:.1f}" fill="{shades[rnd.randint(1,3)]}"/>')
        self.add(''.join(out))
        return tops

    def pixel_arrow(self, x, y, cell, direction='right', color=WHT):
        pat = ["....#........", "...##........", "..###........", ".############", "#############",
               ".############", "..###........", "...##........", "....#........"]
        if direction == 'right':
            pat = [r[::-1] for r in pat]
        self.add(''.join(f'<rect x="{x+i*cell:.1f}" y="{y+j*cell:.1f}" width="{cell*0.88:.1f}" height="{cell*0.88:.1f}" fill="{color}"/>'
                         for j, r in enumerate(pat) for i, c in enumerate(r) if c == '#'))

    # ------------------------------------------------------------- 组合件
    def title_lockup(self, x, y, w, tag='天津大学', notch=None, h=None, pad=None, sub=False, center=False):
        """标签 + CANN + 开发者俱乐部，按宽度自适应，返回高度"""
        u = self.u
        pad = pad if pad is not None else u * 0.5
        iw = w - 2 * pad
        tag_h = u * 0.95
        if h:
            iw = min(iw, (h - 2 * pad - tag_h - u * 0.65) / (124 / 426 + 88 / 446))
        cann_h = iw * 124 / 426
        club_h = iw * 88 / 446
        cx0 = x + pad + ((w - 2 * pad - iw) / 2 if center else 0)
        hh = h or (pad + tag_h + u * 0.4 + cann_h + u * 0.25 + club_h + pad)
        self.card(x, y, w, hh, WHT, notch=notch)
        tw = measure(tag, tag_h * 0.62) + tag_h * 0.9
        self.card(cx0, y + pad, tw, tag_h, BLK, stroke=False)
        self.text(cx0 + tw / 2, y + pad + tag_h / 2 + tag_h * 0.03, tag, tag_h * 0.62, WHT, anchor='middle')
        top = y + pad + tag_h + u * 0.4
        extra = (hh - (pad + tag_h + u * 0.4 + cann_h + u * 0.25 + club_h + pad))
        top += extra * 0.5
        self.crop(self.ICONS['cann'][0], cx0, top, iw, cann_h)
        self.crop(self.ICONS['club'][0], cx0, top + cann_h + u * 0.25, iw, club_h)
        return hh

    def strip(self, x, y, w, h, txt, fill=WHT, color=BLK, size=None, anchor='middle', pad=None, font=HEAVY):
        self.card(x, y, w, h, fill)
        pad = self.u * 0.45 if pad is None else pad
        if size:
            tx = {'start': x + pad, 'middle': x + w / 2, 'end': x + w - pad}[anchor]
            self.text(tx, y + h / 2 + size * 0.04, txt, size, color, font, anchor)
        else:
            self.ftext(x, y, w, h, txt, color, font, anchor, maxsize=h * 0.5, pad=pad)

    def agenda_stairs(self, x, y, w, rowh, items, step=None, gap=None):
        """议程做成台阶：每行一张卡，逐行向右错开一级，呼应 KV 的 01/02/03 台阶"""
        u = self.u
        step = step if step is not None else u * 0.35
        gap = gap if gap is not None else rowh * 0.18
        n = len(items)
        cw = w - step * (n - 1)
        for i, (num, t, name) in enumerate(items):
            cx, cy = x + i * step, y + i * (rowh + gap)
            nb = rowh
            self.card(cx, cy, nb, rowh, BLUE)
            ph = rowh * 0.4
            self.pixtext(cx + nb / 2, cy + (rowh - ph) / 2, num, ph, WHT, 'middle')
            tw = rowh * 2.2
            self.card(cx + nb, cy, tw, rowh, BLK)
            ph2 = rowh * 0.32
            self.pixtext(cx + nb + tw / 2, cy + (rowh - ph2) / 2, t, ph2, '#3BD83B', 'middle')
            self.card(cx + nb + tw, cy, cw - nb - tw, rowh, WHT)
            self.ftext(cx + nb + tw, cy, cw - nb - tw, rowh, name, BLK, HEAVY, 'start', maxsize=rowh * 0.4, pad=rowh * 0.35)
        return n * (rowh + gap) - gap

    def qr(self, x, y, s, label='扫码报名'):
        self.card(x, y, s, s, WHT)
        p = s * 0.1
        # 像素化占位：三个定位角
        b = (s - 2 * p) / 21
        r = []
        for (ox, oy) in [(0, 0), (14, 0), (0, 14)]:
            r.append(f'<rect x="{x+p+ox*b}" y="{y+p+oy*b}" width="{7*b}" height="{7*b}" fill="{BLK}"/><rect x="{x+p+(ox+1)*b}" y="{y+p+(oy+1)*b}" width="{5*b}" height="{5*b}" fill="{WHT}"/><rect x="{x+p+(ox+2)*b}" y="{y+p+(oy+2)*b}" width="{3*b}" height="{3*b}" fill="{BLK}"/>')
        self.add(''.join(r))
        self.text(x + s / 2, y + s * 0.62, '二维码', s * 0.11, '#9a9a9a', HEAVY, 'middle')
        self.text(x + s / 2, y + s * 0.76, '待替换', s * 0.09, '#9a9a9a', HEAVY, 'middle')

    def bubble(self, x, y, w, h, tail='bl', fill=WHT, inner=None):
        """像素对话框：直角 + 阶梯尾巴，黑描边"""
        u = self.u
        b = h * 0.12
        t = {'bl': (x + w * 0.18, y + h, -1), 'br': (x + w * 0.82, y + h, 1)}[tail]
        tx, ty, sd = t
        pts = [(x, y), (x + w, y), (x + w, y + h)]
        if tail == 'br':
            pts += [(tx + b, y + h), (tx + b, y + h + b), (tx, y + h + b), (tx, y + h + 2 * b), (tx - b, y + h + 2 * b), (tx - b, y + h + 3 * b), (tx - 2 * b, y + h + 3 * b), (tx - 2 * b, y + h)]
        else:
            pts += [(tx + 2 * b, y + h), (tx + 2 * b, y + h + 3 * b), (tx + b, y + h + 3 * b), (tx + b, y + h + 2 * b), (tx, y + h + 2 * b), (tx, y + h + b), (tx - b, y + h + b), (tx - b, y + h)]
        pts += [(x, y + h)]
        d = 'M' + 'L'.join(f'{a:.1f} {c:.1f}' for a, c in pts) + 'Z'
        sh = h * 0.07
        self.add(f'<path d="{d}" transform="translate({sh} {sh})" fill="{BLK}"/>')
        self.add(f'<path d="{d}" fill="{fill}" stroke="{BLK}" stroke-width="{max(self.sw, h*0.035)}"/>')

    def brackets(self, x, y, w, h, L, t, color=WHT):
        d = (f'M{x} {y+L}V{y}H{x+L}M{x+w-L} {y}H{x+w}V{y+L}M{x+w} {y+h-L}V{y+h}H{x+w-L}M{x+L} {y+h}H{x}V{y+h-L}')
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{t}" stroke-linecap="square"/>')

    def agenda_bal(self, x, y, w, rowh, items, hi=2, gap=None):
        """平衡版议程：行宽一致、左右对齐；右端 6 格进度条逐行加一格（台阶语义）；成立仪式一行高亮"""
        gap = rowh * 0.14 if gap is None else gap
        n = len(items)
        for i, (num, t, name) in enumerate(items):
            cy = y + i * (rowh + gap)
            hl = (i == hi)
            nb = rowh
            self.card(x, cy, nb, rowh, YEL if hl else BLUE)
            ph = rowh * 0.4
            self.pixtext(x + nb / 2, cy + (rowh - ph) / 2, num, ph, BLK if hl else WHT, 'middle')
            tw = rowh * 2.25
            self.card(x + nb, cy, tw, rowh, BLK)
            ph2 = rowh * 0.3
            self.pixtext(x + nb + tw / 2, cy + (rowh - ph2) / 2, t, ph2, '#3BD83B', 'middle')
            pw = rowh * 2.0
            mw = w - nb - tw - pw
            self.card(x + nb + tw, cy, mw, rowh, YEL if hl else WHT)
            self.ftext(x + nb + tw, cy, mw, rowh, name, BLK, HEAVY, 'start', maxsize=rowh * (0.42 if hl else 0.38), pad=rowh * 0.32)
            self.card(x + w - pw, cy, pw, rowh, WHT)
            cs = pw / (n + 1.5)
            for k in range(n):
                fill = (YEL if hl else BLUE) if k <= i else '#DADADA'
                if k == n - 1 and k <= i:
                    fill = GRN
                self.add(f'<rect x="{x+w-pw+cs*0.75+k*cs:.1f}" y="{cy+rowh/2-cs*0.45 - (k*cs*0.0):.1f}" width="{cs*0.8:.1f}" height="{cs*0.9:.1f}" fill="{fill}"/>')
        return n * (rowh + gap) - gap

    def html(self):
        return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
                f'@font-face{{font-family:FusionPixel;src:url("fonts/fusion-pixel-12px-proportional-zh_hans.ttf")}}'
                f'html,body{{margin:0;padding:0;background:#fff}}svg text{{font-kerning:none}}</style></head><body>'
                f'<svg id="c" xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}" style="display:block">'
                f'{"".join(self.parts)}</svg>'
                f'<script>const s=new URLSearchParams(location.search).get("s");if(s){{const c=document.getElementById("c");c.setAttribute("width",{self.W}*s);c.setAttribute("height",{self.H}*s);}}</script></body></html>')
