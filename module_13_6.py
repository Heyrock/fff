# Цель: написать простейшего телеграмм-бота, используя асинхронные функции.
#
# Задача "Он мне ответил!":
# Измените функции start и all_messages так, чтобы вместо вывода в консоль
# строки отправлялись в чате телеграм.
#
# Запустите ваш Telegram-бот и проверьте его на работоспособность.
# Пример результата выполнения программы:
#
#
# Примечания:
#
# 1. Для ответа на сообщение запускайте метод answer асинхронно.
# 2. При отправке вашего кода на GitHub не забудьте убрать ключ для
# подключения к вашему боту!


from config import api
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = api

bot = Bot(token=api)
dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
)


@dp.message_handler(commands=['start'])
async def start(message):
    # print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_messages(message):
    # print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
    )
