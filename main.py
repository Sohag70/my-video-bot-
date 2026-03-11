import os
import telebot
import requests

# ১. টোকেন চেক করা (সার্ভারে সেট না থাকলে এখানে এরর দিবে)
BOT_TOKEN = os.getenv('BOT_TOKEN')
HF_TOKEN = os.getenv('HF_TOKEN')

if not BOT_TOKEN or not HF_TOKEN:
    print("Error: BOT_TOKEN or HF_TOKEN is missing in Environment Variables!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
API_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ভিডিও জেনারেটর বটে স্বাগতম! আমাকে একটি বর্ণনা দিন।")

@bot.message_handler(func=lambda message: True)
def get_video(message):
    msg = bot.reply_to(message, "ভিডিও তৈরি হচ্ছে, ১ মিনিট অপেক্ষা করুন...")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": message.text})
        if response.status_code == 200:
            with open("vid.mp4", "wb") as f: f.write(response.content)
            with open("vid.mp4", "rb") as v: bot.send_video(message.chat.id, v)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.reply_to(message, f"এরর: {response.status_code}. সার্ভার ব্যস্ত, আবার চেষ্টা করুন।")
    except Exception as e:
        bot.reply_to(message, f"একটি সমস্যা হয়েছে: {str(e)}")

print("Bot is running...")
bot.infinity_polling()
