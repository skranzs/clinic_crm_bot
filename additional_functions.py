from telebot.types import *
from imports import rolessheet, sheet


def keyboard_workers(callback_d, additional='', flag=False):
    keyboard = InlineKeyboardMarkup()
    data = rolessheet.get_all_values()
    for row in data:
        if (row[0] != 'TG ID' and additional == '') or (row[2] == additional and not flag) or (row[2] != additional and flag and row[0] != 'TG ID'):
            keyboard.add(InlineKeyboardButton(row[4], callback_data=f'{callback_d}|{row[0]}'))
    return keyboard


def id_value():
    column_values = sheet.col_values(1)
    if column_values[-1].isdigit():
        new_v = int(column_values[-1]) + 1
        return round(new_v)
    else:
        return '0'


def get_name_by_tg_id(tg_id):
    data = rolessheet.get_all_values()
    for row in data:
        if str(tg_id) in row[0]:
            return row[4]