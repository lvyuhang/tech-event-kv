# 主图提示词

v0.1 的提示词结构是"主体 → 材质 → 背景"，写出来的是**一个物体的说明书**，模型就画一个物体放在背景上。v0.2 改成写**一个场景的镜头描述**：先有世界，主体在世界里，光和空气把两者连起来。

提示词默认写英文。用户的模型中文优先时，用同样的结构翻成中文，材质和光线术语保留英文括注。

## 结构：7 段，按顺序写

```
[1 镜头]     shot type, camera position, lens — 先定观看方式
[2 世界]     where this is: environment, time, weather, atmosphere — 先写世界
[3 主体]     the hero, what it is made of, what it is DOING (一个动作)
[4 互动]     how the hero and the world affect each other — 至少 3 种融合手法（integration.md）
[5 光]       one key light direction + color temperature, rim light, what is the light source
[6 构图]     where the hero sits, what fills the quiet text area (写具体内容，不写 empty)
[7 质感]     render / photographic quality, film grain, color grade
--- Negative ---
```

**第 2 段必须写在第 3 段前面。** 模型对先出现的内容分配更多注意力，先写世界才能画出世界。

**第 4 段不能省。** 这是 v0.1 缺失的部分，也是"贴纸感"的直接原因。

## 各段写法要点

**[1 镜头]** 用具体镜头语言，决定了画面的戏剧性：
- `wide cinematic shot from a low angle` — 宏大、仰视，适合大会主屏
- `aerial view looking straight down` — 图案感、秩序感
- `macro close-up, 100mm lens, extremely shallow depth of field` — 微观、精致
- `eye-level shot across still water` — 安静、有倒影
- 不写 = 模型默认正面平视中景，最平庸

**[3 主体]** 写"由什么构成 + 正在做什么"：
- ✗ `a glass AI logo`
- ✓ `a giant cursor shape, formed by tens of thousands of fireflies still gathering, the lower half dense and bright, the upper half loose drifting points`

**[6 构图]** 从下表抄版式对应的句子，然后把"安静区"改写成具体内容：

| 排版系统/版式 | 16:9 | 9:16 |
|---|---|---|
| 左文右图 | `the hero occupies the right 60% of the frame and bleeds off the right edge; the left 40% is [具体内容: open night sky with faint haze]` | `the hero fills the lower 60% and bleeds off the bottom; the upper 40% is [具体内容]` |
| 居中 | `the hero is centered and large, about 55% of the frame; the bottom fifth is [具体内容: dark still water]` | `the hero centered slightly above middle; the bottom third is [具体内容]` |
| 巨字穿插（bleed） | `the hero stands in the middle third, tall, with clear separation from the background so it can be cut out; the area behind it is [具体内容]` | 同左 |
| 右信息栏 | `the hero sits in the lower-left, within the left 65% of the frame; the top quarter and right third are [具体内容]` | 同左文右图 |

**信息区也要安静**：底部（或放日期地点的位置）同样写成"安静的水面 / 地面 / 天空"，否则信息会压在高亮元素上。竖版尤其注意：写明 `the bottom eighth is calm dark [water/ground] with only a few sparse [elements]`。

**[7 质感]** 选一组，不要全堆：
- 3D 渲染感：`cinematic 3D render, physically based materials, subtle film grain, high dynamic range`
- 摄影感：`shot on 35mm film, natural grain, slight halation around highlights`
- 插画感（D8 拼贴等）：`editorial illustration, risograph texture`

## 负面提示（每条都带）

```
text, letters, words, typography, watermark, logo, signature, UI, frame, border,
isolated object, plain background, sticker, cutout, flat lighting, hard edges against background,
binary code rain, glowing brain, robot, robot hand, earth globe, circuit board texture, hologram UI,
cluttered, too many objects, oversaturated, cheap 3D, plastic look
```

主体本身是字形（≤ 6 个拉丁字符）时，把 `text, letters` 替换为 `extra letters, misspelled, random characters, small text`，并在主体段写清拼写：`the letters "AI" spelled exactly A-I`。生成后逐字母核对。

## 完整示例

