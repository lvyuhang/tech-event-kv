from lib import *

AGENDA = [('01', 'XX:XX', '签到入场'), ('02', 'XX:XX', '开场致辞'), ('03', 'XX:XX', 'CANN 开发者俱乐部成立仪式'),
          ('04', 'XX:XX', 'CANN 技术宣讲'), ('05', 'XX:XX', '互动问答'), ('06', 'XX:XX', '合影留念')]
SLOGAN = '从第一个算子，到第一份贡献'
SUB = '成立仪式暨校园宣讲会'


def lockup_h(d, x, y, w, h, notch=None, tag='天津大学', pad=None):
    """横向锁定：左 CANN 巨字，右两行“开发者 / 俱乐部”"""
    u = d.u
    d.card(x, y, w, h, WHT, notch=notch)
    pad = u * 0.5 if pad is None else pad
    tag_h = u * 0.9
    if tag:
        tw = measure(tag, tag_h * 0.62) + tag_h * 0.9
        d.card(x + pad, y + pad, tw, tag_h, BLK, stroke=False)
        d.text(x + pad + tw / 2, y + pad + tag_h / 2 + 2, tag, tag_h * 0.62, WHT, anchor='middle')
        top = y + pad + tag_h + u * 0.35
    else:
        top = y + pad
    ch = y + h - pad - top
    cw = ch * 426 / 124
    avail = w - 2 * pad
    if cw + ch * 1.55 > avail:
        ch = avail / (426 / 124 + 1.55)
        cw = ch * 426 / 124
        top = y + h - pad - ch
    d.crop(d.ICONS['cann'][0], x + pad, top, cw, ch)
    rx = x + pad + cw + u * 0.3
    lh = ch / 2
    size = min(lh * 0.98, (x + w - pad - rx) / 3.05)
    d.text(rx, top + lh * 0.5 + size * 0.03, '开发者', size, BLK)
    d.text(rx, top + lh * 1.5 + size * 0.03, '俱乐部', size, BLK)


def date_cell(d, x, y, w, h, l1='11月08日', l2='天津大学XXX'):
    d.card(x, y, w, h, BLK)
    s = min(h * 0.27, (w * 0.8) / max(measure(l1, 1), measure(l2, 1)))
    d.text(x + w * 0.1, y + h * 0.32, l1, s, WHT)
    d.text(x + w * 0.1, y + h * 0.68, l2, s, WHT)


def section_tag(d, x, y, h, txt):
    w = measure(txt, h * 0.5) + h * 0.9
    d.card(x, y, w, h, BLK)
    d.text(x + w / 2, y + h / 2 + 2, txt, h * 0.5, WHT, anchor='middle')
    return w


def green_grid(d, x, y, w, h, step):
    d.grid_bg(x, y, w, h, fill=GRN, line=WHT, step=step, lw=step * 0.06)
    d.card(x, y, w, h, 'none')


# =============================================================== 1 宣传图
def kv_16x9():
    d = Doc(1408, 784, 57.5)
    d.add('<image href="kv.svg" width="1408" height="784"/>')
    return d


def long_poster():
    """手机竖滑：第一屏（0–1920）要有标题、时间、地点和报名提示"""
    u = 90
    W, H = 1080, 3900
    d = Doc(W, H, u)
    d.grid_bg()
    d.snow_peak(0, 0, 620, 170, seed=5)
    d.icon('plus', 630, 0, 150, 170, pad=0.2)
    d.icon('times', 780, 0, 150, 170, pad=0.2)
    d.icon('sigma', 930, 0, 150, 170, pad=0.2)
    d.hero_field(720, 170, 360, 1110, logos=True, seed=21, glass_top=0.7, cell=62, logo_w=300)
    hh = d.title_lockup(0, 170, 720)
    y = 170 + hh
    d.strip(0, y, 720, 120, SUB, WHT, size=58)
    d.strip(0, y + 120, 720, 120, SLOGAN, YEL, size=46)
    y2 = y + 240
    date_cell(d, 0, y2, 440, 1280 - y2)
    d.icon('npu', 440, y2, 280, 1280 - y2, pad=0.16)
    # 报名提示（第一屏内）
    d.card(0, 1340, W, 110, BLK)
    d.text(40, 1395, '名额有限', 44, '#3BD83B', PIXEL)
    d.text(1040, 1397, '扫描文末二维码报名  ↓', 44, WHT, HEAVY, 'end')
    # 活动信息
    y = 1530
    section_tag(d, 0, y, 96, '活动信息')
    d.sparkle(1020, y + 48, 40)
    d.sparkle(958, y + 30, 20)
    y += 96
    rows = [('时间', '2026年11月08日（周日）XX:XX'), ('地点', '天津大学XXX'), ('对象', '天津大学在校师生')]
    for i, (k, v) in enumerate(rows):
        yy = y + i * 120
        d.card(0, yy, 200, 120, [BLUE, ORG, GRN][i])
        d.text(100, yy + 60, k, 50, WHT, PIXEL, 'middle')
        d.strip(200, yy, 880, 120, v, WHT, size=40, anchor='start')
    # 议程
    y = 2110
    section_tag(d, 0, y, 96, '活动议程')
    d.icon('matrix', 680, y, 400, 96, cell=False, pad=0.05)
    hgt = d.agenda_bal(0, y + 130, W, 104, AGENDA, hi=2)
    # 报名
    y = y + 130 + hgt + 90
    section_tag(d, 0, y, 96, '扫码报名')
    y += 130
    d.icon('member', 0, y, 620, 330, cell=False, pad=0.0)
    d.card(660, y - 20, 420, 420, WHT)
    d.qr(705, y + 10, 330)
    d.text(870, y + 370, '加入 CANN 开发者俱乐部', 28, BLK, HEAVY, 'middle')
    yb = H - 300
    d.pixel_hill(0, yb, 820, 300, b=30, seed=12, base=0.3, peak=0.95)
    green_grid(d, 820, yb, 260, 300, 65)
    return d


