# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
#
# Задача "Регистрация покупателей":
#
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи.
# Дополните его, следуя пунктам задачи ниже.
#
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
#
# initiate_db дополните созданием таблицы Users, если она ещё не создана
# при помощи SQL запроса. Эта таблица должна содержать следующие поля:
#
# 1. id - целое число, первичный ключ
# 2. username - текст (не пустой)
# 3. email - текст (не пустой)
# 4. age - целое число (не пустой)
# 5. balance - целое число (не пустой)
#
#
# add_user(username, email, age),
# которая принимает: имя пользователя, почту и возраст.
# Данная функция должна добавлять в таблицу Users вашей БД запись с
# переданными данными.
# Баланс у новых пользователей всегда равен 1000.
# Для добавления записей в таблице используйте SQL запрос.
#
#
# is_included(username) принимает имя пользователя и возвращает True,
# если такой пользователь есть в таблице Users, в противном случае False.
# Для получения записей используйте SQL запрос.
#
#
# Изменения в Telegram-бот:
#
# 1. Кнопки главного меню дополните кнопкой "Регистрация".
# 2. Напишите новый класс состояний RegistrationState со следующими объектами
# класса State: username, email, age, balance(по умолчанию 1000).
# 3. Создайте цепочку изменений состояний RegistrationState.
#
# Функции цепочки состояний RegistrationState:
#
# sing_up(message):
# 1. Оберните её в message_handler, который реагирует на текстовое сообщение
# 'Регистрация'.
# 2. Эта функция должна выводить в Telegram-бот сообщение
# "Введите имя пользователя (только латинский алфавит):".
# 3. После ожидать ввода имени в атрибут RegistrationState.username при
# помощи метода set.
#
#
# set_username(message, state):
# 1. Оберните её в message_handler, который реагирует на состояние
# RegistrationState.username.
# 2. Функция должна выводить в Telegram-бот сообщение
# "Введите имя пользователя (только латинский алфавит):". ??????
# 3. Если пользователя message.text ещё нет в таблице, то должны обновляться
# данные в состоянии username на message.text.
# Далее выводится сообщение "Введите свой email:" и принимается новое состояние
# RegistrationState.email.
# 4. Если пользователь с таким message.text есть в таблице, то выводить
# "Пользователь существует, введите другое имя" и запрашивать новое состояние для
# RegistrationState.username.
#
# set_email(message, state):
# 1. Оберните её в message_handler, который реагирует на состояние
# RegistrationState.email.
# 2. Эта функция должна обновлять(ся ?) данные в состоянии RegistrationState.email
# на message.text.
# 3. Далее выводить сообщение "Введите свой возраст:":
# 4. После ожидать ввода возраста в атрибут RegistrationState.age.
#
# set_age(message, state):
# 1. Оберните её в message_handler, который реагирует на состояние
# RegistrationState.age.
# 2. Эта функция должна обновляться данные в состоянии RegistrationState.age
# на message.text.
# 3. Далее брать все данные (username, email и age) из состояния и записывать
# в таблицу Users при помощи ранее написанной crud-функции add_user.
# 4. В конце завершать приём состояний при помощи метода finish().
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями
# для последующего вывода в чате Telegram-бота.
#
# Пример результата выполнения программы:
# Машина состояний и таблица Users в Telegram-bot:
#
# Результат в таблице Users:

from config import api
import logging
import re
# from module_14_5_crud_functions import get_all_products, is_included, add_user
from crud_functions import get_all_products, is_included, add_user
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.dispatcher import FSMContext


logging.basicConfig(
    level=logging.INFO
)

product = get_all_products()
# (1, 'Продукт 1', 'Описание 1', 100)
# (2, 'Продукт 2', 'Описание 2', 200)
# (3, 'Продукт 3', 'Описание 3', 300)
# (4, 'Продукт 4', 'Описание 4', 400)


api = api

bot = Bot(token=api)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
)

# создание реплай-клавиатуры главного меню
kb = ReplyKeyboardMarkup(resize_keyboard=True)

