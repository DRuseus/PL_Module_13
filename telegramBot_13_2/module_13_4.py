from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.filters.command import Command, CommandStart
import asyncio

API = 'None'
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command('Calories'))
async def set_age(message, state: FSMContext):
    await state.set_state(UserState.age)
    await message.answer('Введите свой возраст в полных годах:')

@dp.message(UserState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=float(message.text))
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост в сантиметрах:')

@dp.message(UserState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=float(message.text))
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес в килограммах:')

@dp.message(UserState.weight)
async def send_calories(message, state: FSMContext):
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


@dp.message(CommandStart(s))
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.\n'
                         f'Я умею считать дневную норму калорий /Calories')


@dp.message()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
