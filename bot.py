
import os
import tempfile
import telebot

from config import BOT_TOKEN
from downloader import download_video

bot = telebot.TeleBot(BOT_TOKEN)


# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(message, """
👋 Assalomu alaykum!

📸 JORABEK INSTAGRAM DOWNLOADER

Instagram videolarini yuklab oling!

✨ IMKONIYATLAR:

📥 Reels yuklash
📥 Post videolarini yuklash

🔗 Instagram video linkini yuboring!
""")


# =========================
# HELP
# =========================

@bot.message_handler(commands=['help'])
def help_command(message):

    bot.reply_to(message, """
📌 YORDAM

1. Instagram'dan video linkini nusxalang.
2. Botga yuboring.
3. Bot videoni yuklab beradi.

Faqat Instagram linklari qabul qilinadi.
""")


# =========================
# INSTAGRAM VIDEO
# =========================

@bot.message_handler(content_types=['text'])
def handle_link(message):

    url = message.text.strip().split()[0]

    if not (
        "instagram.com/" in url.lower()
        or "instagr.am/" in url.lower()
    ):
        bot.reply_to(
            message,
            "❌ Faqat Instagram video linkini yuboring!"
        )
        return

    status = bot.reply_to(
        message,
        "⏳ Video yuklanmoqda..."
    )

    try:
        with tempfile.TemporaryDirectory() as folder:

            path = download_video(url, folder)

            if not os.path.isfile(path):
                raise Exception("Video fayli topilmadi!")

            size = os.path.getsize(path)

            if size > 49 * 1024 * 1024:
                bot.edit_message_text(
                    "❌ Video hajmi juda katta!",
                    message.chat.id,
                    status.message_id
                )
                return

            with open(path, "rb") as video:
                bot.send_video(
                    message.chat.id,
                    video,
                    caption="✅ Instagram videosi tayyor!",
                    reply_to_message_id=message.message_id,
                    timeout=120
                )

            bot.delete_message(
                message.chat.id,
                status.message_id
            )

    except Exception as e:

        print("XATOLIK:", e)

        bot.edit_message_text(
            "❌ Video yuklashda xatolik!\n"
            "Linkni tekshirib qayta urinib ko'ring.",
            message.chat.id,
            status.message_id
        )


# =========================
# BOT START
# =========================

print("==============================")
print("JORABEK INSTAGRAM BOT ISHLAYAPTI")
print("==============================")

bot.infinity_polling(skip_pending=True)
