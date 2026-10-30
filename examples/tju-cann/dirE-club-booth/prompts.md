# 视觉提示词包：天大 CANN ·「招新摊位」方向

> 配套 `brief.md`。整图含字版 → 整图无字版 → 分素材版 → 局部修改。

## 0. 共用段

```
style: 3D 潮玩微缩场景（designer toy diorama），C4D + Octane，物理正确的材质，精致、圆润、像潮玩展示台上的一组手办和道具。
  材质：光面软胶（glossy soft vinyl）、哑光软胶（matte soft-touch）、镜面铬（mirror-polished chrome）、
  半透明果冻亚克力（translucent jelly acrylic, inner glow）、透明塑料（clear plastic）。
palette: 亮蓝 #2F6BFF 为主，薄荷绿 #4FDDAA、淡紫 #B9A8FF、暖黄 #FFD45C、海棠粉 #FFB7C9 点缀，白、黑收住。
lighting: 摄影棚柔光箱，高调，主光左上 45°，淡蓝轮廓光，柔和接触阴影；不要泛光、光晕、雾、镜头光斑。
camera: 正面略俯视约 12°，50mm，摊位完整居中。
avoid: 人物、写实照片、写实建筑和校园、深色背景、电路板纹理、彩虹渐变材质、真实品牌 logo、杂乱的小字、乱码、儿童元素。
```

## 1. 整图 · 含字版（16:9）

```
type: 16:9 横版活动主视觉，3D 潮玩微缩的大学社团招新摊位，明亮、热闹、精致。

skeleton: 画面中央一个小巧的招新摊位，约占画面高度 70%，完整可见：
  上方一顶亮蓝白相间的条纹遮阳棚，边缘是波浪形的软胶花边，由四根镜面铬细支架撑起；
  遮阳棚上沿挂一条白色大横幅；横幅上方正中一块小牌子；
  下面一张浅木色软胶桌子，桌子正面垂下一块薄荷绿桌布；
  摊位放在一块浅色圆形展示台上；左右两侧是干净的纯色背景。

title: 小牌子上黑色粗体 "天津大学"；
  横幅上超大超粗圆润的亮蓝色字 "CANN 开发者俱乐部"（全画面最大的字）；
  横幅下方一条暖黄色小飘带，深色字 "成立仪式暨校园宣讲会"；
  薄荷绿桌布上深色超粗大字 "从第一个算子，到第一份贡献"。

table_items（桌面上，只有这 5 件，彼此留空隙）:
  左：一个圆角镜面铬小设备，黑色小屏显示 "> hello, CANN_"，下面四颗果冻亚克力键帽 "C" "A" "N" "N"（亮蓝到薄荷绿）；
  中：一叠白色报名表和一支亮蓝色笔，最上面一张写 "成员 No.0001"；
  中右：一个透明的扭蛋罐，里面是彩色小扭蛋，每颗印一个短词 "add" "matmul" "softmax"；
  右：一个小白陶盆，种着一小枝粉白色海棠花；
  桌角：一小摞贴纸，最上面三张是绿色 "Merged ✓"、薄荷绿圆形 "+1"、淡紫色芯片笑脸。

mascot: 摊位右侧站着一个可爱的 NPU 小芯片角色（透明磨砂玻璃方块身体，两只圆眼睛和微笑，四周镜面铬针脚，短短的软胶手脚），
  双手举着一块小牌子 "招新中"。

atmosphere: 几片海棠花瓣和两三颗软胶星星（暖黄、薄荷绿）轻轻飘在摊位周围；不加其他东西。

background: 纯色渐变，上方淡蓝 #DCE6FF 到下方淡紫 #F4EFFF，没有任何环境；展示台下有柔和投影。

text: 只出现以上引号里的文字，语言 zh，逐字准确，不要增删任何字；不要其他文字和 logo。
（接共用段）
```

## 2. 整图 · 无字版
在第 1 条基础上：
- 删掉 `title` 段；在 `skeleton` 里写"横幅、小牌子、飘带和桌布上都是空白的，不印任何字"
- `text` 改成：只出现 "> hello, CANN_" "C" "A" "N" "N" "成员 No.0001" "add" "matmul" "softmax" "Merged ✓" "+1" "招新中"

