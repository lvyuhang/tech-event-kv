# 方向 A · 材质与风格描述

## 一、从你认可的那个元素里拆出来的材质

| 部位 | 看到的 | 描述词（中文 + 英文关键词，image-2 对英文材质词更敏感） |
|---|---|---|
| 外壳 | 厚实、圆角很大的银色金属，边缘有一圈很亮的高光，表面能映出周围的蓝色 | 镜面抛光铝 / 铬，厚倒角，柔和的环境反射（polished chrome aluminum, thick rounded bevel, soft studio reflections, crisp specular edge highlight） |
| 屏幕 | 黑色，像素字是白色、微微发光，上面盖着一层玻璃，有一道斜向反光 | 深色光面液晶屏 + 玻璃盖板，像素等宽字自发光（glossy black LCD under glass, white pixel monospace text with soft glow, diagonal glass reflection） |
| 键帽 | 半透明、像果冻，亮蓝到薄荷绿渐变，内部有光，字母是白色 | 果冻感半透明亚克力，次表面散射，内发光，顶面微磨砂，边缘圆润（translucent jelly acrylic keycaps, subsurface scattering, inner glow, slightly frosted top, rounded edges, white legends） |
| 灯条 | 侧面一条青色发光条 | 青色自发光灯条（cyan emissive LED strip） |
| 线缆 | 黑色、哑光，金属接头 | 哑光黑色橡胶线 + 镜面金属接头（matte black rubber cable, chrome connector） |
| 背景小方块 | 冰块一样的透明立方体，带一点蓝 | 冰块感磨砂玻璃小立方体，带蓝色色散（frosted ice-glass cubes, light blue tint, soft refraction） |
| 背景光带 | 一条半透明、带彩虹光泽的环形带 | 全息薄膜光泽的半透明丝带（translucent holographic ribbon, iridescent thin-film sheen） |
| 光 | 柔光棚，白色和淡蓝的反射，阴影很浅 | 摄影棚柔光箱照明，高调，浅蓝环境光，柔和接触阴影（studio softbox lighting, high-key, pale blue ambient, soft contact shadows） |

## 二、材质库（M1–M14）

写提示词时，**每个部位都指定一个材质编号**，一个物体最多用 3–4 种。

| 编号 | 材质 | 提示词写法 |
|---|---|---|
| M1 | 镜面铬 | 镜面抛光铬，强烈清晰的高光，映出浅蓝环境（mirror-polished chrome, sharp specular highlights, reflecting pale blue surroundings） |
| M2 | 拉丝铝 | 细拉丝铝，柔和的各向异性高光，银灰色（fine brushed aluminum, soft anisotropic highlights, silver-grey） |
| M3 | 果冻亚克力 | 半透明果冻亚克力，次表面散射，内部发光，亮蓝 → 薄荷绿渐变（translucent jelly acrylic, subsurface scattering, inner glow, blue-to-mint gradient） |
| M4 | 磨砂玻璃 | 磨砂玻璃，柔和折射，边缘更透明，带淡蓝色调（frosted glass, soft refraction, clearer edges, pale blue tint） |
| M5 | 光面软胶 | 光面软胶 / 搪胶，饱满圆润，像潮玩手办（glossy soft vinyl, plump rounded forms, designer toy finish） |
| M6 | 哑光软胶 | 哑光软胶，细腻的颗粒感，柔和漫反射（matte soft-touch silicone, fine texture, soft diffuse） |
| M7 | 黑色液晶屏 | 深色光面液晶屏，玻璃盖板，一道斜向反光；像素字白色或薄荷绿，自发光（glossy black LCD, glass cover, diagonal reflection, glowing pixel monospace text） |
| M8 | 七段数码屏 | 深色屏幕上的薄荷绿七段数码字，微微发光（mint seven-segment display digits, soft glow） |
| M9 | 发光灯条 | 青色 / 薄荷绿自发光灯条（cyan emissive LED strip） |
| M10 | 透明塑料 | 清透的硬塑料，干净的折射和高光（clear plastic, clean refraction and highlights） |
| M11 | 全息薄膜 | 全息彩虹薄膜光泽，蓝紫粉色调（holographic iridescent thin-film, blue-violet-pink sheen） |
| M12 | 釉面陶瓷 | 光滑釉面陶瓷，柔和的高光（smooth glazed ceramic, soft highlights） |
| M13 | 纸张 / 便利贴 | 微哑光的纸，细微纤维纹理，边角微卷（slightly matte paper, subtle fiber texture, gently curled corners） |
| M14 | 哑光橡胶 | 哑光黑色橡胶（matte black rubber） |

