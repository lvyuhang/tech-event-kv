# 案例：天大 CANN 开发者俱乐部 · KV 延展全套物料

> 2026-11-03 至 11-06。定稿 KV（像素便当格）→ 线上 9 件 + 线下 8 件 + 串场 PPT 14 页。用户评价：**本次任务特别成功**。方法论见 `references/extension.md`，经验 L48–L55。

## 最终稿

| 物料 | 图 |
|---|---|
| 16:9 主视觉（日期块更新） | ![](img/final_01a_kv_16x9.jpg) |
| 合影背板 5×2m · NPU 算力体检 1P VS 2P | ![](img/final_02_photowall_power_check.jpg) |
| 合影背板 · 双人 PK 场景示意 | ![](img/scene_02_photowall_two_players.jpg) |
| 横幅 6m×60cm（150 网格、镜像对称） | ![](img/final_09_banner.jpg) |
| 易拉宝 80×200（KV 便当格上部 + 像素山底部） | ![](img/final_05_rollup.jpg) |
| 易拉宝 · 视线高度标注 | ![](img/scene_05_rollup_eye_level.jpg) |
| 日程单页 A4（8 环节，授牌高亮） | ![](img/final_03_agenda_a4.jpg) |
| 指引牌 60×90（目的地 + 箭头在上） | ![](img/final_04_guide_sign.jpg) |
| 指引牌 · 遮挡标注 | ![](img/scene_04_guide_sign.jpg) |
| 桌卡（名字占满） | ![](img/final_08_table_card.jpg) |
| 邀请函（含议程） | ![](img/final_01f_invitation.jpg) |
| 海报长图 | ![](img/final_01b_long_poster.jpg) |
| 公众号封面 900×383 / 1:1 | ![](img/final_01c_wechat_900x383.jpg) ![](img/final_01d_wechat_1x1.jpg) |
| 视频号直播封面 / CSDN 视窗 / 小程序封面 | ![](img/final_01g_live_cover.jpg) ![](img/final_01h_csdn.jpg) ![](img/final_01i_miniapp.jpg) |
| 串场 PPT 14 页 | ![](img/final_ppt_mc_deck.jpg) |

## 过程（反例也是资产）

| 轮次 | 评审 | 图 |
|---|---|---|
| v1 裁切 KV 格子填满版面 | "设计语言延展得不好，简陋、排版不平衡"（L48） | ![](img/process_v1_cropped_tiles_BAD.jpg) |
| v2 按规则重排 | "没有考虑场景：合影谁会去拍？指引牌箭头偏下；议程不平衡"（L49） | ![](img/process_v2_language_no_scene_NEAR.jpg) |
| v3 场景优先 | 物料基本通过，合影背板仍"无趣、散" | ![](img/process_v3_scene_first.jpg) |
| v4 贡献山 + 手举牌 | "还是不行，这是设计思维的部分"（L50）→ 用户给 5 个正例 | ![](img/process_v4_photowall_contrib_mountain_BAD.jpg) |
| 备选 A 心声墙 | 可以；大合影只露顶部 | ![](img/alt_A_voice_wall.jpg) ![](img/scene_A_voice_wall_group.jpg) |
| 定稿 B 算力体检 5×2m | 采用 | 见上 |

## 源码

`src/`：`lib.py`（组件库）、`formats.py`（v1–v4 各物料）、`formats_v5.py`（按方案更新的终版，顶部 `EVENT`/`AGENDA` 即配置）、`render.js`（PNG）、`pdf.js`（真实尺寸 PDF）、`kv.svg`（定稿 KV，图标按坐标从它裁取）。像素字体 Fusion Pixel（OFL）需另行下载到 `src/fonts/`。

```bash
cd src
python3 run.py            # 写出 formats.FORMATS 的 html 与 meta.json（终版把 run.py 里的 formats 换成 formats_v5）
node render.js            # → out/*.png
node pdf.js               # → pdf/*.pdf（有 mm 的物料）
```
