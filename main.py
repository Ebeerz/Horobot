from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import parse
import config
import datetime


bot = Bot(token=config.TAG)
bot_dispatcher = Dispatcher(bot=bot)

current = datetime.datetime.now().time()
timing = "12:00:10"
name = ""
sign = ""
subscription = -1


@bot_dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"Здравствуй, {message.from_user.first_name}")
    await bot.send_message(message.from_user.id, "Какой у вас знак зодиака?")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    today_horo_button = types.KeyboardButton("Гороскоп на сегодня")
    daily_horo_button = types.KeyboardButton("Вкл/выкл ежедневный гороскоп")
    markup.add(today_horo_button, daily_horo_button)
    await bot.send_message(message.from_user.id, "Выберите пожелание", reply_markup=markup)


@bot_dispatcher.message_handler(content_types="text")
async def text_reply(message: types.Message):
    global subscription, current, sign

    if message.text == "Вкл/выкл ежедневный гороскоп":
        subscription *= -1

        if subscription == 1:
            await bot.send_message(message.from_user.id, "Ежедневный гороскоп включен, предсказания присылаются в "
                                                         "12:00 по Мск")

        if subscription == -1:
            await bot.send_message(message.from_user.id, "Ежедневный гороскоп выключен")

        # while subscription == 1:
        #     await daily_subscription(sign)

    elif message.text == "Гороскоп на сегодня":
        prediction = parse.get_horo(str(sign))
        await bot.send_message(message.from_user.id,
                               f"{message.from_user.first_name}, твой гороскоп на сегодня: " + "\n"
                               + prediction)

    elif message.text.lower() in config.SIGNS:
        sign = config.SIGNS[message.text.lower()]
        await bot.send_message(message.from_user.id, f"Знак {sign}")

    else:
        await bot.send_message(message.from_user.id, "Неккоректный ввод: " + message.text.lower())

# async def daily_subscription(sign, susc):
#     current = datetime.datetime.now().time().strftime("%H:%M:%S")
#     if current == "21:00:10":
#         prediction = parse.get_horo(str(sign))
#         await bot.send_message(message.from_user.id,
#                                f"{message.from_user.first_name}, твой гороскоп на сегодня: " + "\n"
#                                + prediction)

# bot_dispatcher.loop.create_task(daily_subscription(sign))
executor.start_polling(bot_dispatcher, skip_updates=True)
