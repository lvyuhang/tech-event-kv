"""v5：按活动方案更新真实信息。所有活动信息集中在 EVENT，换学校只改这里（以及学校槽位的图形模块）。"""
from lib import *
import formats as F

EVENT = {
    'school': '天津大学',
    'title': '天津大学 CANN 开发者俱乐部成立仪式暨校园宣讲会',
    'sub': '成立仪式暨校园宣讲会',
    'slogan': '从第一个算子，到第一份贡献',
    'date': '11月08日',
    'date_dot': '2026.11.08',
    'weekday': '周日',
    'time': '10:30–12:10',
    'campus': '天津大学北洋园校区',
    'venue': '1895大楼A102报告厅',
    'venue_short': 'A102 报告厅',
    'building': '1895大楼',
    'audience': '计算机、软件、人工智能、电子信息、自动化、数学等专业同学',
    'audience_note': '对 AI 计算、C/C++、开源开发感兴趣均可参加，不要求 CANN 经验',
}

# (时间, 环节, 嘉宾姓名, 嘉宾职务, 主要内容, 类型)  类型：hi 高亮 / minor 弱化 / None
# 嘉宾姓名与职务按活动方案原文，印刷前需双方核实；校方致辞领导三选一未定
AGENDA = [
    ('10:30–10:35', '主持开场', '张加万', '软件学院党委书记、院长', '介绍活动背景、到场嘉宾及校园俱乐部共建愿景', None),
    ('10:35–10:45', '校方领导致辞', '待定', '天津大学校领导', '', None),
    ('10:45–10:55', '企业方领导致辞', '赵志鹏', '华为北京研究所所长', '', None),
    ('10:55–11:15', 'CANN 开源社区介绍与共建展望', '陈敏', 'CANN 开源社区 PMC 主席', '从 CANN 学习入门，逐步参与算子开发、开源贡献及技术赛事', None),
    ('11:15–11:25', '校园俱乐部成立暨授牌仪式', '', '校、企、高校研究所三方领导 · 指导教师 · 学生代表', '三方共同揭牌、企业领导授牌、全体代表合影', 'hi'),
    ('11:25–11:30', '中场休息', '', '', '', 'minor'),
    ('11:30–12:00', 'CANN 技术报告', '张雨晨', 'CANN 技术专家', '技术、开发环境、算子开发、开源贡献', None),
    ('12:00–12:10', '学生互动问答', '', '', '', None),
]

GUESTS = [('张加万', '软件学院党委书记、院长'), ('待定', '天津大学校领导'), ('赵志鹏', '华为北京研究所所长'),
          ('陈敏', 'CANN 开源社区 PMC 主席'), ('张雨晨', 'CANN 技术专家')]


