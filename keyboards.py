from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def menu():
    category_button = KeyboardButton("Категории")
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu_kb.add(category_button)
    return menu_kb

def back():
    inline_keyboard = InlineKeyboardMarkup()
    button_back = KeyboardButton('Назад')
    inline_button = InlineKeyboardButton('Next Page', callback_data='next_page')
    inline_keyboard.add(inline_button)
    back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_kb.add(button_back)
    return back_kb  # Верните только объект клавиатуры


def category_choice():
    earrings = KeyboardButton("Серьги")
    rings = KeyboardButton("Кольца")
    pendant = KeyboardButton("Подвески")
    necklaces= KeyboardButton("Колье")
    bracelets = KeyboardButton("Браслеты")
    brooches = KeyboardButton("Броши")
    cufflinks = KeyboardButton("Запонки")
    clips = KeyboardButton("Зажимы")
    chains = KeyboardButton("Цепи")
    tiaras = KeyboardButton("Диадемы")
    souvenirs = KeyboardButton("Сувениры")
    category_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    category_kb.add(earrings)
    category_kb.add(rings)
    category_kb.add(pendant)
    category_kb.add(necklaces)
    category_kb.add(bracelets)
    category_kb.add(brooches)
    category_kb.add(cufflinks)
    category_kb.add(clips)
    category_kb.add(chains)
    category_kb.add(tiaras)
    category_kb.add(souvenirs)
    return category_kb

# def next_page():
#     inline_keyboard = InlineKeyboardMarkup()
#     inline_button = InlineKeyboardButton('Next Page', callback_data='next_page')
#     inline_keyboard.add(inline_button)
#     return inline_keyboard
