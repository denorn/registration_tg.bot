import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

TOKEN = '5816146999:AAGVqQMl4B52d7oxJOlqhS7um7QS8So8uws'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class RegistrationState(StatesGroup):
    FIRST_NAME = State()         # имя
    LAST_NAME = State()    # фамилия
    AGE = State()          # возраст
    PHONE_NUMBER = State() # номер телефона


# /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    chat_id = message.chat.id
    await message.reply("Привет! Меня зовут Рыбоног и я твой верный помощник. Давай знакомиться! Введите своё имя:")

    await RegistrationState.FIRST_NAME.set()


@dp.message_handler(state=RegistrationState.FIRST_NAME)
async def process_name(message: types.Message, state: FSMContext):
    first_name = message.text

    # Сохраняем имя
    async with state.proxy() as data:
        data['first_name'] = first_name

    await message.reply("Отлично! Теперь введи свою фамилию:")

    await RegistrationState.LAST_NAME.set()


@dp.message_handler(state=RegistrationState.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    # Сохраняем фамилию
    async with state.proxy() as data:
        data['last_name'] = last_name

    await message.reply("Отлично! Теперь введи свой возраст:")

    await RegistrationState.AGE.set()


@dp.message_handler(state=RegistrationState.AGE)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text

    # Сохраняем возраст
    async with state.proxy() as data:
        data['age'] = age

    await message.reply("Отлично! Теперь введи номер телефона:")

    await RegistrationState.PHONE_NUMBER.set()


@dp.message_handler(state=RegistrationState.PHONE_NUMBER)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text

    # Сохраняем номер телефона
    async with state.proxy() as data:
        data['phone_number'] = phone_number


    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']
    phone_number = data['phone_number']

    # Сохраняем данные
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (first_name, last_name, age, phone_number) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, age, phone_number))
    conn.commit()
    conn.close()

    # сообщение о успешной регистрации
    await state.finish()
    await message.reply("Всё прошло отлично!")


# Запускаем бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
