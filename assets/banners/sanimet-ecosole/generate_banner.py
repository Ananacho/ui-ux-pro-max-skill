from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1080, 1080
img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img)

# ── Colours ─────────────────────────────────────────────────────
PURPLE      = (61,  46, 158)
PURPLE_DARK = (38,  26, 110)
PURPLE_MID  = (80,  60, 190)
ORANGE      = (255, 107,  0)
WHITE       = (255, 255, 255)
SKY_TOP     = ( 14,  80, 170)
SKY_BOT     = ( 90, 160, 235)
SUN_YELLOW  = (255, 218,  40)
SUN_PALE    = (255, 240, 140)
PANEL_BG    = ( 18,  48, 118)
PANEL_LINE  = ( 28,  28,  75)
PANEL_SHINE = ( 55, 105, 190)
GRASS       = ( 55, 130,  55)
LIGHT_BG    = (250, 250, 255)   # very slight tint behind content

FD = "/usr/share/fonts/truetype"
FB = f"{FD}/dejavu/DejaVuSans-Bold.ttf"
FR = f"{FD}/dejavu/DejaVuSans.ttf"
FI = f"{FD}/liberation/LiberationSans-Italic.ttf"
def fnt(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# ═══════════════════════════════════════════════════════════════
# 1. WHITE base then SKY GRADIENT (0–400)
# ═══════════════════════════════════════════════════════════════
SKY_H = 400
for y in range(SKY_H):
    t = y / SKY_H
    c = tuple(int(SKY_TOP[i]+(SKY_BOT[i]-SKY_TOP[i])*t) for i in range(3))
    draw.line([(0,y),(W,y)], fill=c)

# ═══════════════════════════════════════════════════════════════
# 2. SUN
# ═══════════════════════════════════════════════════════════════
SX, SY, SR = 850, 90, 62
for i in range(4, 0, -1):
    gr = SR + i*17
    draw.ellipse([SX-gr,SY-gr,SX+gr,SY+gr], fill=SUN_PALE)
draw.ellipse([SX-SR,SY-SR,SX+SR,SY+SR], fill=SUN_YELLOW, outline=(235,190,10), width=3)

# ═══════════════════════════════════════════════════════════════
# 3. SOLAR PANELS
# ═══════════════════════════════════════════════════════════════
def rpoly(cx,cy,pw,ph,deg):
    a=math.radians(deg); ca,sa=math.cos(a),math.sin(a)
    return [(cx+x*ca-y*sa,cy+x*sa+y*ca) for x,y in [(-pw/2,-ph/2),(pw/2,-ph/2),(pw/2,ph/2),(-pw/2,ph/2)]]

def panel(cx,cy,pw=195,ph=100,ang=-14):
    draw.polygon(rpoly(cx,cy,pw,ph,ang), fill=PANEL_BG, outline=PANEL_LINE)
    a=math.radians(ang); ca,sa=math.cos(a),math.sin(a)
    for fx in [0.33,0.67]:
        dx=pw*(fx-0.5)
        draw.line([(cx+dx*ca-(-ph/2)*sa,cy+dx*sa+(-ph/2)*ca),(cx+dx*ca-(ph/2)*sa,cy+dx*sa+(ph/2)*ca)], fill=PANEL_LINE, width=2)
    draw.line([(cx-pw/2*ca,cy-pw/2*sa),(cx+pw/2*ca,cy+pw/2*sa)], fill=PANEL_LINE, width=2)
    draw.polygon(rpoly(cx-pw*.12,cy-ph*.12,pw*.2,ph*.6,ang), fill=PANEL_SHINE)

panel(215,295); panel(430,252); panel(645,210); panel(860,168)
for bx,by in [(140,344),(294,344),(356,302),(510,302),(571,260),(725,260),(786,218),(940,218)]:
    draw.line([(bx,by),(bx,by+40)], fill=PANEL_LINE, width=4)

# ═══════════════════════════════════════════════════════════════
# 4. GRASS
# ═══════════════════════════════════════════════════════════════
draw.rectangle([0, 360, W, SKY_H], fill=GRASS)

# ═══════════════════════════════════════════════════════════════
# 5. PURPLE WAVE  – sits BETWEEN the sky and the white content
#    It only occupies ~370-450; below 450 is WHITE
# ═══════════════════════════════════════════════════════════════
WAVE_Y = 372
# Build the wave shape (a band, not a full fill to bottom)
wave_pts = [(0, WAVE_Y)]
for x in range(0, W+1, 3):
    wave_pts.append((x, WAVE_Y + 25 + 25*math.sin(x/155 + 0.3)))
# close the band at the bottom of the wave
for x in range(W,-1,-3):
    wave_pts.append((x, WAVE_Y + 55 + 25*math.sin(x/155 + 0.3)))
draw.polygon(wave_pts, fill=PURPLE)

# lighter crest highlight
crest = [(0, WAVE_Y+8)]
for x in range(0, W+1, 3):
    crest.append((x, WAVE_Y + 10 + 25*math.sin(x/155 + 0.3)))
for x in range(W,-1,-3):
    crest.append((x, WAVE_Y + 28 + 25*math.sin(x/155 + 0.3)))
draw.polygon(crest, fill=PURPLE_MID)

# ═══════════════════════════════════════════════════════════════
# 6. LOGO BADGE (top-left, on sky)
# ═══════════════════════════════════════════════════════════════
LX, LY, LR = 32, 18, 52
draw.ellipse([LX,LY,LX+LR*2,LY+LR*2], fill=WHITE, outline=PURPLE, width=3)
hx,hy = LX+LR, LY+LR+4
draw.polygon([(hx,hy-26),(hx-20,hy-9),(hx+20,hy-9)], fill=PURPLE)
draw.rectangle([hx-16,hy-9,hx+16,hy+16], fill=PURPLE)
draw.rectangle([hx-5,hy+3,hx+5,hy+16], fill=WHITE)
draw.text((LX+LR*2+12, LY+6),  "LA OIAGA", font=fnt(FB,28), fill=WHITE)
draw.text((LX+LR*2+12, LY+38), "SANIMET",  font=fnt(FB,22), fill=SUN_YELLOW)

# ═══════════════════════════════════════════════════════════════
# 7. WHITE CONTENT AREA  (CY=456 → BAR_Y=880)
#    Available height = 424 px
# ═══════════════════════════════════════════════════════════════
CY = 456     # content starts (just after wave settles)

# Ensure white background for content area
draw.rectangle([0, CY-6, W, 878], fill=WHITE)

# ── Headline ──────────────────────────────────────────────────
draw.text((50, CY),      "ENERGIE SOLARĂ",  font=fnt(FB,78), fill=ORANGE)
draw.text((50, CY+84),   "PENTRU CASA TA",  font=fnt(FB,62), fill=PURPLE_DARK)

# ── Sub-title ──
draw.text((52, CY+158),  "Sisteme Solare Ferroli EcoSole",
          font=fnt(FB,30), fill=PURPLE)

# orange accent bar
draw.line([(52, CY+200),(530, CY+200)], fill=ORANGE, width=4)

# ── "Ce gasesti?" pill ──
PY = CY + 212
draw.rounded_rectangle([52, PY, 250, PY+40], radius=20, fill=ORANGE)
draw.text((68, PY+6), "Ce gasesti?", font=fnt(FB,28), fill=WHITE)

# ── Ferroli badge (right side, same row as pill) ──
BX = W - 222
draw.rounded_rectangle([BX, PY, W-18, PY+40], radius=10, fill=PURPLE)
draw.text((BX+12, PY+7), "Ferroli EcoSole", font=fnt(FB,23), fill=WHITE)

# ── Features  2 col × 2 rows ──────────────────────────────────
# Row 1: PY+52 = CY+264,  Row 2: PY+116 = CY+328
FY1 = PY + 54     # = CY+266
FY2 = PY + 116    # = CY+328

feats = [
    ("Economii pana la 70%\nla apa calda",    50,  FY1),
    ("Energie verde,\ncosturi mici",          544, FY1),
    ("Compatibil cu orice\nsistem termic",     50,  FY2),
    ("Instalare rapida\nsi profesionala",     544, FY2),
]

for txt, fx, fy in feats:
    draw.ellipse([fx,fy,fx+34,fy+34], fill=ORANGE)
    draw.line([(fx+7,fy+17),(fx+15,fy+25)], fill=WHITE, width=3)
    draw.line([(fx+15,fy+25),(fx+27,fy+9)], fill=WHITE, width=3)
    lines = txt.split("\n")
    draw.text((fx+44, fy+0),  lines[0], font=fnt(FR,27), fill=PURPLE_DARK)
    if len(lines) > 1:
        draw.text((fx+44, fy+29), lines[1], font=fnt(FR,27), fill=PURPLE_DARK)

# ── CTA italic  (FY2 + 64) ──
CTAY = FY2 + 68    # = CY+396 ≈ 852 → fits before bar at 880
draw.text((52, CTAY),
          "RATE FARA DOBANDA prin partenerii nostri financiari!",
          font=fnt(FI,27), fill=PURPLE)

# ═══════════════════════════════════════════════════════════════
# 8. CONTACT BAR  (880 – 1080)
# ═══════════════════════════════════════════════════════════════
BAR_Y = 882
draw.rectangle([0, BAR_Y, W, H], fill=ORANGE)

draw.rounded_rectangle([36, BAR_Y+26, 252, BAR_Y+82], radius=28, fill=PURPLE)
draw.text((56, BAR_Y+36), "CONTACT", font=fnt(FB,28), fill=WHITE)
draw.ellipse([214, BAR_Y+30, 252, BAR_Y+68], fill=WHITE)
draw.polygon([(228,BAR_Y+44),(228,BAR_Y+58),(246,BAR_Y+51)], fill=ORANGE)

draw.rounded_rectangle([284, BAR_Y+30, 320, BAR_Y+74], radius=8, fill=WHITE)
draw.text((290,BAR_Y+34), "☎", font=fnt(FR,30), fill=PURPLE)
draw.text((330, BAR_Y+26), "Telefon",        font=fnt(FR,21), fill=WHITE)
draw.text((330, BAR_Y+50), "0230 543 539",   font=fnt(FB,28), fill=WHITE)

draw.rounded_rectangle([596, BAR_Y+30, 634, BAR_Y+74], radius=8, fill=WHITE)
draw.text((602,BAR_Y+34), "◉", font=fnt(FR,30), fill=PURPLE)
draw.text((646, BAR_Y+26), "Adresa",                       font=fnt(FR,21), fill=WHITE)
draw.text((646, BAR_Y+50), "Falticeni, Str. 2 Graniceri",  font=fnt(FB,24), fill=WHITE)

# ═══════════════════════════════════════════════════════════════
out = "/home/user/ui-ux-pro-max-skill/assets/banners/sanimet-ecosole/ecosole-1080x1080.png"
img.save(out, "PNG"); print("Saved →", out)
