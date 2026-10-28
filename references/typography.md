# 字体与排版系统

v0.1 的排版是"系统默认字体 + 标题、副标、日期从上往下堆"，这是最初级的做法。设计师的排版有三个特征：

1. **字体是选出来的**，有性格，和概念气质匹配；
2. **对比极强**：字号对比、字重对比、中英文对比；
3. **有一套系统**：网格、细线、编号、标签，每个元素对齐到某个东西，小字也在承载信息。

本文件提供字体库、5 套排版系统和微排版规则。模板 `templates/kv.html` 已实现这些系统，config 里用 `type_system` 选择。

---

## 一、字体库

### 加载方式

config 的 `fonts` 字段：

```json
"fonts": {
  "files": { "Smiley Sans": "fonts/SmileySans-Oblique.ttf" },
  "google": ["Space Grotesk:wght@300..700", "Instrument Serif:ital@0;1"],
  "display": "\"Smiley Sans\"",
  "cjk": "\"Alibaba PuHuiTi 3.0\", \"Noto Sans SC\"",
  "latin": "\"Space Grotesk\"",
  "serif": "\"Instrument Serif\"",
  "mono": "\"JetBrains Mono\""
}
```

- `files`：本地字体文件，放在项目的 `fonts/` 目录下（相对 config.json）。**中文商用字体一律走这里**。
- `google`：渲染环境能访问 Google Fonts 时，按 CSS2 API 的写法列出。不能联网时这一项会被忽略，回退到本地字体。
- 角色：`display`（超大字/字标）、`cjk`（中文正文与标题）、`latin`（英文）、`serif`（编辑风）、`mono`（数据/代码）。

`render.py` 会在渲染前检查每个角色的首选字体是否真的加载了，没加载会打印警告。**看到警告不要忽略**：回退到系统默认字体正是 v0.1 效果差的原因之一。

### 中文字体（可免费商用，使用前到官网核对最新授权）

| 字体 | 性格 | 适合 | 获取 |
|---|---|---|---|
| 思源黑体 / Noto Sans SC | 中性、全字重 | 万能底座，Black 字重做标题很好 | Google Fonts、GitHub adobe-fonts |
| 思源宋体 / Noto Serif SC | 典雅、有文化感 | `editorial` 系统 | 同上 |
| 阿里巴巴普惠体 3.0 | 现代、干净、略宽 | 大厂发布会、`swiss` | 阿里巴巴官网 |
| HarmonyOS Sans SC | 理性、几何、科技 | 技术大会、`swiss` | 华为开发者官网 |
| MiSans | 圆润、友好、可变字重 | AI、消费科技 | 小米官网 |
| 得意黑 Smiley Sans | 窄、斜、锋利、有速度感 | 黑客松、年轻向标题 | GitHub atelier-anchor（OFL） |
| 阿里妈妈数黑体 | 粗、方正、冲击力强 | 超大标题、`bleed` | 阿里妈妈官网 |
| 阿里妈妈方圆体 | 可变、圆角、亲和 | 社区、开源活动 | 同上 |
| 优设标题黑 | 粗壮、斜切、运营感 | 促销感较强，技术活动慎用 | 优设网 |
| 站酷高端黑 / 站酷酷黑 | 硬朗 | 标题 | 站酷 |
| 钉钉进步体 | 方正、略斜、有进取感 | 黑客松、挑战赛 | 钉钉官网 |
| 霞鹜文楷 LXGW WenKai | 手写、温暖 | 社区、人文向分享会 | GitHub lxgw（OFL） |
| 更纱黑体 Sarasa Mono SC | 等宽中英 | `terminal` 系统的中文 | GitHub be5invis（OFL） |

### 英文字体

**开源（OFL，Google Fonts 可直接加载）**

| 字体 | 性格 | 适合角色 |
|---|---|---|
| Inter / Inter Tight / Inter Display | 中性精确 | latin，万能 |
| Geist / Geist Mono | 现代开发者工具气质 | latin、mono |
| Space Grotesk | 略带怪趣的几何体，技术圈常用 | latin、display |
| Unbounded | 宽、圆、未来感 | display |
| Syne | 宽窄跨度大，艺术感 | display |
| Bricolage Grotesque | 有性格的怪诞体 | display、latin |
| Archivo（宽度可变） | 可以做极宽或极窄 | display |
| Big Shoulders Display / Anton | 极窄、高冲击 | `bleed` 巨字 |
| Instrument Serif | 优雅窄衬线，斜体漂亮 | serif |
| Fraunces / Newsreader | 现代衬线 | serif |
| JetBrains Mono / IBM Plex Mono / Martian Mono | 等宽 | mono |
| Doto / Silkscreen | 点阵 / 像素 | 黑客松点缀 |

