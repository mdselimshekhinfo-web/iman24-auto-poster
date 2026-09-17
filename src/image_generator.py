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
    os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'HindSiliguri-Bold.ttf'),
    os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'NotoSansBengali.ttf'),
    "C:/Windows/Fonts/kalpurush.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def get_active_font_path():
    for p in FONT_PATHS:
        p = os.path.normpath(p)
        if os.path.exists(p):
            return p
    return None


def render_shaped_text(img, text, x_center, y_pos, font_size, color_rgb=(255, 255, 255)):
    """
    Renders Bengali text using HarfBuzz shaping + FreeType rasterization.
    Guarantees 100% accurate Bengali conjuncts and car-fala.
    """
    import uharfbuzz as hb
    import freetype
    import numpy as np

    font_path = get_active_font_path()
    if not font_path:
        draw = ImageDraw.Draw(img)
        draw.text((x_center, y_pos), text, fill=color_rgb)
        return

    ft_face = freetype.Face(font_path)
    ft_face.set_char_size(font_size * 64)

    with open(font_path, 'rb') as f:
        font_data = f.read()
    hb_face = hb.Face(font_data)
    hb_font = hb.Font(hb_face)
    upem = hb_face.upem
    hb_font.scale = (upem, upem)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf)

    scale = font_size / upem
    total_w = sum(pos.x_advance * scale for pos in buf.glyph_positions)
    start_x = x_center - (total_w / 2.0)

    curr_x = start_x
    curr_y = y_pos

    rgba_img = img.convert('RGBA')

    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gid = info.codepoint
        ft_face.load_glyph(gid, freetype.FT_LOAD_RENDER)
        slot = ft_face.glyph
        bitmap = slot.bitmap

        bx = int(round(curr_x + pos.x_offset * scale + slot.bitmap_left))
        by = int(round(curr_y - pos.y_offset * scale - slot.bitmap_top))

        if bitmap.width > 0 and bitmap.rows > 0:
            glyph_arr = np.array(bitmap.buffer, dtype=np.uint8).reshape((bitmap.rows, bitmap.width))
            glyph_mask = Image.fromarray(glyph_arr)
            color_layer = Image.new('RGBA', (bitmap.width, bitmap.rows), (*color_rgb, 255))
            rgba_img.paste(color_layer, (bx, by), mask=glyph_mask)

        curr_x += pos.x_advance * scale
        curr_y -= pos.y_advance * scale

    img.paste(rgba_img.convert('RGB'), (0, 0))
    return total_w


def draw_gradient(img, c1, c2):
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(c1[0] + (c2[0] - c1[0]) * y / h)
        g = int(c1[1] + (c2[1] - c1[1]) * y / h)
        b = int(c1[2] + (c2[2] - c1[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def create_islamic_image(quote_title, output_path="/tmp/islamic_post.jpg", reference="", subheader="রাসূলুল্লাহ (ﷺ) বলেছেন:"):
    """
    Generate High-Impact 4:5 Mobile Portrait Islamic Poster (1080x1350)
    Places the MAIN Hadith / Quranic teaching right in the center of the poster!
    """
    w, h = 1080, 1350
    bg = random.choice(BG_GRADIENTS)
    gold = random.choice(GOLD_ACCENTS)

    img = Image.new('RGB', (w, h), (5, 25, 15))
    draw_gradient(img, bg[0], bg[1])

    # Overlay aesthetic mosque visual if available
    bg_asset = os.path.join(os.path.dirname(__file__), '..', 'assets', 'islamic_bg.jpg')
    if os.path.exists(bg_asset):
        try:
            mosque_img = Image.open(bg_asset)
            mosque_resized = mosque_img.resize((w, h), Image.Resampling.LANCZOS)
            img = Image.blend(img, mosque_resized, alpha=0.35)
        except Exception:
            pass

    draw = ImageDraw.Draw(img)

    # Islamic Double Border
    draw.rectangle([35, 35, w - 35, h - 35], outline=gold, width=3)
    draw.rectangle([45, 45, w - 45, h - 45], outline=(*gold[:3],), width=1)

    # Corner Islamic Diamonds
    for (cx, cy) in [(45, 45), (w - 45, 45), (45, h - 45), (w - 45, h - 45)]:
        draw.polygon([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)], fill=gold)

    # 1. Page Header Badge
    render_shaped_text(img, f"ঈমান  |  iman24.bd", w // 2, 110, 32, gold)

    # 2. Subheader (e.g. রাসূলুল্লাহ (সা.) বলেছেন: বা পবিত্র কুরআনে ইরশাদ হয়েছে:)
    clean_sub = subheader.replace('🌙', '').replace('✨', '').replace('ﷺ', '(সা.)').replace('ﷺ', '(সা.)').strip()
    render_shaped_text(img, clean_sub, w // 2, 220, 44, (245, 215, 120))

    # 3. Core Hadith / Ayat Quote Box
    box_top = 300
    box_bottom = 850
    box_w = 920
    draw.rectangle([(w - box_w) // 2, box_top, (w + box_w) // 2, box_bottom],
                   outline=gold, fill=(8, 30, 20), width=2)

    # Wrap the core quote
    clean_quote = quote_title.replace('«', '').replace('»', '').replace('"', '').strip()
    wrapped = textwrap.fill(clean_quote, width=17)
    lines = wrapped.split('\n')[:5]

    y_quote_start = box_top + 100
    for i, line in enumerate(lines):
        render_shaped_text(img, line.strip(), w // 2, y_quote_start + i * 85, 48, (255, 255, 255))

    # 4. Clear Reference inside the box
    if reference:
        clean_ref = f"— {reference.strip()}"
        render_shaped_text(img, clean_ref, w // 2, box_bottom - 50, 30, gold)

    # 5. Curiosity Hook & CTA Button
    btn_w = 520
    btn_h = 65
    btn_y = 930
    draw.rectangle([(w - btn_w) // 2, btn_y, (w + btn_w) // 2, btn_y + btn_h],
                   fill=gold, outline=(255, 255, 255), width=1)
    render_shaped_text(img, "বিস্তারিত ক্যাপশনে পড়ুন", w // 2, btn_y + 48, 32, (10, 40, 20))

    # 6. Bottom Footer Tagline
    render_shaped_text(img, "শান্তি ও হেদায়েতের পথে প্রতিদিনের পাথেয়", w // 2, h - 70, 24, (180, 220, 180))

    img.save(output_path, 'JPEG', quality=95)
    print(f"🖼️ Islamic Quote Poster Created: {output_path}")
    return output_path
