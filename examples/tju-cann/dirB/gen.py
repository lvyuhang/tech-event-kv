import numpy as np
from scipy.spatial import Voronoi
C=160; W,H=2560,1440
BLUE='#1557FF'; BLUE2='#2E7BFF'; CYAN='#33C7F5'; ORANGE='#FF6A13'; GREEN='#1ECB55'; YEL='#FFC61A'; GRAY='#E6E7EB'; INK='#0D0F14'; PINK='#FF8FB0'
def R(c,r,w,h,fill,extra=''): return f'<rect x="{c*C}" y="{r*C}" width="{w*C}" height="{h*C}" fill="{fill}" {extra}/>'
def pix(bitmap,x,y,s,col):
    out=[]
    for j,row in enumerate(bitmap):
        for i,ch in enumerate(row):
            if ch!=' ': out.append(f'<rect x="{x+i*s}" y="{y+j*s}" width="{s}" height="{s}" fill="{col if ch=="#" else ch}"/>')
    return ''.join(out)
svg=[]
# background grid
svg.append(f'<rect width="{W}" height="{H}" fill="{GRAY}"/>')
g=[]
for x in range(0,W,80): g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
for y in range(0,H,80): g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
svg.append('<g stroke="#D3D5DB" stroke-width="2">'+''.join(g)+'</g>')
# ---- right blue zone with stairs
svg.append(R(12,0,4,9,BLUE))
steps=[]
for k in range(12):
    x=12*C+ k*95-120; y=H- k*120
    steps.append(f'<rect x="{x}" y="{y-120}" width="900" height="120" fill="{"#0F47E0" if k%2 else "#3D86FF"}"/>')
svg.append('<g clip-path="url(#cr)">'+''.join(steps)+
  f'<polygon points="{12*C+80},{H} {12*C+150},{H} {15*C+260},0 {15*C+190},0" fill="{YEL}"/>'
  f'<polygon points="{12*C+170},{H} {12*C+215},{H} {15*C+325},0 {15*C+280},0" fill="{ORANGE}"/>'
  f'<polygon points="{12*C+235},{H} {12*C+260},{H} {15*C+370},0 {15*C+345},0" fill="{GREEN}"/>'
  '</g>')
# voronoi mosaic bottom-right
rng=np.random.default_rng(3); vx0,vy0,vw,vh=13*C+40,5*C+60,3*C,4*C
pts=np.c_[rng.uniform(vx0-200,vx0+vw+200,40),rng.uniform(vy0-200,vy0+vh+200,40)]
vor=Voronoi(pts); cols=[BLUE,YEL,ORANGE,CYAN,YEL,BLUE2]
polys=[]
for i,reg in enumerate(vor.point_region):
    rr=vor.regions[reg]
    if -1 in rr or not rr: continue
    p=' '.join(f'{vor.vertices[v][0]:.0f},{vor.vertices[v][1]:.0f}' for v in rr)
    polys.append(f'<polygon points="{p}" fill="{cols[i%len(cols)]}" stroke="#0B2A8F" stroke-width="10" stroke-linejoin="round"/>')
svg.append(f'<clipPath id="vc"><path d="M{vx0+120},{vy0} L{vx0+vw},{vy0-40} L{vx0+vw},{vy0+vh} L{vx0-60},{vy0+vh} Z"/></clipPath><g clip-path="url(#vc)">'+''.join(polys)+'</g>')
# ---- top cloud blobs (flat blue with dither edge)
svg.append(f'<g filter="url(#dither)"><path d="M{3*C},0 H{9*C} V{C*0.55} Q{8.6*C},{C*1.05} {7.8*C},{C*0.8} H{5.2*C} Q{4.4*C},{C*1.25} {3.6*C},{C*0.85} Q{3*C},{C*0.7} {3*C},{C*0.4} Z" fill="{BLUE}"/></g>')
svg.append(f'<g filter="url(#dither)"><path d="M0,{1.15*C} H{1.6*C} Q{2.4*C},{1.2*C} {2.3*C},{1.65*C} Q{2.2*C},{2.0*C} {1.5*C},{1.95*C} H0 Z" fill="{CYAN}"/></g>')
# logos tile
svg.append(R(0,0,3,1,'#FFFFFF'))
# AI chip-face pixel tile (blue)
svg.append(R(0,2,3,2,BLUE2))
chip=['  # # # # #  ','            ','############',' #        # ','##  ##  ## ##','##  ##  ## ##',' #        # ','##   ##   ##',' #  ####  # ','############','            ','  # # # # #  ']
chip=['  # # # # # ','############','#          #','#  ##  ##  #','#  ##  ##  #','#          #','#   ####   #','############','  # # # # # ']
svg.append(pix(chip,0*C+120,2*C+50,18,'#FFFFFF'))
svg.append(f'<text x="{2*C+40}" y="{3*C+120}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="40" fill="#BFE0FF">NPU</text>')
# code braces tile (gray)
svg.append(R(1,4,2,1,'#CFD2D9'))
svg.append(f'<text x="{2*C}" y="{4*C+112}" text-anchor="middle" font-family="DejaVu Sans Mono" font-weight="bold" font-size="104" fill="#FFFFFF">{{·}}</text>')
# gradient shard tile
svg.append(f'<defs><linearGradient id="gs" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".55" stop-color="{YEL}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient></defs>')
svg.append(R(0,5,1,2,'url(#gs)')); svg.append(f'<polygon points="0,{5*C} {C},{5*C} 0,{6.2*C}" fill="#ffffff" opacity=".55"/>')
# CANN letter tiles
for (c,r,bg,fg,ch) in [(0,7,BLUE,'#fff','T'),(1,7,ORANGE,'#fff','J'),(0,8,GREEN,INK,'U'),(1,8,'#FFFFFF',INK,'+1')]:
    svg.append(R(c,r,1,1,bg,'stroke="#0D0F14" stroke-width="4"'))
    svg.append(f'<text x="{c*C+80}" y="{r*C+112}" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="96" fill="{fg}">{ch}</text>')
