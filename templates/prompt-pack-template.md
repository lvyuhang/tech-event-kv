# 视觉提示词包：<活动名> · <方向名>

> 和 brief 配套。四种用法：整图含字版（最快看效果）→ 整图无字版（标题后期排版）→ 分素材版（追求完成度、降低 AI 感）→ 局部修改。

## 0. 共用段（每条都粘贴）
```
style:
palette:
lighting:
camera:
avoid:
```

## 1. 整图 · 含字版（16:9）
```
type:
skeleton:
title:
elements:
background:
bottom_band:
text: 只出现引号里的文字，语言 zh，逐字准确，不要增删任何字
```

## 2. 整图 · 无字版
在第 1 条基础上：删 title 段；skeleton 末尾加"标题区保持干净"；text 只保留元素上的字。

## 3. 分素材版（每个素材单独生成，纯白底，主视觉作风格参考）
| # | 素材 | 画幅 | 提示词 |
|---|---|---|---|

## 4. 局部修改模板
```
Replace/Add <区域里的东西> with <新内容>. Keep everything else unchanged. Same lighting and depth of field.
```

## 5. 挑图标准
1.
2.

## 6. 出图问题 → 补充句
| 问题 | 补充句 |
|---|---|
