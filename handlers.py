from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import keyboards
import db
import random
import time


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        text=f"""Assalomu aleykum {user.full_name}. Test turini tanlang""",
        reply_markup=keyboards.home_keyboard()
    )

def contact(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_contact(
        phone_number="+998938554640",
        first_name="Xakimov Allamurod",
        reply_markup=keyboards.home_keyboard()
    )


def models(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        text=f"{user.full_name} let is start!",
        reply_markup=keyboards.models_keyboard()
    )

def models_yopiqtest(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        text=f"{user.full_name} let is start!",
        reply_markup=keyboards.models_yopiqtest_keyboard()
    )

def one_model(update: Update, context: CallbackContext):
    ml = update.callback_query.data.split(":")[1]
    images = db.get_one_model(ml)
    
    context.user_data['images'] = images
    context.user_data['current_image_index'] = 0
    context.user_data['correct_count'] = 0
    context.user_data['incorrect_count'] = 0

    send_next_image(update, context)

def send_next_image(update: Update, context: CallbackContext):
    images = context.user_data.get('images', [])
    current_index = context.user_data.get('current_image_index', 0)

    if current_index < len(images):
        item = images[current_index]
        image_ls = [j['name'] for j in images if j['name'] != item['name']]
        random_image = random.sample(image_ls, 3)
        btns = [
            InlineKeyboardButton(item['name'], callback_data=f'answer:{current_index}:True'), 
            InlineKeyboardButton(random_image[0], callback_data=f'answer:{current_index}:False'),
            InlineKeyboardButton(random_image[1], callback_data=f'answer:{current_index}:False'),
            InlineKeyboardButton(random_image[2], callback_data=f'answer:{current_index}:False')
        ]
        random.shuffle(btns)
        reply_markup = InlineKeyboardMarkup(
            [
                btns[:2],
                btns[2:]
            ]
        )

        if update.callback_query:
            sent_message = update.callback_query.message.reply_photo(
                photo=item['img_url'],
                caption='Rasmni toping (ingliz tilida)',
                reply_markup=reply_markup
            )
        else:
            sent_message = update.message.reply_photo(
                photo=item['img_url'],
                caption='Rasmni toping (ingliz tilida)',
                reply_markup=reply_markup
            )

        context.user_data['current_image_index'] += 1
    else:
        send_report(update, context)

def answer_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(':')
    current_index = int(data[1])
    is_correct = data[2] == 'True'

    if is_correct:
        context.user_data['correct_count'] += 1
        query.answer(text="To'g'ri javob!")
    else:
        context.user_data['incorrect_count'] += 1
        query.answer(text="Noto'g'ri javob!")

    send_next_image(update, context)

def send_report(update: Update, context: CallbackContext):
    correct_count = context.user_data.get('correct_count', 0)
    incorrect_count = context.user_data.get('incorrect_count', 0)

    report_text = f"To'g'ri javoblar soni: {correct_count} ✅\nXato javoblar soni: {incorrect_count} ❌"

    update.callback_query.message.reply_text(
        text=report_text,
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text='Bosh sahifa 🏠')]],
            resize_keyboard=True
        )
        )


def one_model_yopiqtest(update: Update, context: CallbackContext):
    ml = update.callback_query.data.split(":")[1]
    images = db.get_one_model(ml)
    
    context.user_data['images'] = images
    context.user_data['current_image_index'] = 0
    context.user_data['correct_count'] = 0
    context.user_data['incorrect_count'] = 0
    context.user_data['image_check'] = ''


    send_next_image_yopiqtest(update, context)

def send_next_image_yopiqtest(update: Update, context: CallbackContext):
    images = context.user_data.get('images', [])
    current_index = context.user_data.get('current_image_index', 0)

    if current_index < len(images):
        item = images[current_index]
        if update.callback_query:
            sent_message = update.callback_query.message.reply_photo(
                photo=item['img_url'],
                caption='Rasmni toping (ingliz tilida)',
            )
            context.user_data['image_name'] = item['name']
        else:
            sent_message = update.message.reply_photo(
                photo=item['img_url'],
                caption='Rasmni toping (ingliz tilida)',
            )
            context.user_data['image_name'] = item['name']
        context.user_data['current_image_index'] += 1
    else:
        send_image_end(update, context)

def answer_image(update: Update, context: CallbackContext):
    tex = update.message.text
    image_name = context.user_data.get('image_name', '')
    if tex.lower() == image_name.lower():
        context.user_data['image_check'] = tex+' ✅\n'
        context.user_data['correct_count'] += 1
        send_report_yopiqtest(update, context)
    else:
        context.user_data['image_check'] = tex+ ' ❌ -- ' + image_name + ' ✅\n'
        context.user_data['incorrect_count'] += 1
        send_report_yopiqtest(update, context)

    send_next_image_yopiqtest(update, context)

def send_report_yopiqtest(update: Update, context: CallbackContext):
    image_check = context.user_data.get('image_check', '')
    report_text = f"{image_check}"

    update.message.reply_text(
        text=report_text
        )

def send_image_end(update: Update, context: CallbackContext):
    correct_count = context.user_data.get('correct_count', 0)
    incorrect_count = context.user_data.get('incorrect_count', 0)
    report_text = f"To'g'ri javoblar soni: {correct_count} ta ✅\nXato javoblar soni: {incorrect_count} ta ❌"
    update.message.reply_text(
        text= report_text,
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text='Bosh sahifa 🏠')]],
            resize_keyboard=True
        )
        )