def wechat_head():
    """信息流里只有约 300px 宽：只留标题和标志画面；标题落在中间方形里（转发裁方图仍完整）"""
    u = 48
    d = Doc(900, 383, u)
    d.grid_bg()
    d.icon('npu', 0, 0, 150, 383, pad=0.16)
    d.title_lockup(150, 0, 500, h=383, pad=26, center=True)
    d.hero_field(650, 0, 250, 383, logos=True, seed=31, glass_top=0.6, cell=30, logo_w=215, steps=('01', '02'))
    return d


def wechat_square():
    """次图只有约 150px：CANN + 开发者俱乐部 + 标志画面"""
    u = 75
    d = Doc(900, 900, u)
    d.grid_bg()
    d.icon('logos', 0, 0, 900, 120, pad=0.2)
    d.title_lockup(0, 120, 900, h=560, pad=48, center=True)
    d.hero_field(0, 680, 900, 220, logos=False, seed=41, glass_top=0.0, cell=40, steps=(), stripe_at=0.25)
    return d


def recap_head():
    """回顾封面：现场照片放进“成员卡取景框”，和合影背板呼应"""
    u = 48
    d = Doc(900, 383, u)
    d.card(0, 0, 900, 383, BLUE, stroke=False)
    d.title_lockup(0, 0, 400, h=383, tag='活动回顾', pad=26, center=True)
    x, y, w, h = 420, 22, 460, 339
    d.grid_bg(x, y, w, h, fill='#E6ECF7', line=WHT, step=40, lw=2)
    d.brackets(x + 8, y + 8, w - 16, h - 16, 50, 9, YEL)
    d.text(x + w / 2, y + h / 2 - 14, '现场合影', 36, '#7f93c4', anchor='middle')
    d.text(x + w / 2, y + h / 2 + 28, '替换为实拍', 22, '#7f93c4', PIXEL, 'middle')
    d.bubble(x + w - 150, y + 26, 110, 64, 'bl')
    d.ftext(x + w - 150, y + 26, 110, 64, '+1', BLK, HEAVY, maxsize=48)
    return d