def agenda_full(d, x, y, w, items, rowh=96, minor_h=50, gap=8, detail=True, guest_w=None, time_w=None, size=None):
    """8 环节议程：时间（黑底绿色像素字）| 环节（+ 内容小字）| 嘉宾（姓名 + 职务）。授牌仪式整行黄色高亮，中场休息弱化成细条。"""
    size = size or rowh * 0.3
    time_w = time_w or rowh * 2.15
    guest_w = guest_w if guest_w is not None else w * 0.33
    yy = y
    for (t, name, g, gt, desc, kind) in items:
        if kind == 'minor':
            h = minor_h
            d.card(x, yy, w, h, '#DADADA')
            d.pixtext(x + time_w / 2, yy + (h - h * 0.34) / 2, t, h * 0.34, '#555', 'middle')
            d.text(x + time_w + size * 0.9, yy + h / 2 + 2, name, size * 0.8, '#555')
            yy += h + gap
            continue
        h = rowh
        hl = kind == 'hi'
        d.card(x, yy, time_w, h, YEL if hl else BLK)
        ph = min(h * 0.2, (time_w * 0.84) / (pix_width(t.replace('–', '-'), 1)))
        d.pixtext(x + time_w / 2, yy + (h - ph) / 2, t, ph, BLK if hl else '#3BD83B', 'middle')
        span = (not g and not gt)
        mw = w - time_w - (0 if span else guest_w)
        d.card(x + time_w, yy, mw, h, YEL if hl else WHT)
        pad = size * 0.8
        tsize = min(size * (1.08 if hl else 1), (mw - 2 * pad) / max(measure(name, 1), 1))
        if detail and desc:
            d.text(x + time_w + pad, yy + h * 0.36, name, tsize, BLK)
            dsz = min(size * 0.62, (mw - 2 * pad) / max(measure(desc, 1), 1))
            d.text(x + time_w + pad, yy + h * 0.72, desc, dsz, '#555' if not hl else BLK, HEAVY)
        else:
            d.text(x + time_w + pad, yy + h / 2 + 2, name, tsize, BLK)
        if guest_w > 0 and not span:
            gx = x + w - guest_w
            d.card(gx, yy, guest_w, h, YEL if hl else WHT)
            if g:
                d.text(gx + pad, yy + h * 0.36, g, size * 1.0, BLUE if g != '待定' else '#999')
                gsz = min(size * 0.6, (guest_w - 2 * pad) / max(measure(gt, 1), 1))
                d.text(gx + pad, yy + h * 0.72, gt, gsz, '#555', HEAVY)
            elif gt:
                gsz = min(size * 0.62, (guest_w - 2 * pad) / max(measure(gt, 1), 1))
                # 多方嘉宾：拆两行
                parts = gt.split(' · ')
                if len(parts) > 1:
                    l1, l2 = parts[0], ' · '.join(parts[1:])
                    gsz = min(size * 0.62, (guest_w - 2 * pad) / max(measure(l1, 1), measure(l2, 1)))
                    d.text(gx + pad, yy + h * 0.36, l1, gsz, BLK, HEAVY)
                    d.text(gx + pad, yy + h * 0.68, l2, gsz, BLK, HEAVY)
                else:
                    d.text(gx + pad, yy + h / 2, gt, gsz, BLK, HEAVY)
            if hl:
                d.sparkle(gx + guest_w - size * 0.9, yy + size * 0.8, size * 0.45, BLK)
        yy += h + gap
    return yy - gap - y


def info_rows(d, x, y, w, h, rows, label_w=None):
    label_w = label_w or h * 1.7
    cols = [BLUE, ORG, GRN, BLK]
    for i, (k, v) in enumerate(rows):
        yy = y + i * h
        d.card(x, yy, label_w, h, cols[i % 4])
        d.text(x + label_w / 2, yy + h / 2, k, h * 0.38, WHT, PIXEL, 'middle')
        d.card(x + label_w, yy, w - label_w, h, WHT)
        sz = min(h * 0.36, (w - label_w - h * 0.6) / max(measure(v, 1), 1))
        d.text(x + label_w + h * 0.3, yy + h / 2 + 2, v, sz, BLK)
    return len(rows) * h


E = EVENT


# =============================================================== A4 日程单页
def a4():
    """手持 40cm：议程是主角，8 环节带嘉宾与内容；授牌仪式高亮"""
    W, H = 1240, 1754
    d = Doc(W, H, 80)
    d.grid_bg()
    d.snow_peak(0, 0, 560, 100, b=14, seed=14)
    d.icon('plus', 560, 0, 106, 100, pad=0.2)
    d.icon('times', 666, 0, 106, 100, pad=0.2)
    d.icon('sigma', 772, 0, 108, 100, pad=0.2)
    d.hero_field(880, 0, 360, 560, logos=True, seed=61, glass_top=0.64, cell=46, logo_w=300, steps=('01', '02'))
    d.title_lockup(0, 100, 880, h=380, pad=34)
    d.icon('member', 450, 200, 400, 212, cell=False, pad=0)
    d.strip(0, 480, 880, 80, E['sub'], WHT, size=46)
    d.strip(0, 560, W, 84, E['slogan'], YEL, size=42)
    info_rows(d, 0, 644, W, 76, [('时间', f"{E['date_dot']}（{E['weekday']}）{E['time']}"), ('地点', E['campus'] + E['venue'])], label_w=150)
    y = 830
    F.section_tag(d, 0, y, 72, '活动议程')
    d.sparkle(1185, y + 36, 30)
    d.sparkle(1135, y + 20, 14)
    hgt = agenda_full(d, 0, y + 88, W, AGENDA, rowh=96, minor_h=46, gap=8, detail=True, guest_w=360, time_w=200, size=29)
    yb = y + 88 + hgt
    d.pixel_hill(0, yb + 6, W, H - yb - 6, b=18, seed=15, base=0.4, peak=0.9, holes=False)
    return d


