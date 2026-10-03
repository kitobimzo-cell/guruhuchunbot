import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot status: Active"
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# Flask serverni orqa fonda ishga tushirish
threading.Thread(target=run_flask, daemon=True).start()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None
if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN)
    @bot.message_handler(func=lambda message: True)
    def reply_with_ai(message):
        if not message.text:
            return
        if not model:
            bot.reply_to(message, "Xato: GEMINI_API_KEY sozlanmagan!")
            return
        try:
            response = model.generate_content(
                f"Siz Telegram guruhidagi aqlli va xushmuomala yordamchisiz. Javobni qisqa va aniq bering.\nFoydalanuvchi xabari: {message.text}"
            )
            bot.reply_to(message, response.text)
        except Exception as e:
            print(f"Gemini xatoligi: {e}")
            bot.reply_to(message, f"Xatolik yuz berdi: {e}")
    # Eski ulanishlarni (Webhook) o'chirish
    try:
        bot.remove_webhook()
    except Exception as e:
        print(f"Webhook o'chirishda xatolik: {e}")
    print("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
    bot.infinity_polling(skip_pending=True)
else:
    print("XATO: BOT_TOKEN topilmadi!")