# =============================================================== 2 合影背板
def backdrop():
    """合影背板 5×2m → 2500×1000（1px = 2mm）。
    概念：整块是一张“贡献图”——一座贯穿全幅的绿色贡献山（从第一个算子到第一份贡献），右端接 KV 标志画面；
    玩法：合影的人举绿色“+1”方块牌，人变成山上的方块；左侧 NPU 芯片说 hello，可以和它合影。
    场景：落地桁架，大合影只露顶部 → 标题条在最上；山和 +1 在人身后与手里。"""
    W, H = 2500, 1000
    d = Doc(W, H, 100)
    d.grid_bg(step=50, lw=2.5)
    # 右端：KV 标志画面，与贡献山相接
    d.hero_field(2060, 0, 440, H, logos=False, seed=13, glass_top=0.45, cell=64, steps=('01', '02'), stripe_at=-0.05)
    # 贡献山（贯穿全幅）
    b = 50
    tops = d.contrib_mountain(0, 300, 2060, 700, b, seed=8, start=0.06, end=0.72)
    # 山顶：今天的那一格
    pi = len(tops) - 3
    px, py = pi * b, 300 + 700 - tops[pi] * b
    d.add(f'<rect x="{px+3}" y="{py-b+3}" width="{b-6}" height="{b-6}" rx="4" fill="{YEL}" stroke="{BLK}" stroke-width="4"/>')
    d.bubble(px - 300, py - 230, 330, 150, 'br')
    d.text(px - 135, py - 185, '+1', 66, BLK, HEAVY, 'middle')
    d.pixtext(px - 135, py - 140, '2026.11.08', 30, BLUE, 'middle')
    # 山脚：第一个算子
    d.add(f'<rect x="{0*b+3}" y="{1000-b+3}" width="{b-6}" height="{b-6}" rx="4" fill="{YEL}" stroke="{BLK}" stroke-width="4"/>')
    # 左：NPU 芯片角色 + 对话框（人站旁边合影）
    d.icon('npu', 40, 350, 340, 360, pad=0.08)
    d.bubble(410, 340, 520, 150, 'bl')
    d.crop(d.ICONS['hello'][0], 445, 375, 450, 84)
    # 顶部标题条（大合影唯一完整露出）
    d.icon('logos', 0, 0, 520, 230, pad=0.1)
    d.card(520, 0, 1540, 230, WHT)
    d.crop(d.ICONS['cann'][0], 570, 45, 520, 151, black=True)
    d.crop(d.ICONS['club'][0], 1120, 58, 620, 124)
    d.card(1770, 52, 250, 126, YEL, stroke=False)
    d.text(1790, 92, '成立仪式', 44, BLK)
    d.text(1790, 146, '暨校园宣讲会', 36, BLK)
    # 标题条下：slogan 作为这张图的图名
    d.card(520, 230, 1540, 64, BLK)
    d.text(560, 263, SLOGAN, 36, WHT, HEAVY)
    d.text(2020, 263, '今天，CANN 社区 +1', 36, '#3BD83B', PIXEL, 'end')
    return d


def props():
    """配套手举牌：绿色 +1 方块（多做几块，人手一块）+ 两个像素对话框"""
    W, H = 2000, 760
    d = Doc(W, H, 60)
    d.grid_bg()
    # +1 方块 40×40cm
    for i, (fill, txt, col) in enumerate([('#26BB45', '+1', WHT), ('#0C9A2F', '+1', WHT), (YEL, '+1', BLK)]):
        x0 = 60 + i * 330
        d.add(f'<rect x="{x0+12}" y="72" width="290" height="290" fill="{BLK}"/>')
        d.add(f'<rect x="{x0}" y="60" width="290" height="290" fill="{fill}" stroke="{BLK}" stroke-width="8"/>')
        d.text(x0 + 145, 205, txt, 150, col, HEAVY, 'middle')
        d.add(f'<rect x="{x0+125}" y="362" width="40" height="230" fill="#C9A26B" stroke="{BLK}" stroke-width="5"/>')
    d.text(560, 640, '“+1”方块牌 40×40cm · KT 板 + 手柄，建议 30–50 块，人手一块', 30, '#555', HEAVY, 'middle')
    d.bubble(1080, 60, 820, 230, 'br')
    d.crop(d.ICONS['hello'][0], 1130, 110, 720, 132)
    d.bubble(1080, 380, 560, 200, 'bl')
    d.text(1360, 455, 'Merged ✓', 96, GRN, HEAVY, 'middle')
    d.text(1490, 700, '对话框异形切割 约 60×25cm / 45×22cm', 30, '#555', HEAVY, 'middle')
    return d


