from telebot import TeleBot, types
import os
from downloader import YouTubeDownloader, InstagramDownloader
import dotenv
import shutil

dotenv.load_dotenv()

bot = TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f"Salom {message.from_user.full_name}")

@bot.message_handler()
def start(message: types.Message):
    global downloaded
    bot.send_message(message.chat.id,  "Video yuklanmoqda...")
    if message.text.startswith("https://youtube.com/") or message.text.startswith("https://youtu.be/") or message.text.startswith("https://www.youtube.com/") or message.text.startswith("https://www.youtu.be/"):
        try:
            downloaded = YouTubeDownloader(message.text)
            with open("video.mp4", "rb") as video:
                info = f"Video nomi: {downloaded['title']}\nvideoni yuklagan foydalanuvchi: https://youtube.com/@{downloaded['uploader']}\nvideoni yuklangan sanasi: {downloaded['upload_date']}videodagi ko'rishlar soni: {downloaded['view_count']}\nvideodagi likelar soni: {downloaded['like_count']}\n"
                info2 = f"videoni tavsifi: {downloaded['description']}"
                try:
                    bot.send_video(message.chat.id, video=video, caption=f"{info}")
                    bot.send_message(message.chat.id, info2)
                except:
                    bot.send_video(message.chat.id, video=video)
        except Exception as e:
            bot.send_message(message.chat.id, "Videoni yuklashda xatolik yuz berdi")
        os.remove("video.mp4")
    if message.text.startswith("https://www.instagram.com/") or message.text.startswith("https://instagram.com/"):
        try:
            downloaded = InstagramDownloader(message.text)
            opened = open(downloaded[0], "rb").read()
            with open(downloaded[1][0], "rb") as video:
                try:
                    bot.send_video(message.chat.id, video=video, caption=str(opened.decode("utf-8")))
                except:
                    try:
                        bot.send_video(message.chat.id, video=video)
                    except Exception as e:
                        print(e)
        except:
            bot.send_message(message.chat.id, "Videoni yuklashda xatolik yuz berdi")
        shutil.rmtree(downloaded[2])


bot.infinity_polling(skip_pending=True, timeout=False)