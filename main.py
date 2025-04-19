from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers import user_start, admin_start  # ✅ TO‘G‘RI

bot = Bot(token="7806141272:AAGdCFWoqSmePehBFheGVEeGoAEQDjCVxZI")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if message.from_user.id == 7586510077:
        await admin_start(message)
    else:
        await user_start(message)

if __name__ == "__main__":
    executor.start_polling(dp)
