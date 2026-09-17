#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ঈমান (iman24.bd) — Islamic Auto Poster
=======================================
Daily Authentic Islamic Posts (Hadith, Quran, Duas, Juma Specials)
Runs via GitHub Actions 3x daily in serene Islamic Green Aesthetics!
"""

import os
import sys
import random
from datetime import datetime
import tempfile

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from src.content_generator import generate_islamic_post
from src.image_generator import create_islamic_image
from src.fb_poster import FacebookPoster

FB_PAGE_ID = os.environ.get('FB_PAGE_ID', '104957755550666')
FB_PAGE_ACCESS_TOKEN = os.environ.get('FB_PAGE_ACCESS_TOKEN', '')

IMAGE_TEMP_PATH = os.path.join(tempfile.gettempdir(), "iman_post.jpg")


def extract_islamic_quote_and_ref(content: str):
    """
    Extract core Hadith / Quran quote, reference, and subheader from post:
    - subheader: রাসূলুল্লাহ (ﷺ) বলেছেন: / পবিত্র কুরআনে ইরশাদ হয়েছে: / আল্লাহর রাসূল বলেছেন:
    - quote: মূল হাদিসের বাংলা বাণী বা অর্থ
    - reference: সূত্র বা কিতাবের নাম
    """
    subheader = "রাসূলুল্লাহ (ﷺ) বলেছেন:"
    quote = ""
    reference = ""

    lines = [l.strip() for l in content.split('\n') if l.strip()]

    for line in lines:
        # Check subheader
        if any(w in line for w in ['বলেছেন:', 'ইরশাদ হয়েছে:', 'ফরমান:', 'ইরশাদ করেন:']):
            clean_sub = line.replace('«', '').replace('»', '').replace('*', '').strip()
            # remove salam if attached
            if not any(s in clean_sub for s in ['আসসালামু', 'আলাইকুম']):
                subheader = clean_sub[:45]
                break

    # Look for the core quote (after অর্থ: or in quotation marks)
    for line in lines:
        if 'অর্থ:' in line or 'অর্থ :' in line:
            quote = line.split(':', 1)[1].replace('"', '').replace('«', '').replace('»', '').strip()
            break
        elif line.startswith('"') and line.endswith('"') and len(line) > 15:
            quote = line.replace('"', '').strip()
            break

    # If quote not found by prefix, find the primary message line
    if not quote:
        for line in lines:
            if any(s in line for s in ['আসসালামু', 'আলাইকুম', 'প্রিয়', 'ভাই ও বোনেরা', 'বিসমিল্লাহ', '#', 'শেয়ার']):
                continue
            if any('\u0600' <= c <= '\u06FF' for c in line): # skip raw Arabic
                continue
            if 15 < len(line) < 120:
                quote = line.replace('*', '').replace('"', '').strip()
                break

    if not quote:
        quote = "উত্তম চরিত্র ও সুন্দর ব্যবহারের চেয়ে ভারী আমল আর কিছু নেই।"

    # Look for reference
    for line in lines:
        if any(w in line for w in ['সূত্র:', 'সূত্র :', 'সহিহ বুখারী', 'সহিহ মুসলিম', 'সুনানে', 'তিরমিযী', 'সূরা ']):
            clean_ref = line.replace('(', '').replace(')', '').replace('সূত্র:', '').strip()
            # take first 40 chars
            reference = clean_ref[:45]
            break

    return subheader, quote[:110], reference


def run(post_slot: int = 1):
    print("\n" + "═" * 55)
    print("🌙  ঈমান (iman24.bd) — Islamic Auto Poster")
    print(f"⏰  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)")
    print("═" * 55 + "\n")

    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("❌ Missing credentials!")
        sys.exit(1)

    fb = FacebookPoster(FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN)
    if not fb.verify_token():
        sys.exit(1)

    slot_types = {1: 'hadith', 2: 'quran', 3: 'dua'}
    post_type = slot_types.get(post_slot, random.choice(['hadith', 'quran', 'dua']))

    print(f"📖 Generating Islamic post ({post_type})...")
    content = generate_islamic_post(post_type)
    if not content:
        content = "আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহ। প্রতিটি মুহূর্তে আল্লাহর শুকরিয়া আদায় করুন। আলহামদুলিল্লাহ।"

    print(f"\n📄 Preview:\n{content[:200]}...\n")

    subheader, core_quote, reference = extract_islamic_quote_and_ref(content)
    print(f"🎯 Subheader: {subheader}")
    print(f"📜 Core Quote: {core_quote}")
    print(f"📚 Reference: {reference}")

    create_islamic_image(core_quote, output_path=IMAGE_TEMP_PATH, reference=reference, subheader=subheader)

    print("📤 Posting with Islamic Green Image...")
    post_id = fb.post_with_image(content, IMAGE_TEMP_PATH)
    if not post_id:
        print("⚠️ Image post failed, trying text...")
        post_id = fb.post_text(content)

    if os.path.exists(IMAGE_TEMP_PATH):
        os.remove(IMAGE_TEMP_PATH)

    if post_id:
        print(f"✅ SUCCESS! Post ID: {post_id}")
        fb.post_comment(
            post_id,
            "📌 পোস্টটি ভালো লাগলে সদকায়ে জারিয়ার নিয়তে শেয়ার করে দ্বীনের দাওয়াত ছড়িয়ে দিন। পেজটি ফলো দিয়ে সাথে থাকুন। জাযাকাল্লাহু খাইরান! 💚"
        )
    else:
        print("❌ Post failed!")
        sys.exit(1)


if __name__ == "__main__":
    slot = int(os.environ.get('POST_SLOT', random.randint(1, 3)))
    run(slot)
