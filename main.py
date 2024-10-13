import aiohttp
import asyncio
from telebot.async_telebot import AsyncTeleBot

# апи ключ для телеграм бота
bot = AsyncTeleBot('')
# апи ключ с weatherstack
API_key = ""


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет! Я бот-помощник, который предоставляет данные о погоде в данную секунду в любой точке этого мира. Просто отправь мне город'
    await bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    temp, humidity, pressure = 0, 0, 0

    # урл для запроса 
    url = f"https://api.weatherstack.com/current?access_key={API_key}"

    # параметр с городом
    querystring = {"query": message.text}

    # делаем запрос на получение данных о погоде
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=querystring, timeout=5) as response:
                data = await response.json()
        except Exception as e:
            # выводим ошибку, если что-то пошло не так
            print(f"Произошла ошибка: {e}")
            result = "Произошла ошибка.Попробуйте позже"
        else:
            # обработка внутренних ошибок
            if not data.get("success"):
                result = "Произошла ошибка.Попробуйте позже"

            # обработка данных о погоде 
            city = message.text
            weather = data.get("current")
            if weather:
                temp = weather.get("temperature", 0)
                humidity = weather.get("humidity", 0)
                # перевод в мм рт.ст.
                pressure = weather.get("pressure", 0)*(0.75)

                # собираем обработанные данные
                result = f"Город:{city}\n Температура: {temp}°С\n Влажность: {humidity}%\n Давление: {pressure}мм рт.ст."
    await bot.reply_to(message, result)


asyncio.run(bot.polling())








