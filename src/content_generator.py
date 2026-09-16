"""
Islamic Content Generator for 'ঈমান' (iman24.bd)
Generates authentic Islamic reminders, Quranic verses, Hadith, Duas, and Friday specials in Bengali.
"""

import requests
import random
import os

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
GEMINI_MODELS = [
    "gemini-flash-latest",
    "gemini-2.5-flash-lite",
    "gemma-4-26b-a4b-it",
]

SYSTEM_PROMPT = """তুমি "ঈমান" ফেসবুক পেজের ইসলামিক কনটেন্ট রাইটার।
তোমার লক্ষ্য:
১. সম্পূর্ণ সহিহ কুরআন ও সুন্নাহ ভিত্তিক চমৎকার ও হৃদয়ছোঁয়া ভাষায় পোস্ট লেখা।
২. ভাষা হবে শান্ত, মার্জিত, শ্রদ্ধাশীল এবং খাঁটি বাংলা।
৩. প্রতিটি হাদিস বা আয়াতের সাথে স্পষ্ট রেফারেন্স (যেমন: সহিহ বুখারী, সূরা আল-ইমরান) উল্লেখ করবে।
৪. কোনো বিভ্রান্তিকর বা বিতর্কিত রাজনৈতিক বিষয় আলোচনা করবে না।
৫. পোস্টের শুরুতে সুন্দর ইসলামিক অভিবাদন (আসসালামু আলাইকুম ওয়া রাহমাতুল্লাহ) দেবে।
৬. ৫-৬টি ইসলামিক হ্যাশট্যাগ (#ঈমান #ইসলাম #হাদিস #কুরআন #দোয়া #ইসলামিকপোস্ট) দেবে।"""


def call_ai(prompt):
    if not GEMINI_API_KEY:
        return None

    full_prompt = SYSTEM_PROMPT + "\n\n" + prompt
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
    }
    headers = {"Content-Type": "application/json"}

    for model in GEMINI_MODELS:
        try:
            url = GEMINI_BASE + model + ":generateContent?key=" + GEMINI_API_KEY
            r = requests.post(url, json=payload, headers=headers, timeout=45)
            if r.status_code == 200:
                return r.json()['candidates'][0]['content']['parts'][0]['text']
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
হাদিসের আরবি ও বাংলা অর্থ এবং সঠিক কিতাবের রেফারেন্স উল্লেখ করো। শেষে আমল করার আহ্বান জানাও।"""
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
আয়াতের সহজ সরল বাংলা অনুবাদ ও বাস্তব জীবনে এর শিক্ষা তুলে ধরো।"""
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
আরবি টেক্সট, বাংলা উচ্চারণ ও বাংলা অর্থসহ স্পষ্ট করে সাজিয়ে দাও।"""
    return call_ai(prompt)


def generate_juma_post():
    """Friday Special Post"""
    prompt = """পবিত্র জুমার দিনের ফজিলত, সূরা কাহাফ তিলাওয়াত এবং দরূদ শরীফ পাঠের গুরুত্ব নিয়ে একটি বরকতময় জুমার শুভেচ্ছা পোস্ট লেখো।"""
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