# =============================================================== 易拉宝
def rollup():
    """入口易拉宝 80×200（1px=1mm）。上部按 KV 便当格：雪山 + logo 条、左侧模块列、带缺口的标题卡；
    二维码离地 1.1–1.3m；底部 KV 式像素山 + 小模块 + 右侧标志画面窄条（底座遮挡区只放装饰）"""
    W, H = 800, 2000
    d = Doc(W, H, 80)
    d.grid_bg()
    # 顶部带
    d.snow_peak(0, 0, 440, 120, b=14, seed=16)
    d.icon('logos', 440, 0, 360, 120, pad=0.14)
    # 左模块列
    d.icon('npu', 0, 120, 230, 250, pad=0.14)
    d.card(0, 370, 230, 90, BLK)
    d.crop(d.ICONS['hello'][0], 12, 386, 206, 58)
    d.tju(0, 460, 230, 80)
    # 标题卡（右上缺口放运算符）
    d.title_lockup(230, 120, 570, h=420, pad=30, notch=('tr', 170, 96))
    d.icon('plus', 630, 120, 85, 96, pad=0.18)
    d.icon('sigma', 715, 120, 85, 96, pad=0.18)
    d.strip(0, 540, W, 76, E['sub'], WHT, size=44)
    d.strip(0, 616, W, 76, E['slogan'], YEL, size=40)
    # 信息行（二维码离地约 1.1–1.3m）
    d.card(0, 692, 400, 200, BLK)
    d.text(30, 738, f"{E['date']} {E['weekday']}", 40, WHT)
    d.pixtext(30, 772, E['time'], 30, '#3BD83B')
    d.text(30, 846, E['venue'], 30, WHT)
    d.icon('member', 400, 692, 200, 200, pad=0.06, fill=WHT)
    d.card(600, 692, 200, 200, WHT)
    d.qr(625, 702, 150)
    d.text(700, 870, '扫码报名', 22, BLK, PIXEL, 'middle')
    # 议程
    y = 930
    F.section_tag(d, 0, y, 64, '活动议程')
    d.sparkle(762, y + 32, 26)
    d.sparkle(718, y + 18, 12)
    hgt = agenda_full(d, 0, y + 78, W, AGENDA, rowh=74, minor_h=38, gap=6, detail=False, guest_w=250, time_w=170, size=24)
    yb = y + 78 + hgt + 30
    # 底部：KV 式
    d.icon('mug', 0, yb, 170, 160, pad=0.12)
    d.icon('flower', 170, yb, 170, 160, pad=0.1)
    d.card(340, yb, 200, 160, WHT)
    d.sparkle(420, yb + 85, 46)
    d.sparkle(490, yb + 50, 20)
    d.sparkle(495, yb + 115, 14)
    d.hero_field(540, yb, 260, H - yb, logos=False, seed=81, glass_top=0.35, cell=44, steps=('01',), stripe_at=-0.15)
    d.pixel_hill(0, yb + 160, 540, H - yb - 160, b=27, seed=17, base=0.35, peak=0.9)
    return d


