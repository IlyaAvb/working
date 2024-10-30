from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

import asyncio

import config
import markups
import datetime
import database

bot = Bot(token=config.TOKEN_BOT)
dp = Dispatcher()

async def on_starup():
    await database.start()
    print('Бот запущен!')

class PriceState(StatesGroup):
    megik = State()
    sbsv = State()
    orion = State()
    kalinka = State()
    zelenkova = State()
    prestizh = State()
    omelchenko = State()


class Form(StatesGroup):
    waiting_for_sum = State()
    waiting_for_minus = State()


def cheker(price):
    try:
        price = int(price)
        return price
    except ValueError:
        return None


@dp.message(Command('start'))
async def start_message(message: types.Message):
    await message.answer(f'Привет {message.from_user.username}', reply_markup=markups.markup_start)


@dp.message(F.text == 'Старт')
async def start_command(message: types, state: FSMContext):
    await state.set_state(PriceState.megik)
    await message.answer('Получил от МЕГИК:')

@dp.message(PriceState.megik)
async def add_state_for_megik(message: types.Message, state: FSMContext):
    megik = cheker(message.text)
    if megik is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии
    await message.answer(f'Мегик: {megik}', reply_markup=markups.create_change_button('megik'))
    await state.update_data(megik=megik)
    await state.set_state(PriceState.orion)
    await message.answer('Получил от ОРИОН:')

@dp.message(PriceState.orion)
async def add_state_for_orion(message: types.Message, state: FSMContext):
    orion = cheker(message.text)
    if orion is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'ОРИОН: {orion}', reply_markup=markups.create_change_button('orion'))

    await state.update_data(orion=orion)
    await state.set_state(PriceState.kalinka)
    await message.answer('Получил от КАЛИНКА:')

@dp.message(PriceState.kalinka)
async def add_state_for_kalinka(message: types.Message, state: FSMContext):
    kalinka = cheker(message.text)
    if kalinka is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'Калинка: {kalinka}', reply_markup=markups.create_change_button('kalinka'))

    await state.update_data(kalinka=kalinka)
    await state.set_state(PriceState.zelenkova)
    await message.answer('Получил от ЗЕЛЕНКОВА:')

@dp.message(PriceState.zelenkova)
async def add_state_for_zelenkova(message: types.Message, state: FSMContext):
    zelenkova = cheker(message.text)
    if zelenkova is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'Зеленкова: {zelenkova}', reply_markup=markups.create_change_button('zelenkova'))

    await state.update_data(zelenkova=zelenkova)
    await state.set_state(PriceState.sbsv)
    await message.answer('Получил от СБСВ:')

@dp.message(PriceState.sbsv)
async def add_state_for_sbsv(message: types.Message, state: FSMContext):
    sbsv = cheker(message.text)
    if sbsv is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'СБСВ: {sbsv}', reply_markup=markups.create_change_button('sbsv'))

    await state.update_data(sbsv=sbsv)
    await state.set_state(PriceState.prestizh)
    await message.answer('Получил от ПРЕСТИЖ:')

@dp.message(PriceState.prestizh)
async def add_state_for_prestizh(message: types.Message, state: FSMContext):
    prestizh = cheker(message.text)
    if prestizh is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'Престиж: {prestizh}', reply_markup=markups.create_change_button('prestizh'))

    await state.update_data(prestizh=prestizh)
    await state.set_state(PriceState.omelchenko)
    await message.answer('Получил от Омельченко:')

@dp.message(PriceState.omelchenko)
async def add_state_for_omelchenko(message: types.Message, state: FSMContext):
    omelchenko = cheker(message.text)
    if omelchenko is None:
        await message.answer('Ошибка: вы ввели некорректное значение. Пожалуйста, введите целое число.')
        return  # Остаемся в том же состоянии

    await message.answer(f'Омельченко: {omelchenko}', reply_markup=markups.create_change_button('omelchenko'))

    await state.update_data(omelchenko=omelchenko)
    data = await state.get_data()
    await database.add_items(data)
    await state.clear()
    await message.answer(f'Готово', reply_markup=markups.done_markups)

@dp.callback_query(lambda callback: callback.data.startswith('change_'))
async def change_callback(callback: types.CallbackQuery, state: FSMContext):
    state_name = callback.data.split('_')[1]
    data = await state.get_data()
    if state_name == 'megik':
        await callback.message.answer(f"Получил от МЕГИК: {data.get('megik')}. Введите новое значение")
        await state.set_state(PriceState.megik)
    elif state_name == 'sbsv':
        await callback.message.answer(f"Получил от СБСВ: {data.get('sbsv')}. Введите новое значение")
        await state.set_state(PriceState.sbsv)
    elif state_name == 'orion':
        await callback.message.answer(f"Получил от ОРИОН: {data.get('orion')}. Введите новое значение")
        await state.set_state(PriceState.orion)
    elif state_name == 'kalinka':
        await callback.message.answer(f"Получил от КАЛИНКА: {data.get('kalinka')}. Введите новое значение")
        await state.set_state(PriceState.kalinka)
    elif state_name == 'zelenkova':
        await callback.message.answer(f"Получил от ЗЕЛЕНКОВА: {data.get('zelenkova')}. Введите новое значение")
        await state.set_state(PriceState.kalinka)
    elif state_name == 'prestizh':
        await callback.message.answer(f"Получил от ПРЕСТИЖ: {data.get('prestizh')}. Введите новое значение")
        await state.set_state(PriceState.prestizh)
    elif state_name == 'omelchenko':
        await callback.message.answer(f"Получил от ОМЕЛЬЧЕНКО: {data.get('omelchenko')}. Введите новое значение")
        await state.set_state(PriceState.omelchenko)

@dp.callback_query(lambda callback: callback.data.startswith('get_sum'))
async def get_sum(callback: types.CallbackQuery):
    sum = await database.get_sum_from_db()
    await callback.message.answer(f'СУММА: {sum}', reply_markup=markups.minus_btn)


@dp.message(F.text == 'МИНУС')
async def minus_sum_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_minus)
    await message.answer('Напиши сумму, которую вычесть')


@dp.message(Form.waiting_for_minus)
async def minus_sum(message: types.Message, state: FSMContext):
    sum_for_minus = cheker(message.text)
    await state.update_data(sum_for_minus=sum_for_minus)

    # Отладочное сообщение
    await message.answer(f'Вы ввели сумму для вычитания: {sum_for_minus}')

    # Переход к следующему состоянию
    await state.set_state(Form.waiting_for_sum)

    # Запрос суммы из базы данных
    sum_from_db = await database.get_sum_from_db()  # Получаем сумму из базы данных
    await state.update_data(sum_from_db=sum_from_db)

    data = await state.get_data()

    # Отладочные сообщения
    await message.answer(f'Сумма из базы данных: {data["sum_from_db"]}')

    # Выполните операцию вычитания
    result = data["sum_from_db"] - data["sum_for_minus"]
    await message.answer(f'ОСТАТОК: {result} ✅✅✅')

    # Завершение состояния
    await state.clear()


async def main():
    await on_starup()
    await dp.start_polling(bot)





if __name__ == '__main__':
    asyncio.run(main())