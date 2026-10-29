# 视觉提示词包：天大 CANN 开发者俱乐部 ·「路牌杆」方向

> 配套 `brief.md`。四种用法：整图含字版（最快看效果）→ 整图无字版（标题后期排版）→ 分素材版（完成度最高、AI 感最低）→ 局部修改。

## 0. 共用段（每条都粘贴）

```
style: 3D 潮玩风格运营 KV，C4D + Octane 渲染，物理正确的材质，精致、圆润、像桌面玩具；
  材质：镜面抛光铬（mirror-polished chrome）、半透明果冻亚克力（translucent jelly acrylic, subsurface scattering, inner glow）、
  光面软胶（glossy soft vinyl）、磨砂玻璃（frosted glass）、黑色光面液晶屏（glossy black LCD with glowing pixel text）。
palette: 亮蓝 #2F6BFF 为主，珊瑚粉 #FF4D6D、薄荷绿 #4FDDAA、淡紫 #B9A8FF、暖黄 #FFD45C 点缀，海棠粉 #FFB7C9，白、黑收住。
lighting: 摄影棚柔光箱（studio softbox），高调，主光左上 45°，淡蓝轮廓光；保留暗部；不要泛光、光晕、雾、镜头光斑。
camera: 平视略仰，35mm，主体居中对称。
avoid: 写实城市地标、写实建筑、写实照片、真实品牌 logo、抖音 logo、红心、小马、深色背景、电路板纹理、彩虹渐变材质、杂乱的小字、乱码、儿童形象。
```

## 1. 整图 · 含字版（16:9）

```
type: 16:9 横版活动主视觉，3D 潮玩运营 KV，明亮、热闹、精致。

skeleton: 画面正中一根镜面金属路牌杆，从底部白色色带上方一直伸到画面顶部；
  杆顶是 3D 立体字 "CANN"（亮蓝果冻亚克力，白色描边，微微发光）；
  杆上错落挂着 4 张 3D 卡片（见 elements），朝向各不相同，有前后层次；
  左右两侧下部各一组潮玩模型风格的校园建筑，把画面框住；画面最下方约 14% 是一条纯白色带。

title: 主标题被路牌杆劈成左右两半，超大、超粗、圆润的定制中文字，亮蓝 #2F6BFF，白色粗描边，轻微立体厚度：
  左半 "开发者"（略低），右半 "俱乐部"（略高）；左半上方一行小的黑色粗体 "天津大学"；
  左半下方一行珊瑚粉 #FF4D6D 粗体斜排 "成立仪式暨校园宣讲会"。

elements:
  卡片①（杆左上）：带亮蓝挂绳的白色成员卡，顶部亮蓝色带，文字 "CANN 开发者俱乐部" "No.0001"，左侧一个小头像剪影；
  卡片②（杆右上，最大）：横向的淡蓝色磨砂玻璃 UI 卡片，边缘发光，卡片上大字 "从第一个算子，到第一份贡献"；
  卡片③（杆左下）：圆角镜面铬小设备，黑色小屏显示 "> hello, CANN_"，下面四颗果冻亚克力键帽 "C" "A" "N" "N"（亮蓝到薄荷绿），侧面青色灯条；
  卡片④（杆右下）：圆角粉白色牌子，上面是一个可爱的透明 NPU 小芯片角色（两只圆眼睛和微笑，四周镜面金属针脚），
    双手端着亮蓝色马克杯，杯口冒出由 "0" "1" 组成的软软的热气；牌子底部一个胶囊标签，左右两个小箭头，中间 "add"；
  漂浮标签：左上一枚绿色光面胶囊 "Merged ✓"；右侧一个薄荷绿小方块 "+1"。
  校园（潮玩模型，圆润简化，像桌面摆件）：左侧红砖教学楼（带钟楼）+ 两棵粉白海棠树；右侧白色和玻璃的现代实验楼 + 一棵海棠树；
    几片海棠花瓣飘向中间。

background: 天空上方淡蓝 #A9CBFF，下方渐变到粉色 #FFD0DE，有柔软的云。

bottom_band: 底部白色色带：左边留空（放 logo）；右边一个搜索框样式的信息条——左格黑底白字 "11 月 8 日"，
  右格白底黑字 "天津大学 XXX"，黑色细外框，最右一个放大镜图标。

text: 只出现以上引号里的文字，语言 zh，逐字准确，不要增删任何字；不要其他文字和 logo。
（接共用段）
```

## 2. 整图 · 无字版

在第 1 条基础上：
- 删掉 `title` 段
- `skeleton` 末尾加："杆子左右两侧、画面垂直 30%–60% 的区域保持干净的天空，留给标题排版"
- `text` 改成：只出现 "CANN" "CANN 开发者俱乐部" "No.0001" "从第一个算子，到第一份贡献" "> hello, CANN_" "C" "A" "N" "N" "0" "1" "add" "Merged ✓" "+1" "11 月 8 日" "天津大学 XXX"

## 3. 分素材版（每个单独生成；纯白底、无投影；先生成 S1，之后每个都把 S1 作为风格参考）

