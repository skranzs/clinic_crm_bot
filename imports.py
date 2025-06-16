from telebot import *
import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telebot.storage import StateMemoryStorage
import time
import pytz
from docxtpl import DocxTemplate
from telebot.types import *
from bot_auth import *
from search import *
from book_class import *
sheet = client.open_by_key('1Z3UJepBjg8bwJyBjfzo30PdzvjJtwqZabnOs4G5FyeE').worksheet('Пациенты')
rolessheet = client.open_by_key('1Z3UJepBjg8bwJyBjfzo30PdzvjJtwqZabnOs4G5FyeE').worksheet('Общая база')
visitsheet = client.open_by_key('1Z3UJepBjg8bwJyBjfzo30PdzvjJtwqZabnOs4G5FyeE').worksheet('Приёмы')
from edit_class import *
users = {}
data = rolessheet.get_all_values()
for row in data:
    if row[0] != 'ID':
        users[row[0]] = row[2]


def strw(call, znach):
    if call.data.startswith(f'{znach}'):
        return True
    else:
        return False


def splc(call):
    return call.data.split('|')[1]


