import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
from googleapiclient.discovery import build
import telebot

def authenticate_google_services():
    json_keyfile_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(json_keyfile_path, scopes=scope)
    client = gspread.authorize(creds)
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, ['https://www.googleapis.com/auth/drive'])
    drive = GoogleDrive(gauth)
    drive_scope = ['https://www.googleapis.com/auth/drive']
    creds_drive = service_account.Credentials.from_service_account_file(json_keyfile_path, scopes=drive_scope)
    service = build('drive', 'v3', credentials=creds_drive)
    bot = telebot.TeleBot('7914311377:AAFmTlDyLgzDBj4AZSxMUVfM_2c8Gm7KxFc')
    return client, drive, service, bot