**商用付费（客户有授权时优先）**：Neue Haas Grotesk、Helvetica Now、PP Neue Montreal、PP Mori、ABC Diatype、Söhne、Monument Extended、GT America。

### 字体配方（按气质）

| 气质 | display | cjk | latin | mono |
|---|---|---|---|---|
| 理性、精确（技术大会默认） | Inter Display 200 | HarmonyOS Sans SC Black | Inter | JetBrains Mono |
| 现代、开发者 | Geist 300 | 阿里巴巴普惠体 Heavy | Geist | Geist Mono |
| 宏大、冲击 | Big Shoulders Display 900 | 阿里妈妈数黑体 | Space Grotesk | IBM Plex Mono |
| 年轻、速度 | Unbounded 800 | 得意黑 | Space Grotesk | Martian Mono |
| 人文、典雅 | Instrument Serif Italic | 思源宋体 Heavy | Inter | IBM Plex Mono |
| 极客 | JetBrains Mono 800 | 更纱黑体 Bold | JetBrains Mono | JetBrains Mono |

规则：
- 一张 KV 最多 **2 个字体家族 + 1 个等宽**。
- 中英文要**性格一致**：几何中文配几何英文，宋体配衬线。
- **不要用伪粗体**。想要粗就选有 Black/Heavy 字重的字体。

---

## 二、排版系统

每套系统定义：网格、标题处理、信息组织、点缀元素。config 里 `type_system` 选择。

### `swiss` 瑞士网格（默认）
- **网格**：12 栏，外边距 = 短边 7%，栏间距 = 短边 1.5%。所有元素左边缘对齐到栏线。
- **标题**：中文 Black 字重，字号大（短边 11–14%），字距 -0.02em，行高 1.02。英文名用 display 字体的**细字重**（200–300）、同等或更大字号，与中文形成粗细对比；或用小号全大写宽字距。
- **信息**：日期、地点、主办方做成"标签 + 值"的网格单元，标签用 mono 小号全大写（`DATE` `VENUE` `HOST`），值用 latin 字体中等字号；单元之间用 1px 细线分隔。
- **点缀**：左上角编号（`01`、`Vol.03`）、顶部细线、场馆真实坐标（`22.54°N 114.06°E`）、角标十字。
- **适合**：几乎所有技术大会。

### `bleed` 巨字出血
- **网格**：同 swiss。
- **标题**：一个**超大字形**（活动缩写、年份或核心英文词，≤ 6 字符）用 display 字体横跨画面，高度占画面 40–60%，一侧出血被裁切。主体抠图（`hero_fg`）压在巨字上，形成前后穿插。中文活动名则相对较小（短边 5–7%），放在网格上一个精确的位置。
- **信息**：底部一行，按栏均分排列。
- **点缀**：巨字可以用 `title_fill: hero`（主图填充）或 `gradient`（取色渐变）或半透明描边。
- **适合**：品牌发布会、年度大会、有强缩写的活动（如 "TIC"、"WWDC"）。
- **需要**：`hero_fg` 抠图；没有抠图时巨字放在主体后方，用 `fx.haze` 让主体压住巨字的感觉更强。
- **位置**：默认放在中间带。画面有地平线、水面、地面时，用 `mark_baseline`（如 `0.6`）让巨字底边落在地平线上，下沿淡入雾中，像立在场景里。**巨字不能挡住画面的叙事焦点**（如两个元素交汇的位置）。

### `lockup` 品牌字锁定（识别度最高）
- **结构**：活动名里最有辨识度的 1–3 个中文字（或 ≤ 6 个字母）做成巨字 `mark`，高度约占画面 40%；全称剩余部分 `lockup` 和英文名在巨字正下方组成锁定组合；slogan 写成一行代码注释（`// 每一行代码，汇成星河`）放在顶栏下；信息栏在右下。
- **巨字细节**：默认 `mark_fill: texture`，用 `mark_texture`（如 glyph_flow.py 生成的代码纹理）填充，近看是密排代码，远看是实心字。也可以用 `solid` / `outline` / `gradient`。
- **穿插**：配合 `hero_fg`，让发光的主体或流从巨字前面穿过。
- **适合**：活动名本身有画面感、需要强识别度的大会。
- **参数**：`mark`、`mark_size`（相对画面高度，横版默认 0.4）、`mark_top`、`mark_fill`、`mark_texture`；`text.lockup` 为锁定组合文字（默认取 h1 去掉 mark 的部分）。

