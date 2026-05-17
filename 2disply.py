from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import math

# ===================== MATRIX SETUP =====================
W = 64      # total display width (two 32x32 panels)
H = 32      # display height

options = RGBMatrixOptions()
options.rows = H
options.cols = W
options.hardware_mapping = "adafruit-hat"

m = RGBMatrix(options=options)

# Center of the display
cx = W // 2
cy = H // 2

# ===================== COLORS FOR EACH PHASE =====================
# Each transformation uses a different color
COLORS = [
    (255, 180, 0),   # Scaling
    (0, 255, 140),   # Shearing
    (255, 0, 0),     # Rotation
    (255, 0, 0),     # Translation
]
color = COLORS[0]

# ===================== ROTATION & TRANSLATION TRANSFORMS =====================
# This square is used for rotation and translation phases
side = 12
half = side // 2     # half of the side for centering

# Generate points forming the outline of a centered square
def get_square_edge(cx, cy, half):
   
    pts = []
    x1 = cx - half
    x2 = cx + half
    y1 = cy - half
    y2 = cy + half

    # Top edge
    for x in range(x1, x2+1):
        pts.append((x, y1))
    # Right edge
    for y in range(y1, y2+1):
        pts.append((x2, y))
    # Bottom edge
    for x in range(x2, x1-1, -1):
        pts.append((x, y2))
    # Left edge
    for y in range(y2, y1-1, -1):
        pts.append((x1, y))

    return pts

square_points = get_square_edge(cx, cy, half)

# ===================== SCALING & SHEARING TRANSFORMS =====================
# Scale point (x,y) around the center
def scale_transform(x, y, s):

    x -= cx
    y -= cy
    x *= s
    y *= s
    return int(x + cx), int(y + cy)
# Shear point (x,y) horizontally around center
def shear_transform(x, y, sh):
    x -= cx
    y -= cy
    x = x + sh * y    # x-shear
    return int(x + cx), int(y + cy)

# Draw a filled diamond-like shape using scaling or shearing
def draw_transformed_shape(mode, scale=1, shear=0):
    m.Clear()
    for y in range(H):
        for x in range(W):

            # Choose transformation
            if mode == 1:       # scaling
                tx, ty = scale_transform(x, y, scale)
            elif mode == 2:     # shearing
                tx, ty = shear_transform(x, y, shear)

            # Manhattan distance to determine filled area
            d = abs(tx - cx) + abs(ty - cy)

            if d < 10:
                m.SetPixel(x, y, color[0], color[1], color[2])

# ===================== ROTATION & TRANSLATION TRANSFORMS =====================
# Rotate outline square points around center
def rotate_point(px, py, angle):

    tx = px - cx
    ty = py - cy

    rx = tx * math.cos(angle) - ty * math.sin(angle)
    ry = tx * math.sin(angle) + ty * math.cos(angle)

    return int(rx + cx), int(ry + cy)
# Translate outline square horizontally
def translate_point(px, py, dx, dy):
    return px + dx, py + dy
# Draw red square outline rotated around center
def draw_rotating_square(angle):
    m.Clear()
    for px, py in square_points:
        rx, ry = rotate_point(px, py, angle)
        if 0 <= rx < W and 0 <= ry < H:
            m.SetPixel(rx, ry, 255, 0, 0)
# Draw red square outline moving left-right
def draw_translating_square(dx):
    m.Clear()
    for px, py in square_points:
        tx, ty = translate_point(px, py, dx, 0)  # dy=0 ( horizontal motion )
        if 0 <= tx < W and 0 <= ty < H:
            m.SetPixel(tx, ty, 255, 0, 0)

# ===================== ANIMATION VARIABLES =====================
phase = 1   # Start with scaling

# Scaling parameters
scale_size = 10
scale_dir = 1
scale_min = 6
scale_max = 16
scale_cycles = 0

# Shearing parameters
shear_value = 0
shear_dir = 1
shear_max = 3
shear_cycles = 0

# Rotation parameters
angle = 0
rotation_cycles = 0

# Translation parameters
dx = 0
move_dir = 1
move_limit = 10
translation_cycles = 0

# ===================== MAIN ANIMATION LOOP =====================
try:
    while True:

        # SCALING PHASE 
        if phase == 1:
            draw_transformed_shape(1, scale=scale_size/10)
            scale_size += 0.12 * scale_dir

            # Reverse direction at limits
            if scale_size > scale_max or scale_size < scale_min:
                scale_dir *= -1
                scale_cycles += 1

            # After several cycles, switch phase
            if scale_cycles >= 4:
                phase = 2
                color = COLORS[1]
                time.sleep(0.3)

        # SHEARING PHASE 
        elif phase == 2:
            draw_transformed_shape(2, shear=shear_value)
            shear_value += 0.12 * shear_dir

            # Reverse at limits
            if shear_value > shear_max or shear_value < -shear_max:
                shear_dir *= -1
                shear_cycles += 1

            if shear_cycles >= 4:
                phase = 3
                color = COLORS[2]
                time.sleep(0.3)

        # ROTATION PHASE 
        elif phase == 3:
            draw_rotating_square(angle)
            angle += 0.07

            if angle > math.pi * 4:
                rotation_cycles += 1
                angle = 0

            if rotation_cycles >= 2:
                phase = 4
                color = COLORS[3]
                time.sleep(0.3)

        # TRANSLATION PHASE 
        elif phase == 4:
            draw_translating_square(dx)
            dx += move_dir

            # Bounce limit left-right
            if dx > move_limit or dx < -move_limit:
                move_dir *= -1
                translation_cycles += 1

            # Reset after several cycles
            if translation_cycles >= 4:
                phase = 1
                color = COLORS[0]

                # Reset all values
                scale_size = 10
                shear_value = 0
                dx = 0
                scale_cycles = shear_cycles = rotation_cycles = translation_cycles = 0

                time.sleep(0.3)

        time.sleep(0.03)

except KeyboardInterrupt:
    m.Clear()
