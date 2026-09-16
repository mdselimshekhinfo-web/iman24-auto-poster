"""
Islamic Image Generator Module for 'ঈমান' (iman24.bd)
Creates aesthetic Islamic banners with serene green gradient backgrounds, golden accents, and Noto Sans Bengali font.
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

PAGE_NAME = "ঈমান — iman24.bd"

# Aesthetic Islamic Green Gradients
BG_GRADIENTS = [
    ((5, 45, 25), (10, 25, 15)),      # Deep Emerald Forest
    ((10, 60, 40), (4, 30, 20)),      # Rich Islamic Jade
    ((15, 50, 35), (2, 20, 15)),      # Velvet Midnight Green
    ((8, 40, 30), (1, 15, 10)),       # Deep Olive Green
]

# Golden & Light Emerald Accents
GOLD_ACCENTS = [
    (212, 175, 55),    # Classic Islamic Gold
    (230, 195, 90),    # Soft Champagne Gold
    (180, 220, 180),   # Light Mint Emerald
    (245, 215, 120),   # Warm Sunlight Gold
]

FONT_PATHS = [
    os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'NotoSansBengali.ttf'),
    "C:/Windows/Fonts/NotoSansBengali.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def get_font(size):
    for path in FONT_PATHS:
        try:
            path = os.path.normpath(path)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_gradient(img, c1, c2):
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * y / h)
        g = int(c1[1] + (c2[1] - c1[1]) * y / h)
        b = int(c1[2] + (c2[2] - c1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_islamic_borders(draw, w, h, gold):
    # Inner border line
    draw.rectangle([25, 25, w - 25, h - 25], outline=gold, width=2)
    draw.rectangle([32, 32, w - 32, h - 32], outline=(*gold[:3], 100), width=1)

    # Decorative corner diamonds
    for (cx, cy) in [(32, 32), (w - 32, 32), (32, h - 32), (w - 32, h - 32)]:
        draw.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], fill=gold)


def create_islamic_image(title, output_path="/tmp/islamic_post.jpg"):
    w, h = 1200, 630
    bg = random.choice(BG_GRADIENTS)
    gold = random.choice(GOLD_ACCENTS)

    img = Image.new('RGB', (w, h), (0, 0, 0))
    draw_gradient(img, bg[0], bg[1])

    draw = ImageDraw.Draw(img)
    draw_islamic_borders(draw, w, h, gold)

    # Page Header Badge
    font_badge = get_font(24)
    badge = f" 🌙 {PAGE_NAME} "
    draw.text((w // 2 - 130, 45), badge, fill=gold, font=font_badge)

    # Main text / Hadith / Verse Title
    font_title = get_font(48)
    font_sub = get_font(26)

    clean_title = title.replace('🌙', '').replace('✨', '').replace('🕌', '').strip()[:110]
    wrapped = textwrap.fill(clean_title, width=24)
    lines = wrapped.split('\n')[:4]

    total_h = len(lines) * 65
    y_start = (h - total_h) // 2

    for i, line in enumerate(lines):
        y = y_start + i * 65
        # Shadow
        draw.text((w // 2 - 280 + 2, y + 2), line, fill=(0, 0, 0), font=font_title)
        # Gold text
        draw.text((w // 2 - 280, y), line, fill=(255, 255, 255), font=font_title)

    # Bottom Tagline
    draw.text((w // 2 - 220, h - 70), "শান্তি ও হেদায়েতের পথে প্রতিদিনের পাথেয়", fill=gold, font=font_sub)

    img.save(output_path, 'JPEG', quality=95)
    print(f"🖼️ Islamic Green Image Created: {output_path}")
    return output_path
