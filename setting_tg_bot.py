from telebot.types import *
from imports import bot


def settings_admin(call):
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Удаление сотрудника', callback_data='007')
    btn3 = InlineKeyboardButton('Информация', callback_data='008')
    keyboard.add(btn1, btn3)
    keyboard.add(InlineKeyboardButton('<< Вернуться назад', callback_data='return_menu_edit'))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите категорию:', reply_markup=keyboard)