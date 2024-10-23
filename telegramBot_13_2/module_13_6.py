from aiogram import Bot, Dispatcher, F
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import CallbackData
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardButton

from API_K import API


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Собственный фильтр, который пришлось создать, чтоб InlineKeyboardButton мог перехватываться
class MyFilter(CallbackData, prefix='my'):
    action: str


# API = 'None'
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())

start_button_1 = KeyboardButton(text='Расчёт нормы калорий')
info_button = KeyboardButton(text='Информация о боте')
il_button_calc = InlineKeyboardButton(text='Начать расчёт', callback_data=MyFilter(action='start').pack())
il_button_info = InlineKeyboardButton(text='Формула расчёта',
                                      callback_data=MyFilter(action='formula').pack())

il_markup_1 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc, il_button_info]])
il_markup_2 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc]])
markup_1 = ReplyKeyboardMarkup(keyboard=[[start_button_1, info_button]], resize_keyboard=True, one_time_keyboard=True)


# У объекта класса ReplyKeyboardMarkup больше нет метода .add(), теперь надо указывать кнопки при определении клавиатуры


# Опять же докуметация навела меня на билдер, который собирает сетки из кнопок

# builder = ReplyKeyboardBuilder()
# builder.add(start_button, info_button)


@dp.callback_query(MyFilter.filter(F.action == 'formula'))
async def formula(call):
    await call.message.answer('Формула Миффлина-Сан Жеора\n'
                              'Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161',
                              reply_markup=il_markup_2)
    await call.answer()


@dp.callback_query(MyFilter.filter(F.action == 'start'))
async def formula(call, state: FSMContext):
    await state.set_state(UserState.age)
    await call.message.answer('Введите свой возраст в полных годах:')
    await call.answer()


@dp.message(F.text == 'Информация о боте')
async def get_info(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(
        'Это телеграм-бот, который поможет тебе правильно питаться и поддерживать здоровый образ жизни.\n'
        'Выберете опцию:',
        reply_markup=il_markup_1)


@dp.message(CommandStart())
async def start(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.\n',
                         reply_markup=markup_1)


@dp.message(F.text.contains('норму калорий'))
async def set_age(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.set_state(UserState.age)
    await message.answer('Выберите опцию:', reply_markup=il_markup_1)


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
