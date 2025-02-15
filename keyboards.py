from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_models, get_one_model

def home_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton('🔓 Open Test'), KeyboardButton('🔐 Closed Test')],
            [KeyboardButton('☎️Contact')],
        ],
        resize_keyboard=True,
    )

def models_keyboard():
    btns = []
    for model in get_models():
        btns.append([InlineKeyboardButton(model, callback_data=f'model:{model}')])
    return InlineKeyboardMarkup(
        btns,
        resize_keyboard=True
    )

def models_yopiqtest_keyboard():
    buttons = []
    for model in get_models():
        buttons.append([InlineKeyboardButton(model, callback_data=f'model_yopiq:{model}')])
    return InlineKeyboardMarkup(
        buttons
    )