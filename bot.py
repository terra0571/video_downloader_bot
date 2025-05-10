import os
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

# Log konfiguratsiyasi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sozlamalarni yuklash
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
SNAPVIDEO_API = "https://api.phimtat.vn/snapvideo/json.php"

# Botni ishga tushirish
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def download_video(url: str) -> dict:
    try:
        params = {"apikey": API_KEY, "url": url}
        response = requests.get(SNAPVIDEO_API, params=params, timeout=30)
        return response.json()
    except Exception as e:
        logger.error(f"Download error: {e}")
        return {"error": str(e)}

@dp.message(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Salom! Video yuklash uchun havola yuboring")

@dp.message()
async def video_handler(message: types.Message):
    if not message.text.startswith(('http://', 'https://')):
        return await message.answer("Iltimos, to'g'ri URL yuboring")
    
    msg = await message.answer("Video yuklanmoqda...")
    
    try:
        result = await download_video(message.text)
        if result.get('url'):
            await message.answer_video(result['url'], caption="Yuklandi!")
        else:
            await message.answer("Video yuklab bo'lmadi")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
    finally:
        await msg.delete()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
