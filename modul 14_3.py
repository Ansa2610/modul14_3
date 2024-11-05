from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# woman: 10 x weight (kg) + 6,25 x growth (sm) – 5 x age (yy) – 161

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kbl = InlineKeyboardMarkup(resize_keybord=True)
button_kbl1 = InlineKeyboardButton(text='How many calories do I need?', callback_data='calories')
button_kbl2 = InlineKeyboardButton(text='Formulas to calculate', callback_data='formulas')
kbl.add(button_kbl1)
kbl.add(button_kbl2)

kbl_new = InlineKeyboardMarkup(resize_keyboard=True)
button_1 = InlineKeyboardButton(text="Product1", callback_data='product buying')
button_2 = InlineKeyboardButton(text="Product2", callback_data='product buying')
button_3 = InlineKeyboardButton(text="Product3", callback_data='product buying')
button_4 = InlineKeyboardButton(text="Product4", callback_data='product buying')
kbl_new.add(button_1)
kbl_new.add(button_2)
kbl_new.add(button_3)
kbl_new.add(button_4)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_count = KeyboardButton(text="Count")
button_info = KeyboardButton(text='Information')
button_buy = KeyboardButton(text='Buy')
kb.add(button_count)
kb.add(button_info)
kb.add(button_buy)


@dp.message_handler(text='Buy')
async def get_buying_list(message):
	with open('1.jpg', 'rb') as img:
		await message.answer_photo(img, f'Name: Product1 | Description: description 1 | Price: {1 * 100} Rub')
	with open('2.jpg', 'rb') as img:
		await message.answer_photo(img, f'Name: Product2 | Description: description 2 | Price: {2 * 100} Rub')
	with open('3.jpg', 'rb') as img:
		await message.answer_photo(img, f'Name: Product3 | Description: description 3 | Price: {3 * 100} Rub')
	with open('4.jpg', 'rb') as img:
		await message.answer_photo(img, f'Name: Product4 | Description: description 4 | Price: {4 * 100} Rub')
	await message.answer("Choose product you wish to buy:", reply_markup=kbl_new)


@dp.callback_query_handler(text='product buying')
async def send_confirmation_message(call):
	await call.message.answer('Your purchase was successful!')
	await call.answer()



@dp.message_handler(text=['hello'])
async def hello_message(message):
	print('Enter command /start to initiate communication')
	await message.answer('Enter command /start to initiate communication')


@dp.message_handler(commands=['start'])
async def start(message):
	# print('Hello! I am bot and can count calories for women')
	await message.answer('Hello! I am bot and can count calories for women', reply_markup=kb)


@dp.message_handler(text='Information')
async def information_message(message):
	print(
		'This bot is created to assist your with calculation of calories.'
		'At the moment bot is able to calculate calories for women only.'
		'Soon will be added an option to calculate calories for men.'
	)
	await message.answer(
		'This bot is created to assist your with calculation of calories. '
		'At the moment bot is able to calculate calories for women only. '
		'Soon will be added an option to calculate calories for men. '
	)


class UserState(StatesGroup):
	age = State()
	growth = State()
	weight = State()


@dp.message_handler(text='Count')
async def main_menu(message):
	await message.answer('Choose option:', reply_markup=kbl)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
	await call.message.answer(
		'Formula to calculate calories for women:'
		' 10 x weight (kg) + 6,25 x growth (sm) – 5 x age (yy) – 161'
	)
	await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
	await call.message.answer(f'Enter your age')
	await UserState.age.set()
	await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
	await state.update_data(age=message.text)
	await message.answer(f'Enter your growth in sm')
	await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
	await state.update_data(growth=message.text)
	await message.answer(f'Enter your weight in kg')
	await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
	await state.update_data(weight=message.text)
	data = await state.get_data()
	results = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
	await message.answer(f'Your normal amount of calories per day is {results}')
	await state.finish()


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)