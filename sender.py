import re
import os
from pathlib import Path
import smtplib
import yagmail
from random import randrange
from time import sleep
from dotenv import load_dotenv
from yagmail.error import YagInvalidEmailAddress, YagConnectionClosed, YagAddressError

load_dotenv(dotenv_path=Path('.') / '.env')
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
SUBJECT = 'SUBJECT'
PLAN_FILE = Path.joinpath(Path.cwd(), 'EGE_2021.zip')
UNSENDED_FILE = Path.joinpath(Path.cwd(), 'unsended.txt')
EMAIL_TEMPLATE = '''

<strong>P.S. Пожалуйста не отвечайте на это письмо, этот ящик только для рассылки обновления
По всем вопросам пишите мне на <a href=mailto:irene-schmidt@4languagetutors.ru>irene-schmidt@4languagetutors.ru</a>
</strong>

-- 
С уважением,
Кузнецова Ирина
<a href='http://4languagetutors.ru/'>http://4languagetutors.ru/</a>
<a href='https://www.instagram.com/irene_vs_english/'>https://www.instagram.com/irene_vs_english/ - Мой инстаграм</a>
'''


def send_email(receiver_address, id):
    try:
        yag = yagmail.SMTP(SENDER_EMAIL, PASSWORD,
                           smtp_ssl=True,  soft_email_validation=False)
        contents = [
            EMAIL_TEMPLATE, PLAN_FILE
        ]
        yag.send(receiver_address, SUBJECT, contents)
        print(f'{id}. Sended to {receiver_address}')
    except (YagInvalidEmailAddress, YagConnectionClosed,
            YagAddressError, smtplib.SMTPDataError, smtplib.SMTPServerDisconnected) as ex:
        print(ex)
        print(f'{id}. Error sending to {receiver_address}')
        with open(UNSENDED_FILE, 'a') as file:
            file.writelines(f'{id}. {receiver_address}\n')


def emails_reader(file_name='email_list.txt'):
    emails = []
    with open(Path.joinpath(Path.cwd(), file_name)) as fp:
        line = fp.readline()
        while line:
            emails.append(line.strip())
            line = fp.readline()
    return emails


def main():
    emails = emails_reader()
    for id, email in enumerate(emails):
        send_email(email)

        sleep(randrange(5, 20))


if __name__ == '__main__':
    main()
