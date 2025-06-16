import os.path
import bot_auth
import patient_list
from imports import *
from edit_reduction import em
from find_by_id import upload_new_info
from save_photo import handle_photo, save_photo
from class_remember import rem_id
from time import *
from new_patient import register_name_surname_patient
from additional_functions import keyboard_workers, id_value, get_name_by_tg_id
from setting_tg_bot import settings_admin
rem_id.set_data(sheet.get_all_values())


@bot.message_handler(commands=['start'])
def handle_start(message, edit_flag=False):
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(
        text="🔎 Найти пациента",
        switch_inline_query_current_chat=""
    )
    btn2 = InlineKeyboardButton('Добавить пациента', callback_data='010')
    btn3 = InlineKeyboardButton('Расписание', callback_data='002')
    btn4 = InlineKeyboardButton('Настройки', callback_data='003')
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn4)
    if not edit_flag:
        msg = bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard)
        edit_id.set_id(new_id=msg.message_id)
    else:
        msg = em(message, 'Выберите категорию:', keyboard, flag=True)
        edit_id.set_id(new_id=msg.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data, 'CALL DATA')
    if strw(call, '001'):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ожидайте...')
        msg, keyboard = patient_search(call)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=keyboard)
    if strw(call, '003'):
        settings_admin(call)
    if strw(call, '004'):
        id_pat = splc(call)

        create_session(call.from_user.id, id_pat)

        msg_text, keyboard = start_booking(call.message, id_pat)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_text, reply_markup=keyboard)
    if strw(call, 'date'):
        date = call.data.split(":")[1]
        session = get_session(call.from_user.id)
        session.date = date

        # Получаем занятые времена
        all_rows = visitsheet.get_all_values()
        occupied = [row[1] for row in all_rows if row[0] == date]
        print(date, occupied)

        time_slots = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "14:00", "14:30", "15:00", '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00']
        markup = InlineKeyboardMarkup(row_width=4)
        btns = []
        for time in time_slots:
            if time in occupied:
                btns.append(InlineKeyboardButton(text=f"{time} ❌", callback_data="busy"))
            else:
                btns.append((InlineKeyboardButton(text=f"{time} ✅", callback_data=f"time|{time}")))
        markup.add(*btns)
        bot.edit_message_text("Выберите время:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    if strw(call, 'time'):
        time = splc(call)
        session = get_session(call.from_user.id)
        session.time = time

        # Проверим ещё раз, свободно ли
        all_rows = visitsheet.get_all_values()
        for row in all_rows:
            if row[0] == session.date and row[1] == time:
                bot.answer_callback_query(call.id, "Это время уже занято.")
                return

        # Сохраняем
        visitsheet.append_row([session.date, session.time, session.patient_id])
        data_search = sheet.col_values(1)
        for i, name in enumerate(data_search):
            if name == session.patient_id:
                sheet.update_cell(i + 1, 7, session.date)
                sheet.update_cell(i + 1, 8, session.time)
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('<< Вернуться к пациенту', callback_data=f'patient_return|{session.patient_id}')
        keyboard.add(btn1)
        bot.edit_message_text(
            f"✅ Запись подтверждена:\n🗓 {session.date} в ⏰ {session.time}",
            call.message.chat.id,
            call.message.message_id, reply_markup=keyboard)
        # Чистим сессию
        sessions.pop(call.from_user.id, None)
    if strw(call, '005'):
        id_patient = splc(call)
        msg = em(call, 'Отправьте фото:', flag=True)
        bot.register_next_step_handler(msg, handle_photo)
        rem_id.set_id(id_patient)
    if strw(call, '006'):
        id_patient = splc(call)
        msg = em(call, 'Введите описание:', flag=True)
        bot.register_next_step_handler(msg, upload_description, id_patient)
    if strw(call, '007'):
        keyboard = keyboard_workers('delete', 'Админ', True)
        keyboard.add(telebot.types.InlineKeyboardButton('<< Вернуться назад', callback_data='003'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите человека:', reply_markup=keyboard)
    if strw(call, '008'):
        data_search, persons, count = rolessheet.get_all_values(), '', 0
        for row in data_search:
            if row[0] not in ['TG ID', '1196990853']:
                persons += f'{row[-1]} ({row[-3]}) {row[-2]}\n'
                count += 1
        message_text = (f'У Вас зарегистрировано {count} сотрудников\n'
                        f'К ним относятся:\n'
                        f'{persons}')
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('<<< Вернуться в настройки', callback_data='003')
        keyboard.add(btn1)
        em(call, message_text, keyboard)
    if strw(call, 'patient_return'):
        id_patient, data_search, list_patient = splc(call), sheet.get_all_values(), []
        for row in data_search:
            if row[0] == id_patient:
                list_patient = row
                break
        msg_t = patient_list.create_patient_list_message(list_patient, call.message.chat.id)
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Назначить приём', callback_data=f'004|{id_patient}')
        btn2 = InlineKeyboardButton('Добавить фотографии', callback_data=f'005|{id_patient}')
        btn3 = InlineKeyboardButton('Изменить анамнез', callback_data=f'012|{id_patient}')
        btn4 = InlineKeyboardButton('Изменить описание', callback_data=f'006|{id_patient}')
        btn5 = InlineKeyboardButton('<<< Вернуться в меню', callback_data=f'return_menu_edit')
        keyboard.add(btn1, btn2)
        keyboard.add(btn3, btn4)
        keyboard.add(btn5)
        album_dir = os.path.join("downloaded_photos", id_patient).replace('\\', '/')
        # print(type(album_dir), album_dir == 'downloaded_photos/0', album_dir,
              # print(os.path.exists(f'downloaded_photos\\0')))
        media = []
        if os.path.exists(album_dir):
            photo_files = sorted(os.listdir(album_dir))
            if photo_files:
                for filename in photo_files:
                    path = os.path.join(album_dir, filename)
                    with open(path, 'rb') as photo:
                        media.append(telebot.types.InputMediaPhoto(photo.read()))
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if media:
            msg = bot.send_media_group(call.message.chat.id, media)
            msg_ids = [ms.message_id for ms in msg]
            rem_id.set_id_img(msg_ids)
        bot.send_message(call.message.chat.id, msg_t, reply_markup=keyboard)
    if strw(call, 'return_menu_edit'):
        id_img = rem_id.get_id_img()
        if len(id_img) != 0:
            for i in id_img:
                bot.delete_message(chat_id=call.message.chat.id, message_id=i)
        rem_id.set_zero_id_img()
        handle_start(call, edit_flag=True)
    if strw(call, '010'):
        msg = em(call, 'Введите имя и фамилию пациента через пробел', flag=True)
        bot.register_next_step_handler(msg, register_name_surname_patient)
    if strw(call, 'delete'):
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton('Да', callback_data=f'011|{call.data.split("|")[1]}')
        btn2 = telebot.types.InlineKeyboardButton('Нет', callback_data='003')
        keyboard.add(btn1, btn2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Вы подтверждаете, что хотите удалить сотрудника {get_name_by_tg_id(splc(call))}?',
                              reply_markup=keyboard)
    if strw(call, '011'):
        cell = rolessheet.find(splc(call))
        rolessheet.delete_rows(cell.row)
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('<<< Вернуться в настройки', callback_data='003')
        keyboard.add(btn1)
        em(call, 'Вы успешно удалили сотрудника.', keyboard)


def upload_description(message, id_patient):
    global data
    data_search = sheet.get_all_values()
    for row in data_search:
        if row[0] == id_patient:
            upload_new_info(sheet, id_patient, 5, f'{row[4]}\n{message.text}')
            break
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('<< Вернуться к пациенту', callback_data=f'patient_return|{id_patient}')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, 'Вы успешно обновили описание!', reply_markup=keyboard)
    data = sheet.get_all_values()


def search_patients(query, patients_list):
    query = query.lower()
    results = []
    for patient in patients_list:
        if (query in patient[1].lower() or  # Имя
            query in patient[2].lower()):    # Фамилия
            results.append(patient)
    return results


@bot.message_handler(func=lambda message: message.via_bot and message.via_bot.username == 'podologvoytenko_bot')
def handle_via_bot_message(message):
    try:
        chat_id = message.chat.id
        bot.delete_message(chat_id=message.chat.id, message_id=edit_id.get_id())
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        id_patient, data_search, list_patient = message.text.replace('(', '*').replace(')', '*').split('*')[1], sheet.get_all_values(), []
        for row in data_search:
            if row[0] == id_patient:
                list_patient = row
                break
        msg_t = patient_list.create_patient_list_message(list_patient, message.chat.id)
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('Назначить приём', callback_data=f'004|{id_patient}')
        btn2 = InlineKeyboardButton('Добавить фотографии', callback_data=f'005|{id_patient}')
        btn3 = InlineKeyboardButton('Изменить анамнез', callback_data=f'012|{id_patient}')
        btn4 = InlineKeyboardButton('Изменить описание', callback_data=f'006|{id_patient}')
        btn5 = InlineKeyboardButton('<<< Вернуться в меню', callback_data=f'return_menu_edit')
        keyboard.add(btn1, btn2)
        keyboard.add(btn3, btn4)
        keyboard.add(btn5)

        album_dir = os.path.join("downloaded_photos", id_patient).replace('\\', '/')
        print(type(album_dir), album_dir == 'downloaded_photos/0', album_dir, print(os.path.exists(f'downloaded_photos\\0')))
        media = []
        if os.path.exists(album_dir ):
            photo_files = sorted(os.listdir(album_dir))
            if photo_files:
                for filename in photo_files:
                    path = os.path.join(album_dir, filename)
                    with open(path, 'rb') as photo:
                        media.append(telebot.types.InputMediaPhoto(photo.read()))
        if media:
            msg = bot.send_media_group(chat_id, media)
            msg_ids = [ms.message_id for ms in msg]
            rem_id.set_id_img(msg_ids)
        bot.send_message(message.chat.id, msg_t, reply_markup=keyboard)


    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_search(query):
    data = rem_id.get_data()
    patients = [i for i in data if i[0] != 'ID пациента']
    search_results = search_patients(query.query, patients)

    results = []
    for patient in search_results:
        title = f"{patient[2]} {patient[1]} ({patient[0]})"  # Фамилия Имя
        description = "Пациент"

        item = types.InlineQueryResultArticle(
            id=str(patient[0]),
            title=title,
            description=description,
            thumbnail_url='https://i.pinimg.com/originals/d6/98/cb/d698cb0a02785bbadd991f942a39a214.jpg',
            input_message_content=types.InputTextMessageContent(
                message_text=f"{title}"
            )
        )
        results.append(item)

    bot.answer_inline_query(query.id, results, cache_time=1)



if __name__ == '__main__':
    bot.polling(non_stop=True)