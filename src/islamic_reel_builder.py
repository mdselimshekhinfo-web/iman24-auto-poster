#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Islamic Reel Builder Module (Variant 2 & Variant 4)
Generates high-engagement Islamic reels:
1. Alem-Student Mentorship Dialogue (আলেম-শিক্ষার্থী ডায়লগ রিল)
2. Quran Reflection & Recitation (কোরআনের গভীর উপলব্ধি ও তিলাওয়াত রিল)
Features:
- Dual-character Bengali Neural Voiceover (edge-tts)
- Google Fonts 'Hind Siliguri' Glassmorphism typography via Chrome Headless
- Automated FFmpeg looping/mixing with background video and ambient audio
"""

import os
import sys
import asyncio
import subprocess
import tempfile
import edge_tts

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class IslamicReelBuilder:
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir or os.path.join(tempfile.gettempdir(), 'islamic_reels')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    async def generate_speech_audio(self, text: str, voice: str, output_path: str, pitch="0Hz", rate="0%"):
        communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
        await communicate.save(output_path)
        return output_path

    async def build_mentorship_audio(self, youth_question: str, scholar_answer: str, output_audio: str):
        """
        Synthesize dual-voice dialogue:
        1. Youth asking question (bn-IN-BashkarNeural / slightly energetic, earnest)
        2. Scholar answering with wisdom (bn-BD-PradeepNeural / warm, calm, deep)
        """
        youth_file = os.path.join(self.temp_dir, 'voice_youth.mp3')
        scholar_file = os.path.join(self.temp_dir, 'voice_scholar.mp3')
        
        await self.generate_speech_audio(youth_question, 'bn-IN-BashkarNeural', youth_file, pitch="+4Hz", rate="+2%")
        await self.generate_speech_audio(scholar_answer, 'bn-BD-PradeepNeural', scholar_file, pitch="-2Hz", rate="-4%")
        
        concat_txt = os.path.join(self.temp_dir, 'dialogue_concat.txt')
        with open(concat_txt, 'w', encoding='utf-8') as f:
            f.write(f"file '{youth_file.replace(os.sep, '/')}'\n")
            f.write(f"file '{scholar_file.replace(os.sep, '/')}'\n")
            
        cmd = [
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', concat_txt,
            '-c:a', 'libmp3lame', '-b:a', '128k',
            output_audio
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_audio

    def get_audio_duration(self, audio_path: str) -> float:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', audio_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())

    def render_overlay_html(self, topic_title: str, hadith_ref: str, category="ঈমান নসিহত") -> str:
        """
        Renders transparent PNG overlay with perfect Bengali typography (Hind Siliguri)
        """
        overlay_html_path = os.path.join(self.temp_dir, 'overlay_temp.html')
        overlay_png_path = os.path.join(self.temp_dir, 'overlay_temp.png')

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@600;700&display=swap');
  body {{
    margin: 0;
    width: 1080px;
    height: 1920px;
    background: transparent;
    font-family: 'Hind Siliguri', 'Nirmala UI', sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 80px 40px;
    box-sizing: border-box;
  }}
  .top-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }}
  .badge {{
    background: #F5B041;
    color: #000;
    font-size: 28px;
    font-weight: 700;
    padding: 8px 32px;
    border-radius: 50px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
  }}
  .title-card {{
    background: rgba(15, 23, 42, 0.88);
    border: 2px solid rgba(245, 176, 65, 0.6);
    color: #ffffff;
    font-size: 46px;
    font-weight: 700;
    padding: 20px 45px;
    border-radius: 22px;
    text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 35px rgba(0,0,0,0.6);
    line-height: 1.35;
  }}
  .bottom-card {{
    background: rgba(15, 23, 42, 0.88);
    border: 1.5px solid rgba(245, 176, 65, 0.5);
    color: #F5B041;
    font-size: 34px;
    font-weight: 600;
    padding: 16px 40px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  }}
</style>
</head>
<body>
  <div class="top-box">
    <div class="badge">{category}</div>
    <div class="title-card">{topic_title}</div>
  </div>
  <div class="bottom-card">{hadith_ref}</div>
</body>
</html>"""
        with open(overlay_html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        cmd = [
            CHROME_PATH,
            '--headless=new',
            '--default-background-color=00000000',
            f'--screenshot={overlay_png_path}',
            '--window-size=1080,1920',
            '--hide-scrollbars',
            overlay_html_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return overlay_png_path

    def create_mentorship_reel(
        self,
        bg_video_path: str,
        youth_question: str,
        scholar_answer: str,
        topic_title: str,
        hadith_ref: str,
        output_reel_path: str
    ):
        """
        Creates a complete Alem-Youth mentorship reel
        """
        audio_path = os.path.join(self.temp_dir, 'dialogue_final.mp3')
        asyncio.run(self.build_mentorship_audio(youth_question, scholar_answer, audio_path))
        
        duration = self.get_audio_duration(audio_path) + 1.0 # 1 sec buffer
        overlay_png = self.render_overlay_html(topic_title, hadith_ref, category="ঈমান নসিহত")

        filter_complex = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];[bg][1:v]overlay=0:0[vout]"

        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1', '-i', bg_video_path,
            '-i', overlay_png,
            '-i', audio_path,
            '-t', str(duration),
            '-filter_complex', filter_complex,
            '-map', '[vout]',
            '-map', '2:a',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '22', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k',
            '-shortest',
            output_reel_path
        ]

        print(f"Rendering Alem-Youth Mentorship Reel: {os.path.basename(output_reel_path)}")
        subprocess.run(cmd, check=True)
        print(f"SUCCESS: Generated {output_reel_path} (Duration: {duration:.1f}s)")
        return output_reel_path

    def render_quran_overlay_html(self, surah_ref: str, arabic_verse: str, bangla_meaning: str) -> str:
        """
        Renders transparent PNG overlay for Quran Reflection reels
        """
        overlay_html_path = os.path.join(self.temp_dir, 'quran_overlay.html')
        overlay_png_path = os.path.join(self.temp_dir, 'quran_overlay.png')

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Hind+Siliguri:wght@600;700&display=swap');
  body {{
    margin: 0;
    width: 1080px;
    height: 1920px;
    background: transparent;
    font-family: 'Hind Siliguri', 'Nirmala UI', sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 80px 40px;
    box-sizing: border-box;
  }}
  .top-box {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    width: 100%;
  }}
  .badge {{
    background: #10B981;
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    padding: 8px 32px;
    border-radius: 50px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
  }}
  .verse-card {{
    background: rgba(15, 23, 42, 0.90);
    border: 2px solid rgba(16, 185, 129, 0.6);
    padding: 25px 40px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 10px 35px rgba(0,0,0,0.6);
    width: 90%;
  }}
  .arabic {{
    font-family: 'Amiri', 'Traditional Arabic', serif;
    font-size: 44px;
    color: #F5B041;
    line-height: 1.5;
    direction: rtl;
    margin-bottom: 15px;
  }}
  .meaning {{
    font-size: 36px;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.4;
  }}
  .bottom-card {{
    background: rgba(15, 23, 42, 0.88);
    border: 1.5px solid rgba(16, 185, 129, 0.5);
    color: #10B981;
    font-size: 34px;
    font-weight: 600;
    padding: 16px 40px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  }}
