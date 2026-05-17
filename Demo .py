from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import math

# ===== LED SETUP =====
W = 32
H = 32

o = RGBMatrixOptions()
o.rows = H
o.cols = W
o.hardware_mapping = "adafruit-hat"
m = RGBMatrix(options=o)

cx = W // 2
cy = H // 2

# ===== COLORS FOR EACH PHASE =====
C = [
    (255, 0, 60),    # Phase 1 color
    (0, 160, 255),   # Phase 2 color
    (255, 180, 0),   # Phase 3 color
    (0, 255, 140),   # Phase 4 color
]
color = C[0]

# ======== TRANSFORMATION PARAMETERS ========
# Phase 1 - Move Up/Down
shift = 0
SY = 0.25
dy = 1
limit = 10

# Phase 2 - Rotation
ang = 0
RS = 3
rot_end = 360 * 2

# Phase 3 - Scaling
size = 10
min_s = 6
max_s = 16
SS = 0.08
ds = 1
scale_cycles = 0

# Phase 4 - Shearing
sh = 0
SHS = 0.03
dsh = 1
max_sh = 3
shear_cycles = 0

phase = 1   # start with movement


# ======== TRANSFORM FUNCTION ========
def trans(x, y, a, s, sh, yy):
    x -= cx
    y -= cy

    # vertical move (phase 1)
    y += yy

    # scale (phase 3)
    x *= s
    y *= s

    # shear (phase 4)
    x += sh * y

    # rotate (phase 2)
    r = math.radians(a)
    xr = x * math.cos(r) - y * math.sin(r)
    yr = x * math.sin(r) + y * math.cos(r)

    return int(xr + cx), int(yr + cy)


# ======== DRAW DIAMOND ========
def draw(a, s, sh, yy):
    m.Clear()
    for y in range(H):
        for x in range(W):

            tx, ty = trans(x, y, a, s, sh, yy)

            d = abs(tx - cx) + abs(ty - cy)
            if d < 10:
                m.SetPixel(x, y, color[0], color[1], color[2])


# ======== MAIN LOOP ========
try:
    while True:

        # ========== PHASE 1 — UP/DOWN ==========
        if phase == 1:
            draw(0, 1, 0, shift)

            shift += SY * dy
            if shift > limit or shift < -limit:
                dy *= -1

            # one full bounce finished
            if abs(shift) < 0.1 and dy == -1:
                time.sleep(0.5)          # pause
                phase = 2
                color = C[1]             # change color

        # ========== PHASE 2 — ROTATION ==========
        elif phase == 2:
            draw(ang, 1, 0, 0)

            ang += RS
            if ang > rot_end:
                time.sleep(0.5)          # pause
                phase = 3
                color = C[2]             # change color

        # ========== PHASE 3 — SCALING ==========
        elif phase == 3:
            draw(0, size / 10, 0, 0)

            size += SS * ds
            if size > max_s or size < min_s:
                ds *= -1
                scale_cycles += 1

            if scale_cycles >= 4:
                time.sleep(0.5)          # pause
                phase = 4
                color = C[3]             # change color

        # ========== PHASE 4 — SHEARING ==========
        elif phase == 4:
            draw(0, 1, sh, 0)

            sh += SHS * dsh
            if sh > max_sh or sh < -max_sh:
                dsh *= -1
                shear_cycles += 1

            if shear_cycles >= 4:
                time.sleep(0.5)          # pause
                # restart full sequence
                phase = 1
                color = C[0]
                sh = 0
                shear_cycles = 0
                scale_cycles = 0
                ang = 0
                shift = 0
                dy = 1

        time.sleep(0.03)

except KeyboardInterrupt:
    m.Clear()
