from class_remember import rem_id
from imports import sheet, bot
from telebot.types import *
from additional_functions import id_value

def register_name_surname_patient(message):
    msg = bot.send_message(message.chat.id, 'Введите размер обуви')
    bot.register_next_step_handler(msg, register_size_of_foot, message.text)


def register_size_of_foot(message, name_and_surname):
    msg = bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(msg, register_phone_number, name_and_surname, message.text)


def register_phone_number(message, name_and_surname, size_of_foot):
    global data
    nas = name_and_surname.split()
    name, surname = nas[0], nas[1]
    sheet.append_row([id_value(), name, surname, size_of_foot, '', message.text])
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('<<< Вернуться в меню', callback_data='return_menu_edit')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, 'Вы успешно добавили пациента!', reply_markup=keyboard)
    rem_id.set_data(sheet.get_all_values())

