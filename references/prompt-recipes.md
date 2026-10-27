# 主图提示词

提示词默认写英文（大多数生图模型对英文的材质和光线词理解更稳）。如果用户的模型是中文优先的，就把同样的 6 段结构翻成中文，材质术语保留英文括注。

## 6 段结构

```
[1 主体]   what the hero object is, its shape and scale
[2 材质]   material, surface, how light passes through it
[3 构图]   where the subject sits + where the empty space is (from the layout)
[4 背景]   background color and gradient, atmosphere
[5 光线镜头] lighting setup, camera angle, depth of field
[6 画质]   render quality keywords
--- negative ---
```

写的时候每段一句话，用逗号连接。主体段落最重要，写具体：不写 "a tech shape"，写 "a giant 3D letter G made of a single continuous glass tube"。

## 构图段：版式 → 留白写法

这是排版能不能放下文字的关键。按选定的版式，从下表抄对应的构图句：

| 版式 | 16:9 构图句 | 9:16 构图句 |
|---|---|---|
| L1 左文右图 | `subject placed on the right two-thirds of the frame, partly bleeding off the right edge, the left third is calm empty background for text` | `subject in the lower 60% of the frame, partly bleeding off the bottom, the top 40% is calm empty background for text` |
| L2 居中 | `subject centered, occupying about 50% of the frame, generous even negative space around it, a calm empty band across the bottom fifth` | `subject centered slightly above middle, calm empty band across the bottom third` |
| L3 右信息栏 | `subject in the lower-left area, within the left 65% and the bottom 70% of the frame, the top quarter and the right third are clean empty background` | 同 L1 的 9:16 |
| L4 满版文字 | `abstract texture filling the frame evenly, low contrast, no focal object, suitable as a background behind large text` | 同左 |

**每个画幅单独写一条提示词**，构图句不同。主屏是 16:9，海报是 9:16，正方形用 L2 句式。

## 负面提示（每条都带）

```
text, letters, words, typography, watermark, logo, signature, caption, UI, frame, border,
binary code rain, glowing brain, robot hand, earth globe, circuit board texture,
cluttered, busy background, low contrast, oversaturated, cartoon, flat illustration (除非方向要求),
people, faces (除非 brief 要求)
```

D4 巨构字形这类主体就是字的方向，从负面提示里去掉 `text, letters`，改成 `extra letters, misspelled, random characters, small text`。

## 字形主体的写法

当主体是字母或数字时，模型容易拼错。要这样写：

- 拼写明确："the word "DEV" spelled exactly D-E-V, three letters"
- 字符 ≤ 6 个，越短越稳；长词拆成单个字母描述或只取首字母
- 描述字体形态："bold rounded sans-serif", "flowing cursive script"
- 生成后**一定要检查拼写**，拼错就重生成，不要交付

## 示例

**D1 暗场流光 + 缩写 "AI"，L1，16:9**
```
A giant 3D sculpture of the letters "AI" spelled exactly A-I, formed by one continuous thick glass tube in a flowing cursive script, |
iridescent liquid glass with orange, magenta, cyan and lime glow running inside, subtle bloom, |
subject placed on the right two-thirds of the frame, partly bleeding off the right edge, the left third is calm empty background for text, |
deep violet-black radial gradient background with a soft purple haze in the lower left, |
low camera angle, shallow depth of field, foreground part of the tube softly out of focus, |
cinematic 3D render, octane, high detail, 8k
Negative: extra letters, misspelled, random characters, small text, watermark, logo, binary code rain, globe, people, cluttered
```

**D2 白底光谱玻璃 + 花括号 `{ }`，L3，16:9**
```
A pair of giant curly braces "{ }" sculpted from layered translucent colored acrylic slabs in blue, violet, pink and amber, slightly rotated in 3D space, |
glass refraction, chromatic dispersion at the edges, soft caustic shadows, |
subject in the lower-left area, within the left 65% and the bottom 70% of the frame, the top quarter and the right third are clean empty background, |
pure white seamless studio background, |
soft top light, 35mm lens, slight perspective, crisp focus, |
high-end product render, clean, high detail
Negative: text, letters, watermark, logo, UI, cluttered, dark background, people
```

## 适配不同模型

| 情况 | 调整 |
|---|---|
| 模型支持画幅参数 | 用参数指定（如 `--ar 16:9`），构图句照写 |
| 模型只出正方形 | 生成 2048×2048，构图句改用 L2 居中，延展时靠 `focal` 裁切；在交付说明里标注 |
| 模型支持参考图 / 风格参考 | 把用户给的参考 KV 作为风格参考传入，提示词里去掉配色段，避免冲突 |
| 模型支持负面提示字段 | 负面单独传；不支持就省略，正向里加 "clean, minimal, no text" |

适配器的具体调用方式见 `scripts/image_model.py`。
