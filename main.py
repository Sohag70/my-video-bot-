import os
import telebot
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# আপনার দেওয়া এপিআই কী সরাসরি কোডে বসানো হয়েছে
API_TOKEN = "8722321473:AAGYgRQpCmXmSbqcpA1d9-QCnSK7SJ2lfhQ"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me any English text and I will generate a video for you.")

@bot.message_handler(func=lambda message: True)
def generate_video(message):
    try:
        user_text = message.text
        # ইউজারকে প্রসেসিং মেসেজ পাঠানো
        sent_msg = bot.reply_to(message, "Generating video... please wait about 1 minute.")

        # ব্যাকগ্রাউন্ড সেটআপ (নীল রঙ, ৫ সেকেন্ড)
        bg = ColorClip(size=(640, 360), color=(0, 102, 204), duration=5)

        # টেক্সট লেয়ার সেটআপ
        txt = TextClip(user_text, fontsize=60, color='white', size=(600, 300), method='caption')
        txt = txt.set_duration(5).set_position('center')

        # ভিডিও ফাইল তৈরি
        output_file = "video.mp4"
        final_video = CompositeVideoClip([bg, txt])
        final_video.write_videofile(output_file, fps=24, codec="libx264")

        # ভিডিওটি টেলিগ্রামে পাঠানো
        with open(output_file, "rb") as v:
            bot.send_video(message.chat.id, v, caption="Here is your video!")
        
        # প্রসেসিং মেসেজটি ডিলিট করা
        bot.delete_message(message.chat.id, sent_msg.message_id)
        
        # সার্ভার থেকে ফাইলটি মুছে ফেলা (জায়গা বাঁচাতে)
        if os.path.exists(output_file):
            os.remove(output_file)

    except Exception as e:
        bot.reply_to(message, "Sorry, something went wrong. Try a shorter English text.")
        print(f"Error: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
