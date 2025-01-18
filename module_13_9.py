# -*- coding: cp1251 -*-
# ����: �������� ��������� Inline ���������� � ������ �� ��� � Telegram-bot.
#
# ������ "��� ������ ������":
#
# ���������� ��������� ��� ���������� ������, ����� ��� ������� �� ������
# '����������' ����������� Inline-����������.
#
# �������� ���������� InlineKeyboardMarkup � 2 �������� InlineKeyboardButton:
#
# 1. � ������� '���������� ����� �������' � callback_data='calories'
# 2. � ������� '������� �������' � callback_data='formulas'
#
# �������� ����� ������� main_menu(message), �������:
#
# 1. ����� ������� � ��������� message_handler, ������������� ��� ��������
# ������ '����������'.
# 2. ���� ������� ����� ��������� ����� ��������� Inline ���� � �����
# '�������� �����:'
#
# �������� ����� ������� get_formulas(call), �������:
#
# 1. ����� ������� � ��������� callback_query_handler, ������� �����
# ����������� �� ����� 'formulas'.
# 2. ����� ��������� ��������� � �������� ��������-��� �����.
#
# �������� ������� set_age � ��������� ��� ��:
#
# 1. ��������� ������� �� callback_query_handler, ������� ����� �����������
# �� ����� 'calories'.
# 2. ������ ������� ��������� �� message, � call. ������ � ��������� �����
# ��������� - call.message.
#
# �� ����� ��������� ��������� ��������:
#
# 1. �������� ������� /start
# 2. �� ��� ������� ����������� ������� ����: '����������' � '����������'.
# 3. � ����� �� ������ '����������' ����������� Inline ����:
# '���������� ����� �������' � '������� �������'
# 4. �� Inline ������ '������� �������' ����������� ��������� � ��������.
# 5. �� Inline ������ '���������� ����� �������' �������� �������� ������
# ��������� �� �������.

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

# �������� ������-����������
kb = ReplyKeyboardMarkup(resize_keyboard=True)

bt_calculate = KeyboardButton(text='����������')
bt_inform = KeyboardButton(text='����������')
kb.add(bt_calculate, bt_inform)

# �������� ������-����������
inl_kb = InlineKeyboardMarkup()
inl_bt_calories = InlineKeyboardButton(
    text='���������� ����� �������',
    callback_data='calories',
)
inl_bt_formulas = InlineKeyboardButton(
    text='������� �������',
    callback_data='formulas',
)
inl_kb.add(
    inl_bt_calories,
    inl_bt_formulas
)


# �������� ������ ���������
class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
    sex = State()


# ������� ������� �������
def calories_calc(age, height, weight, sex):
    if sex.lower() == '�':
        result = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex.lower() == '�':
        result = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        result = '��� ��������� �������� ������ ���'
    return result


# ����� ������-����������
@dp.message_handler(text='����������')
# @dp.message_handler(text='1')
async def main_menu(message: Message):
    await message.answer(
        text='�������� �����:',
        reply_markup=inl_kb,
    )


# ��������� ������-������ 'formulas'
@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call: CallbackQuery):
    await call.message.answer(
        text='������� ��������-��� �����'
    )
    await call.answer()


# # ��������� ������-������ 'formulas',
# ��������� ��������� 'age' ��� ������ ���������
@dp.callback_query_handler(text=['calories'])
async def set_age(call: CallbackQuery):
    await call.message.answer('������� ���� ������� (�):')
    await call.answer()
    await UserState.age.set()


# ��������� ��������� 'height' ��� ������ ���������
@dp.message_handler(state=UserState.age)
async def set_height(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer('������� ���� ���� (��):')
        await UserState.height.set()
    except ValueError:
        await message.answer('������!')
        await message.answer('�������, ����������, ������ ����� ���')


# ��������� ��������� 'weight' ��� ������ ���������
@dp.message_handler(state=UserState.height)
async def set_weight(message: Message, state: FSMContext):
    try:
        height = int(message.text)
        await state.update_data(height=height)
        await message.answer('������� ���� ��� (��):')
        await UserState.weight.set()
    except ValueError:
        await message.answer('������!')
        await message.answer('�������, ����������, ������ ����')


# ��������� ��������� 'sex' ��� ������ ���������
@dp.message_handler(state=UserState.weight)
async def set_sex(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)
        await message.answer('������� ��� ��� (�/�):')
        await UserState.sex.set()
    except ValueError:
        await message.answer('������!')
        await message.answer('�������, ����������, ������ ���')


# ����� ���������� �������
@dp.message_handler(state=UserState.sex)
async def send_calories(message: Message, state: FSMContext):
    sex = message.text.lower()

    try:
        await state.update_data(sex=sex)
        if sex not in ('�', '�'):
            raise ValueError
        data = await state.get_data()
        result = calories_calc(
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            sex=data['sex'],
        )
        await message.answer(f'���� ����� �������: {result}')
        await state.finish()
    except ValueError:
        await message.answer('������!')
        await message.answer('��������, ����������, ��� � ��� �')


# ��������� ������� /start
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(
        text='������! � ��� ���������� ������ ��������.',
        reply_markup=kb,
    )


# ��������� ��������� '����������'
@dp.message_handler(text=['����������'])
async def info(message: Message):
    await message.answer(
        text='����� ����� �� ���� ���� �������'
    )


# ��������� ���� ������ ���������
@dp.message_handler()
async def all_messages(message: Message):
    await message.answer(
        text='������� ������� /start, ����� ������ �������.'
    )


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
    )
