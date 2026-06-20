import time
import requests
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from instagrapi import Client

# ==================== دور زدن سرور رندر ====================
# این بخش فقط برای این است که سرور رندر به ما پلن رایگان بدهد
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is ON!")

def keep_alive():
    port = int(os.environ.get('PORT', 8080))
    HTTPServer(('0.0.0.0', port), DummyHandler).serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
# ===========================================================

TELEGRAM_BOT_TOKEN = '8748534577:AAFuAgh0HPGKAnrU1572y1DJhMILqg3F698'
SESSION_ID = '79922557562%3AcYoFFkJ38uT4Lv%3A25%3AAYgxOIiZE-83NTE3lzmRI5hmgj8LHSLdmL7mpQdpcg'

ACCOUNTS_MAPPING = {
    'amirkhani_84': -1003929729813,
    'Abolfazl | Amirkhani': -1003929729813,
    'entrepreneur8880n': -1004479685723,
    'Ggv': -1004479685723
}

def send_video_perfectly(chat_id, instagram_url):
    try:
        print("⏳ در حال دریافت ویدیو از واسطه...")
        api_url = "https://api.cobalt.tools/api/json"
        payload = {"url": instagram_url, "vQuality": "720"}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        response = requests.post(api_url, json=payload, headers=headers).json()
        
        if 'url' in response:
            video_url = response['url']
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
            res = requests.post(tg_url, data={'chat_id': chat_id, 'video': video_url, 'caption': "✅ دانلود شده توسط سرور ابری"}).json()
            if res.get('ok'): print("✅ فیلم به تلگرام ارسال شد.")
        else:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                          data={'chat_id': chat_id, 'text': f"مشاهده مستقیم:\n{instagram_url}"})
    except Exception:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"لینک:\n{instagram_url}"})

print("🚀 در حال روشن کردن موتور ربات روی سرور رایگان رندر...")
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID.strip())
    print("✅ اتصال نامرئی به اینستاگرام برقرار شد!")
except Exception as e:
    print(f"❌ خطای اتصال: {e}")
    exit()

last_processed_msg_ids = {}

while True:
    try:
        threads = cl.direct_threads()
        for thread in threads:
            for user in thread.users:
                target_id = ACCOUNTS_MAPPING.get(user.username) or ACCOUNTS_MAPPING.get(user.full_name)
                if target_id and thread.messages:
                    msg = thread.messages[0]
                    if user.username not in last_processed_msg_ids:
                        last_processed_msg_ids[user.username] = msg.id
                        continue

                    if msg.id != last_processed_msg_ids[user.username]:
                        last_processed_msg_ids[user.username] = msg.id
                        
                        link = None
                        if hasattr(msg, 'clip') and msg.clip: link = f"https://www.instagram.com/reel/{msg.clip.code}/"
                        elif hasattr(msg, 'media_share') and msg.media_share: link = f"https://www.instagram.com/p/{msg.media_share.code}/"
                        
                        if link: send_video_perfectly(target_id, link)
    except: pass
    time.sleep(60)
