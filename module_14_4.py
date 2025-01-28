# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.
#
# Задача "Продуктовая база":
#
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи.
# Дополните его, следуя пунктам задачи ниже.
#
# Дополните ранее написанный код для Telegram-бота:
#
# Создайте файл crud_functions.py и напишите там следующие функции:
#
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при
# помощи SQL запроса. Эта таблица должна содержать следующие поля:
#
# 1. id - целое число, первичный ключ
# 2. title(название продукта) - текст (не пустой)
# 3. description(описание) - тест
# 4. price(цена) - целое число (не пустой)
#
# get_all_products, которая возвращает все записи из таблицы Products,
# полученные при помощи SQL запроса.
#
#
# Изменения в Telegram-бот:
#
# В самом начале запускайте ранее написанную функцию get_all_products.
#
# Измените функцию get_buying_list в модуле с Telegram-ботом, используя
# вместо обычной нумерации продуктов функцию get_all_products.
# Полученные записи используйте в выводимой надписи:
# "Название: <title> | Описание: <description> | Цена: <price>"
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями
# для последующего вывода в чате Telegram-бота.
#
#
# Пример результата выполнения программы:
#
# Добавленные записи в таблицу Product и их отображение в Telegram-bot:
#
#
# Примечания:
# 1. Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)



from config import api
# from module_14_4_crud_functions import get_all_products
from crud_functions import get_all_products
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.dispatcher import FSMContext


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

# создание реплай-клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)

bt_calculate = KeyboardButton(text='Рассчитать')
bt_inform = KeyboardButton(text='Информация')
bt_buy = KeyboardButton(text='Купить')
kb.add(bt_calculate, bt_inform, bt_buy)

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
    for i in range(4):
        text = f'Название {product[i][1]} | ' \
               f'Описание: {product[i][2]} | ' \
               f'Цена: {product[i][3]}'
        await message.answer(
            text=text
        )
        with open(
            file=f'xxx_products/{i + 1}.pnd.jpg',
            mode='rb'
        ) as img:
            await message.answer_photo(
                photo=img
        )
    await message.answer(
        text='Выберите продукт для покупки:',
        reply_markup=buy_inl_kb,
    )


# обработка инлайн-кнопок покупки товаров
@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer(
        text='Вы успешно приобрели продукт!'
    )
    await call.answer()


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