# operator pixel tiles top (+ and ×)
svg.append(R(9,1,1,1,BLUE,'stroke="#0D0F14" stroke-width="4"'))
plus=['  ##  ','  ##  ','######','######','  ##  ','  ##  ']
svg.append(pix(plus,9*C+32,1*C+32,16,'#FFFFFF'))
svg.append(R(10,1,1,1,'#FFFFFF','stroke="#0D0F14" stroke-width="4"'))
times=['##    ##',' ##  ## ','  ####  ','  ####  ',' ##  ## ','##    ##']
svg.append(pix(times,10*C+32,1*C+40,12,INK))
svg.append(R(11,1,1,1,YEL,'stroke="#0D0F14" stroke-width="4"'))
sig=['######','##    ',' ##   ','  ##  ',' ##   ','##    ','######']
svg.append(pix(sig,11*C+44,1*C+30,14,INK))
# terminal tile
svg.append(R(9,3,3,1,INK))
svg.append(f'<text x="{9*C+36}" y="{3*C+98}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="46" fill="#3BFF8A">&gt;_ hello, CANN</text>')
svg.append(f'<rect x="{9*C+36+14*27.7+8:.0f}" y="{3*C+58}" width="24" height="48" fill="#3BFF8A"/>')
# haitang flower tile
svg.append(R(12,6,2,2,CYAN))
fx,fy=13*C,7*C
for k in range(5):
    a=np.deg2rad(-90+k*72); x=fx+np.cos(a)*68; y=fy+np.sin(a)*68
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="66" fill="{PINK}"/>')
for k in range(5):
    a=np.deg2rad(-90+k*72); x=fx+np.cos(a)*68; y=fy+np.sin(a)*68
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="40" fill="#FFC2D3"/>')
svg.append(f'<circle cx="{fx}" cy="{fy}" r="44" fill="{YEL}"/><circle cx="{fx}" cy="{fy}" r="20" fill="#fff"/>')
# green blob bottom
svg.append(f'<g filter="url(#dither)"><path d="M{4.5*C},{H} Q{4.8*C},{8.35*C} {5.6*C},{8.45*C} H{8.2*C} Q{9.2*C},{8.3*C} {9.6*C},{8.75*C} L{10*C},{H} Z" fill="{GREEN}"/></g>')
# sparkles
def spark(x,y,s,col=YEL): return f'<path d="M{x},{y-s} Q{x+s*0.12},{y-s*0.12} {x+s},{y} Q{x+s*0.12},{y+s*0.12} {x},{y+s} Q{x-s*0.12},{y+s*0.12} {x-s},{y} Q{x-s*0.12},{y-s*0.12} {x},{y-s} Z" fill="{col}"/>'
svg.append(spark(14.1*C,1.3*C,90)); svg.append(spark(13.4*C,2.1*C,44)); svg.append(spark(2.75*C,5.35*C,50)); svg.append(spark(10.7*C,5.7*C,46))
defs=f'''<defs><clipPath id="cr"><rect x="{12*C}" y="0" width="{4*C}" height="{H}"/></clipPath>
<filter id="dither" x="-10%" y="-10%" width="120%" height="120%">
 <feGaussianBlur in="SourceAlpha" stdDeviation="22" result="b"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="4" result="n"/>
 <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="nr"/>
 <feComposite in="b" in2="nr" operator="arithmetic" k1="0" k2="1.6" k3="0.9" k4="-1.05" result="m"/>
 <feComponentTransfer in="m" result="mt"><feFuncA type="discrete" tableValues="0 1"/></feComponentTransfer>
 <feComposite in="SourceGraphic" in2="mt" operator="in"/>
</filter></defs>'''
open('art.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs}{"".join(svg)}</svg>')
print('ok')