# =============================================================== 海报长图
def long_poster():
    W = 1080
    u = 90
    H = 4300
    d = Doc(W, H, u)
    d.grid_bg()
    d.snow_peak(0, 0, 620, 170, seed=5)
    d.icon('plus', 630, 0, 150, 170, pad=0.2)
    d.icon('times', 780, 0, 150, 170, pad=0.2)
    d.icon('sigma', 930, 0, 150, 170, pad=0.2)
    d.hero_field(720, 170, 360, 1110, logos=True, seed=21, glass_top=0.7, cell=62, logo_w=300)
    hh = d.title_lockup(0, 170, 720)
    y = 170 + hh
    d.strip(0, y, 720, 120, E['sub'], WHT, size=58)
    d.strip(0, y + 120, 720, 120, E['slogan'], YEL, size=46)
    y2 = y + 240
    d.card(0, y2, 440, 1280 - y2, BLK)
    d.text(40, y2 + (1280 - y2) * 0.3, E['date'], 54, WHT)
    d.pixtext(40, y2 + (1280 - y2) * 0.5, E['time'], 34, '#3BD83B')
    d.text(40, y2 + (1280 - y2) * 0.8, E['venue_short'], 40, WHT)
    d.icon('npu', 440, y2, 280, 1280 - y2, pad=0.16)
    d.card(0, 1340, W, 110, BLK)
    d.text(40, 1395, '不要求 CANN 经验', 40, '#3BD83B', PIXEL)
    d.text(1040, 1397, '扫描文末二维码报名  ↓', 42, WHT, HEAVY, 'end')
    # 活动信息
    y = 1530
    F.section_tag(d, 0, y, 96, '活动信息')
    d.sparkle(1020, y + 48, 40)
    d.sparkle(958, y + 30, 20)
    y += 96
    info_rows(d, 0, y, W, 110, [('时间', f"2026年{E['date']}（{E['weekday']}）{E['time']}"), ('地点', E['campus'] + ' ' + E['venue']),
                                ('对象', '计算机 · 软件 · AI · 电子信息 · 自动化 · 数学')], label_w=200)
    d.ftext(200, y + 330, 880, 70, E['audience_note'], '#555', HEAVY, 'start', maxsize=30, pad=24)
    # 议程
    y = 2190
    F.section_tag(d, 0, y, 96, '活动议程')
    d.icon('matrix', 680, y, 400, 96, cell=False, pad=0.05)
    hgt = agenda_full(d, 0, y + 130, W, AGENDA, rowh=128, minor_h=60, gap=10, detail=True, guest_w=330, time_w=230, size=34)
    # 报名
    y = y + 130 + hgt + 90
    F.section_tag(d, 0, y, 96, '扫码报名')
    y += 130
    d.icon('member', 0, y, 620, 330, cell=False, pad=0.0)
    d.card(660, y - 20, 420, 420, WHT)
    d.qr(705, y + 10, 330)
    d.text(870, y + 370, '加入 CANN 开发者俱乐部', 28, BLK, HEAVY, 'middle')
    yb = y + 460
    d.H = yb + 300
    d.pixel_hill(0, yb, 820, 300, b=30, seed=12, base=0.3, peak=0.95)
    F.green_grid(d, 820, yb, 260, 300, 65)
    return d


# =============================================================== 16:9 KV：只替换日期块
def kv_16x9():
    d = Doc(1408, 784, 57.5)
    d.add('<image href="kv.svg" width="1408" height="784"/>')
    # 原 KV 日期格 (702,537,156,93)，盖一块新的
    x, y, w, h = 703, 538, 155, 91
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLK}"/>')
    d.text(x + 14, y + 24, E['date'] + ' ' + E['time'][:5], 17, WHT)
    d.text(x + 14, y + 50, E['building'], 17, WHT)
    d.text(x + 14, y + 74, 'A102 报告厅', 17, WHT)
    return d


# =============================================================== B 背板：补时间地点
def backdrop_b():
    d = F.power_check_wide()
    # 左栏底部黑条（原 hello, CANN_）换成时间地点
    d.card(0, 650, 620, 110, BLK)
    d.text(30, 688, f"{E['date']} {E['time']}", 40, WHT)
    d.text(30, 736, E['campus'] + ' ' + E['venue'], 26, '#3BD83B', HEAVY)
    return d


