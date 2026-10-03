import os
import re
import random
import requests
import google.generativeai as genai

# --- المفاتيح المستخرجة من الصور ومدمجة مباشرةً ---
GEMINI_API_KEY = "AQ.Ab8RN6ICh5FjndEL2LMDgAYYbMZUc3aUFbjSEAltdnLMeeoGWQ"

META_USER_TOKEN = "EAGShuoQhGJ4BSrIb9RWbPb8FQWhReZAKxqaFxBYTDE6E07wcsOiFOH4a8uWsBMiHqTCgq5uHj4PFszyNlbdZB1rj04iB5qN0MdPmHb2OK8EMQJxIutIHSiTvsCFLtpko2bdaTBDrI6jZBPSyyqiNZBZBzOhAGtFxwqxpejAZByiqVnLVDfZAcJdpFy72UGcHP6G0dG0NeENoSkVHCwTk5lOZBrrKP5ru9PRZBmyLYx2OqZCkqcCOb6Hz59zxW3S9A0bC4rqLi9dyRdAt4CmyRuBI8g9fWkQcoR"
META_APP_ID = "28325320123816094"
META_APP_SECRET = "f4f9f8987e16618d1a4935c8a3e8c559"

TELEGRAM_BOT_TOKEN = "8885987238:AAEYEVUbJgOsul1VsYS7knCct_CF6EX3sI"
TELEGRAM_CHAT_ID = "7017442024"

# 1. قائمة اللغات التسع المعتمدة
LANGUAGES = {
    "ar": {"name": "العربية", "flag": "🇪🇬", "prompt_lang": "Arabic"},
    "en": {"name": "English", "flag": "🇺🇸", "prompt_lang": "English"},
    "de": {"name": "Deutsch", "flag": "🇩🇪", "prompt_lang": "German"},
    "es": {"name": "Español", "flag": "🇪🇸", "prompt_lang": "Spanish"},
    "fr": {"name": "Français", "flag": "🇫🇷", "prompt_lang": "French"},
    "pt": {"name": "Português", "flag": "🇵🇹", "prompt_lang": "Portuguese"},
    "it": {"name": "Italiano", "flag": "🇮🇹", "prompt_lang": "Italian"},
    "ru": {"name": "Русский", "flag": "🇷🇺", "prompt_lang": "Russian"},
    "jp": {"name": "日本語", "flag": "🇯🇵", "prompt_lang": "Japanese"}
}

# تهيئة موديل الذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)

def generate_paradox_deal(lang_code):
    lang_info = LANGUAGES[lang_code]
    prompt = f"""
    You are 'Mr. Paradox', a charismatic, short, chubby stickman in a bright blue suit.
    Your style is witty, sarcastic, highly engaging, and captivating.
    
    Task: Write a short, highly engaging Amazon affiliate deal post/script in {lang_info['prompt_lang']}.
    Target Market: Amazon trending deals (Electronics, Gadgets, Home, Fashion).
    
    Structure:
    1. Mr. Paradox signature witty hook.
    2. Product benefit highlights.
    3. Call to Action (CTA) to check the deal link.
    4. Relevant active hashtags including #MrParadox.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def publish_to_meta(content):
    if not META_USER_TOKEN:
        print("⚠️ Meta User Token missing.")
        return
    try:
        url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={META_USER_TOKEN}"
        res = requests.get(url).json()
        if 'data' in res and len(res['data']) > 0:
            page_id = res['data'][0]['id']
            page_token = res['data'][0]['access_token']
            post_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
            requests.post(post_url, data={'message': content, 'access_token': page_token})
            print("✅ Successfully posted to Meta Feed!")
        else:
            print("⚠️ No Facebook pages found.")
    except Exception as e:
        print("❌ Meta posting error:", e)

def send_to_telegram(content):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": content}
            requests.post(url, data=payload)
            print("✅ Successfully sent to Telegram channel!")
        except Exception as e:
            print("❌ Telegram error:", e)

def update_store(content, lang_code):
    flag = LANGUAGES[lang_code]['flag']
    card_html = f"""
            <!-- DEALS_START -->
            <div class="bg-gray-900/90 rounded-2xl p-5 border border-sky-500/40 shadow-xl mb-4">
                <div class="flex justify-between items-center mb-2">
                    <span class="bg-sky-500/20 text-sky-300 text-xs px-3 py-1 rounded-full font-bold">🎩 Mr. Paradox {flag}</span>
                </div>
                <p class="text-gray-200 text-sm whitespace-pre-line mb-4">{content[:220]}...</p>
                <a href="https://www.amazon.com" target="_blank" class="block text-center bg-gradient-to-r from-sky-500 to-blue-600 text-white font-bold py-2.5 rounded-xl transition hover:opacity-90">
                    Get Offer / احصل على العرض 🛒
                </a>
            </div>
    """
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        updated_html = re.sub(r'<!-- DEALS_START -->', card_html, html, count=1)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("✅ Storefront index.html updated successfully!")

if __name__ == "__main__":
    selected_lang = random.choice(list(LANGUAGES.keys()))
    print(f"🚀 Running Mr. Paradox Engine for Language: {selected_lang} ({LANGUAGES[selected_lang]['name']})")
    
    deal_text = generate_paradox_deal(selected_lang)
    print("\n--- Generated Output ---")
    print(deal_text)
    print("------------------------\n")
    
    publish_to_meta(deal_text)
    send_to_telegram(deal_text)
    update_store(deal_text, selected_lang)
    print("✨ Automation run completed successfully!")
