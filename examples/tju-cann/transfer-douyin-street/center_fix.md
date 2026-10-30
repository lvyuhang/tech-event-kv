# 中间区域修改：让"路牌"一眼可认、元素变简单

## 问题在哪
参考图的路牌一眼可认，是因为：
- 杆子粗、从底到顶**完整可见**，杆顶有一个简单的装饰
- 挂的是**真正的路牌形状**：长方形路名牌（"W NANJING Rd."）、箭头形指向牌
- 只有 4 块，彼此留着空隙，杆子从缝里露出来

我们这张把"牌子"换成了成员卡、金属设备、角色立牌、玻璃 UI 卡，**内容对了，形状丢了**：四个物件挤在一起把杆子挡住，杆顶的 CANN 立体字又太大，看起来像一堆物件，而不是一根路牌。

## 改法：内容写在"牌子"上，不再挂物件
| 位置 | 改成 | 说明 |
|---|---|---|
| 杆顶 | 一个薄荷绿小圆球装饰，印 "+" | 替代巨大的 CANN 立体字，杆子的轮廓出来 |
| 顶部路名牌 | 经典长方形蓝色搪瓷路名牌，白边，白字 **"CANN Rd."** | 路牌最有辨识度的形状；CANN 仍在最高处 |
| 指向牌 ↗ | 亮蓝箭头牌，向右上指：**"到第一份贡献"** | slogan 后半句，指向目的地 |
| 指向牌 ↙ | 薄荷绿箭头牌，向左指：**"从第一个算子"** | slogan 前半句，起点 |
| 角色 | NPU 小芯片坐在上面那块箭头牌的顶上，端着冒 "0 1" 热气的杯子，腿垂下来 | 保留亲和力，但不再占一整块牌子 |
| 小屏设备 | "> hello, CANN_" 设备缩小，挂在下面那块箭头牌下方 | 你认可的元素保留，作为挂件 |
| Merged | 绿色胶囊 "Merged ✓" 挂在 "到第一份贡献" 箭头的尖端旁 | 目的地 |
| 删掉 | 成员卡、粉色角色立牌、玻璃 slogan 卡、左上漂浮的 Merged | 减到杆 + 3 块牌 + 1 个挂件 + 1 个角色 |

slogan 从一张卡变成了两块方向相反的指向牌："从第一个算子" ← → "到第一份贡献"。**路牌本身就把 slogan 讲完了**，而且这是参考里没有的、只属于这场活动的用法。

示意见 `center_sketch.png`（中间区域）。

---

## 用法一：局部修改（推荐，标题、建筑、天空、底部都保留）

蒙版画在画面中间：从"开发者"右边到"俱乐部"左边，从顶到底部色带；另外把右上那张玻璃 slogan 卡和左上的 "Merged ✓" 也圈进蒙版。

```
Redesign only the masked center area as a clear, classic street signpost. Keep the titles, buildings, sky, petals and the white bottom band exactly unchanged.

A thick mirror-polished chrome signpost pole, fully visible from its round base on the ground up to the top, with sky visible on both sides of it.
On top of the pole: a small glossy mint-green ball finial with a white "+" on it.
Near the top: a classic rectangular blue enamel street-name sign with a white border and rounded corners, white bold text "CANN Rd.".
Below it, two arrow-shaped direction signs pointing in opposite directions, mounted on the pole with visible metal brackets:
  upper sign: bright blue #2F6BFF, arrow pointing to the upper right, white bold text "到第一份贡献";
  lower sign: mint green #4FDDAA, arrow pointing to the left, dark text "从第一个算子".
A small cute transparent NPU chip character (two round eyes, a smile, chrome pins) sits on top of the upper arrow sign with its legs dangling, holding a blue mug with steam made of "0" and "1".
A small glossy green capsule badge "Merged ✓" hangs near the tip of the upper arrow.
A small chrome device with a black screen showing "> hello, CANN_" and four jelly acrylic keycaps "C" "A" "N" "N" hangs from a short chain under the lower arrow sign.
Nothing else in the center: no ID card, no glass card, no extra floating objects. Generous spacing between the signs.
Same 3D designer-toy style, materials, soft studio lighting and colors as the rest of the image. Text exact, language zh for Chinese.
```

## 用法二：整图重新生成
把 `prompts.md` 第 1 条里的 `skeleton` 和 `elements` 两段换成下面这段，其余不变：

```
skeleton: 画面正中一根粗壮的镜面金属路牌杆，从底部白色色带上方的圆形底座一直伸到画面顶部，**完整可见，两侧露出天空**；
  杆顶一个薄荷绿光面小圆球，印白色 "+"；
  靠近顶部一块经典长方形蓝色搪瓷路名牌，圆角、白色描边，白色粗体 "CANN Rd."；
  下面两块箭头形指向牌，用看得见的金属支架固定在杆上，方向相反：
    上面一块亮蓝 #2F6BFF，箭头指向右上，白字 "到第一份贡献"；
    下面一块薄荷绿 #4FDDAA，箭头指向左，深色字 "从第一个算子"；
  牌子之间留出空隙。左右两侧下部各一组潮玩模型风格的校园建筑；画面最下方约 14% 是一条纯白色带。
elements:
  一个可爱的透明 NPU 小芯片角色坐在上面那块箭头牌的顶上，腿垂下来，端着亮蓝色马克杯，杯口冒出由 "0" "1" 组成的热气；
  上面箭头的尖端旁挂一枚绿色光面胶囊 "Merged ✓"；
  下面箭头牌下方用短链挂着一个小小的镜面铬设备，黑屏显示 "> hello, CANN_"，下面四颗果冻亚克力键帽 "C" "A" "N" "N"；
  右侧漂浮一个薄荷绿 "+1" 小方块；几片海棠花瓣。
  中间只有这些，不加成员卡、玻璃卡片或其他漂浮物。
```

## 改完看这几点
1. 远看能不能一眼认出"路牌"：杆子完整、路名牌、两块箭头牌
2. 两块箭头牌连起来读得出 slogan，方向正确（起点向左、终点向右上）
3. 中间元素不超过：杆 + 3 块牌 + 1 个角色 + 1 个挂件 + 1 个徽章
4. 牌子之间有空隙，能看到杆子