# =============================================================== 指引牌
def guide(direction):
    W, H = 600, 900
    d = Doc(W, H, 60)
    d.grid_bg()
    d.icon('logos', 0, 0, W, 84, pad=0.14)
    d.card(0, 84, W, 440, YEL)
    d.text(W / 2, 140, E['building'], 44, BLK, PIXEL, 'middle')
    d.text(W / 2, 228, E['venue_short'], min(96, fit(E['venue_short'], 540)), BLK, anchor='middle')
    cell = 26
    d.pixel_arrow(W / 2 - 13 * cell / 2, 290, cell, direction, BLK)
    lockup_h = F.lockup_h
    lockup_h(d, 0, 524, W, 180, tag=None, pad=28)
    d.strip(0, 704, W, 66, E['sub'], BLK, WHT, size=36)
    d.hero_field(0, 770, W, 130, logos=False, seed=71 if direction == 'left' else 72, glass_top=0.0, cell=34, steps=(), stripe_at=0.3)
    return d


# =============================================================== 横幅（两行）
def banner():
    """6m×60cm 舞台横幅（3000×300，1px=2mm）。网格 150：两侧各 3 格宽、左右镜像对称。
    左：标志画面(2×2) + NPU / 咖啡杯；右：Σ / 海棠 + 镜像标志画面(2×2)。中间标题卡 2100 宽。"""
    W, H = 3000, 300
    d = Doc(W, H, 50)
    d.grid_bg(step=50, lw=2)
    # 左
    d.hero_field(0, 0, 300, H, logos=False, seed=111, glass_top=0.48, cell=30, steps=('01',), stripe_at=0.05)
    d.icon('npu', 300, 0, 150, 150, pad=0.1)
    d.icon('mug', 300, 150, 150, 150, pad=0.12)
    # 右（镜像）
    d.icon('sigma', 2550, 0, 150, 150, pad=0.2)
    d.icon('flower', 2550, 150, 150, 150, pad=0.1)
    n0 = len(d.parts)
    d.hero_field(0, 0, 300, H, logos=False, seed=111, glass_top=0.48, cell=30, steps=(), stripe_at=0.05)
    mirrored = ''.join(d.parts[n0:])
    del d.parts[n0:]
    d.add(f'<g transform="translate({W} 0) scale(-1 1)">{mirrored}</g>')
    # 中：标题卡
    x0, x1 = 450, 2550
    d.card(x0, 0, x1 - x0, 150, WHT)
    pad = 50
    txt = '开发者俱乐部成立仪式暨校园宣讲会'
    tag = E['school']
    k = measure(tag, 1) + 0.6 + 1.15 * 426 / 124 + measure(txt, 1) + 0.7
    sz = min(86, (x1 - x0 - 2 * pad) / k)
    x = x0 + pad + ((x1 - x0 - 2 * pad) - k * sz) / 2
    tw = measure(tag, sz) + 0.6 * sz
    d.card(x, 75 - sz * 0.56, tw, sz * 1.12, BLK, stroke=False)
    d.text(x + tw / 2, 77, tag, sz, WHT, anchor='middle')
    x += tw + 0.35 * sz
    ch = 1.15 * sz
    d.crop(d.ICONS['cann'][0], x, 75 - ch / 2, ch * 426 / 124, ch)
    x += ch * 426 / 124 + 0.35 * sz
    d.text(x, 78, txt, sz, BLK)
    d.card(x0, 150, x1 - x0, 150, YEL)
    d.text((x0 + x1) / 2, 228, E['slogan'], 72, BLK, anchor='middle', ls=0.18)
    return d


# =============================================================== 桌卡（5 位嘉宾）
def table_card(name, title):
    W, H = 900, 1300
    hh = H // 2
    d = Doc(W, H, 60)

    def face(seed):
        f = Doc(W, hh, 60)
        f._id = seed * 1000
        f.card(0, 0, W, hh, WHT, stroke=False)
        f.icon('logos', 0, 0, W, 100, pad=0.16, stroke=False)
        size = min(220, 720 / max(len(name), 2))
        f.text(W / 2, 270, name, size, BLK if name != '待定' else '#999', anchor='middle', ls=0.08)
        ts = min(40, 760 / max(measure(title, 1), 1))
        f.text(W / 2, 445, title, ts, '#555', HEAVY, 'middle')
        f.hero_field(0, 520, W, 130, logos=False, seed=seed, glass_top=0.0, cell=34, steps=(), stripe_at=0.35)
        return ''.join(f.parts)

    d.add(f'<g transform="rotate(180 {W/2} {hh/2})">{face(101)}</g>')
    d.add(f'<g transform="translate(0 {hh})">{face(102)}</g>')
    d.add(f'<path d="M0 {hh}H{W}" stroke="#888" stroke-width="3" stroke-dasharray="12 10"/>')
    return d


