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
from urllib.parse import quote
from urllib.parse import urljoin
from keyboards import menu, back, category_choice
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
    await bot.send_message(chat_id=message.chat.id, text="Хей привет, Данный бот сделан как Пэт-Проект для сайта Эпл Якутские брилианты", reply_markup=menu())

@dp.message_handler(text='Категории')
async def category_way(message: types.Message, state: FSMContext):  
    await bot.send_message(chat_id=message.chat.id, text='Вы успешно вошли в категории:', reply_markup=category_choice())
    await state.set_state("in_category")


@dp.message_handler(text="Назад", state="in_category")
async def back_to_categories(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Вы вернулись на главную страницу:', reply_markup=menu())
    await state.finish()

@dp.message_handler(lambda message: message.text == "Далее", state="parsing_next_page")
async def parse_next_page(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Парсинг следующей страницы:', reply_markup=back())
    await state.set_state("in_category")

@dp.message_handler(text="Серьги", state="in_category")
async def earrings_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Серьги которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-earrings/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')


            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")


    except error.HTTPError as e:
        print(e)

# @dp.callback_query_handler(lambda c: c.data == 'next_page')
# async def earrings_pars_page(callback_query: types.CallbackQuery, state: FSMContext):
#     try:
#         # Get the current page number from state
#         page_number = await state.get_data()
#         if not page_number:
#             page_number = 2  # If not present, start from page 2, as the first page was already parsed
#         else:
#             page_number = page_number.get("page_number", 2)

#         base_url = "https://epldiamond.ru/catalog/"
#         should_continue = True

#         while should_continue:
#             category_url = f"{base_url}{quote('diamond-earrings/')}?PAGEN_2={page_number}"
#             should_continue = await earrings_pars_page(callback_query.message, category_url)

#             # Increase the page number for the next iteration
#             page_number += 1

#         # Save the current page number in state
#         await state.set_data({"page_number": page_number})

#     finally:
#         await bot.answer_callback_query(callback_query.id)

@dp.message_handler(text="Кольца", state="in_category")
async def rings_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Кольца которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-rings/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")


    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Подвески", state="in_category")
async def pendants_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Подвески которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-pendants/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Колье", state="in_category")
async def necklaces_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Колье которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-necklaces/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)


@dp.message_handler(text="Браслеты", state="in_category")
async def bracelets_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Браслеты которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-bracelets/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Броши", state="in_category")
async def brooches_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Броши которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-brooches/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Запонки", state="in_category")
async def cufflinks_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Запонки которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/diamond-cufflinks/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Зажимы", state="in_category")
async def clips_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Зажимы которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/tie-clips/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Цепи", state="in_category")
async def chains_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Цепи которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/chains/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Диадемы", state="in_category")
async def tiaras_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Диадемы которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/tiaras/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

@dp.message_handler(text="Сувениры", state="in_category")
async def souvenirs_pars(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Сувениры которые есть на нашем сайте:', reply_markup=back())
    try:
        req = request.Request('https://epldiamond.ru/catalog/souvenirs/', headers=headers)
        with request.urlopen(req) as resp:
            data = resp.read()
            soup = BeautifulSoup(data, 'lxml')
            earrings_data = soup.find_all('div', class_='b-product-card__main')

            # ... (previous code)

            if len(earrings_data) > 0:
                for item in earrings_data:
                    name = item.find('span', itemprop='name')
                    price = item.find('div', class_='b-product-card__price-row')
                    images = item.find_all('link', itemprop='image')
                    discount = item.find('div', class_='b-product-card__discount')
                    link_earrings = item.find('a', class_='b-product-card__title')
                    # description = item.find('div', class_='b-product-card__more-description')

                    if name and price and images and link_earrings:
                        name_text = name.text.strip()

                        if discount:
                            price_text = price.find('span', class_='b-product-card__price--old').text.strip()
                            discount_text = discount.find('span', class_='b-product-card__price').text.strip()
                            # description_text = description.find('div', itemprop='description').text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\nЦена без скидки: {price_text}\nЦена со скидкой: {discount_text}")

                        else:
                            price_text = price.text.strip()
                            # description_text = description.text.strip()
                            await bot.send_message(chat_id=message.chat.id, text=f"{name_text}\n{price_text}")

                        image_url = images[0].get('href')
                        link_url = link_earrings.get('href')

                        if image_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            image_url = urljoin(base_url, image_url)

                        if link_url and not image_url.startswith(('http://', 'https://')):
                            base_url = 'https://epldiamond.ru/'
                            link_url = urljoin(base_url, link_url)

                        link_button = InlineKeyboardButton(text="Посмотреть товар", url="https:" + link_url)

                        # Создаем объект клавиатуры с кнопкой ссылки
                        product_link = InlineKeyboardMarkup().add(link_button)
                        await bot.send_photo(chat_id=message.chat.id, photo=image_url, reply_markup=product_link)

                        # await state.set_state("parsing_next_page")

    except error.HTTPError as e:
        print(e)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)