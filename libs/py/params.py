import os

HOST = os.getenv('HOST',None)
PORT = os.getenv('PORT',None)

DB = os.getenv('DB',None)
DB_USER = None
DB_PASSWORD = None
DB_ID = None
DB_PORT = None

BROWSER = 'Firefox'

SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR','screenshots')
