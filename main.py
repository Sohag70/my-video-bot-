import os
import telebot
import replicate

# টোকেনগুলো এনভায়রনমেন্ট থেকে নেওয়া হচ্ছে
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
os.environ["REPLICATE_API_TOKEN"] = os.getenv('REPLICATE_API_TOKEN')

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    chat_id = message.chat.id
    prompt = message.text
    
    msg = bot.reply_to(message, "মেটা এআই প্রযুক্তিতে ভিডিও তৈরি হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        # Zeroscope মডেল ব্যবহার করে ভিডিও তৈরি
        output = replicate.run(
            "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c067844e1d359647f0f62d16450f757",
            input={"prompt": prompt}
        )
        
        # ভিডিওটি টেলিগ্রামে পাঠানো
        if output:
            bot.send_video(chat_id, output[0])
            bot.delete_message(chat_id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"দুঃখিত, সমস্যা হয়েছে: {str(e)}", chat_id, msg.message_id)

bot.polling()