FORMATS = {
    '01a_KV_16x9': (kv_16x9, None),
    '01b_海报长图_1080w': (long_poster, None),
    '02_合影背板_B_5x2m': (backdrop_b, (5000, 2000)),
    '03_日程单页_A4': (a4, (210, 297)),
    '04a_指引牌_左_60x90cm': (lambda: guide('left'), (600, 900)),
    '04b_指引牌_右_60x90cm': (lambda: guide('right'), (600, 900)),
    '05_易拉宝_80x200cm': (rollup, (800, 2000)),
    '09_横幅_6mx60cm': (banner, (6000, 600)),
}
for i, (n, t) in enumerate(GUESTS):
    FORMATS[f'08_{i+1}_桌卡_{n}'] = ((lambda n=n, t=t: table_card(n, t)), (90, 130))


# =============================================================== 邀请函（含议程）
INVITE_TEXT = ('诚挚邀请您莅临天津大学 CANN 开发者俱乐部成立仪式暨校园宣讲会，'
               '与校企嘉宾和同学们一起，见证俱乐部正式成立，开启从第一个算子到第一份贡献的旅程。')


def wrap(txt, size, width, font=HEAVY):
    lines, cur = [], ''
    for ch in txt:
        if measure(cur + ch, size, font) > width:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    # 避免行首标点
    for i in range(1, len(lines)):
        if lines[i] and lines[i][0] in '，。、；：！？':
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
    return lines


def invitation():
    W = 1080
    H = 2400
    d = Doc(W, H, 90)
    d.grid_bg()
    d.snow_peak(0, 0, 620, 150, seed=5)
    d.icon('plus', 630, 0, 150, 150, pad=0.2)
    d.icon('times', 780, 0, 150, 150, pad=0.2)
    d.icon('sigma', 930, 0, 150, 150, pad=0.2)
    hh = d.title_lockup(0, 150, 720)
    y = 150 + hh
    d.strip(0, y, 720, 110, E['sub'], WHT, size=54)
    y += 110
    # 邀请函标签
    d.card(0, y, 720, 210, BLK)
    d.text(40, y + 88, '邀请函', 92, WHT)
    d.text(40, y + 168, 'INVITATION', 36, '#3BD83B', PIXEL)
    y += 210
    d.hero_field(720, 150, 360, y - 150, logos=True, seed=27, glass_top=0.62, cell=58, logo_w=300, steps=('01', '02'))
    # 正文
    y += 70
    d.card(0, y, W, 520, WHT)
    d.text(60, y + 80, '尊敬的', 44, BLK)
    d.add(f'<path d="M210 {y+105}H620" stroke="{BLK}" stroke-width="3"/>')
    d.text(632, y + 80, '：', 44, BLK)
    ls = wrap(INVITE_TEXT, 38, W - 160)
    for i, l in enumerate(ls):
        d.text(80 if i else 140, y + 175 + i * 66, l, 38, '#222', HEAVY)
    d.strip(0, y + 520 - 96, W, 96, E['slogan'], YEL, size=44)
    # 时间地点
    y += 560
    info_rows(d, 0, y, W, 100, [('时间', f"2026年{E['date']}（{E['weekday']}）{E['time']}"), ('地点', E['campus'] + ' ' + E['venue'])], label_w=180)
    # 议程
    y += 250
    F.section_tag(d, 0, y, 84, '活动议程')
    d.sparkle(1020, y + 42, 36)
    d.sparkle(965, y + 24, 16)
    hgt = agenda_full(d, 0, y + 104, W, AGENDA, rowh=88, minor_h=44, gap=8, detail=False, guest_w=360, time_w=210, size=30)
    yb = y + 104 + hgt + 40
    d.card(0, yb, W, 110, BLK)
    d.text(W / 2, yb + 55, '敬请莅临', 56, WHT, anchor='middle', ls=0.3)
    yb += 110
    d.H = int(round(yb + 220))
    d.pixel_hill(0, yb, 820, 220, b=28, seed=12, base=0.35, peak=0.95)
    F.green_grid(d, 820, yb, 260, 220, 55)
    return d


