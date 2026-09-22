"""
Facebook Poster Module for Iman page
"""
import requests
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


class FacebookPoster:
    def __init__(self, page_id, access_token):
        self.page_id = page_id
        self.access_token = access_token
        self.api_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def verify_token(self):
        url = f"{self.base_url}/{self.page_id}"
        params = {'fields': 'id,name,fan_count,can_post', 'access_token': self.access_token}
        try:
            r = requests.get(url, params=params, timeout=15).json()
            if 'id' in r and r.get('can_post'):
                print(f"✅ Token OK! Page: {r.get('name')} | ID: {r.get('id')}")
                return True
            print(f"❌ Token error: {r}")
            return False
        except Exception as e:
            print(f"❌ Verify failed: {e}")
            return False

    def post_text(self, message):
        url = f"{self.base_url}/{self.page_id}/feed"
        payload = {'message': message, 'access_token': self.access_token}
        try:
            r = requests.post(url, data=payload, timeout=30).json()
            return r.get('id')
        except Exception as e:
            print(f"❌ Post text error: {e}")
            return None

    def post_with_image(self, message, image_path):
        url = f"{self.base_url}/{self.page_id}/photos"
        try:
            with open(image_path, 'rb') as f:
                payload = {'message': message, 'access_token': self.access_token}
                files = {'source': ('post.jpg', f, 'image/jpeg')}
                r = requests.post(url, data=payload, files=files, timeout=60).json()
                return r.get('id')
        except Exception as e:
            print(f"❌ Post image error: {e}")
            return None

    def post_comment(self, post_id, message):
        url = f"{self.base_url}/{post_id}/comments"
        payload = {'message': message, 'access_token': self.access_token}
        try:
            r = requests.post(url, data=payload, timeout=20).json()
            return r.get('id')
        except Exception:
            return None

    def post_reel(self, video_path, caption, scheduled_timestamp=None):
        """
        Uploads and publishes a Facebook Reel using the 3-phase video_reels API:
        1. Initialize upload session
        2. Stream binary video payload with offset & file_size
        3. Finish & Publish Reel
        """
        import os
        try:
            if not os.path.exists(video_path):
                print(f"❌ Video file not found: {video_path}")
                return None

            file_size = os.path.getsize(video_path)

            # Step 1: Start upload phase
            init_url = f"{self.base_url}/{self.page_id}/video_reels"
            init_payload = {
                'upload_phase': 'start',
                'access_token': self.access_token
            }
            init_res = requests.post(init_url, data=init_payload, timeout=30).json()
            video_id = init_res.get('video_id')
            upload_url = init_res.get('upload_url')

            if not upload_url or not video_id:
                print(f"❌ Failed to init reels upload: {init_res}")
                return None

            # Step 2: Upload binary bytes
            with open(video_path, 'rb') as f:
                video_data = f.read()

            upload_headers = {
                'Authorization': f'OAuth {self.access_token}',
                'offset': '0',
                'file_size': str(file_size)
            }
            upload_res = requests.post(upload_url, headers=upload_headers, data=video_data, timeout=120)
            if upload_res.status_code != 200:
                print(f"❌ Video binary upload failed: {upload_res.status_code} {upload_res.text}")
                return None

            # Step 3: Finish and Publish / Schedule
            finish_url = f"{self.base_url}/{self.page_id}/video_reels"
            finish_payload = {
                'upload_phase': 'finish',
                'access_token': self.access_token,
                'video_id': video_id,
                'description': caption
            }
            if scheduled_timestamp:
                finish_payload['video_state'] = 'SCHEDULED'
                finish_payload['scheduled_publish_time'] = str(scheduled_timestamp)
            else:
                finish_payload['video_state'] = 'PUBLISHED'

            finish_res = requests.post(finish_url, data=finish_payload, timeout=30).json()
            if finish_res.get('success'):
                status_txt = "Scheduled" if scheduled_timestamp else "Published"
                print(f"✅ Reel {status_txt} Successfully! Reel Video ID: {video_id}")
                return video_id
            else:
                print(f"❌ Failed to finish reels: {finish_res}")
                return None
        except Exception as e:
            print(f"❌ post_reel exception: {e}")
            return None

    def post_scheduled_image(self, message: str, image_path: str, scheduled_timestamp: int):
        """
        Upload photo as unpublished and schedule publish time (between 10 mins and 75-90 days in future)
        """
        url = f"{self.base_url}/{self.page_id}/photos"
        try:
            with open(image_path, 'rb') as img_file:
                payload = {
                    'message': message,
                    'published': 'false',
                    'scheduled_publish_time': str(scheduled_timestamp),
                    'access_token': self.access_token,
                }
                files = {'source': ('post_image.jpg', img_file, 'image/jpeg')}
                response = requests.post(url, data=payload, files=files, timeout=60)

            result = response.json()
            if 'id' in result:
                print(f"✅ Photo Scheduled successfully! ID: {result['id']} for unix timestamp: {scheduled_timestamp}")
                return result['id']
            else:
                print(f"❌ Scheduled image failed: {result.get('error', {}).get('message', result)}")
                return None
        except Exception as e:
            print(f"❌ Scheduled image error: {e}")
            return None

    def post_scheduled_reel(self, video_path: str, caption: str, scheduled_timestamp: int):
        """Uploads and schedules an Islamic Facebook Reel for future publishing"""
        return self.post_reel(video_path, caption, scheduled_timestamp=scheduled_timestamp)

