"""摄影感后期：景深（移轴）、高光泛光、逆光光晕、调色、暗角、颗粒。

    python scripts/photo_post.py color.png depth.png out.png --focus 22 --k 70 [--sun 0.1,0.3]

用于程序化 3D 场景（路线 G）：渲染器输出颜色图和深度图（灰度 = 距离 / 150 米），
本脚本按薄透镜模型做景深，并加泛光、光晕、调色、暗角和颗粒，让 CG 画面更接近摄影。
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("color"); ap.add_argument("depth"); ap.add_argument("out")
ap.add_argument("--focus", type=float, default=22.0, help="对焦距离（米）")
ap.add_argument("--k", type=float, default=60.0, help="虚化强度")
ap.add_argument("--maxblur", type=float, default=9.0)
ap.add_argument("--sun", default="0.12,0.30", help="画面里逆光光源的位置（相对坐标）")
a = ap.parse_args()

img = np.asarray(Image.open(a.color).convert("RGB")).astype(np.float32) / 255
H, W, _ = img.shape
lin = img ** 2.2
d = np.asarray(Image.open(a.depth).convert("L")).astype(np.float32) / 255 * 150 + 0.01

# 1. 景深：薄透镜近似，模糊圈 ∝ |1/d - 1/f|
coc = np.clip(a.k * np.abs(1 / d - 1 / a.focus) * (H / 1080), 0, a.maxblur)
levels = [0, 1.2, 2.5, 4.5, 7, 10]
stack = [lin] + [ndimage.gaussian_filter(lin, (s, s, 0)) for s in levels[1:]]
out = np.zeros_like(lin)
for i in range(len(levels) - 1):
    lo, hi = levels[i], levels[i + 1]
    w = np.clip((coc - lo) / (hi - lo), 0, 1)
    m = ((coc >= lo) & (coc < hi))[..., None]
    out = np.where(m, stack[i] * (1 - w[..., None]) + stack[i + 1] * w[..., None], out)
out = np.where((coc >= levels[-1])[..., None], stack[-1], out)

# 2. 高光泛光
lum = out.mean(-1, keepdims=True)
bright = np.clip(out - 0.55, 0, None) * (lum > 0.5)
bloom = ndimage.gaussian_filter(bright, (H * 0.012, H * 0.012, 0)) * 0.8 + ndimage.gaussian_filter(bright, (H * 0.05, H * 0.05, 0)) * 0.9
out = out + bloom

# 3. 逆光光晕（太阳在画面外左上方）
sx, sy = map(float, a.sun.split(","))
ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot((xs / W - sx) * W / H, ys / H - sy)
glow = np.exp(-r * 2.2) * 0.22 + np.exp(-r * 7) * 0.12
out = out + glow[..., None] * np.array([1.0, 0.72, 0.42])

# 4. 调色：暖高光、略冷的阴影、轻微 S 曲线
out = out / (1 + out * 0.25)
g = out ** (1 / 2.2)
shadow_tint = np.array([0.96, 1.0, 1.04]); high_tint = np.array([1.04, 1.0, 0.94])
t = g.mean(-1, keepdims=True)
g = g * (shadow_tint * (1 - t) + high_tint * t)
g = np.clip(g, 0, 1)
g = g + 0.06 * (g - 0.5) * (1 - np.abs(2 * g - 1))      # 中间调对比
sat = g.mean(-1, keepdims=True)
g = sat + (g - sat) * 1.08
# 5. 暗角 + 颗粒
v = 1 - 0.22 * (((xs / W - 0.5) * 1.5) ** 2) * (0.4 + 0.6 * ys / H) - 0.18 * np.clip(ys / H - 0.7, 0, 1) ** 2
g = g * v[..., None]
rng = np.random.default_rng(7)
grain = ndimage.gaussian_filter(rng.normal(0, 1, (H, W)), 0.6)
g = g + grain[..., None] * 0.018
Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8)).save(a.out)
print(a.out)
