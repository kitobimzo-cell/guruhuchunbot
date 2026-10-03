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
# Запуск веб-сервера для Render
threading.Thread(target=run_flask, daemon=True).start()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден в Environment Variables!")
if not GEMINI_API_KEY:
    print("ОШИБКА: GEMINI_API_KEY не найден в Environment Variables!")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None
if BOT_TOKEN:
    bot = telebot.TeleBot(BOT_TOKEN)
    @bot.message_handler(func=lambda message: True)
    def reply_with_ai(message):
        if not message.text or not model:
            return
        try:
            response = model.generate_content(
                f"Siz Telegram guruhidagi aqlli va xushmuomala yordamchisiz. Javobni qisqa va aniq bering.\nFoydalanuvchi xabari: {message.text}"
            )
            bot.reply_to(message, response.text)
        except Exception as e:
            print(f"Xatolik Gemini: {e}")
    print("Бот успешно запущен!")
    bot.infinity_polling(skip_pending=True)
else:
    print("Завершение работы: BOT_TOKEN отсутствует.")

