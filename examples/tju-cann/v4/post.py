import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
m = np.asarray(Image.open('r_main.png').convert('RGBA')).astype(np.float32)/255
f = np.asarray(Image.open('r_fg.png').convert('RGBA')).astype(np.float32)/255
# foreground: defocus + slight motion blur (premultiplied)
pf = f.copy(); pf[...,:3] *= pf[...,3:]
pf = ndimage.gaussian_filter(pf, (6,6,0))
k = np.zeros((1,41)); k[0,:] = 1/41
pf = ndimage.convolve(pf, k[...,None], mode='nearest')*0.5 + pf*0.5
rgb = m[...,:3]*(1-pf[...,3:]) + pf[...,:3]
# soft bloom on highlights
lum = rgb.mean(-1, keepdims=True)
bl = ndimage.gaussian_filter(np.clip(rgb-0.8,0,None)*(lum>0.75), (24,24,0))
rgb = 1-(1-rgb)*(1-bl*0.8)
Image.fromarray((np.clip(rgb,0,1)*255).astype(np.uint8)).save('hero_post.png')
print('ok')
