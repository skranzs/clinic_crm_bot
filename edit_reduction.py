from telebot.types import *
from imports import bot

def em(call, text, markup=None, flag=False):
    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)
    if flag:
        return msg