在共用段后加：`background: 纯白 #FFFFFF，物体孤立，没有地面、投影和其他物体。camera: 略微俯视约 15°，物体完整、略微倾斜 10°。`

| # | 素材 | 画幅 | 提示词（subject） |
|---|---|---|---|
| S1 | 路牌杆 + 杆顶 CANN | 9:16 | 一根镜面抛光铬路牌杆，底部一个圆形金属底座；杆顶是 3D 立体字 "CANN"，亮蓝色半透明果冻亚克力，白色描边，内部微微发光；杆身上有 4 个小小的金属挂扣，空着。 |
| S2 | 成员卡 | 1:1 | 一张圆角白色光面软胶卡片，顶部亮蓝色带，上方一条亮蓝色挂绳和镜面金属扣；卡面文字 "CANN 开发者俱乐部" "No.0001"，左侧一个小头像剪影；卡片微微倾斜。 |
| S3 | slogan 卡 | 16:9 | 一张横向的圆角 UI 卡片，淡蓝色磨砂玻璃，边缘一圈柔和的蓝色发光描边；卡片左侧一个小的亮蓝圆形图标；卡面大字 "从第一个算子，到第一份贡献"，黑色粗体。 |
| S4 | hello, CANN 设备 | 1:1 | 圆角镜面铬小设备，厚倒角；黑色光面液晶屏显示白色像素字 "> hello, CANN_"；下面四颗果冻亚克力键帽 "C" "A" "N" "N"，亮蓝到薄荷绿渐变，内部发光；侧面一条青色灯条，一根哑光黑色线缆。（你已有这张，可直接用） |
| S5 | NPU 小芯片牌子 | 1:1 | 一块圆角粉白色光面软胶牌子；牌子上站着一个透明磨砂玻璃的 NPU 小芯片角色，两只圆眼睛和微笑，四周镜面金属针脚，内部发蓝光；双手端着亮蓝色光面马克杯，杯口冒出由 "0" "1" 组成的软软热气；牌子底部一个白色胶囊标签，左右两个小箭头，中间 "add"。 |
| S6 | Merged 标签 | 1:1 | 一枚绿色光面软胶胶囊徽章，白字 "Merged ✓"，边缘圆润，微微倾斜。 |
| S7 | +1 方块 | 1:1 | 一个圆角薄荷绿果冻亚克力小立方体，内部发光，正面白色 "+1"。 |
| S8 | 校园模型（左） | 1:1 | 潮玩模型风格的红砖教学楼，带一座小钟楼，圆润简化、像桌面摆件，光面软胶质感；楼前两棵开满粉白花的海棠树，树也是软胶质感；放在一块圆形草地底座上。 |
| S9 | 校园模型（右） | 1:1 | 潮玩模型风格的现代实验楼，白色墙面和大片蓝色玻璃窗，圆润简化、像桌面摆件；旁边一棵粉白海棠树；放在一块圆形草地底座上。 |
| S10 | 海棠花瓣 | 1:1 | 七八片粉白色软胶质感的海棠花瓣，大小不一，分散漂浮，边缘微透光。 |
| S11 | 背景天空 | 16:9 | 纯背景：上方淡蓝 #A9CBFF 渐变到下方粉色 #FFD0DE 的天空，有几朵柔软的 3D 云，干净，没有任何物体和文字。 |

合成时：S11 铺底 → S8 / S9 放两侧下部 → S1 居中 → S2–S5 挂到杆上 → S6、S7、S10 点缀 → 标题和底部色带在排版里做。

## 4. 局部修改模板

```
Replace <区域里的东西> with <新内容>. Keep everything else unchanged. Same lighting, materials and depth of field.
```
常用：
- 卡片字错：`Replace the text on the blue glass card with exactly "从第一个算子，到第一份贡献". Keep everything else unchanged.`
- 建筑太写实：`Make the buildings on both sides look like rounded designer-toy models made of glossy soft vinyl, simplified details. Keep everything else unchanged.`
- 杂物太多：`Remove all floating objects except the "Merged ✓" capsule, the "+1" cube and the haitang petals.`

## 5. 挑图标准
1. 标题和 slogan 读得清、逐字正确（含字版）
2. 四张卡片一眼能看出内容，不糊成一团
3. 建筑是潮玩模型，不写实
4. 没有参考品牌的任何资产
5. 明亮、不发雾，金属有清晰高光，亚克力透光

## 6. 出图问题 → 补充句
| 问题 | 补充句 |
|---|---|
| 金属发灰像塑料 | `mirror-polished chrome with crisp long specular highlights` |
| 亚克力不透 | `highly translucent jelly acrylic, visible inner glow` |
| 发雾、对比低 | `crisp, high clarity, no haze, no bloom, defined shadows` |
| 太写实 | `designer toy proportions, chunky rounded forms, simplified details` |
| 屏幕字模糊 | `sharp pixel-perfect monospace text on the screen` |
| 卡片太多太乱 | `only four cards on the pole, generous spacing between them` |