</style>
</head>
<body>
  <div class="top-box">
    <div class="badge">কোরআনের উপলব্ধি</div>
    <div class="verse-card">
      <div class="arabic">{arabic_verse}</div>
      <div class="meaning">« {bangla_meaning} »</div>
    </div>
  </div>
  <div class="bottom-card">{surah_ref}</div>
</body>
</html>"""
        with open(overlay_html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        cmd = [
            CHROME_PATH,
            '--headless=new',
            '--default-background-color=00000000',
            f'--screenshot={overlay_png_path}',
            '--window-size=1080,1920',
            '--hide-scrollbars',
            overlay_html_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return overlay_png_path

    def create_quran_reflection_reel(
        self,
        bg_video_path: str,
        voiceover_text: str,
        surah_ref: str,
        arabic_verse: str,
        bangla_meaning: str,
        output_reel_path: str
    ):
        """
        Creates a complete Quran reflection reel
        """
        audio_path = os.path.join(self.temp_dir, 'quran_audio.mp3')
        asyncio.run(self.generate_speech_audio(voiceover_text, "bn-BD-PradeepNeural", audio_path, pitch="-2Hz", rate="-4%"))
        
        duration = self.get_audio_duration(audio_path) + 1.0
        overlay_png = self.render_quran_overlay_html(surah_ref, arabic_verse, bangla_meaning)

        filter_complex = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];[bg][1:v]overlay=0:0[vout]"

        cmd = [
            'ffmpeg', '-y',
            '-stream_loop', '-1', '-i', bg_video_path,
            '-i', overlay_png,
            '-i', audio_path,
            '-t', str(duration),
            '-filter_complex', filter_complex,
            '-map', '[vout]',
            '-map', '2:a',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '22', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k',
            '-shortest',
            output_reel_path
        ]

        print(f"Rendering Quran Reflection Reel: {os.path.basename(output_reel_path)}")
        subprocess.run(cmd, check=True)
        print(f"SUCCESS: Generated {output_reel_path} (Duration: {duration:.1f}s)")
        return output_reel_path