### `invite` 一图一句（高端品牌）
- **结构**：主画面满版；只保留 tagline（`slogan`）、活动名 + 日期（`mark` + `info[0]`）、可选的极小注释（`note`，如"Unofficial concept"）。没有顶栏、编号、标签网格。
- **参数**：`invite_align`（`center` / `left`）、`invite_y`（文字组中心的高度，默认横版 0.8）。
- **适合**：Apple 这一级的品牌、发布会邀请函、主画面足够强的方向。
- **前提**：主画面必须是高精度渲染或摄影，否则减法只会显得空。

### `editorial` 编辑部
- **网格**：不对称，大量留白。
- **标题**：宋体 Heavy 中文 + 衬线斜体英文（Instrument Serif Italic），两者字号接近，交错排列；或中文**竖排**，英文横排。
- **信息**：像杂志版权页：`VOL.03 — 2026 秋 — 深圳`，细线分隔。
- **点缀**：期号、页码式的数字、引号。
- **适合**：人文向技术分享、设计 × 技术、开源社区年会、白底方向。

### `terminal` 终端
- **网格**：等宽字符网格，所有文字对齐到字符格。
- **标题**：中文仍然用粗体大字（不要用等宽中文做大标题，太弱），上方用 mono 写一行命令：`$ devcon --year 2026 --city shenzhen`。
- **信息**：写成命令行输出或配置文件：`date: 2026.12.11–12`、`venue: "深圳会展中心"`，带语法高亮色。
- **点缀**：底部状态栏（类似 tmux / vim 的模式栏）、闪烁光标 `▍`、行号。
- **适合**：黑客松、技术沙龙、开发者社区。
- **注意**：命令和输出必须真实合理，与活动内容相关。

### `center` 居中纪念碑
- **网格**：中轴对称。
- **标题**：居中，中文大字 + 下方英文宽字距；整体压在画面下 1/3 或主体正前方。
- **信息**：一行居中，用 `·` 分隔。
- **适合**：方图、对称主体、竖版海报。

### 系统 × 尺寸

模板会自动适配横竖：横版左右分区，竖版上下分区，方图通常切到 `center`。某个尺寸单独指定 `type_system` 可覆盖。

---

## 三、微排版规则

这些细节决定了"像设计师做的"还是"像程序生成的"。

**中文**
- 标题用 `font-feature-settings: "palt"`（标点挤压），避免逗号句号占一整格。模板默认开启。
- 粗字重标题字距收紧到 -0.01 ~ -0.03em；细字重放宽到 0.02em。
- 标题不要在一个词中间断行。用数组手动分行，按语义断：`["AI 原生", "开发者大会"]`。
- 中文标题尽量不放标点；需要停顿时用换行代替。

**英文与数字**
- 全大写小字必须加字距 0.12–0.4em；大字号全大写字距 -0.02 ~ 0em。
- 日期、时间用等宽数字（`tabular-nums`）；超大号年份用 display 字体的默认数字。
- 连接号用 en dash `–`（`12.11–12`），不要用连字符 `-`。
- 中英混排时把 latin 字体排在字体栈前面，这样英文和数字用英文字体渲染。

**层级**
- 最大字与次一级字的字号比 ≥ 3:1。对比弱是"初级感"的主要来源。
- 同一层级只用一种样式。
- 全画面最多 4 个层级（不算点缀小字）。

**点缀元素必须承载真实信息**
- 坐标用场馆真实坐标；编号用真实届数；版本号、场次数、讲者数用真实数据。
- 不知道就不放，**不要编造**。

---

## 四、版式与安全区

所有版式共用外边距：短边 × 7%（大屏 6%，竖版 8%）。

- **大屏**：底部 8% 可能被舞台遮挡，不放关键信息。
- **公众号头图 900×383**：转发卡片等场景可能只露出中间区域，必须同时出 `square` 次图。
- **社媒竖版**：顶部 12% 和底部 18% 会被 UI 覆盖。
- **印刷**：四边 3mm 出血，文字离裁切线 ≥ 5mm。
