import os
from aiogram import Bot, Dispatcher, executor, types
import logging
import redis


# указываем какие переменные окружения используем
API_TOKEN = os.getenv("API_TOKEN")
REDIS_DB = os.getenv("REDIS_DB")
USER_ID = int(os.getenv("USER_ID"))

# подключаемся к Redis, как к базе данных, для подгрузки баланса кошелька
r = redis.StrictRedis(REDIS_DB, db=0)

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# определяем бота Telegram
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# описываем клавиатуру ReplyKeyboardMarkup
item_eth = types.KeyboardButton('ETH')
item_pht = types.KeyboardButton('PHT')
item_vin = types.KeyboardButton('VIN')
item_all = types.KeyboardButton('ALL')
markup = types.ReplyKeyboardMarkup(keyboard=[[item_eth, item_pht, item_vin, item_all]], resize_keyboard=True)


def auth_custom(func):
    """
    Функция-декоратор для того, чтобы ботом мог пользоваться только один юзер, его id указываем в переменных
    окружения, другой пользователь не сможет узнать баланс чужого кошелька.
    """
    async def wrapper(message):
        if message['from']['id'] != USER_ID:
            return await message.reply("У вас нет доступа", reply=False)
        return await func(message)
    return wrapper


@dp.message_handler(commands=['start'])
@auth_custom
async def start(message: types.Message):
    """ При первом запуске и нажатии на кнопку старт, бот отправляет текстовое сообщение и отображает
        клавиатуру для выбора варианта дальнейших действий """
    start_text = 'Пожалуй, начнём!'
    await bot.send_message(chat_id=USER_ID, text=start_text, reply_markup=markup)


@dp.message_handler(content_types=['text'])
@auth_custom
async def get_balance(message: types.InputTextMessageContent):

    """ Функция get_balance получает от пользователя выбранный им на клавиатуре ReplyKeyboardMarkup
        вариант кнопки в формате текста и, в зависимости выбранного варианта, отправляет ему в
        ответном сообщении баланс по интересующему его токену. Данные по балансам подтягиваются из Redis"""

    if message.text == 'ETH':
        text_eth = str(r.get('balance_eth')).strip('b').strip("'") + ' ETH on the Wallet'
        await bot.send_message(message.chat.id, text=text_eth, reply_markup=markup)
    if message.text == 'PHT':
        text_pht = str(r.get('balance_pht')).strip('b').strip("'") + ' PHT on the Wallet'
        await bot.send_message(message.chat.id, text=text_pht, reply_markup=markup)
    if message.text == 'VIN':
        text_vin = str(r.get('balance_vin')).strip('b').strip("'") + ' VIN on the Wallet'
        await bot.send_message(message.chat.id, text=text_vin, reply_markup=markup)
    if message.text == 'ALL':
        text_all = str(r.get('balance_eth')).strip('b').strip("'") + ' ETH on the Wallet\n' \
                   + str(r.get('balance_pht')).strip('b').strip("'") + ' PHT on the Wallet\n' \
                   + str(r.get('balance_vin')).strip('b').strip("'") + ' VIN on the Wallet\n'
        await bot.send_message(message.chat.id, text=text_all, reply_markup=markup)


# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
