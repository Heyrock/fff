# Цель: получить навык работы с состояниями в телеграм-боте.
#
# Задача "Цепочка вопросов":
#
# Необходимо сделать цепочку обработки состояний для нахождения нормы
# калорий для человека.
#
# Группа состояний:
#
# 1. Импортируйте классы State и StateGroup из aiogram.dispatcher.filters.state.
# 2. Создайте класс UserState наследованный от StateGroup.
# 3. Внутри этого класса опишите 3 объекта класса State: age, growth, weight
# (возраст, рост, вес).
# Эта группа(класс) будет использоваться в цепочке вызовов message_handler'ов.
# Напишите следующие функции для обработки состояний:
#
# Функцию set_age(message):
#
# 1. Оберните её в message_handler, который реагирует на текстовое сообщение
# 'Calories'.
# 2. Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
# 3. После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
#
# Функцию set_growth(message, state):
#
# 1. Оберните её в message_handler, который реагирует на переданное состояние
# UserState.age.
# 2. Эта функция должна обновлять данные в состоянии age на message.text
# (написанное пользователем сообщение). Используйте метод update_data.
# 3. Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
# 4. После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
#
# Функцию set_weight(message, state):
#
# 1. Оберните её в message_handler, который реагирует на переданное состояние
# UserState.growth.
# 2. Эта функция должна обновлять данные в состоянии growth на message.text
# (написанное пользователем сообщение). Используйте метод update_data.
# 3. Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
# 4. После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
#
# Функцию send_calories(message, state):
#
# 1. Оберните её в message_handler, который реагирует на переданное состояние
# UserState.weight.
# 2. Эта функция должна обновлять данные в состоянии weight на message.text
# (написанное пользователем сообщение). Используйте метод update_data.
# 3. Далее в функции запомните в переменную data все ранее введённые состояния
# при помощи state.get_data().
# 4. Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
# (для женщин или мужчин - на ваше усмотрение).
# Данные для формулы берите из ранее объявленной переменной data по ключам
# age, growth и weight соответственно.
# 5. Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
# 6. Финишируйте машину состояний методом finish().
#
# !В течение написания этих функций помните, что они асинхронны и все функции и методы должны запускаться с оператором await.
#
# Пример результата выполнения программы:
#
#
# Примечания:
#
# При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к
# вашему боту!

from config import api
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


api = api

bot = Bot(token=api)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
)


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
    sex = State()


def calories_calc(age, height, weight, sex):
    if sex.lower() == 'м':
        result = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex.lower() == 'ж':
        result = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        result = 'Для неведомых зверушек данных нет'
    return result


@dp.message_handler(text=['Calories'])
# @dp.message_handler(text=['1'])
async def set_age(message):
    await message.answer('Введите свой возраст (г):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_height(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите ваш пол (М/Ж):')
    await UserState.sex.set()


@dp.message_handler(state=UserState.sex)
async def send_calories(message, state):
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


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
    )