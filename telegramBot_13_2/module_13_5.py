from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
import asyncio, logging
from API_K import API

# API = 'None'
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())

start_button_1 = KeyboardButton(text='Расчитать дневную норму калорий')
info_button = KeyboardButton(text='Информация о боте')
start_button_2 = KeyboardButton(text='>>>Начать считать мою норму калорий (БЕСПЛАТНО, БЕЗ РЕГИСТРАЦИИ)<<<')

markup_1 = ReplyKeyboardMarkup(keyboard=[[start_button_1, info_button]], resize_keyboard=True, one_time_keyboard=True)
markup_2 = ReplyKeyboardMarkup(keyboard=[[start_button_2]], resize_keyboard=True, one_time_keyboard=True)
# У объекта класса ReplyKeyboardMarkup больше нет метода .add(), теперь надо указывать кнопки внутри клавиатуры.


# Опять же докуметация навела меня на билдер, который собирает сетки из кнопок

# builder = ReplyKeyboardBuilder()
# builder.add(start_button, info_button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(F.text == 'Информация о боте')
async def get_info(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer('Это телеграм-бот, который поможет тебе правильно питаться и поддерживать здоровый образ жизни.'
                         'Чтобы начать жми на кнопку снизу', reply_markup=markup_2)


@dp.message(F.text.contains('норму калорий'))
async def set_age(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.set_state(UserState.age)
    await message.answer('Введите свой возраст в полных годах:')


@dp.message(UserState.age)
async def set_growth(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(age=float(message.text))
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост в сантиметрах:')


@dp.message(UserState.growth)
async def set_weight(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(growth=float(message.text))
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес в килограммах:')


@dp.message(UserState.weight)
async def send_calories(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    await message.answer(f'Если вы мужчина то ваша норма калорий в день составляет:\n'
                         f'{10 * weight + 6.25 * growth + 5 * age + 5}\n'
                         f'А если в женщина, то ваша дневная норма калорий:\n'
                         f'{10 * weight + 6.25 * growth + 5 * age - 161}')
    await state.clear()


@dp.message(CommandStart())
async def start(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.\n',
                         reply_markup=markup_1)


@dp.message()
async def all_messages(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main() -> None:
    logging.basicConfig(filename='t_bot.log', filemode='w', level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s, %(levelname)s, %(message)s')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
