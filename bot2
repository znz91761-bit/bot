import time
import requests
from instagrapi import Client

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
        print(f"⏳ در حال دانلود ویدیو از طریق سرور واسطه...")
        api_url = "https://api.cobalt.tools/api/json"
        payload = {"url": instagram_url, "vQuality": "720"}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = requests.post(api_url, json=payload, headers=headers).json()
        
        if 'url' in response:
            video_url = response['url']
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
            res = requests.post(tg_url, data={'chat_id': chat_id, 'video': video_url, 'caption': "✅ دانلود شده توسط سرور ابری"}).json()
            
            if res.get('ok'):
                print("✅ فیلم با موفقیت به تلگرام ارسال شد.")
            else:
                print(f"❌ خطای تلگرام در دریافت فیلم: {res}")
        else:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                          data={'chat_id': chat_id, 'text': f"مشاهده مستقیم در اینستاگرام:\n{instagram_url}"})
    except Exception as e:
        print(f"❌ خطای سرور دانلود: {e}")
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      data={'chat_id': chat_id, 'text': f"لینک اصلی (خطا در دانلود):\n{instagram_url}"})

print("🚀 در حال روشن کردن موتور ربات روی سرور ابری...")
cl = Client()
try:
    cl.login_by_sessionid(SESSION_ID.strip())
    print("✅ اتصال نامرئی به اینستاگرام برقرار شد!")
except Exception as e:
    print(f"❌ خطای اتصال به اینستاگرام: {e}")
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
                        print(f"✅ مانیتورینگ برای [{user.username}] فعال شد.")
                        continue

                    if msg.id != last_processed_msg_ids[user.username]:
                        last_processed_msg_ids[user.username] = msg.id
                        print(f"\n🔔 پیام جدید از [{user.username}] دریافت شد.")
                        
                        link = None
                        if hasattr(msg, 'clip') and msg.clip: 
                            link = f"https://www.instagram.com/reel/{msg.clip.code}/"
                        elif hasattr(msg, 'media_share') and msg.media_share: 
                            link = f"https://www.instagram.com/p/{msg.media_share.code}/"
                        
                        if link:
                            send_video_perfectly(target_id, link)
                        elif msg.text:
                            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                                          data={'chat_id': target_id, 'text': f"متن دریافتی:\n{msg.text}"})
    except Exception as e:
        print(f"⚠️ در حال بررسی مجدد شبکه... ({e})")
    time.sleep(60)
