from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import CommandStart
import asyncio
from API_K import API

# API = 'None'
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start(message):
    print(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.')
    # await bot.send_message(chat_id=message.chat.id, text=f'Привет! Я бот, помогающий твоему здоровью.')


@dp.message()
async def all_messages(message):
    print('Введите команду /start, чтобы начать общение.')
    # await bot.send_message(chat_id=message.chat.id, text='Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