**方向：萤火（涌现）· 16:9 · 左文右图**
```
[1] Wide cinematic shot from a low angle, 24mm lens, deep night.
[2] A vast wetland on an early summer night, still black water, tall reeds at the edges, thin low mist over the water, a faint cold blue afterglow on the distant horizon.
[3] Above the water, tens of thousands of fireflies are gathering into the shape of a giant text cursor — a tall vertical bar — the lower half already dense and glowing, the upper half still loose, drifting points of light.
[4] The fireflies' warm green light spills onto the mist and the tips of the reeds; the whole form is mirrored in the still water below; stray fireflies drift toward the camera as soft out-of-focus bokeh in the foreground; the top of the form dissolves into the night sky.
[5] The fireflies are the main light source, warm yellow-green; a cool blue ambient fill from the horizon; no other lights.
[6] The cursor stands in the right 60% of the frame and its reflection reaches the bottom edge; the left 40% is open night sky above a calm stretch of dark water with only faint haze.
[7] Cinematic photograph-like 3D render, long exposure feel, subtle film grain, high dynamic range, deep blacks.
Negative: text, letters, words, watermark, logo, UI, isolated object, plain background, sticker, glowing brain, robot, earth globe, circuit board, cluttered, oversaturated, cheap 3D
```

**方向：珊瑚括号（置换）· 16:9 · 巨字穿插**
```
[1] Eye-level shot, 50mm lens, underwater, crystal clear.
[2] A sunlit shallow sea floor of pale sand, shafts of light coming down through the water surface, tiny suspended particles in the water, the far distance fading to turquoise.
[3] A pair of giant curly braces { } growing out of the sand, built from living coral in soft coral pink, orange and violet, small fish swimming between their branches.
[4] Rippling caustic light from the surface plays over the coral and the sand; soft blue shadows pool under the braces; the coral's colours tint the surrounding water; sand and small coral fragments in the foreground are out of focus.
[5] Sunlight from directly above, filtered by water, warm highlights, cool turquoise ambient.
[6] The braces stand in the middle third of the frame, tall, clearly separated from the background; on both sides the frame shows open turquoise water with light shafts.
[7] Cinematic underwater photograph, natural grain, rich but natural colour.
Negative: text, letters, watermark, logo, isolated object, plain background, sticker, scuba diver, cluttered, oversaturated, plastic look
```

## 每个方向出几张

- 每个画幅（16:9 / 9:16）单独一条提示词，构图句不同
- 每条至少生成 4 张，从中挑 1 张。挑选标准：主体可读 > 融合质量 > 留白区干净 > 细节
- 4 张都不行，先改提示词再重生，不要硬选

## 运营招募 / 校园类（3D 潮玩）提示词

7 段式适合场景型主图。3D 潮玩 KV 是"物件环绕标题"的版面，改用**分区命名**的结构（对 gpt-image-2 这类擅长排版和文字的模型效果更好）：

```
type          画幅 + 类型（16:9 横版活动主视觉）
centerpiece   主角和动作，写清在画面哪个垂直区间（如 8%–36%）；"连接"的动作写成具体手势
left_cluster  左侧物件，从上到下；标明哪些在前景、失焦、出画
right_cluster 右侧物件
composition   整体形状（开口向下的弧形）、最大物件比例、视觉重心
style         材质（玻璃 / 亚克力 / 软胶 / 毛绒 / 金属）、渲染（C4D + Octane）、景深与运动模糊
background    渐变天空色值、棋盘格、像素碎片
palette       主色 + 点缀色的色值
tech_details  每个技术元素写成物件上的具体文字（引号里逐字）
safe_area     合影遮挡区、logo 区
text_elements 含字版：每行文字用引号逐字给出，标明语言 zh、大小层级、字形描述；无字版：写 text_area 保持干净
avoid         反面清单
```

- 文字用引号逐字给出，并写明 `语言：zh`、"逐字准确，不要增删任何字"。
- **每个方向出含字版和无字版**。含字版先当风格板，让用户在真实出图里选方向；选定后用无字版出主图，标题再排版。
- 不让模型画 logo，只留出位置。
- 示例：`examples/tju-cann/v3/prompts_image2.md`。

## 适配不同模型

| 情况 | 调整 |
|---|---|
| 模型支持画幅参数 | 用参数指定，构图句照写 |
| 模型只出正方形 | 生成 2048×2048 用"居中"句式，延展时靠 `focal` 裁切；交付说明里标注 |
| 模型支持参考图 | 把用户给的参考 KV 作为风格参考，并删掉第 7 段，避免冲突 |
| 模型不支持负面提示 | 省略负面，在第 7 段末尾加 `clean composition, no text` |
| 模型倾向画得太满（常见于对话型模型自带的生图） | 第 6 段放到第 2 段之后，并加一句 `restrained, only one subject` |
| 主体边缘需要干净以便抠图 | 第 4 段的"边缘消融"改用"倒影"和"光溢出"，避免主体与背景同色 |

适配器调用方式见 `scripts/image_model.py`。