横幅和桌布的字在排版里贴上去（按透视变形），字形最可控。

## 3. 分素材版（纯白底、无投影；先生成 S1，之后都以 S1 作风格参考）

在共用段后加：`background: 纯白 #FFFFFF，物体孤立，没有地面、投影和其他物体。`

| # | 素材 | 画幅 | 提示词（subject） |
|---|---|---|---|
| S1 | 空摊位 | 16:9 | 小巧的招新摊位：亮蓝白条纹遮阳棚（波浪软胶花边）、四根镜面铬支架、空白白色横幅、上方空白小牌子、浅木色软胶桌子、空白薄荷绿桌布，桌面上什么都没有，放在浅色圆形展示台上。 |
| S2 | hello, CANN 设备 | 1:1 | （你已有这张，可直接用） |
| S3 | 报名表 | 1:1 | 一叠白色报名表，纸张微哑光、边角微卷，最上面一张印 "成员 No.0001" 和几条横线，旁边斜放一支亮蓝色光面软胶笔。 |
| S4 | 扭蛋罐 | 1:1 | 一个透明塑料扭蛋罐，镜面铬盖子，里面装满彩色小扭蛋（上半透明、下半亮蓝 / 薄荷绿 / 淡紫 / 暖黄软胶），扭蛋上印 "add" "matmul" "softmax"。 |
| S5 | 海棠盆栽 | 1:1 | 一个白色釉面小陶盆，种着一小枝海棠，粉白色光面软胶花朵、淡黄色花心、嫩绿叶子。 |
| S6 | 贴纸堆 | 1:1 | 一小摞带白色模切边的贴纸，最上面三张：绿色胶囊 "Merged ✓"、薄荷绿圆形 "+1"、淡紫色芯片笑脸；最上面一张一角微微翘起。 |
| S7 | NPU 吉祥物 | 1:1 | 一个可爱的 NPU 小芯片角色站立：透明磨砂玻璃方块身体，内部发蓝光，两只圆眼睛和微笑，四周镜面铬针脚，短短的白色软胶手脚；双手举着一块白色小牌子 "招新中"。 |
| S8 | 氛围 | 1:1 | 六七片粉白软胶海棠花瓣和三颗软胶四角星（暖黄、薄荷绿、淡紫），分散漂浮。 |
| S9 | 背景 | 16:9 | 纯背景：上方淡蓝 #DCE6FF 到下方淡紫 #F4EFFF 的渐变，中下部一块浅色圆形展示台，没有其他物体和文字。 |

合成顺序：S9 → S1 → 桌面 S2–S6（从后往前）→ S7 放摊位右侧 → S8 → 横幅、小牌子、飘带、桌布上的字在排版里按透视贴上。

## 4. 局部修改模板
```
Replace <区域里的东西> with <新内容>. Keep everything else unchanged. Same lighting, materials and colors.
```
常用：
- 横幅字错：`Replace the text on the white banner with exactly "CANN 开发者俱乐部", bold rounded bright blue letters. Keep everything else unchanged.`
- 桌上太满：`Keep only five items on the table: the hello CANN device, the sign-up sheets, the capsule jar, the haitang pot and the sticker stack. Remove everything else.`
- 摊位不像摊位：`Make the striped awning, the banner on top and the tablecloth clearly visible, like a university club recruitment booth.`

## 5. 挑图标准
1. 远看是不是"招新摊位"
2. 横幅主标题最大、逐字正确；桌布 slogan 读得清
3. 桌上只有 5 件，不乱
4. 潮玩质感，纯色背景，不写实
5. 明亮、不发雾

## 6. 出图问题 → 补充句
| 问题 | 补充句 |
|---|---|
| 摊位太写实 | `designer toy diorama, chunky rounded forms, simplified details, soft vinyl` |
| 金属发灰 | `mirror-polished chrome with crisp specular highlights` |
| 发雾 | `crisp, high clarity, no haze, no bloom` |
| 桌面太乱 | `only five items on the table, generous spacing` |
| 横幅字被遮 | `the banner is fully visible and unobstructed, facing the camera` |
