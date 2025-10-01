import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load env variables
load_dotenv()
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

# Configure Google Generative AI
genai.configure(api_key=AI_API_KEY)
# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)
def generate_sqa_post():
    prompt = """একটি 5-10 লাইনের মজার গল্প বাংলায় লিখো (tone: friendly, সহজে পড়ার মতো)।
গল্পের শেষে একটি মজার প্রশ্ন থাকবে, যাতে পাঠক অংশ নিতে আগ্রহী হয়।

➤ দৈর্ঘ্য: 5-10 লাইন (সংক্ষিপ্ত ও আকর্ষণীয়)
➤ ফরম্যাট: সোশ্যাল মিডিয়া পোস্টের মতো হবে
➤ আউটপুট অবশ্যই ছোট ছোট প্যারাগ্রাফ আকারে (প্রতি 1-2 লাইন আলাদা প্যারা করে দাও)
➤ ভাষা: অবশ্যই বাংলায় লিখবে
➤ লেখার মধ্যে উপযুক্ত স্থানে ইমোজি ব্যবহার করবে
➤ Hashtags: মোট 7-10টি, এর মধ্যে অবশ্যই থাকবে #hyeyou

⚠️ কেবলমাত্র পোস্ট কনটেন্ট রিটার্ন করবে (কোনো অতিরিক্ত ব্যাখ্যা নয়)।
"""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {"message": message, "access_token": FB_ACCESS_TOKEN}
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        print("🚀 Generating new SQA post...")
        message = generate_sqa_post()
        print("✅ Post generated successfully!")

        print("📤 Posting to Facebook...")
        result = post_to_facebook(message)
        print(f"✅ Post published! Post ID: {result.get('id')}")
        
        # Log (optional)
        with open("post_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} ------ {message}\n\n\n\n\n\n")
            
        Message = message
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "text": Message
        }
        response = requests.post(url, data=payload)
    except Exception as e:
        Message = f"❌ Error: {e}"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "text": Message
        }
        response = requests.post(url, data=payload)
        print(f"❌ Error: {e}")
