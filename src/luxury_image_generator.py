#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full-Bleed Luxury Islamic Post & Reel Generator for 'ঈমান' (iman24.bd)
======================================================================
Produces ultra-premium, magazine-style vertical Islamic posts (1080x1350):
- Uses 100% unique context-specific AI background per Hadith/Ayat (no recurring temple stock)
- Elegant dark atmospheric gradient vignette
- Authentic HarfBuzz shaped Bengali typography with champagne gold accents
- Clear hadith reference and sleek bottom CTA
"""

import os
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFilter
import uharfbuzz as hb
import freetype
import numpy as np

WORKSPACE_DIR = r"F:\fb_iman"
FONT_PATH = os.path.normpath(r"F:\fb\assets\fonts\NotoSansBengali-Bold.ttf")
if not os.path.exists(FONT_PATH):
    FONT_PATH = os.path.normpath(r"F:\fb\assets\fonts\HindSiliguri-Bold.ttf")
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/kalpurush.ttf"


def render_shaped_text(img, text, x_center, y_pos, font_size, color_rgb=(255, 255, 255)):
    if not os.path.exists(FONT_PATH):
        ImageDraw.Draw(img).text((x_center, y_pos), text, fill=color_rgb)
        return

    ft_face = freetype.Face(FONT_PATH)
    ft_face.set_char_size(font_size * 64)

    with open(FONT_PATH, 'rb') as f:
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
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gid = info.codepoint
        ft_face.load_glyph(gid, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING)
        slot = ft_face.glyph
        bitmap = slot.bitmap

        if bitmap.width > 0 and bitmap.rows > 0:
            bw, bh = bitmap.width, bitmap.rows
            buf_data = np.array(bitmap.buffer, dtype=np.uint8).reshape((bh, bw))
            alpha_img = Image.fromarray(buf_data, mode='L')

            glyph_color = Image.new('RGBA', (bw, bh), (*color_rgb, 255))
            glyph_color.putalpha(alpha_img)

            gx = int(curr_x + slot.bitmap_left)
            gy = int(y_pos - slot.bitmap_top)
            img.paste(glyph_color, (gx, gy), glyph_color)

        curr_x += pos.x_advance * scale


def create_luxury_islamic_post(bg_path, subheader, quote_title, reference, output_path):
    """
    Creates an ultra-premium full-bleed open Islamic post (1080x1350).
    """
    w, h = 1080, 1350

    # 1. Base Image Handling
    if bg_path and os.path.exists(bg_path):
        base = Image.open(bg_path).convert('RGB')
        # Center crop to 1080x1350 (4:5 ratio)
        bw, bh = base.size
        target_ratio = w / h
        if bw / bh > target_ratio:
            new_w = int(bh * target_ratio)
            offset_x = (bw - new_w) // 2
            base = base.crop((offset_x, 0, offset_x + new_w, bh))
        else:
            new_h = int(bw / target_ratio)
            offset_y = (bh - new_h) // 2
            base = base.crop((0, offset_y, bw, offset_y + new_h))
        canvas = base.resize((w, h), Image.Resampling.LANCZOS)
    else:
        canvas = Image.new('RGB', (w, h), (8, 22, 16))

    # 2. Cinematic Atmospheric Vignette (Full Bleed Depth)
    vignette = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    
    # Top soft darkening
    for y in range(350):
        alpha = int(220 * (1 - y / 350) ** 1.3)
        v_draw.line([(0, y), (w, y)], fill=(4, 12, 8, alpha))
        
    # Center text area gentle dark backing for 100% legibility
    center_backing = Image.new('RGBA', (w - 120, 680), (6, 16, 12, 185))
    center_backing = center_backing.filter(ImageFilter.GaussianBlur(25))
    vignette.paste(center_backing, (60, 320), center_backing)

    # Bottom darkening
    for y in range(850, h):
        alpha = int(245 * ((y - 850) / (h - 850)) ** 1.1)
        v_draw.line([(0, y), (w, y)], fill=(4, 10, 8, alpha))

    # Composite canvas
    canvas = Image.alpha_composite(canvas.convert('RGBA'), vignette).convert('RGBA')
    draw = ImageDraw.Draw(canvas)

    # Gold Colors
    GOLD_MAIN = (235, 200, 95)
    GOLD_SOFT = (212, 175, 55)
    WHITE_PURE = (255, 255, 255)

    # Thin luxury inner outline
    draw.rectangle([35, 35, w - 35, h - 35], outline=(*GOLD_SOFT, 120), width=1)

    # 1. Top Brand Pill Badge
    brand_w, brand_h = 320, 52
    brand_x = (w - brand_w) // 2
    brand_y = 75
    draw.rounded_rectangle([brand_x, brand_y, brand_x + brand_w, brand_y + brand_h], radius=16, fill=(8, 24, 16, 230), outline=(*GOLD_MAIN, 180), width=1)
    render_shaped_text(canvas, "ঈমান  •  iman24.bd", w // 2, brand_y + 36, 26, color_rgb=GOLD_MAIN)

    # 2. Subheader (e.g. রাসূলুল্লাহ (সা.) ইরশাদ করেছেন:)
    clean_sub = subheader.replace('', '').replace('[SUCCESS]', '').replace('ﷺ', '(সা.)').strip()
    render_shaped_text(canvas, clean_sub, w // 2, 230, 36, color_rgb=(210, 235, 220))

    # Decorative Gold Divider
    div_y = 270
    draw.line([(w // 2 - 140, div_y), (w // 2 + 140, div_y)], fill=(*GOLD_MAIN, 180), width=2)
    draw.polygon([(w // 2, div_y - 4), (w // 2 + 4, div_y), (w // 2, div_y + 4), (w // 2 - 4, div_y)], fill=GOLD_MAIN)

    # 3. Core Hadith / Ayat Quote
    clean_quote = quote_title.replace('«', '').replace('»', '').replace('"', '').strip()
    q_len = len(clean_quote)
    if q_len <= 50:
        wrap_w = 20
        font_sz = 48
        spacing = 86
        y_start = 430
    elif q_len <= 90:
        wrap_w = 23
        font_sz = 42
        spacing = 76
        y_start = 400
    elif q_len <= 140:
        wrap_w = 26
        font_sz = 36
        spacing = 68
        y_start = 370
    else:
        wrap_w = 28
        font_sz = 33
        spacing = 60
        y_start = 350

    wrapped = textwrap.fill(clean_quote, width=wrap_w)
    lines = [l.strip() for l in wrapped.split('\n') if l.strip()]

    for i, line in enumerate(lines[:8]):
        render_shaped_text(canvas, line, w // 2, y_start + i * spacing, font_sz, color_rgb=WHITE_PURE)

    # 4. Clean Reference
    ref_y = y_start + len(lines[:8]) * spacing + 50
    if reference:
        clean_ref = f"— {reference.strip()}"
        render_shaped_text(canvas, clean_ref, w // 2, ref_y, 32, color_rgb=GOLD_MAIN)

    # 5. Bottom CTA Pill Button
    btn_w = 460
    btn_h = 58
    btn_y = 1140
    btn_x = (w - btn_w) // 2
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=16, fill=(*GOLD_MAIN, 240))
    render_shaped_text(canvas, "বিস্তারিত ক্যাপশনে পড়ুন", w // 2, btn_y + 42, 28, color_rgb=(10, 25, 16))

    # 6. Bottom Tagline
    render_shaped_text(canvas, "শান্তি ও হেদায়েতের পথে প্রতিদিনের পাথেয়", w // 2, h - 80, 24, color_rgb=(180, 215, 195))

    canvas.convert('RGB').save(output_path, 'JPEG', quality=95)
    print(f"[SUCCESS] Luxury Islamic Post Created: {output_path}")
    return output_path
