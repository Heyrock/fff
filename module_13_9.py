# -*- coding: cp1251 -*-
# Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.
#
# Задача "Ещё больше выбора":
#
# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку
# 'Рассчитать' присылалась Inline-клавиатура.
#
# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
#
# 1. С текстом 'Рассчитать норму калорий' и callback_data='calories'
# 2. С текстом 'Формулы расчёта' и callback_data='formulas'
#
# Создайте новую функцию main_menu(message), которая:
#
# 1. Будет обёрнута в декоратор message_handler, срабатывающий при передаче
# текста 'Рассчитать'.
# 2. Сама функция будет присылать ранее созданное Inline меню и текст
# 'Выберите опцию:'
#
# Создайте новую функцию get_formulas(call), которая:
#
# 1. Будет обёрнута в декоратор callback_query_handler, который будет
# реагировать на текст 'formulas'.
# 2. Будет присылать сообщение с формулой Миффлина-Сан Жеора.
#
# Измените функцию set_age и декоратор для неё:
#
# 1. Декоратор смените на callback_query_handler, который будет реагировать
# на текст 'calories'.
# 2. Теперь функция принимает не message, а call. Доступ к сообщению будет
# следующим - call.message.
#
# По итогу получится следующий алгоритм:
#
# 1. Вводится команда /start
# 2. На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
# 3. В ответ на кнопку 'Рассчитать' присылается Inline меню:
# 'Рассчитать норму калорий' и 'Формулы расчёта'
# 4. По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
# 5. По Inline кнопке 'Рассчитать норму калорий' начинает работать машина
# состояний по цепочке.

from config import api
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.dispatcher import FSMContext


api = api

bot = Bot(token=api)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
)

# создание реплай-клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)

bt_calculate = KeyboardButton(text='Рассчитать')
bt_inform = KeyboardButton(text='Информация')
kb.add(bt_calculate, bt_inform)

# создание инлайн-клавиатуры
inl_kb = InlineKeyboardMarkup()
inl_bt_calories = InlineKeyboardButton(
    text='Рассчитать норму калорий',
    callback_data='calories',
)
inl_bt_formulas = InlineKeyboardButton(
    text='Формулы расчёта',
    callback_data='formulas',
)
inl_kb.add(
    inl_bt_calories,
    inl_bt_formulas
)


# создание класса состояний
class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
    sex = State()


# функция расчета калорий
def calories_calc(age, height, weight, sex):
    if sex.lower() == 'м':
        result = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex.lower() == 'ж':
        result = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        result = 'Для неведомых зверушек данных нет'
    return result


# вызов инлайн-клавиатуры
@dp.message_handler(text='Рассчитать')
# @dp.message_handler(text='1')
async def main_menu(message: Message):
    await message.answer(
        text='Выберите опцию:',
        reply_markup=inl_kb,
    )


# обработка инлайн-кнопки 'formulas'
@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call: CallbackQuery):
    await call.message.answer(
        text='формула Миффлина-Сан Жеора'
    )
    await call.answer()


# # обработка инлайн-кнопки 'formulas',
# установка состояния 'age' для машины состояний
@dp.callback_query_handler(text=['calories'])
async def set_age(call: CallbackQuery):
    await call.message.answer('Введите свой возраст (г):')
    await call.answer()
    await UserState.age.set()


# установка состояния 'height' для машины состояний
@dp.message_handler(state=UserState.age)
async def set_height(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer('Введите свой рост (см):')
        await UserState.height.set()
    except ValueError:
        await message.answer('Ошибка!')
        await message.answer('Введите, пожалуйста, цифрой число лет')


# установка состояния 'weight' для машины состояний
@dp.message_handler(state=UserState.height)
async def set_weight(message: Message, state: FSMContext):
    try:
        height = int(message.text)
        await state.update_data(height=height)
        await message.answer('Введите свой вес (кг):')
        await UserState.weight.set()
    except ValueError:
        await message.answer('Ошибка!')
        await message.answer('Введите, пожалуйста, цифрой рост')


# установка состояния 'sex' для машины состояний
@dp.message_handler(state=UserState.weight)
async def set_sex(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)
        await message.answer('Введите ваш пол (М/Ж):')
        await UserState.sex.set()
    except ValueError:
        await message.answer('Ошибка!')
        await message.answer('Введите, пожалуйста, цифрой вес')


# вывод количества калорий
@dp.message_handler(state=UserState.sex)
async def send_calories(message: Message, state: FSMContext):
    sex = message.text.lower()

    try:
        await state.update_data(sex=sex)
        if sex not in ('м', 'ж'):
            raise ValueError
        data = await state.get_data()
        result = calories_calc(
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            sex=data['sex'],
        )
        await message.answer(f'ваша норма калорий: {result}')
        await state.finish()
    except ValueError:
        await message.answer('Ошибка!')
        await message.answer('Выберите, пожалуйста, пол М или Ж')


# обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(
        text='Привет! Я бот помогающий твоему здоровью.',
        reply_markup=kb,
    )


# обработка сообщения 'Информация'
@dp.message_handler(text=['Информация'])
async def info(message: Message):
    await message.answer(
        text='Здесь могла бы быть Ваша реклама'
    )


# обработка всех прочих сообщений
@dp.message_handler()
async def all_messages(message: Message):
    await message.answer(
        text='Введите команду /start, чтобы начать общение.'
    )


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
    )
