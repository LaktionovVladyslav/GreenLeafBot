import telebot
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import types

from config import Config
from models import User, PlantCulture

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
bot = telebot.AsyncTeleBot(Config.TOKEN)
app = Flask(__name__)


def log_in(user):
    user_obj = session.query(User).filter(User.id == user.id).first()
    if not user_obj:
        user_obj = User(user)
        session.add(user_obj)
        try:
            session.commit()
        except Exception as error:
            print(error)
            session.rollback()
    return user_obj


def gen_keyboard(items, count=None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if count:
        button_items = zip(*[iter(items)] * count)
        for button_item in button_items:
            keyboard.row(*button_item)
    else:
        keyboard.row(*items)
    return keyboard


def gen_inline_keyboard(items, count=None, back_position=None):
    inline_keyboard = types.InlineKeyboardMarkup()
    button_items = []
    for item in items:
        if back_position:
            button_items.append(types.InlineKeyboardButton('Назад', callback_data='back_{}'.format(back_position)))
        button_items.append(types.InlineKeyboardButton(item.get('text'), callback_data=item.get('value')))
    if count:
        button_items = zip(*[iter(button_items)] * count)
        for button_item in button_items:
            inline_keyboard.row(*button_item)
    else:
        button_items = button_items
        inline_keyboard.row(*button_items)
    return inline_keyboard


def update_main_menu():
    menu_items = [
        'Позиции',
        'Корзина',
        'Сделать заказ',
    ]
    return gen_keyboard(menu_items)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user = log_in(user=message.from_user)
    text = "Здраствуй {first_name} {last_name}\nСтартовый текст".format(
        first_name=user.first_name, last_name=user.last_name
    )
    bot.send_message(message.chat.id, text=text, reply_markup=update_main_menu())


@bot.callback_query_handler(func=lambda call: "positions" in str(call.data))  # Готово
def command_click_inline(call):
    user = log_in(user=call.from_user)
    items = [dict(text=plant_culture.name, value="pc_{}".format(
        plant_culture.id
    )) for plant_culture
             in session.query(PlantCulture).all()]
    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Позиции',
                          reply_markup=gen_inline_keyboard(items, 3))


@bot.callback_query_handler(func=lambda call: "basket_" in str(call.data))  # Готово
def command_click_inline(call):
    user = log_in(user=call.from_user)
    plant_culture_id = call.data.split('_')[1]
    plant_culture = session.query(PlantCulture). \
        filter(PlantCulture.id == plant_culture_id).first()
    user.orders.append(plant_culture)
    session.commit()
    if user.orders:
        text = 'Ваша корзина\n'
        items = [dict(text="{} {}грн ❌".format(order.name, order.price), value="del_{}".format(
            order.id,
        )) for order
                 in user.orders]
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                              reply_markup=gen_inline_keyboard(items, count=3))


@bot.callback_query_handler(func=lambda call: "pc_" in str(call.data))  # Готово
def command_click_inline(call):
    user = log_in(user=call.from_user)
    plant_culture_id = call.data.split('_')[1]
    plant_culture = session.query(PlantCulture). \
        filter(PlantCulture.id == plant_culture_id).first()
    text = "{name}\n{price}\n{description}".format(
        name=plant_culture.name,
        price=plant_culture.price,
        description=plant_culture.description
    )
    items = [dict(text="Добавить в корзину", value="basket_{}".format(
        plant_culture.id,
    ))]
    bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                          reply_markup=gen_inline_keyboard(items, back_position='positions'))


@bot.message_handler(func=lambda message: 'Позиции' in str(message.text))
def button_handler(message):
    user = log_in(user=message.from_user)
    items = [dict(text=plant_culture.name, value="pc_{}".format(
        plant_culture.id,
        message.message_id
    )) for plant_culture
             in session.query(PlantCulture).all()]
    text = 'Позиции'
    bot.send_message(user.id, text=text, reply_markup=gen_inline_keyboard(items, 3))


@bot.message_handler(func=lambda message: 'Корзина' in str(message.text))
def button_handler(message):
    user = log_in(user=message.from_user)
    if user.orders:
        text = 'В вашей корзине\n'
        items = [dict(text="{} {}грн ❌".format(order.name, order.price), value="del_{}".format(
            order.id,
        )) for order
                 in user.orders]
        bot.send_message(user.id, text=text, reply_markup=gen_inline_keyboard(items, count=3))


@bot.message_handler(func=lambda message: 'Сделать заказ' in str(message.text))
def button_handler(message):
    user = log_in(user=message.from_user)
    if user.orders:
        text = 'В вашем заказе\n'
        for order in user.orders:
            text += '- {} {}грн\n'.format(order.name, order.price)
        text += "Всего {}грн".format(sum([order.price for order in user.orders]))
        bot.send_message(user.id, text=text)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    bot.delete_webhook()
    bot.polling()
