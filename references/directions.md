# 风格方向库（视觉语言）

**风格方向不是概念。** 概念（concept.md）决定画什么、说什么；风格方向决定用什么视觉语言去画。先有概念，再从这里挑一个与之匹配的风格。

每个方向给出：适用场景、世界（环境）、材质、配色、配套排版系统（typography.md）、提示词片段。提示词片段只是素材，要按 prompt-recipes.md 的 7 段结构组织。

---

## D1 暗场流光 · Dark Glow
- **适合**：主会场大屏、年度大会、AI 主题。会场灯光暗，深底效果最好。
- **世界**：深夜、深空、深水、暗房；空气里有微弱的雾或光尘，不是纯黑。
- **材质**：自发光体、彩虹流体玻璃、光丝、萤光生物。
- **配色**：底 `#07060F`–`#1B0F3A`，光取 2–3 色，不要全光谱。
- **排版**：`swiss`（细英文 + 粗中文）或 `bleed`。
- **片段**：`deep violet night atmosphere with faint haze`、`its glow spills onto the mist`、`mirrored in dark glossy water`、`soft bloom around highlights`

## D2 白底光谱玻璃 · Spectral Glass
- **适合**：发布会、品牌活动、印刷海报。
- **世界**：明亮的空间——晨光中的白色房间、雪地、浅色沙丘、云层之上。**不要写 studio background**，写一个明亮的场所。
- **材质**：彩色亚克力、玻璃、色散。
- **配色**：底 `#F6F7FA`；色块 4–6 个高饱和色，或品牌色系。
- **排版**：`swiss` 或 `editorial`；文字用深色。
- **片段**：`soft morning light in a white space`、`coloured caustics thrown across the pale floor`、`chromatic dispersion at the edges`、`long soft shadows`
- **融合要点**：白底最容易贴纸感，必须写 caustics（焦散）和地面投影。

## D3 流体有机 · Liquid Organic
- **适合**：AI、大模型、生态、"生长"类主张。
- **世界**：水面、黏稠液体池、雨后、晨雾。
- **材质**：液态金属、果冻、肥皂膜、生物组织感。
- **配色**：浅版奶油底 + 珊瑚/紫；深版近黑 + 镀铬。
- **排版**：`editorial` 或 `swiss`。
- **片段**：`liquid chrome rising out of a still pool, ripples spreading`、`subsurface scattering`、`the liquid surface reflects the sky`

## D4 巨构建筑 · Monumental
- **适合**：品牌发布、基础设施、安全、数据库（稳固、长期）。
- **世界**：荒漠、盐湖、雪原、峡谷、巨大的室内空间；人物剪影提供尺度。
- **材质**：混凝土、石材、拉丝金属、磨砂玻璃。
- **配色**：单色系 + 1 个点缀色。
- **排版**：`bleed`（巨字）或 `swiss`。
- **片段**：`a monumental structure on a vast salt flat`、`a tiny human silhouette for scale`、`long dramatic shadow at golden hour`

## D5 终端 · Terminal
- **适合**：黑客松、技术沙龙、开发者社区。
- **世界**：主图可以很弱——暗房里 CRT 屏幕的光、夜晚城市的窗格、雨夜玻璃。重点在排版。
- **材质**：磷光、扫描线、玻璃屏幕反光。
- **配色**：底 `#0D1117`；高亮 `#7EE787` `#79C0FF` `#FFA657`。
- **排版**：`terminal`。
- **注意**：代码内容由模板渲染，且必须真实、与活动相关。

## D6 微缩世界 · Miniature
- **适合**：黑客松、开源、游戏开发、社区活动。轻松、有玩味。
- **世界**：移轴摄影的微缩场景；符号是一座小岛、一个工地、一个游乐场，上面有很多小人在忙碌。
- **材质**：模型质感、黏土、体素、等距积木。
- **配色**：高饱和撞色 3–4 色。
- **排版**：`swiss`（粗体）或 `terminal`。
- **片段**：`tilt-shift miniature photograph`、`tiny people working on it`、`soft afternoon light`

## D7 光场粒子 · Particle Field
- **适合**：AI、数据、云计算。"涌现""汇聚"类主张的最佳载体。
- **世界**：夜空、深海、风中——粒子要有来源（萤火虫、雪、发光浮游生物、尘埃），不要抽象的"数据点"。
- **材质**：自发光微粒，局部聚合、局部散开。
- **配色**：底近黑；粒子 1–2 色相。避开"蓝白光点"老套搭配。
- **排版**：`swiss` 或 `bleed`。

## D8 拼贴 · Collage
- **适合**：开源、开发者生态、多城巡回。
- **世界**：纸面、桌面、展墙。
- **材质**：3D 物体 + 扁平色块 + 半调网点 + 剪纸。
- **配色**：品牌色 + 黑 + 1 个荧光色。
- **排版**：`editorial` 或 `terminal`。

---

## 选择规则

1. 先选概念，再选风格。同一个概念在 D1 和 D2 下应该是两种完全不同的气质。
2. 给用户的 3 个方向之间要拉开：至少一深一浅；至少一个 L3 概念。
3. 品牌色优先：品牌色是暖色时避开冷色主导的方向，或者用品牌色重写配色。
4. 主屏优先深色（D1、D4、D7）；印刷和推文优先浅色（D2、D3 浅版、D6）。