# =============================================================== 3 A4 日程单页
def a4():
    """拿在手里 40cm 读：议程是主角，成立仪式高亮；底部扫码入群"""
    u = 80
    W, H = 1240, 1754
    d = Doc(W, H, u)
    d.grid_bg()
    d.snow_peak(0, 0, 560, 120, b=14, seed=14)
    d.icon('plus', 560, 0, 106, 120, pad=0.2)
    d.icon('times', 666, 0, 106, 120, pad=0.2)
    d.icon('sigma', 772, 0, 108, 120, pad=0.2)
    d.hero_field(880, 0, 360, 690, logos=True, seed=61, glass_top=0.62, cell=52, logo_w=300)
    d.title_lockup(0, 120, 880, h=480)
    d.strip(0, 600, 880, 90, SUB, WHT, size=52)
    d.strip(0, 690, 820, 96, SLOGAN, YEL, size=46)
    d.card(820, 690, 420, 96, BLUE)
    d.pixtext(1030, 690 + 30, '2026.11.08', 36, WHT, anchor='middle')
    d.card(0, 786, 620, 90, BLK)
    d.text(30, 831, '地点', 36, '#3BD83B', PIXEL)
    d.text(130, 833, '天津大学XXX', 36, WHT)
    d.card(620, 786, 620, 90, WHT)
    d.text(650, 831, '时间', 36, BLUE, PIXEL)
    d.text(750, 833, '周日 XX:XX – XX:XX', 36, BLK)
    y = 940
    section_tag(d, 0, y, 80, '活动议程')
    d.sparkle(1180, y + 40, 32)
    d.sparkle(1126, y + 22, 15)
    hgt = d.agenda_bal(0, y + 100, W, 74, AGENDA, hi=2, gap=10)
    yb = y + 100 + hgt + 40
    d.card(0, yb, W, H - yb, WHT)
    d.icon('member', 24, yb + 22, 330, H - yb - 44, cell=False, pad=0)
    d.text(390, yb + (H - yb) * 0.38, '扫码加入 CANN 开发者俱乐部', 38, BLK)
    d.text(390, yb + (H - yb) * 0.68, '活动资料与后续技术分享都在群里', 26, '#666', HEAVY)
    q = H - yb - 30
    d.qr(W - q - 15, yb + 15, q)
    return d


# =============================================================== 4 指引牌
def guide(direction):
    """画架指引牌：边走边看 3–10m，方向是唯一要紧的信息 → 箭头和“主会场”在最上面、最大；下部会被托槽和人挡"""
    u = 60
    W, H = 600, 900
    d = Doc(W, H, u)
    d.grid_bg()
    d.icon('logos', 0, 0, W, 84, pad=0.14)
    d.card(0, 84, W, 420, YEL)
    d.text(W / 2, 168, '主会场', 108, BLK, anchor='middle', ls=0.1)
    cell = 30
    aw = 13 * cell
    d.pixel_arrow(W / 2 - aw / 2, 240, cell, direction, BLK)
    lockup_h(d, 0, 504, W, 196, tag=None, pad=30)
    d.strip(0, 700, W, 70, SUB, BLK, WHT, size=38)
    d.hero_field(0, 770, W, 130, logos=False, seed=71 if direction == 'left' else 72, glass_top=0.0, cell=34, steps=(), stripe_at=0.3)
    return d


# =============================================================== 5 易拉宝
def rollup():
    """入口易拉宝：视线高度 1.5–1.7m ≈ 离顶 300–500mm；标题与议程上移，二维码在 1.0–1.2m 高；底部 150mm 被底座挡"""
    u = 80
    W, H = 800, 2000
    d = Doc(W, H, u)
    d.grid_bg()
    d.icon('logos', 0, 0, W, 110, pad=0.16)
    d.title_lockup(0, 110, W, h=440, pad=40, center=True)
    d.strip(0, 550, W, 86, SUB, WHT, size=48)
    d.strip(0, 636, W, 86, SLOGAN, YEL, size=44)
    date_cell(d, 0, 722, 330, 200)
    d.card(330, 722, 260, 200, BLK)
    d.text(460, 790, '扫码报名', 34, '#3BD83B', PIXEL, 'middle')
    d.text(460, 850, '→', 60, WHT, HEAVY, 'middle')
    d.card(590, 722, 210, 200, WHT)
    d.qr(605, 737, 170)
    y = 960
    section_tag(d, 0, y, 72, '活动议程')
    d.sparkle(760, y + 36, 28)
    d.sparkle(714, y + 20, 13)
    hgt = d.agenda_bal(0, y + 92, W, 70, AGENDA, hi=2, gap=10)
    yb = y + 92 + hgt + 30
    d.hero_field(0, yb, W, H - yb, logos=False, seed=81, glass_top=0.42, cell=48, steps=('01', '02'), stripe_at=0.2)
    return d


