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


def extract_title(content):
    for line in content.split('\n'):
        clean = line.strip()
        for ch in ['🌙', '✨', '🕌', '📖', '🤲', '📌', '⭐', '👉', '💚']:
            clean = clean.replace(ch, '')
        clean = clean.strip().lstrip('#').strip()
        if 8 < len(clean) < 100:
            return clean
    return "আল্লাহর রহমত থেকে নিরাশ হয়ো না"


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

    title = extract_title(content)
    create_islamic_image(title, output_path=IMAGE_TEMP_PATH)

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
