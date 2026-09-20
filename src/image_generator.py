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
    Generate Soul-Soothing, Mood-Refreshing 4:5 Mobile Islamic Reminder Poster (1080x1350).
    Features high-res peaceful visuals (Madinah, Makkah, calm mosque, morning Quran, tranquil nature)
    with an elegant dark glassmorphism card highlighting the core Hadith/Ayat.
    """
    w, h = 1080, 1350
    gold = random.choice(GOLD_ACCENTS)

    # 1. Select a peaceful aesthetic background
    bg_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'backgrounds')
    selected_bg = None
    if os.path.exists(bg_dir):
        bg_files = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if bg_files:
            selected_bg = os.path.join(bg_dir, random.choice(bg_files))

    # Fallback to single bg if directory missing
    if not selected_bg:
        single_bg = os.path.join(os.path.dirname(__file__), '..', 'assets', 'islamic_bg.jpg')
        if os.path.exists(single_bg):
            selected_bg = single_bg

    if selected_bg and os.path.exists(selected_bg):
        try:
            base = Image.open(selected_bg).convert('RGB')
            base = base.resize((w, h), Image.Resampling.LANCZOS)
        except Exception:
            base = Image.new('RGB', (w, h), (5, 25, 15))
            draw_gradient(base, random.choice(BG_GRADIENTS)[0], random.choice(BG_GRADIENTS)[1])
    else:
        base = Image.new('RGB', (w, h), (5, 25, 15))
        draw_gradient(base, random.choice(BG_GRADIENTS)[0], random.choice(BG_GRADIENTS)[1])

    # 2. Add Mood-Refreshing Vignette & Glassmorphism Overlay
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # Top atmospheric gradient
    for y in range(260):
        alpha = int(150 * (1 - y / 260))
        ov_draw.line([(0, y), (w, y)], fill=(8, 18, 12, alpha))

    # Card dimensions (Centered, golden framed, frosted glass)
    box_w = 940
    box_top = 340
    box_bottom = 980
    box_left = (w - box_w) // 2
    box_right = (w + box_w) // 2

    # Frosted dark emerald/charcoal container with rich opacity for crystal clear text
    ov_draw.rounded_rectangle(
        [box_left, box_top, box_right, box_bottom],
        radius=24,
        fill=(6, 20, 15, 218),
        outline=(*gold[:3], 225),
        width=3
    )

    # Bottom atmospheric gradient
    for y in range(1140, h):
        alpha = int(185 * ((y - 1140) / 210))
        ov_draw.line([(0, y), (w, y)], fill=(5, 15, 10, alpha))

    img = Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Islamic Double Border
    draw.rectangle([30, 30, w - 30, h - 30], outline=gold, width=2)
    draw.rectangle([38, 38, w - 38, h - 38], outline=(*gold[:3],), width=1)

    # Corner Islamic Diamonds
    for (cx, cy) in [(38, 38), (w - 38, 38), (38, h - 38), (w - 38, h - 38)]:
        draw.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], fill=gold)

    # 1. Page Header Badge
    render_shaped_text(img, "ঈমান  |  iman24.bd", w // 2, 90, 30, gold)

    # 2. Subheader (e.g. রাসূলুল্লাহ (সা.) ইরশাদ করেছেন:)
    clean_sub = subheader.replace('🌙', '').replace('✨', '').replace('ﷺ', '(সা.)')
    clean_sub = clean_sub.replace('((সা.))', '(সা.)').replace('((সা.))', '(সা.)').strip()
    render_shaped_text(img, clean_sub, w // 2, 185, 42, (255, 255, 255))

    # 3. Core Hadith / Ayat Quote
    clean_quote = quote_title.replace('«', '').replace('»', '').replace('"', '').strip()
    
    # Adaptive wrap width & sizing based on quote length
    quote_len = len(clean_quote)
    if quote_len <= 50:
        wrap_w = 18
        font_size_quote = 48
        line_spacing = 88
        y_quote_start = box_top + 130
    elif quote_len <= 90:
        wrap_w = 22
        font_size_quote = 42
        line_spacing = 76
        y_quote_start = box_top + 100
    elif quote_len <= 130:
        wrap_w = 25
        font_size_quote = 36
        line_spacing = 66
        y_quote_start = box_top + 80
    else:
        wrap_w = 27
        font_size_quote = 33
        line_spacing = 58
        y_quote_start = box_top + 65

    wrapped = textwrap.fill(clean_quote, width=wrap_w)
    lines = [l.strip() for l in wrapped.split('\n') if l.strip()]

    for i, line in enumerate(lines[:8]):
        render_shaped_text(img, line, w // 2, y_quote_start + i * line_spacing, font_size_quote, (255, 255, 255))


    # 4. Clear Reference inside the box
    if reference:
        clean_ref = f"— {reference.strip()}"
        render_shaped_text(img, clean_ref, w // 2, box_bottom - 60, 32, gold)

    # 5. Curiosity Hook & CTA Pill Button
    btn_w = 480
    btn_h = 60
    btn_y = 1040
    draw.rounded_rectangle([(w - btn_w) // 2, btn_y, (w + btn_w) // 2, btn_y + btn_h], radius=16, fill=gold)
    render_shaped_text(img, "বিস্তারিত ক্যাপশনে পড়ুন", w // 2, btn_y + 44, 30, (15, 30, 20))

    # 6. Bottom Footer Tagline
    render_shaped_text(img, "শান্তি ও হেদায়েতের পথে প্রতিদিনের পাথেয়", w // 2, h - 70, 26, (225, 240, 225))

    img.save(output_path, 'JPEG', quality=95)
    print(f"[OK] Soul-Refreshing Islamic Poster Created: {output_path}")
    return output_path

