# Цель: подготовить Telegram-бота для взаимодействия с базой данных.
#
# Задача "Витамины для всех!":
#
# Подготовка:
# Подготовьте Telegram-бота из последнего домашнего задания 13 модуля,
# сохранив код с ним в файл module_14_3.py.
#
# Если вы не решали новые задания из предыдущего модуля рекомендуется
# выполнить их.
#
# Дополните ранее написанный код для Telegram-бота:
#
# Создайте и дополните клавиатуры:
# 1. В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
# 2. Создайте Inline меню из 4 кнопок с надписями
# "Product1", "Product2", "Product3", "Product4".
# У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
#
# 1. Message хэндлер, который реагирует на текст "Купить" и оборачивает
# функцию get_buying_list(message).
#
# 2. Функция get_buying_list должна выводить надписи
# 'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>'
# 4 раза.
# После каждой надписи выводите картинки к продуктам.
# В конце выведите ранее созданное Inline меню с надписью
# "Выберите продукт для покупки:".
#
# 3. Callback хэндлер, который реагирует на текст "product_buying" и
# оборачивает функцию send_confirm_message(call).
#
# 4. Функция send_confirm_message, присылает сообщение
# "Вы успешно приобрели продукт!"
#
# Пример результата выполнения программы:
#
# Обновлённое главное меню:
#
# Список товаров и меню покупки:
#
# Примечания:
#
# 1. Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)


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


products_description = [
    'Что-то красное',
    'Что-то длинное',
    'Что-то пупырчатое',
    'Лампочка'
]


# обработка кнопки 'Купить'
@dp.message_handler(text=['Купить'])
async def get_buying_list(message: Message):
    for i in range(1, 5):
        text = f'Product{i} | ' \
               f'Описание: {products_description[i - 1]} | ' \
               f'Цена: {i * 100}'
        await message.answer(
            text=text
        )
        with open(
            file=f'xxx_products/{i}.pnd.jpg',
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
