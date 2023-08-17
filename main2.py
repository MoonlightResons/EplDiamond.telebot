import os, re, configparser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
from urllib import request, error
import ssl
from urllib.parse import urljoin
from keyboards import category, back, category_choice
from urllib.parse import quote
# config = configparser.ConfigParser()
# config.read("token.ini")
# TOKEN = config["tgbot"]
# bot = Bot(token=TOKEN)
BOT_TOKEN = "6214273311:AAEvxk889vjvbljjTssXOReBKpMceqVq2Wk"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Хей привет, Данный бот сделан как Пэт-Проект для сайта Эпл Якутские брилианты", reply_markup = category())

@dp.message_handler(text='Категории')
async def category_way(message: types.Message, state: FSMContext):
    await state.set_state("in_category")
    await bot.send_message(chat_id=message.chat.id, text='Вы успешно вернулись в главное меню категорий:', reply_markup=category_choice())

@dp.message_handler(text="Серьги", state="in_category")
async def earrings_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Серьги которые есть на нашем сайте:', reply_markup=back())

    # Получаем текущий номер страницы из состояния (если нет, то 1)
    page_number = await state.get_data()
    if not page_number:
        page_number = 1
    else:
        page_number = page_number.get("page_number", 1)

    base_url = "https://epldiamond.ru/catalog/"
    should_continue = True

    while should_continue:
        category_url = f"{base_url}{quote('diamond-earrings/')}?PAGEN_2={page_number}"
        print(f"Парсинг страницы {page_number}...")
        should_continue = await earrings_pars_page(message, category_url)

        # Увеличиваем номер страницы для следующего прохода
        page_number += 1

    # Сохраняем текущий номер страницы в состоянии
    await state.set_data({"page_number": page_number})

# ... (предыдущий код)


async def earrings_pars_page(message: types.Message, page_number: int):
    try:
        category_url = f"https://epldiamond.ru/catalog/diamond-earrings/?PAGEN_2={page_number}"
        req = request.Request(category_url, headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # Проверяем, что количество данных о товарах корректно
            for item in earrings_data:
                name = item.find('span', itemprop='name')
                price = item.find('div', class_='b-product-card__price-row')
                images = item.find_all('link', itemprop='image')
                discount = item.find('div', class_='b-product-card__discount')

                if name and price and images:
                    name_text = name.text.strip()

                        # Проверяем наличие информации о скидке
                    if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")
                    else:
                            price_text = price.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        # Выбираем только первое изображение из списка
                    image_url = images[0].get('href')

                        # Проверяем, что URL является абсолютным и корректным
                    if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'  # Замените на базовый URL вашего сайта
                            image_url = urljoin(base_url, image_url)

                    await bot.send_photo(chat_id=message.chat.id, photo=image_url)

                    if next_button:
    # Добавляем кнопку "Далее"
                        inline_button = InlineKeyboardButton('Далее', callback_data=f'next_page:{page_number + 1}')
                        inline_keyboard = InlineKeyboardMarkup().add(inline_button)
                        await bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку 'Далее', чтобы увидеть следующую страницу.", reply_markup=inline_keyboard)
                        return True  # Возвращаем True, чтобы цикл продолжился для следующей страницы
                    else:
                        await bot.send_message(chat_id=message.chat.id, text="На сайте нет данных о следующих страницах.")
                        return False  # Возвращаем False, чтобы завершить цикл


                # Проверяем, есть ли кнопка "Далее" на странице
                next_button = soup.find('a', class_='b-pagination__next')
                if next_button:
                    # Добавляем кнопку "Далее"
                    inline_button = InlineKeyboardButton('Далее', callback_data=f'next_page:{page_number + 1}')
                    inline_keyboard = InlineKeyboardMarkup().add(inline_button)
                    await bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку 'Далее', чтобы увидеть следующую страницу.", reply_markup=inline_keyboard)
                else:
                    await bot.send_message(chat_id=message.chat.id, text="На сайте нет данных о следующих страницах.")

            else:
                await bot.send_message(chat_id=message.chat.id, text="На сайте нет данных о серьгах.")

    except error.HTTPError as e:
        print(e)
        return False

@dp.callback_query_handler(lambda c: c.data.startswith('next_page:'))
async def process_next_page(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        _, page_number = callback_query.data.split(':')
        await earrings_pars_page(callback_query.message, int(page_number))

    finally:
        await bot.answer_callback_query(callback_query.id)

    
@dp.message_handler(text="Назад", state="in_category")
async def back_to_categories(message: types.Message, state: FSMContext):
    await state.finish()  # Сбрасываем состояние
    await category_way(message, state)
    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
