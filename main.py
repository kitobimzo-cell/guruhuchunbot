import os
import telebot
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_with_ai(message):
    text = message.text
    if not text:
        return

    try:
        response = model.generate_content(
            f"Siz Telegram guruhidagi aqlli va xushmuomala yordamchisiz. Javobni qisqa va aniq bering.\nFoydalanuvchi xabari: {text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if name == "main":
    print("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
