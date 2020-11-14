import logging
import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    filename='logs.txt',
    )

URL = os.getenv('SITE_URL')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
MESSAGE_TEXT = f'Проблемы с сервером {URL} - текущий статус код: '
TWILIO_ERROR_TEXT = 'Не удалось отправить сообщение. Проверьте данные для подключения к Twilio'
FROM_PHONE_NUMBER = os.getenv('FROM_PHONE_NUMBER')
TO_PHONE_NUMBER = os.getenv('TO_PHONE_NUMBER')
OK_STATUS = 200
SECONDS_BETWEEN_ATTEMPTS = 60

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_message(current_status):
    try:
        message = client.messages.create(
            body=MESSAGE_TEXT + str(current_status),
            from_=FROM_PHONE_NUMBER,
            to=TO_PHONE_NUMBER,
            )
        logging.info(f'Сообщение успешно отправлено. SID: {message.sid}')
    except Exception:
        logging.critical(TWILIO_ERROR_TEXT)


def check_site_status(url):
    response = requests.get(url)

    return response.status_code


while True:
    logging.info(f'Проверяем доступность сервера {URL}')
    status = check_site_status(URL)

    if status == OK_STATUS:
        logging.info('Статус 200')
    else:
        logging.info(f'Статус {status} - отправляем сообщение')
        send_message(status)

    time.sleep(SECONDS_BETWEEN_ATTEMPTS)