FORMATS['01f_邀请函_含议程_1080w'] = (invitation, None)


# =============================================================== 线上补充尺寸
def live_cover():
    """视频号直播封面 1080×1440（3:4）：信息流小图，标题 + 日期 + 直播标签"""
    W, H = 1080, 1440
    d = Doc(W, H, 90)
    d.grid_bg()
    d.snow_peak(0, 0, 620, 160, seed=5)
    d.icon('logos', 620, 0, 460, 160, pad=0.16)
    d.hero_field(720, 160, 360, 1000, logos=False, seed=41, glass_top=0.55, cell=62, steps=('01', '02'))
    hh = d.title_lockup(0, 160, 720, tag='直播中')
    y = 160 + hh
    d.strip(0, y, 720, 120, E['sub'], WHT, size=56)
    d.strip(0, y + 120, 720, 120, E['slogan'], YEL, size=44)
    y2 = y + 240
    d.card(0, y2, 720, 1160 - y2, BLK)
    hb = 1160 - y2
    d.text(48, y2 + hb * 0.24, f"{E['date']} {E['weekday']}", min(56, hb * 0.26), WHT)
    d.pixtext(48, y2 + hb * 0.43, E['time'], min(34, hb * 0.16), '#3BD83B')
    d.text(48, y2 + hb * 0.8, '天津大学 · ' + E['venue_short'], min(38, hb * 0.18), WHT)
    d.pixel_hill(0, 1160, 1080, 280, b=34, seed=12, base=0.35, peak=0.95)
    return d


def csdn_ad():
    """CSDN 首页视窗广告 640×760：日期、地点、报名按钮"""
    W, H = 640, 760
    d = Doc(W, H, 54)
    d.grid_bg()
    d.icon('logos', 0, 0, 380, 90, pad=0.16)
    d.snow_peak(380, 0, 260, 90, b=10, seed=3, dissolve_w=0.6)
    d.title_lockup(0, 90, W, h=300, pad=28, center=True)
    d.strip(0, 390, W, 70, E['sub'], WHT, size=34)
    d.strip(0, 460, W, 66, E['slogan'], YEL, size=32)
    d.card(0, 526, 400, 66, BLK)
    d.text(24, 561, f"{E['date']} {E['time'][:5]}", 30, WHT)
    d.card(0, 592, 400, 66, WHT)
    d.text(24, 627, '天津大学 · ' + E['venue_short'], 28, BLK)
    d.card(0, 658, 400, 102, BLUE)
    d.text(200, 711, '立即报名 →', 42, WHT, anchor='middle')
    d.hero_field(400, 526, 240, 234, logos=False, seed=44, glass_top=0.2, cell=34, steps=(), stripe_at=-0.1)
    return d


def mini_cover():
    """小程序封面 9:7（900×700）"""
    W, H = 900, 700
    d = Doc(W, H, 60)
    d.grid_bg()
    d.icon('logos', 0, 0, 600, 110, pad=0.15)
    d.title_lockup(0, 110, 600, h=360, pad=34)
    d.strip(0, 470, 600, 80, E['sub'], WHT, size=40)
    d.card(0, 550, 600, 75, BLK)
    d.text(30, 588, f"{E['date']} {E['time']}", 34, WHT)
    d.card(0, 625, 600, 75, WHT)
    d.text(30, 663, '天津大学 · ' + E['venue_short'], 32, BLK)
    d.hero_field(600, 0, 300, 700, logos=False, seed=45, glass_top=0.5, cell=50, steps=('01', '02'))
    return d


FORMATS['01g_视频号直播封面_1080x1440'] = (live_cover, None)
FORMATS['01h_CSDN首页视窗_640x760'] = (csdn_ad, None)
FORMATS['01i_小程序封面_9x7_900x700'] = (mini_cover, None)