# =============================================================== 7 麦克标
def mic():
    """麦克标 8×6cm：照片和直播里远看，每面只放一个元素"""
    fw, fh = 800, 600
    d = Doc(fw * 4, fh, 50)
    # 面 1：CANN
    d.card(0, 0, fw, fh, WHT, stroke=False)
    d.crop(d.ICONS['cann'][0], 70, 150, 660, 192)
    d.hero_field(0, 430, fw, 170, logos=False, seed=91, glass_top=0.0, cell=34, steps=(), stripe_at=0.35)
    # 面 2：开发者俱乐部
    d.card(fw, 0, fw, fh, YEL, stroke=False)
    d.text(fw + 400, 210, '开发者', 170, BLK, anchor='middle')
    d.text(fw + 400, 410, '俱乐部', 170, BLK, anchor='middle')
    # 面 3：联合 logo
    d.card(fw * 2, 0, fw, fh, BLUE, stroke=False)
    d.crop(d.ICONS['logos'][0], fw * 2 + 60, 230, 680, 117)
    # 面 4：NPU 像素图标
    d.card(fw * 3, 0, fw, fh, BLUE, stroke=False)
    d.crop(d.ICONS['npu'][0], fw * 3 + 230, 90, 340, 360)
    d.card(fw * 3, 470, fw, 130, BLK, stroke=False)
    d.crop(d.ICONS['hello'][0], fw * 3 + 140, 490, 520, 90)
    for i in range(1, 4):
        d.add(f'<path d="M{i*fw} 0V{fh}" stroke="#888" stroke-width="3" stroke-dasharray="12 10"/>')
    return d


# =============================================================== 8 桌卡
def table_card(name):
    """桌卡：台下和镜头看名字 → 名字占满；品牌退到上下两条"""
    W, H = 900, 1300
    hh = H // 2
    u = 60
    d = Doc(W, H, u)

    def face(seed):
        f = Doc(W, hh, u)
        f._id = seed * 1000
        f.card(0, 0, W, hh, WHT, stroke=False)
        f.icon('logos', 0, 0, W, 100, pad=0.16, stroke=False)
        size = min(230, 760 / max(len(name), 2) / 1.0)
        f.text(W / 2, 300, name, size, BLK, anchor='middle', ls=0.06)
        f.hero_field(0, 520, W, 130, logos=False, seed=seed, glass_top=0.0, cell=34, steps=(), stripe_at=0.35)
        return ''.join(f.parts)

    d.add(f'<g transform="rotate(180 {W/2} {hh/2})">{face(101)}</g>')
    d.add(f'<g transform="translate(0 {hh})">{face(102)}</g>')
    d.add(f'<path d="M0 {hh}H{W}" stroke="#888" stroke-width="3" stroke-dasharray="12 10"/>')
    return d


# =============================================================== 9 横幅
def banner():
    """舞台上方横幅 6m×0.6m，10–30m 外看：一行字尽量大"""
    W, H = 3000, 300
    d = Doc(W, H, 50)
    d.card(0, 0, W, H, BLUE, stroke=False)
    d.add(f'<path d="{"".join(f"M{x} 0V{H}" for x in range(0, W, 50))}{"".join(f"M0 {y}H{W}" for y in range(0, H, 50))}" stroke="{GRID_B}" stroke-width="1.5"/>')
    d.hero_field(0, 0, 150, H, logos=False, seed=111, glass_top=0.0, cell=30, steps=(), stripe_at=-0.2)
    d.hero_field(W - 150, 0, 150, H, logos=False, seed=112, glass_top=0.0, cell=30, steps=(), stripe_at=-0.2)
    txt = '天津大学 CANN 开发者俱乐部成立仪式暨校园宣讲会'
    s = fit(txt, 2620)
    d.text(W / 2, 154, txt, s, WHT, anchor='middle')
    return d


# =============================================================== A 头顶心声墙
VOICES = [
    # (文案, 底色, 字色, 尾巴方向, 字体)
    ('在我电脑上是好的', WHT, BLK, 'bl', HEAVY),
    ('能跑就别动', YEL, BLK, 'br', HEAVY),
    ('DDL 是第一生产力', BLUE, WHT, 'bl', HEAVY),
    ('我的第一个算子跑起来了！', WHT, BLK, 'br', HEAVY),
    ('精度对上了吗……', WHT, BLK, 'bl', HEAVY),
    ('LGTM', GRN, WHT, 'br', HEAVY),
    ('Merged ✓', BLK, '#3BD83B', 'bl', HEAVY),
    ('编译通过！', YEL, BLK, 'bl', HEAVY),
    ('再改最后一版', WHT, BLK, 'br', HEAVY),
    ('显存又爆了', ORG, WHT, 'bl', HEAVY),
    ('报错不慌 先搜 issue', WHT, BLK, 'br', HEAVY),
    ('+1 我也要贡献', BLUE, WHT, 'bl', HEAVY),
    ('今天提 PR 了吗', WHT, BLK, 'br', HEAVY),
    ('咖啡续命中', WHT, BLK, 'bl', HEAVY),
]