bt_calculate = KeyboardButton(text='Рассчитать')
bt_inform = KeyboardButton(text='Информация')
bt_buy = KeyboardButton(text='Купить')
bt_registration = KeyboardButton(text='Регистрация')
kb.add(bt_calculate, bt_inform, bt_buy, bt_registration)


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

# создание инлайн-клавиатуры 'покупка'
buy_inl_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Product1',
                callback_data='product_buying',
            )
        ],
        [
            InlineKeyboardButton(
                text='Product2',
                callback_data='product_buying',
            )
        ],
        [
            InlineKeyboardButton(
                text='Product3',
                callback_data='product_buying',
            )
        ],
        [
            InlineKeyboardButton(
                text='Product4',
                callback_data='product_buying',
            )
        ],
    ],
)



# класс состояний
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


# обработка инлайн-кнопки 'calories',
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
        await message.answer('Ошибка')
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
        await message.answer('Ошибка')
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
        await message.answer('Ошибка')
        await message.answer('Введите, пожалуйста, цифрой вес')


# вывод количества калорий
@dp.message_handler(state=UserState.sex)
async def send_calories(message: Message, state: FSMContext):
    sex = message.text.lower()

    try:
        if sex not in ('м', 'ж'):
            raise ValueError
        await state.update_data(sex=sex)
        data = await state.get_data()
        result = calories_calc(
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            sex=data['sex'],
        )
        await state.finish()
        await message.answer(f'ваша норма калорий: {result}')
    except ValueError:
        await message.answer('Ошибка')
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


# обработка кнопки 'Купить'
@dp.message_handler(text=['Купить'])
async def get_buying_list(message: Message):
    for i in range(len(product)):
        text = f'Название {product[i][1]} | ' \
               f'Описание: {product[i][2]} | ' \
               f'Цена: {product[i][3]}'
        await message.answer(
            text=text
        )
        with open(
            file=f'xxx_products/{product[i][0]}.pnd.jpg',
            mode='rb'
        ) as img:
            await message.answer_photo(
                photo=img
        )
    await message.answer(
        text='Выберите продукт для покупки:',
        reply_markup=buy_inl_kb,
    )


# обработка ВСЕХ инлайн-кнопок покупки товаров
@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer(
        text='Вы успешно приобрели продукт!'
    )
    await call.answer()


# класс состояний пользователя при регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


# функция - обработка сообщения 'Регистрация'
# установка FSM-состояния 'username'
@dp.message_handler(text=['Регистрация'])
async def sign_up(message: Message):
    await message.answer(
        text='Введите имя пользователя (только латинский алфавит):'
    )
    await RegistrationState.username.set()


# функция - установка FSM-состояния 'email'
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    username = message.text
    try:
        if not username.isascii():
            raise ValueError

        if is_included(username):
            raise TypeError

        await state.update_data(username=username)
        await message.answer(text='Введите свой email:')
        await RegistrationState.email.set()

    except ValueError:
        await message.answer(text='Ошибка')
        await message.answer(text='Имя должно быть латиницей')

    except TypeError:
        await message.answer('Ошибка')
        await message.answer('Такое имя уже есть в базе')


# функция - установка FSM-состояния 'age'
@dp.message_handler(state=RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    email = message.text
    try:
        if not re.match(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+[a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$',
                email):
            raise ValueError
        await state.update_data(email=email)
        await message.answer(text='Введите свой возраст:')
        await RegistrationState.age.set()

    except ValueError:
        await message.answer('Ошибка')
        await message.answer('Введите корректный email,\n'
                             'например (mail@example.com)')


# функция - завершение регистрации
@dp.message_handler(state=RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        data = await state.get_data()
        add_user(
            username=data['username'],
            email=data['email'],
            age=data['age'],
        )
        await state.finish()
        await message.answer(
            text='Поздравляем!\n'
                 f'Вы зарегистрированы под именем {data["username"]}'
        )
    except ValueError:
        await message.answer('Ошибка')
        await message.answer('Возраст должен быть целым числом')


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
