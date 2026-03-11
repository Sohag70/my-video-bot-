import os
import telebot
import requests

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
HF_TOKEN = os.getenv('HF_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ভিডিও জেনারেটর বটে স্বাগতম! আমাকে একটি প্রম্পট পাঠান।")

@bot.message_handler(func=lambda message: True)
def get_video(message):
    msg = bot.reply_to(message, "ভিডিও তৈরি হচ্ছে, ১ মিনিট অপেক্ষা করুন...")
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": message.text})
    
    if response.status_code == 200:
        with open("vid.mp4", "wb") as f: f.write(response.content)
        with open("vid.mp4", "rb") as v: bot.send_video(message.chat.id, v)
        bot.delete_message(message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "দুঃখিত, বর্তমানে এআই মডেলটি ব্যস্ত। কিছুক্ষণ পর আবার চেষ্টা করুন।")

if __name__ == "__main__":
    bot.infinity_polling()
    


