import os
from collections import defaultdict
from threading import Timer

from class_remember import rem_id
from imports import bot
from telebot.types import *

SAVE_DIR = 'downloaded_photos'
os.makedirs(SAVE_DIR, exist_ok=True)

# Для хранения фото и таймеров медиагрупп
media_group_photos = defaultdict(list)
media_group_timers = {}

def finalize_media_group(group_id, patient_id, chat_id):
    file_ids = media_group_photos[group_id]
    save_album(patient_id, file_ids)

    # Очистка
    del media_group_photos[group_id]
    del media_group_timers[group_id]

    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('<< Вернуться к пациенту', callback_data=f'patient_return|{rem_id.get_id()}')
    keyboard.add(btn1)
    bot.send_message(chat_id, "Фото сохранено!", reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    patient_id = rem_id.get_id()
    if patient_id == 0:
        return  # Пациент не выбран

    chat_id = message.chat.id
    group_id = message.media_group_id
    file_id = message.photo[-1].file_id  # Самое большое фото

    if group_id:
        # Это медиагруппа — накапливаем фото
        media_group_photos[group_id].append(file_id)

        # Сброс старого таймера
        if group_id in media_group_timers:
            media_group_timers[group_id].cancel()

        # Новый таймер: если в течение 2 секунд не придут новые фото — сохраняем
        t = Timer(2.0, finalize_media_group, args=[group_id, patient_id, chat_id])
        media_group_timers[group_id] = t
        t.start()
    else:
        # Одиночное фото — сохраняем сразу
        save_album(patient_id, [file_id])
        keyboard = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton('<< Вернуться к пациенту', callback_data=f'patient_return|{rem_id.get_id()}')
        keyboard.add(btn1)
        bot.send_message(chat_id, "Фото сохранено!", reply_markup=keyboard)

    rem_id.set_flag(True)

def save_album(patient_id, file_ids):
    album_dir = os.path.join(SAVE_DIR, str(patient_id))
    os.makedirs(album_dir, exist_ok=True)

    # Найти максимум текущих номеров, если есть старые фото
    existing_photos = [f for f in os.listdir(album_dir) if f.startswith("photo_") and f.endswith(".jpg")]
    existing_indices = [int(f.split('_')[1].split('.')[0]) for f in existing_photos if f.split('_')[1].split('.')[0].isdigit()]
    start_index = max(existing_indices, default=0) + 1

    for idx, fid in enumerate(file_ids, start=start_index):
        file_info = bot.get_file(fid)
        downloaded_file = bot.download_file(file_info.file_path)

        filename = f"photo_{idx}.jpg"
        filepath = os.path.join(album_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(downloaded_file)

    print(f"[Сохранено] Альбом {patient_id} → добавлено {len(file_ids)} фото")


def save_photo(message):
    photo = message.photo[-1]  # Самое большое фото
    file_info = bot.get_file(photo.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    # Уникальное имя файла
    filename = os.path.join(SAVE_DIR, f'{photo.file_id}.jpg')
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    print(f'Сохранено: {filename}')
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('<< Вернуться к пациенту', callback_data=f'patient_return|{rem_id.get_id()}')
    keyboard.add(btn1)
    bot.send_message(message.chat.id, "Фото сохранено!", reply_markup=keyboard)