def voice(d, x, y, txt, h, fill, col, tail, font=HEAVY):
    size = h * 0.42
    w = measure(txt, size) + h * 0.9
    d.bubble(x, y, w, h, tail, fill=fill)
    d.text(x + w / 2, y + h / 2 + size * 0.04, txt, size, col, font, 'middle')
    return w


def voice_wall():
    """方向 A：开发者头顶心声墙 · 合影背板 5×2m（2500×1000，1px=2mm）
    像“关♥活动人”：整面是受众自己的心里话，人站在哪句旁边就“说的是我”。
    对话框按网格成行交错排布、互不重叠，尾巴朝下；标题卡在上中，大合影仍露出。"""
    W, H = 2500, 1000
    d = Doc(W, H, 100)
    d.grid_bg(step=50, lw=2.5)
    d.hero_field(2200, 0, 300, H, logos=False, seed=13, glass_top=0.45, cell=54, steps=('01', '02'), stripe_at=-0.1)
    d.pixel_hill(0, 760, 2200, 240, b=40, seed=7, base=0.35, peak=0.75)
    # 标题卡
    cx, cy, cw, ch = 790, 0, 900, 330
    d.card(cx, cy, cw, ch, WHT)
    d.icon('logos', cx, cy, 330, 64, pad=0.1)
    d.crop(d.ICONS['cann'][0], cx + 36, cy + 80, 520, 151)
    d.text(cx + 590, cy + 117, '开发者', 84, BLK)
    d.text(cx + 590, cy + 200, '俱乐部', 84, BLK)
    d.card(cx, cy + ch - 80, cw, 80, YEL)
    d.text(cx + cw / 2, cy + ch - 38, SUB, 44, BLK, anchor='middle')
    # 对话框：(行 y, x 起, x 止, 文案索引列表, 起始偏移)
    V = VOICES
    rows = [
        (20, 30, 770, [0, 1], 0), (180, 30, 770, [2], 60), (340, 30, 770, [11, 7], 0),
        (20, 1720, 2180, [3], 0), (180, 1720, 2180, [5], 0), (340, 1720, 2180, [9], 40),
        (500, 260, 2180, [4, 10, 8, 12], 380),
    ]
    extra = {195: [(7, 520, 215)], 40: [], 350: []}
    for (yy, x0, x1, idxs, off) in rows:
        widths = [measure(V[i][0], 96 * 0.42) + 96 * 0.9 for i in idxs]
        gap = max(40, (x1 - x0 - off - sum(widths)) / max(len(idxs), 1))
        x = x0 + off
        for k, (i, w) in enumerate(zip(idxs, widths)):
            t, fl, col, tail, fnt = V[i]
            voice(d, x, yy + (22 if k % 2 else 0), t, 96, fl, col, tail, fnt)
            x += w + gap
    voice(d, 1955, 200, V[6][0], 96, V[6][1], V[6][2], V[6][3])
    # 左下：NPU 角色在打招呼
    d.icon('npu', 40, 600, 170, 170, pad=0.1)
    d.bubble(230, 610, 360, 92, 'bl', fill=BLK)
    d.crop(d.ICONS['hello'][0], 252, 630, 316, 54)
    return d


def floor_sticker():
    """配套地贴 2.5×1.2m：把画面延伸到脚下（1250×600）"""
    W, H = 1250, 600
    d = Doc(W, H, 50)
    d.grid_bg(step=50, lw=2)
    d.card(0, 0, W, H, 'none')
    d.card(225, 210, 800, 180, BLK)
    d.crop(d.ICONS['hello'][0], 265, 240, 720, 120)
    # 像素脚印：站位
    foot = [".##.", "####", "####", "####", ".###", ".##.", ".##.", "####", "####", ".##."]
    for (fx, fy, flip) in [(390, 430, 0), (480, 445, 1), (750, 430, 0), (840, 445, 1)]:
        for j, row in enumerate(foot):
            row = row[::-1] if flip else row
            for i, c in enumerate(row):
                if c == '#':
                    d.add(f'<rect x="{fx+i*12}" y="{fy+j*12}" width="11" height="11" fill="{BLUE}"/>')
    d.text(W / 2, 120, '站这里  头顶自动生成心声', 44, BLUE, PIXEL, 'middle')
    return d


