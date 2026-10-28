#!/bin/sh
# 重新生成本示例的生成式图层（在仓库根目录运行）
D=examples/galaxy-devcon/heroes/v3
python scripts/glyph_flow.py --w 1920 --h 1080 --out $D/flow_16x9 --n 13000 --spread 0.15 --path "-0.03,0.86 0.16,0.88 0.34,0.86 0.50,0.80 0.62,0.68 0.72,0.50 0.81,0.32 0.90,0.17" --fg-from 0.55
python scripts/glyph_flow.py --w 1080 --h 1920 --out $D/flow_9x16 --n 11000 --spread 0.13 --path "-0.05,0.80 0.22,0.80 0.46,0.75 0.64,0.64 0.74,0.50 0.79,0.36 0.82,0.24" --fg-from 0.55
python scripts/glyph_flow.py --w 1080 --h 1080 --out $D/flow_1x1 --n 9000 --spread 0.12 --path "-0.04,0.78 0.20,0.80 0.42,0.76 0.60,0.64 0.70,0.54 0.76,0.38 0.80,0.22" --fg-from 0.55
python scripts/glyph_flow.py --w 900 --h 383 --out $D/flow_wechat --n 5000 --spread 0.14 --path "-0.03,0.94 0.30,0.93 0.52,0.84 0.66,0.62 0.76,0.38 0.84,0.16" --fg-from 0.55
