"""
Islamic Content Generator for 'ঈমান' (iman24.bd)
Generates authentic Islamic reminders, Quranic verses, Hadith, Duas, and Friday specials in Bengali.
"""

import requests
import random
import re
import os

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
GEMINI_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
]

SYSTEM_PROMPT = """তুমি "ঈমান" ফেসবুক পেজের ইসলামিক কনটেন্ট রাইটার।
তোমার লক্ষ্য:
১. সম্পূর্ণ সহিহ কুরআন ও সুন্নাহ ভিত্তিক চমৎকার ও হৃদয়ছোঁয়া ভাষায় খাঁটি বাংলায় ফেসবুক পোস্ট তৈরি করা।
২. কোনো প্রকার ইংরেজি চিন্তা, ইংরেজি হেডিং, প্ল্যানিং নোট বা ড্রাফটিং লেখা যাবে না। সরাসরি চূড়ান্ত পোস্টের বাংলা টেক্সটটি আউটপুট হিসেবে দেবে।
৩. প্রতিটি হাদিস বা আয়াতের সাথে স্পষ্ট রেফারেন্স (যেমন: সহিহ বুখারী, সূরা আল-ইমরান) উল্লেখ করবে।
৪. পোস্টের শুরুতে 'আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহ' দিয়ে শুরু করবে।
৫. শেষে ৫-৬টি ইসলামিক হ্যাশট্যাগ (#ঈমান #ইসলাম #হাদিস #কুরআন #দোয়া #ইসলামিকপোস্ট) দেবে।"""


def sanitize_post(text):
    """Clean any accidental internal model thinking / reasoning notes"""
    if not text:
        return text
    # Remove lines containing English planning keywords
    cleaned_lines = []
    skip_mode = False
    for line in text.split('\n'):
        l_strip = line.strip()
        # If line contains English planning phrases, skip it
        if any(marker in l_strip for marker in [
            'Idea 1:', 'Idea 2:', 'Idea 3:', 'Decision:', 'Hadith Selection:',
            'Refined selection', 'Greeting:', 'Hook (Intro):', 'Drafting (Mental):',
            'Drafting:', 'Call to Action (Amal):', 'Reflection/Expansion', 'The Hadith (Arabic'
        ]):
            continue
        if re.match(r'^\s*\*\s*\*(Idea|Decision|Refined|Greeting|Hook|Drafting|Call to Action)', l_strip):
            continue
        # Also skip English system-like descriptions at the top
        if 'Islamic Content Writer' in l_strip or 'Facebook page "ঈমান"' in l_strip or 'Authentic (Sahih)' in l_strip:
            continue
        cleaned_lines.append(line)

    result = '\n'.join(cleaned_lines).strip()
    return result


def call_ai(prompt):
    if not GEMINI_API_KEY:
        return None

    full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 2500}
    }
    headers = {"Content-Type": "application/json"}

    for model in GEMINI_MODELS:
        try:
            url = GEMINI_BASE + model + ":generateContent?key=" + GEMINI_API_KEY
            r = requests.post(url, json=payload, headers=headers, timeout=25)
            if r.status_code == 200:
                raw_text = r.json()['candidates'][0]['content']['parts'][0]['text']
                return sanitize_post(raw_text)
            print(f"⚠️ {model} returned status: {r.status_code}")
        except Exception as e:
            print(f"⚠️ Error {model}: {e}")

    return None


def generate_hadith_post():
    """Morning: Sahih Hadith with Reference"""
    topics = [
        "সৎ চরিত্র ও মিষ্টি কথার গুরুত্ব সম্পর্কে সহিহ হাদিস",
        "বিপদ ও পেরেশানিতে ধৈর্য ধারণের ফজিলত",
        "প্রতিবেশীর অধিকার ও পিতা-মাতার খেদমত",
        "রিজিক বৃদ্ধি ও বরকতের সহজ আমল",
        "তাহাজ্জুদ ও ফজরের নামাজের ফজিলত",
    ]
    topic = random.choice(topics)
    prompt = f"""'{topic}' বিষয়ে একটি মন ছুঁয়ে যাওয়া সহিহ হাদিসের ফেসবুক পোস্ট লেখো।
হাদিসের আরবি ও বাংলা অর্থ এবং সঠিক কিতাবের রেফারেন্স উল্লেখ করো।
শুধুমাত্র পোস্টের খাঁটি বাংলা টেক্সট দেবে। কোনো প্ল্যানিং বা ড্রাফট নোট লিখবে না।"""
    return call_ai(prompt)


def generate_quran_verse_post():
    """Noon / Afternoon: Quranic Verse & Tafsir lesson"""
    topics = [
        "আল্লাহর রহমত থেকে নিরাশ না হওয়ার নির্দেশ (সূরা যুমার)",
        "কষ্টের পরেই রয়েছে স্বস্তি (সূরা ইনশিরাহ)",
        "সবর ও সালাতের মাধ্যমে সাহায্য প্রার্থনা (সূরা বাকারা)",
        "আল্লাহর উপর পূর্ণ তাওয়াক্কুল বা ভরসার শক্তি",
    ]
    topic = random.choice(topics)
    prompt = f"""'{topic}' বিষয়ে পবিত্র কুরআনের আয়াত দিয়ে একটি সুন্দর শিক্ষণীয় ফেসবুক পোস্ট লেখো।
আয়াতের সহজ সরল বাংলা অনুবাদ ও বাস্তব জীবনে এর শিক্ষা তুলে ধরো।
শুধুমাত্র পোস্টের খাঁটি বাংলা টেক্সট দেবে। কোনো প্ল্যানিং বা ড্রাফট নোট লিখবে না।"""
    return call_ai(prompt)


def generate_dua_and_dhikr_post():
    """Evening: Daily Essential Duas & Dhikr"""
    topics = [
        "ঋণ ও দুশ্চিন্তা থেকে মুক্তির দোয়া",
        "ঘরে প্রবেশের ও বের হওয়ার সুন্নত আমল ও দোয়া",
        "সাইয়্যিদুল ইস্তিগফারের ফজিলত ও বাংলা উচ্চারণ",
        "ঘুমানোর আগের সুন্নত দোয়া ও সুরক্ষার আমল",
    ]
    topic = random.choice(topics)
    prompt = f"""'{topic}' বিষয়ে একটি অতি প্রয়োজনীয় দোয়ার পোস্ট লেখো।
আরবি টেক্সট, বাংলা উচ্চারণ ও বাংলা অর্থসহ স্পষ্ট করে সাজিয়ে দাও।
শুধুমাত্র পোস্টের খাঁটি বাংলা টেক্সট দেবে। কোনো প্ল্যানিং বা ড্রাফট নোট লিখবে না।"""
    return call_ai(prompt)


def generate_juma_post():
    """Friday Special Post"""
    prompt = """পবিত্র জুমার দিনের ফজিলত, সূরা কাহাফ তিলাওয়াত এবং দরূদ শরীফ পাঠের গুরুত্ব নিয়ে একটি বরকতময় জুমার শুভেচ্ছা পোস্ট লেখো।
শুধুমাত্র পোস্টের খাঁটি বাংলা টেক্সট দেবে। কোনো প্ল্যানিং বা ড্রাফট নোট লিখবে না।"""
    return call_ai(prompt)


def generate_islamic_post(post_type=None):
    if not post_type:
        post_type = random.choice(['hadith', 'quran', 'dua'])

    if post_type == 'hadith':
        return generate_hadith_post()
    elif post_type == 'quran':
        return generate_quran_verse_post()
    else:
        return generate_dua_and_dhikr_post()
