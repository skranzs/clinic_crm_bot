from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import *
import pytz

class BookingSession:
    def __init__(self, operator_id, patient_id):
        self.operator_id = operator_id
        self.patient_id = patient_id
        self.date = None
        self.time = None

    def is_complete(self):
        return self.date and self.time


sessions = {}

def get_session(operator_id):
    return sessions.get(operator_id)



# Функция создания сессии
def create_session(operator_id, patient_id):
    sessions[operator_id] = BookingSession(operator_id, patient_id)
    return sessions[operator_id]


def start_booking(message, patient_id):
    operator_id = message.from_user.id
    sessions[operator_id] = BookingSession(operator_id, patient_id)
    markup = InlineKeyboardMarkup(row_width=5)
    moscow_tz = pytz.timezone("Europe/Moscow")
    now_moscow = datetime.now(moscow_tz)
    today = now_moscow.date()
    btns = []
    for i in range(30):
        date = today + timedelta(days=i)
        if i == 0 and now_moscow.hour >= 9:
            continue
        btns.append(InlineKeyboardButton(
            text=date.strftime("%d-%m-%y"),
            callback_data=f"date:{date.strftime('%d-%m-%y')}"
        ))
    markup.add(*btns)
    return f"Выберите дату приёма для пациента:", markup