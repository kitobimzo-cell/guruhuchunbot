import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

app = Flask(name)

@app.route('/')
def home():
    return "Bot status: Active"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash") if GEMINI_API_KEY else None
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

@bot.message_handler(func=lambda message: True)
def reply_with_ai(message):
    if not message.text or not model or not bot:
        return
    try:
        response = model.generate_content(
            f"Siz Telegram guruhidagi aqlli va xushmuomala yordamchisiz. Javobni qisqa va aniq bering.\nFoydalanuvchi xabari: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik: {e}")

if name == "main":
    threading.Thread(target=run_flask, daemon=True).start()
    if bot:
        print("Bot ishladi...")
        bot.infinity_polling(skip_pending=True)