# =============================================================== B 算力体检
def power_check():
    """方向 B：NPU 今日算力体检 · 打卡板 2.4×2.4m（1200×1200，1px=2mm）
    机制：人站在仪表盘圆心前，头正好挡住 NPU 芯片（你就是今天的 NPU），抬手当指针指向今天的状态。
    圆心离地 ≈ 1.5m（y=450 → 实际 2.4-0.9），环落在头部和抬手的高度。"""
    W, H = 1200, 1200
    d = Doc(W, H, 60)
    d.grid_bg(step=40, lw=2)
    # 标题带
    d.icon('logos', 0, 0, 380, 130, pad=0.12)
    d.card(380, 0, 820, 130, WHT)
    d.text(410, 68, 'NPU', 80, BLUE, PIXEL)
    d.text(620, 70, '今日算力体检', 84, BLK)
    # 仪表盘（像素环）
    cxp, cyp, r1, r2, b = 600, 640, 270, 380, 26
    segs = [(180, 138, '#BDBDBD', '摸鱼中'), (138, 92, BLUE, '正常算力'), (92, 46, GRN, '满血运行'), (46, 0, ORG, '算子炸了')]
    rects = []
    for gx in range(int(cxp - r2 - b), int(cxp + r2 + b), b):
        for gy in range(int(cyp - r2 - b), int(cyp) + 1, b):
            mx, my = gx + b / 2, gy + b / 2
            rr = math.hypot(mx - cxp, my - cyp)
            if r1 <= rr <= r2 and my <= cyp:
                ang = math.degrees(math.atan2(cyp - my, mx - cxp))
                for a0, a1, col, _ in segs:
                    if a1 <= ang <= a0:
                        rects.append(f'<rect x="{gx+1.5}" y="{gy+1.5}" width="{b-3}" height="{b-3}" fill="{col}"/>')
    d.add(''.join(rects))
    for a0, a1, col, lab in segs:
        am = math.radians((a0 + a1) / 2)
        lx, ly = cxp + math.cos(am) * (r2 + 80), cyp - math.sin(am) * (r2 + 55)
        w = measure(lab, 40) + 44
        d.card(lx - w / 2, ly - 32, w, 64, col if col != '#BDBDBD' else WHT)
        d.text(lx, ly + 2, lab, 40, BLK if col in ('#BDBDBD', GRN) else WHT, anchor='middle')
    for pct, a in [('0', 176), ('200', 4)]:
        am = math.radians(a)
        d.pixtext(cxp + math.cos(am) * (r1 - 40), cyp - math.sin(am) * (r1 - 40) - 10, pct, 22, '#777', 'middle')
    # 圆心：NPU 芯片 = 人头的位置
    d.icon('npu', cxp - 100, cyp - 215, 200, 215, pad=0.1)
    d.text(cxp, cyp + 42, '站在这里 你就是今天的 NPU', 36, BLUE, PIXEL, 'middle')
    d.text(cxp, cyp + 92, '抬手指向你的算力', 30, '#777', PIXEL, 'middle')
    # 底部：KV 语言
    d.hero_field(900, 760, 300, 440, logos=False, seed=21, glass_top=0.3, cell=46, steps=(), stripe_at=-0.1)
    d.pixel_hill(0, 960, 900, 240, b=30, seed=9, base=0.35, peak=0.75)
    d.card(40, 790, 500, 130, WHT)
    d.text(70, 832, CANN_CLUB_LINE, 32, BLK)
    d.text(70, 882, SLOGAN, 28, BLUE)
    return d


def gauge(d, cxp, cyp, r1, r2, b, lab_size=34, label_out=60):
    segs = [(180, 138, '#BDBDBD', '摸鱼中'), (138, 92, BLUE, '正常算力'), (92, 46, GRN, '满血运行'), (46, 0, ORG, '算子炸了')]
    rects = []
    for gx in range(int(cxp - r2 - b), int(cxp + r2 + b), b):
        for gy in range(int(cyp - r2 - b), int(cyp) + 1, b):
            mx, my = gx + b / 2, gy + b / 2
            rr = math.hypot(mx - cxp, my - cyp)
            if r1 <= rr <= r2 and my <= cyp:
                ang = math.degrees(math.atan2(cyp - my, mx - cxp))
                for a0, a1, col, _ in segs:
                    if a1 <= ang <= a0:
                        rects.append(f'<rect x="{gx+1.2}" y="{gy+1.2}" width="{b-2.4}" height="{b-2.4}" fill="{col}"/>')
    d.add(''.join(rects))
    for a0, a1, col, lab in segs:
        am = math.radians((a0 + a1) / 2)
        lx, ly = cxp + math.cos(am) * (r2 + label_out * 1.3), cyp - math.sin(am) * (r2 + label_out * 0.7)
        w = measure(lab, lab_size) + lab_size
        d.card(lx - w / 2, ly - lab_size * 0.8, w, lab_size * 1.6, col if col != '#BDBDBD' else WHT)
        d.text(lx, ly + 2, lab, lab_size, BLK if col in ('#BDBDBD', GRN) else WHT, anchor='middle')


