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
Prompt = os.getenv("Prompt")
# Configure Google Generative AI
genai.configure(api_key=AI_API_KEY)
# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)
def generate_sqa_post():
    prompt = Prompt
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

    except Exception as e:
        print(f"❌ Error: {e}")
