import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.middleware.i18n import I18nMiddleware
import yt_dlp
from dotenv import load_dotenv

# .env faylidan sozlamalarni yuklash
load_dotenv()

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN", "7496406827:AAFQLB2h5eNd6DcUuq_T9W6tr1cive_KgPk")

# Til sozlamalari
I18N_DOMAIN = 'bot'
LOCALES_DIR = 'locales'

# Botni ishga tushirish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Til middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)
_ = i18n.gettext

# Foydalanuvchilar uchun til saqlash
user_languages = {}

# Start komandasi
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(
        types.KeyboardButton("🇺🇿 O'zbekcha"),
        types.KeyboardButton("🇷🇺 Русский"),
        types.KeyboardButton("🇬🇧 English")
    )
    await message.reply(_("Iltimos, tilni tanlang:"), reply_markup=markup)

# ... (qolgan funksiyalar o'zgarishsiz) ...

if __name__ == '__main__':
    # Papkalarni yaratish
    os.makedirs(LOCALES_DIR, exist_ok=True)
    os.makedirs('downloads', exist_ok=True)
    
    # Til fayllari
    for lang in ['uz', 'ru', 'en']:
        lang_file = os.path.join(LOCALES_DIR, f"{lang}.json")
        if not os.path.exists(lang_file):
            with open(lang_file, 'w', encoding='utf-8') as f:
                f.write('{}')
    
    logger.info("Bot ishga tushmoqda...")
    executor.start_polling(dp, skip_updates=True)