def power_check_wide():
    """B 5×2m：NPU 今日算力体检 · 1P VS 2P（2500×1000，1px=2mm）
    落地桁架：离地 1.5m = y 250。两个仪表盘圆心在 y 250，外环半径 0.48m；
    人站在圆心前，头挡住 NPU 芯片（你就是今天的 NPU），抬手当指针。两人可以同时 PK。"""
    W, H = 2500, 1000
    d = Doc(W, H, 100)
    d.grid_bg(step=50, lw=2.5)
    # 右：KV 标志画面
    d.hero_field(2120, 0, 380, H, logos=False, seed=23, glass_top=0.45, cell=60, steps=('01', '02'), stripe_at=-0.1)
    # 底：绿色像素山
    d.pixel_hill(620, 760, 1500, 240, b=40, seed=5, base=0.35, peak=0.8)
    # 左：标题栏（KV 标题卡语言）
    d.icon('logos', 0, 0, 620, 130, pad=0.12)
    d.card(0, 130, 620, 520, WHT)
    d.text(40, 205, 'NPU', 84, BLUE, PIXEL)
    d.text(40, 320, '今日算力体检', 92, BLK)
    d.crop(d.ICONS['cann'][0], 40, 395, 300, 87)
    d.text(356, 440, '开发者俱乐部', 40, BLK)
    d.card(0, 520, 620, 130, YEL)
    d.text(40, 562, SUB, 40, BLK)
    d.text(40, 615, SLOGAN, 32, BLK)
    d.card(0, 650, 620, 110, BLK)
    d.crop(d.ICONS['hello'][0], 30, 670, 340, 70)
    d.pixel_hill(0, 760, 620, 240, b=40, seed=6, base=0.2, peak=0.4)
    # 两个仪表盘
    cy = 300
    for k, cx in enumerate([975, 1790]):
        gauge(d, cx, cy, 145, 215, 18, lab_size=30, label_out=34)
        d.icon('npu', cx - 66, cy - 138, 132, 138, pad=0.08)
        tag = ['1P', '2P'][k]
        d.card(cx - 60, cy + 18, 120, 60, YEL if k == 0 else GRN)
        d.text(cx, cy + 50, tag, 44, BLK, PIXEL, 'middle')
        d.text(cx, cy + 118, '站这里 你就是今天的 NPU', 30, BLUE, PIXEL, 'middle')
        d.text(cx, cy + 160, '抬手指向你的算力', 26, '#777', PIXEL, 'middle')
    # 中间 VS
    d.text(1382, 250, 'VS', 110, ORG, HEAVY, 'middle')
    # 下部（会被挡住）：一行规则小卡
    d.card(700, 590, 1340, 100, WHT)
    d.text(740, 640, '玩法：两人各站一个表盘  一起抬手  算力低的那位去买咖啡', 38, BLK)
    return d


CANN_CLUB_LINE = 'CANN 开发者俱乐部 · 成立仪式'


FORMATS = {
    '01a_KV_16x9': (kv_16x9, None),
    '01b_海报长图_1080w': (long_poster, None),
    '01c_公众号头图_900x383': (wechat_head, None),
    '01d_公众号次图_1x1': (wechat_square, None),
    '01e_活动总结头图_900x383': (recap_head, None),
    '02_合影背板_5x2m': (backdrop, (5000, 2000)),
    '03_日程单页_A4': (a4, (210, 297)),
    '04a_指引牌_左_60x90cm': (lambda: guide('left'), (600, 900)),
    '04b_指引牌_右_60x90cm': (lambda: guide('right'), (600, 900)),
    '05_易拉宝_80x200cm': (rollup, (800, 2000)),
    '07_麦克标_8x6cm_四面展开': (mic, (320, 60)),
    '08a_人名桌卡_90x130mm': (lambda: table_card('嘉宾姓名'), (90, 130)),
    '08b_人名桌卡_两字名': (lambda: table_card('嘉宾'), (90, 130)),
    '09_横幅_6mx60cm': (banner, (6000, 600)),
    '10_建议加做_手举牌': (props, None),
    'A_心声墙_合影背板_5x2m': (voice_wall, (5000, 2000)),
    'A_配套地贴_2.5x1.2m': (floor_sticker, (2500, 1200)),
    'B_算力体检_打卡板_2.4x2.4m': (power_check, (2400, 2400)),
    'B_算力体检_合影背板_5x2m': (power_check_wide, (5000, 2000)),
}
