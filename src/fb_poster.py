"""
Facebook Poster Module for Iman page
"""
import requests
import json


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