**配色固定**：亮蓝 #2F6BFF、薄荷绿 #4FDDAA、淡紫 #B9A8FF、暖黄 #FFD45C、银、白，少量海棠粉 #FFB7C9。

## 三、共用风格段（替换之前的版本）

```
style: 高端 3D 产品级潮玩渲染，C4D + Octane / Redshift，物理正确的材质，细节精致，像大厂校招 KV 里的主视觉物件。
  造型：厚实、圆润、倒角大、比例略可爱，像一件精致的桌面玩具。
  材质：以镜面铬 / 拉丝铝外壳 + 半透明果冻亚克力按键 + 深色玻璃屏幕为主，少量光面软胶；
    每种材质的高光、反射、透光都清楚可辨。
  配色：亮蓝 #2F6BFF、薄荷绿 #4FDDAA、淡紫 #B9A8FF、暖黄 #FFD45C、银、白。
lighting: 摄影棚柔光箱照明（studio softbox），高调，主光来自左上方 45°，右后方淡蓝色轮廓光，
  金属上有清晰的长条形高光，亚克力内部透出柔光；阴影浅而柔，不要泛光、光晕、雾、镜头光斑。
camera: 略微俯视约 15°，50mm，物体完整，略微倾斜 10–15°，四周留白。
background: 纯白 #FFFFFF，物体孤立，没有地面、投影和其他物体（方便抠图）。
quality: 8K 细节，干净锐利，边缘清晰；除指定文字外没有任何文字和 logo。
```

---

## 四、每个元素的材质分配（直接替换 assets_more.md 里的 subject 段）

**hello, CANN 设备（已有，作为基准）**
外壳 M1 · 屏幕 M7 "> hello, CANN_" · 键帽 M3 "C" "A" "N" "N" · 侧面灯条 M9 · 线缆 M14 + M1 接头

**★1 扭蛋机**
```
subject: 一台小巧的复古扭蛋机。底座：镜面抛光铬外壳（M1），厚倒角；正面一个亮蓝色果冻亚克力大旋钮（M3），出蛋口内侧是哑光黑色橡胶（M14）。
  球仓：清透的透明塑料圆罩（M10），顶部一圈拉丝铝盖（M2）。
  扭蛋：上下两半，上半是透明塑料（M10），下半是光面软胶（M5），颜色亮蓝、薄荷绿、淡紫、暖黄；每颗印白色短词 "add" "matmul" "softmax" "conv"。
  出蛋口刚滚出一颗薄荷绿扭蛋 "add"，内部微微发光。
```

**★2 复古电子闹钟**
```
subject: 一个圆角方形的复古电子闹钟。外壳：亮蓝色光面软胶（M5）；顶部两个镜面铬铃铛（M1）和一根拉丝铝敲杆（M2）。
  正面：深色光面屏（M7），薄荷绿七段数码字 "11:08"（M8）；侧面一颗薄荷绿果冻亚克力按键（M3）；底部四个哑光橡胶小脚（M14）。
```

**★3 奶茶杯**
```
subject: 一杯外带奶茶。杯身：清透的透明塑料（M10），杯壁有细小的冷凝水珠；奶茶液体是半透明的淡薄荷绿，带柔和的光线透射。
  "珍珠"：杯底一颗颗半透明果冻亚克力小立方体（M3），亮蓝、淡紫、薄荷绿，彼此透光。
  杯盖：透明圆顶盖（M10）；吸管：粗的光面软胶吸管（M5），暖黄色。杯身贴一枚绿色光面贴纸 "Merged ✓"（M5，边缘微翘）。
```

**★4 掌上游戏机**
```
subject: 一台竖版复古掌上游戏机。外壳：亮蓝色光面软胶（M5），边缘一圈拉丝铝饰条（M2）。
  屏幕：深色光面屏 + 玻璃盖板（M7），像素字顶部 "LEVEL 1"、中间 "第一个算子"，下面一条薄荷绿像素进度条，满了一半。
  十字键：镜面铬（M1）；两颗圆形按键：果冻亚克力（M3），薄荷绿和淡紫；底部两条哑光软胶扬声器槽（M6）。
```

**5 拍立得相机**
```
subject: 一台圆润的拍立得相机。机身上半白色哑光软胶（M6）、下半亮蓝色光面软胶（M5）；镜头：镜面铬圈（M1）+ 磨砂玻璃镜片（M4），镜片里有淡淡的全息反光（M11）。
  出片口吐出一张照片：白色纸边（M13），照片画面是一枚绿色胶囊 "PR #1 Merged ✓" 和几颗小星星。
```

