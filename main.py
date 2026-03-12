import os
import telebot
import replicate

# Environment Variables থেকে টোকেন নেওয়া
BOT_TOKEN = os.getenv('BOT_TOKEN')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ভিডিও জেনারেটর বট সক্রিয়! আমাকে ইংরেজিতে ভিডিওর বর্ণনা দিন।")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    chat_id = message.chat.id
    prompt = message.text
    
    msg = bot.reply_to(message, "ভিডিও তৈরি হচ্ছে, দয়া করে ১-২ মিনিট অপেক্ষা করুন...")
    
    try:
        # মডেলের নাম এবং ইনপুট সঠিক ফরম্যাটে দেওয়া হয়েছে
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c067844e1d359647f0f62d16450f757",
            input={
                "prompt": prompt,
                "num_frames": 16,
                "fps": 8
            }
        )
        
        if output:
            # ভিডিও ফাইলটি সরাসরি টেলিগ্রামে পাঠানো
            bot.send_video(chat_id, output[0])
            bot.delete_message(chat_id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"দুঃখিত, সমস্যা হয়েছে: {str(e)}", chat_id, msg.message_id)

bot.infinity_polling()
