from aiogram import Bot, Dispatcher, types, handlers, F
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

API = 'None'
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(F.text == '/start')
async def start(message):
    print('Привет! Я бот, помогающий твоему здоровью.')
    #await bot.send_message(chat_id=message.chat.id, text=f'Привет! Я бот, помогающий твоему здоровью.')


@dp.message()
async def all_messages(message):
    print('Введите команду /start, чтобы начать общение.')
    #await bot.send_message(chat_id=message.chat.id, text='Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    dp.run_polling(bot)
