# 风格方向库（技术类活动）

每个方向是一份配方：背景 × 材质 × 配色 × 推荐版式 × 提示词关键词。配色给的是起点，品牌色优先。

---

## D1 暗场流光（Dark Glow）
- **气质**：宏大、沉浸、有舞台感。最适合主会场大屏。
- **背景**：近黑的深紫或深蓝径向渐变，一角带一团大面积柔光。
- **材质**：自发光霓虹管、彩虹色流体玻璃、光丝。
- **配色**：底 `#0A0716` `#1B0F3A`；光 `#7C5CFF` `#FF8A3D` `#3DFFB0`。文字纯白。
- **版式**：L1 左文右图（主体出血到右边）。
- **关键词**：`glowing iridescent glass tube, volumetric light, deep violet black background, soft bloom, shallow depth of field`
- **案例**：Alibaba.com FY27（见 case-studies.md）。

## D2 白底光谱玻璃（Spectral Glass）
- **气质**：干净、精致、通透，带一点乐观。适合大厂发布会、AI 主题。
- **背景**：纯白或极浅冷灰，可加很淡的彩色投影。
- **材质**：半透明亚克力、彩色玻璃、折射与色散。
- **配色**：底 `#FFFFFF` `#F4F6FA`；色块取 4–6 个高饱和色（`#2F6BFF` `#00C2FF` `#7A4DFF` `#FF4D9A` `#FFB020` `#22C55E`）。文字 `#0B0B12`。
- **版式**：L1 左文右图，或 L3 右信息栏。
- **关键词**：`translucent colored acrylic, glass refraction, chromatic dispersion, pure white background, soft caustics, studio lighting`
- **案例**：TCL TIC 2024、WDCC 2022。

## D3 流体有机（Liquid Organic）
- **气质**：智能、生长、柔和。适合 AI、大模型、"生态"主题。
- **背景**：浅色奶油渐变或深色均可。
- **材质**：液态金属、果冻、软胶、肥皂泡薄膜。
- **配色**：浅版 `#F6F1EA` + `#FF7A59` `#7B61FF`；深版 `#0E0E14` + 镀铬。
- **版式**：L2 居中，或 L1。
- **关键词**：`liquid chrome, soft gel, flowing organic form, subsurface scattering, smooth gradient background`

## D4 巨构字形（Monumental Type）
- **气质**：权威、聚焦、有建筑感。适合品牌发布会、年度大会。
- **背景**：单色（黑、白或品牌色），极简。
- **材质**：拉丝金属、混凝土、磨砂玻璃、石材，配强烈的侧光。
- **配色**：单色 + 1 个点缀色。
- **版式**：L2 居中或 L4 满版大字。
- **关键词**：`monumental 3D letterform, brushed metal, dramatic side light, long shadow, minimal, architectural scale`
- **注意**：字形 ≤ 6 个拉丁字符或数字；越短越稳。

## D5 终端代码（Terminal）
- **气质**：极客、真实、开发者认同感强。适合黑客松、技术沙龙。
- **背景**：近黑或深墨绿。
- **材质**：主图可以很弱甚至不用生图，靠代码排版：等宽字、光标、语法高亮配色、CRT 微光。
- **配色**：底 `#0D1117`；高亮 `#7EE787` `#79C0FF` `#FFA657` `#FF7B72`。
- **版式**：L4 满版文字，主图作为背景纹理。
- **关键词**（如需主图）：`abstract CRT phosphor glow, scanlines, dark terminal ambience, bokeh of monospace glyph shapes`
- **注意**：代码内容要真实可读、和活动相关（比如 `$ git checkout -b devcon-2026`），由模板渲染，不要让模型生成代码文字。

## D6 像素与网格（Pixel Grid）
- **气质**：年轻、玩味、复古未来。适合黑客松、游戏开发、开源社区。
- **背景**：浅色网格纸或深色点阵。
- **材质**：体素（voxel）、像素块、等距（isometric）积木。
- **配色**：高饱和撞色，3–4 色为限：`#FF5C39` `#2D5BFF` `#FFD23F` `#111111`。
- **版式**：L1 或 L3。
- **关键词**：`isometric voxel sculpture, clean pastel grid background, toy-like, soft ambient occlusion`

## D7 光场粒子（Particle Field）
- **气质**：深邃、数据感、宇宙尺度。适合 AI、数据、云计算。
- **背景**：深色。
- **材质**：数以万计的光点聚合成符号，局部散开。
- **配色**：底 `#05060A`；粒子取 1–2 个色相，避免"科技蓝白点"的老套搭配，可用暖金 `#FFC46B` + 冷青 `#4FE3FF`。
- **版式**：L1 或 L2。
- **关键词**：`millions of tiny luminous particles forming a shape, partially dissolving, long exposure, dark void, cinematic`

## D8 拼贴混合（Tech Collage）
- **气质**：多元、社区、有人味。适合开源、开发者生态、多城市巡回活动。
- **背景**：浅纸色或品牌色块。
- **材质**：3D 物体 + 扁平色块 + 半调网点 + 截图式 UI 元素拼贴。
- **配色**：品牌色 + 黑 + 1 个荧光色。
- **版式**：L3 或 L4。
- **关键词**：`editorial collage, mix of 3D object and flat shapes, halftone texture, cut paper, bold composition`
- **注意**：拼贴里的 UI 截图元素由模板叠加，主图只负责 3D 和纹理部分。

---

## 选方向的规则

1. 先按 brief.md 的"活动类型 → 倾向方向"缩小到 3–4 个。
2. 给用户的 2–3 个方向之间要拉开差异：至少一深一浅，或一个具象一个抽象。
3. 品牌色是暖色的，避开冷色主导的方向，反之亦然；或者直接用品牌色重写配方配色。
4. 大屏优先深色（D1、D7）：会场灯光暗，深底更出效果。印刷海报和推文优先浅色（D2、D6）。
