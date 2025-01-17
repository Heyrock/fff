# Цель: научится создавать клавиатуры и кнопки на них в Telegram-bot.
#
# Задача "Меньше текста, больше кликов":
#
# Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах
# тела для расчёта калорий выдавались по нажатию кнопки.
#
# 1. Измените massage_handler для функции set_age.
# Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
# 2. Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton
# на ней со следующим текстом: 'Рассчитать' и 'Информация'.
# Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства
# при помощи параметра resize_keyboard.
# 3. Используйте ранее созданную клавиатуру в ответе функции start,
# используя параметр reply_markup.
#
# В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
# При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция
# set_age с которой начинается работа машины состояний для age, growth и weight.
# 
# Пример результата выполнения программы:
#
# Клавиатура по команде /start:++
#
# После нажатия на кнопку 'Рассчитать':
#
# Примечания:
# 1. При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к
# вашему боту!

from config import api
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


api = api

bot = Bot(token=api)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
)

kb = ReplyKeyboardMarkup(resize_keyboard=True)

bt_calculate = KeyboardButton(text='Рассчитать')
bt_inform = KeyboardButton(text='Информация')
kb.add(bt_calculate, bt_inform)


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


# обработка сообщения 'Рассчитать', установка состояния 'age' для машины состояний
@dp.message_handler(text=['Рассчитать'])
# @dp.message_handler(text=['1'])
async def set_age(message: Message):
    await message.answer('Введите свой возраст (г):')
    await UserState.age.set()


# установка состояния 'height' для машины состояний
@dp.message_handler(state=UserState.age)
async def set_height(message: Message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.height.set()


# установка состояния 'weight' для машины состояний
@dp.message_handler(state=UserState.height)
async def set_weight(message: Message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


# установка состояния 'sex' для машины состояний
@dp.message_handler(state=UserState.weight)
async def set_sex(message: Message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите ваш пол (М/Ж):')
    await UserState.sex.set()


# вывод количества калорий
@dp.message_handler(state=UserState.sex)
async def send_calories(message: Message, state):
    await state.update_data(sex=message.text)
    data = await state.get_data()
    result = calories_calc(
        age=int(data['age']),
        height=int(data['height']),
        weight=int(data['weight']),
        sex=data['sex'],
    )
    await message.answer(f'ваша норма калорий: {result}')
    await state.finish()


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
