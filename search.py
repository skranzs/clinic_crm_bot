from bot_auth import *
from telebot.types import *
sheet = client.open_by_key('1Z3UJepBjg8bwJyBjfzo30PdzvjJtwqZabnOs4G5FyeE').worksheet('Пациенты')

def patient_search(call, message_id='', category=''):
    message_text = "Выберите пациента, с которым вы хотите продолжить взаимодействие:"
    status_column = sheet.col_values(1)
    for i, value in enumerate(status_column):
        print(value)
    matching_indices = [i + 1 for i, value in enumerate(status_column) if value != 'ID пациента'][:11]
    print(matching_indices)
    matching_rows = [sheet.row_values(index) for index in matching_indices[:11]]
    call_data = '001'
    keyboard = create_inline_buttons(matching_rows, category=category, page_number=1)
    keyboard.add(InlineKeyboardButton('<< Вернуться назад', callback_data=call_data))
    return message_text, keyboard


def create_inline_buttons(objects_data, page_number, category=''):
    buttons = []
    start_index = (page_number - 1) * 10
    flag_for_check = False
    try:
        for_check_next_page = objects_data[10]
        flag_for_check = True
    except IndexError:
        pass
    objects_data = objects_data[:10]
    for i in range(0, min(start_index + 10, len(objects_data))):
        object_id = objects_data[i][0]
        object_name = objects_data[i][1]
        callback = f'object|{object_id}'
        button = InlineKeyboardButton(text=f"{object_name}", callback_data=callback)
        buttons.append(button)
    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    keyboard = InlineKeyboardMarkup(row_width=2)
    print(buttons)
    for row_buttons in rows:
        keyboard.add(*row_buttons)
    if flag_for_check is True:
        next_page_button = InlineKeyboardButton(text="Следующая страница",
                                                      callback_data=f"next_page_{page_number + 1}_{category}")
        keyboard.add(next_page_button)
    if len(objects_data) == 0:
        return True
    if page_number != 1:
        previous_page_button = InlineKeyboardButton(text="Предыдущая страница",
                                                          callback_data=f"previous_page_{page_number + 1}_{category}")
        keyboard.add(previous_page_button)
    return keyboard