#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 21 Thematic Islamic Backgrounds for Week 2 using Google AI Pro (Imagen 3)
"""

import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from gemini_webapi import GeminiClient

PSID = 'g.a000CAnCpWbTgxaLbtUkAjmFHjAt_dSkNR1UUTHWGE_UHqrPUiuN4mt-NNHzw9EeELxOCEw37wACgYKAWESARYSFQHGX2MiiR5dzfxSUHwSkdcFq4Yu8BoVAUF8yKqUyJZLKcdt9RWBSkqdoI0-0076'
PSIDTS = 'sidts-CjIBXMw41RC0YrmIOS_MbANz7gq773Ulb57aJRYn1n4hpWXoYjaXkgsN4hXOXBDDZ4ijeBAA'

OUT_DIR = r"F:\fb_iman\assets\ai_backgrounds_week2"
os.makedirs(OUT_DIR, exist_ok=True)

ISLAMIC_POST_PROMPTS = [
    # Day 1
    {"slot": "iman_day1_slot1", "prompt": "An ancient open marble courtyard of an Islamic sanctuary at twilight, glowing lanterns, tranquil reflecting water fountain, cinematic lighting, 8k hyperrealistic"},
    {"slot": "iman_day1_slot3", "prompt": "A serene dawn horizon over desert dunes with soft golden morning sunlight, dramatic light rays breaking through clouds, symbolizing ease after hardship, photorealistic 8k"},
    {"slot": "iman_day1_slot5", "prompt": "A peaceful dark night room overlooking a glowing crescent moon through arched Islamic carved window, calm atmosphere, prayer rug, cinematic depth of field 8k"},
    # Day 2
    {"slot": "iman_day2_slot1", "prompt": "Majestic lush green mountain valley with tranquil crystal clear river and warm golden sunlight, symbolizing gratitude and patience in nature, photorealistic 8k"},
    {"slot": "iman_day2_slot3", "prompt": "An expansive calm ocean at sunrise with golden rays reflecting on gentle waves, representing complete trust in God (Tawakkul), majestic, photorealistic 8k"},
    {"slot": "iman_day2_slot5", "prompt": "Interior of a majestic grand mosque with soft ambient moonlight streaming through high stained-glass dome windows onto polished marble floor, 8k Octane render"},
    # Day 3
    {"slot": "iman_day3_slot1", "prompt": "A warm atmospheric gathering room with traditional Islamic lanterns, carved wooden doors and peaceful ambiance, symbolizing family bonding and kinship, 8k cinematic"},
    {"slot": "iman_day3_slot3", "prompt": "A majestic towering mountain peak under a dramatic starry sky with soft glowing clouds, representing patient endurance, epic cinematic photorealism 8k"},
    {"slot": "iman_day3_slot5", "prompt": "A quiet prayer hall before dawn (Tahajjud), soft warm candlelight, illuminated arched colonnade, peaceful spiritual sanctuary, 8k photorealistic"},
    # Day 4
    {"slot": "iman_day4_slot1", "prompt": "A serene tranquil garden with blooming white jasmine flowers and crystal stream under golden evening sunlight, representing truthfulness and good character, 8k"},
    {"slot": "iman_day4_slot3", "prompt": "Golden desert sand dunes at majestic sunset with dramatic sweeping shadows and radiant warm orange sky, cinematic composition 8k"},
    {"slot": "iman_day4_slot5", "prompt": "A warm glowing brass lantern hanging in a quiet stone archway at midnight, soft mist, peaceful contemplative night, 8k photorealistic"},
    # Day 5 (Friday)
    {"slot": "iman_day5_slot1", "prompt": "Grand courtyard of a magnificent white marble mosque on a bright blessed Friday morning, crystal clear blue sky, towering minarets, photorealistic 8k"},
    {"slot": "iman_day5_slot3", "prompt": "A beautiful open illuminated Quran stand in a quiet library corner with soft golden sunbeams streaming in, spiritual and peaceful, 8k photorealistic"},
    {"slot": "iman_day5_slot5", "prompt": "A serene tranquil river at sunset with lush olive trees and soft golden reflections, representing peace and divine blessings, 8k"},
    # Day 6
    {"slot": "iman_day6_slot1", "prompt": "A vibrant green oasis with date palms and flowing freshwater spring under a clear sky, symbolizing charity and abundant blessings, 8k photorealistic"},
    {"slot": "iman_day6_slot3", "prompt": "Calm peaceful misty forest at sunrise with radiant sunbeams filtering through ancient trees, representing hope and divine mercy, 8k photorealistic"},
    {"slot": "iman_day6_slot5", "prompt": "A tranquil starry night over a quiet oasis desert with glowing constellations, representing deep contemplation and Dhikr, 8k"},
    # Day 7
    {"slot": "iman_day7_slot1", "prompt": "A grand Islamic architectural archway leading to a radiant illuminated courtyard with tranquil fountain and lush palms, 8k photorealistic"},
    {"slot": "iman_day7_slot3", "prompt": "A serene mountain lake reflecting snow-capped peaks and clear twilight sky, representing pure inner peace and steadfast faith, 8k"},
    {"slot": "iman_day7_slot5", "prompt": "A peaceful prayer hall at dusk with soft amber lanterns hanging from high vaulted ceilings, profound serenity, 8k photorealistic"},
]

async def main():
    print("Initializing Gemini Client...", flush=True)
    client = GeminiClient(secure_1psid=PSID, secure_1psidts=PSIDTS)
    await client.init()
    print("Gemini Web Client initialized successfully.", flush=True)

    for idx, item in enumerate(ISLAMIC_POST_PROMPTS, 1):
        target_file = os.path.join(OUT_DIR, f"{item['slot']}.jpg")
        if os.path.exists(target_file) and os.path.getsize(target_file) > 10000:
            print(f"[{idx}/21] Already exists: {target_file}", flush=True)
            continue

        print(f"[{idx}/21] Generating {item['slot']}...", flush=True)
        try:
            resp = await client.generate_content(item['prompt'])
            if resp.images:
                temp_dir = os.path.join(OUT_DIR, f"temp_{item['slot']}")
                os.makedirs(temp_dir, exist_ok=True)
                await resp.images[0].save(temp_dir)
                
                # Check files in temp_dir
                saved_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for f in files:
                        if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                            saved_files.append(os.path.join(root, f))

                if saved_files:
                    from PIL import Image
                    im = Image.open(saved_files[0])
                    im.save(target_file, 'JPEG', quality=95)
                    print(f"[SUCCESS] [{idx}/21] Saved: {target_file} ({im.size})", flush=True)
                    
                    # Clean up temp
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                else:
                    print(f"[WARNING] [{idx}/21] No image file saved in temp for {item['slot']}", flush=True)
            else:
                print(f"[WARNING] [{idx}/21] No image returned in response for {item['slot']}", flush=True)
        except Exception as e:
            print(f"[ERROR] [{idx}/21] Error generating {item['slot']}: {e}", flush=True)
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
