import json
import time
import shutil
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from get_actual_atm_data import get_currency_places
from aiogram.dispatcher.filters import Text

bot = Bot(token='', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Че по валюте']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Все ещё уверен, что сможешь снять валюту?', reply_markup=keyboard)


@dp.message_handler(Text(equals='Че по валюте'))
async def get_atms_with_currency(message: types.Message):
    await message.answer('Ищу..')

    while True:
        get_currency_places()

        with open('data/current_result.json') as file:
            current_result = json.load(file)

        with open('data/previous_result.json') as file:
            previous_result = json.load(file)

        for item in current_result:
            if item not in previous_result:
                currency_available = ''
                for currency in item['currencies_available']:
                    currency_available += f'{currency}\n '
                atm_card = f'Адрес: {hlink(item["address"], item["map_link"])}\n ' \
                           f'{hbold("Работает: ")} {item["is_work"]}\n' \
                           f'{hbold("Имеется: ")}\n {currency_available}\n'\


                await message.answer(atm_card)

        shutil.copyfile('data/current_result.json', 'data/previous_result.json')

        time.sleep(2)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
