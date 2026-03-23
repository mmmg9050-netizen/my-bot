import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os

# التوكن الخاص بك
TOKEN = '8724256615:AAEgxTYG1t3GlT_2xNUoGzjDCgaZh1WNh3s'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت MG! 🎬\nأرسل الرابط وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda m: "http" in m.text)
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_video = types.InlineKeyboardButton("فيديو 🎬", callback_data=f"vid|{url}")
    btn_audio = types.InlineKeyboardButton("صوت (MP3) 🎵", callback_data=f"aud|{url}")
    markup.add(btn_video, btn_audio)
    bot.reply_to(message, "اختر صيغة التحميل:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data_parts = call.data.split("|")
    download_type = data_parts[0]
    url = data_parts[1]
    bot.edit_message_text("جاري التحميل... ⏳", call.message.chat.id, call.message.message_id)
    try:
        file_ext = "mp4" if download_type == "vid" else "mp3"
        file_name = f"file_{call.message.chat.id}.{file_ext}"
        ydl_opts = {'outtmpl': file_name, 'quiet': True, 'format': 'bestaudio/best' if download_type == "aud" else 'best'}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open(file_name, 'rb') as f:
            if download_type == "vid":
                bot.send_video(call.message.chat.id, f)
            else:
                bot.send_audio(call.message.chat.id, f)
        if os.path.exists(file_name):
            os.remove(file_name)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, "❌ خطأ في الرابط.")

bot.infinity_polling()
