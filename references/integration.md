# 主体与背景的融合

"一个物体放在渐变背景上"是生图 KV 最常见的廉价感来源：主体像贴纸，背景像壁纸，两者之间没有任何物理关系。设计师做 3D KV 时，主体和环境是**同一个场景里**一起打光、一起渲染的。

融合要在两个地方解决：**写提示词时**（让模型画出一个世界，而不是一个物体）和**排版合成时**（让文字也进入这个世界）。

---

## 一、提示词层：七种融合手法

每条主图提示词**至少使用其中 3 种**，并在 concept.md 里写明用了哪几种。

| # | 手法 | 做法 | 提示词写法示例 |
|---|---|---|---|
| 1 | **光的溢出** | 主体是光源，或者主体反射/折射出的光落在环境上 | `its glow spills onto the wet ground below, casting soft green light on the reeds` / `caustic light patterns from the glass fall across the floor` |
| 2 | **环境接触** | 主体与环境有物理接触：立在地面、浸在水里、埋在雾里、被云包裹 | `the base of the form is submerged in still water` / `low mist wraps around the lower third` |
| 3 | **倒影与反射** | 主体在地面/水面有倒影；主体表面反射出环境的颜色 | `mirrored in the dark glossy floor` / `its chrome surface reflects the violet sky` |
| 4 | **纵深分层** | 前景虚焦元素 + 中景主体 + 远景大气，三层都有东西 | `out-of-focus fragments in the foreground, the main form in midground, distant hazy horizon` |
| 5 | **同源背景** | 背景由主体的材质/颜色/元素在更大尺度上构成 | `the background is the same iridescent liquid, but vast and defocused` / `scattered particles of the same light drift into the distance` |
| 6 | **边缘消融** | 主体边缘不是硬边，而是散成粒子、雾、液体，融进背景 | `the upper edge dissolves into drifting particles that fade into the night` |
| 7 | **统一光照** | 主体和环境共享同一个光源方向和色温；主体轮廓光用背景色 | `lit by one low warm key light from the left, cool rim light matching the blue atmosphere` |

### 禁用短语

以下短语会让模型画出"贴纸效果"，**不要写**：

`isolated`、`on a plain background`、`on a solid background`、`centered object`、`floating object`、`product shot`、`studio background`（D2 白底玻璃方向除外，且必须同时写手法 1 和 3）、`simple background`、`minimal background`（改写成具体的空气、雾、光的状态）

### "安静区"的写法

文字区要空，但不是"空白"。不要写 `empty space`，要写**这块区域里是什么**：

| ✗ | ✓ |
|---|---|
| `the left third is empty for text` | `the left third is open night sky with only a faint haze, calm and uncluttered` |
| `blank space at the top` | `the top 40% is soft overcast light fading to pale grey, no objects` |
| `negative space` | `a wide stretch of still dark water with gentle reflections` |

这样文字区有质感（雾、天空、水面），文字放上去之后也"在场景里"。

---

## 二、合成层：让文字进入画面

模板 `templates/kv.html` 提供以下合成手段，在 config 里开启。

### 1. 前后穿插（`hero_fg`）
主体抠图（带透明通道的 PNG）放在文字层之上，文字就能从主体后面穿过。这是图文一体最有效的手段。
- 抠图：`python scripts/cutout.py heroes/hero_16x9.png`（见脚本说明），或用生图工具自带的抠图功能
- 适合：`bleed` 排版系统的巨字，或任何主体与标题有重叠的版式
- 原则：主体只遮挡标题的**一小部分**（10–25%），必须仍能读出完整标题

### 2. 取色（`color_from_hero`）
`render.py` 自动从主图中提取主色、高光色和暗部色，写进 `--accent`、`--glow`、`--shade` 变量。标题渐变、细线、高亮文字都用这些颜色，不另外编颜色。

### 3. 统一后期（`fx`）
| 参数 | 作用 | 建议值 |
|---|---|---|
| `grain` | 全画面细颗粒，图和字一起覆盖 | 0.06–0.12；深色画面高一点 |
| `vignette` | 暗角，收拢视线 | 0.25–0.45 |
| `haze` | 底部或一侧加一层主图色的雾，压在文字下层 | 0.3–0.6 |
| `glow` | 标题带极轻的主图色光晕（光的溢出落到字上） | 深色画面 0.2–0.4；浅色画面关闭 |
| `grade` | 一层取色叠加，统一图和字的色温 | 0.05–0.15 |

颗粒和调色**必须盖在文字上面**，这样文字才像"印在画面里"，而不是"浮在屏幕上"。

### 4. 标题填充（`title_fill`）
- `solid`：纯色（swiss / editorial / terminal / center 默认）
- `fade`：上实下虚，下沿淡出到环境里，像立在雾或水中（bleed 巨字默认）
- `gradient`：用取出的主图色做渐变
- `hero`：标题用主图本身填充（`background-clip: text`），适合超大号字形且主图较亮时
- `outline`：只描边，巨字太抢时用
- `accent`：用主图取出的强调色

---

## 三、融合自检

用 Read 看渲染结果，逐条回答：

- [ ] 把主体抠掉，背景本身还有内容吗？（有光、有雾、有地面、有远景 = 是）
- [ ] 主体底部/边缘与环境有接触或过渡吗？还是有一圈硬边？
- [ ] 主体的颜色有没有出现在背景和文字里？
- [ ] 文字看起来是在画面里，还是浮在画面上方的另一层？（有颗粒覆盖、取色、穿插 = 在画面里）
- [ ] 遮住文字，主图单独看是一张完整的画吗？

任一条否 → 主图问题回到提示词加融合手法重新生成；合成问题调 `fx` / `hero_fg` / `color_from_hero`。