**6 科学计算器**
```
subject: 一台圆角科学计算器。边框：拉丝铝（M2），倒角处镜面高光；面板：亮蓝色光面软胶（M5）。
  顶部：深色光面屏（M7）显示 "z = x + y"。按键：果冻亚克力（M3），其中三颗大键印 "add" "mul" "exp"，其余数字键是白色哑光软胶（M6）。
```

**7 刷卡签到机**
```
subject: 一台小巧的刷卡签到机。外壳：镜面铬（M1），正面一块深色光面屏（M7）显示薄荷绿像素字 "Welcome, Dev #0001 ✓"。
  感应区：磨砂玻璃圆形面板（M4），发出一圈薄荷绿光环（M9）。一张亮蓝色光面软胶成员卡（M5）正贴在感应区上，卡面印白字 "CANN Club"。
```

**8 游戏手柄**
```
subject: 一个圆润的游戏手柄。外壳：白色光面软胶（M5）；摇杆：镜面铬（M1）顶部配哑光软胶帽（M6）；
  右侧四颗按键：果冻亚克力（M3），分别是亮蓝 "+"、薄荷绿 "−"、淡紫 "×"、暖黄 "÷"，按键内部发光。
```

**9 魔方**
```
subject: 一个圆角魔方，正在被转动到一半。每个小方块是磨砂玻璃（M4）包裹果冻亚克力芯（M3），彼此透光；
  朝前一面是亮蓝、薄荷绿、淡紫交错的 3×3，其他面是白色和浅灰；转轴缝隙里露出一点镜面铬（M1）。
```

**10 头戴耳机**
```
subject: 一副头戴式耳机。头梁：镜面铬（M1）+ 白色哑光软胶内衬（M6）；耳垫：白色哑光软胶（M6）；
  两个耳罩外侧：两颗大号果冻亚克力键帽（M3），分别印 "add"（亮蓝）和 "mul"（薄荷绿），内部发光。
```

**11 U 盘**
```
subject: 一个 U 盘。外壳：清透的透明塑料（M10），能看到里面发蓝光的小芯片和细密电路；接口：镜面铬（M1）；
  挂绳：哑光橡胶（M14），挂着一块小小的拉丝铝吊牌（M2），刻着 "my_first_op"。
```

**12 盖章**
```
subject: 一个圆润的印章。握柄：亮蓝色光面软胶（M5），顶部一颗薄荷绿果冻亚克力球（M3）；底座：拉丝铝（M2）。
  旁边纸面（M13）上留下一个薄荷绿方形印记 "+1"，边缘有真实的印泥颗粒感。
```

**13 一摞课本**
```
subject: 三本叠起来的精装课本。封面是光面软胶质感（M5），分别亮蓝、淡紫、白色，书脊烫银字（M1）《线性代数》《C++ 程序设计》《深度学习》；
  书页是微哑光纸（M13）。最上面一本里夹着一颗薄荷绿果冻亚克力键帽 "add"（M3）当书签。
```

**14 便利贴**
```
subject: 一叠方形便利贴，微哑光纸（M13），暖黄色，最上面一张边角翘起，用亮蓝马克笔手写 "TODO: 第一个算子"，后面一个薄荷绿勾。
  便利贴底下压着一支镜面铬笔夹的圆珠笔（M1）。
```

**NPU 小芯片**
```
subject: 一块方形小芯片。主体：磨砂玻璃（M4），内部细密电路纹和发蓝光的核心；四周针脚：镜面铬（M1）；
  表面一张简单的脸（两只圆眼睛 + 微笑），用薄荷绿自发光像素画出（M9）；上方印 "NPU"。
```

**海棠花枝（前景）**
```
subject: 一枝海棠花。花瓣：光面软胶（M5），粉白渐变，边缘微透光；花心：暖黄色哑光软胶（M6）；叶子：嫩绿光面软胶（M5）；枝干：浅棕哑光软胶（M6）。
```

**背景点缀（合成时用）**
```
subject: 一组大小不一的冰块感磨砂玻璃小立方体（M4），带淡蓝色调和柔和折射；以及一条半透明、带全息彩虹光泽的环形丝带（M11）。
```

---

## 五、常见问题的改法

| 出图问题 | 加这句 |
|---|---|
| 金属发灰、像塑料 | `mirror-polished chrome with crisp long specular highlights and strong reflections` |
| 亚克力不透、像实心塑料 | `highly translucent jelly acrylic, visible inner glow and light passing through` |
| 整体发雾、对比低 | `crisp, high clarity, no haze, no bloom, defined shadows` |
| 太写实、不像玩具 | `designer toy proportions, chunky rounded forms, simplified details` |
| 屏幕字模糊 | `sharp pixel-perfect monospace text on the screen, high contrast` |
