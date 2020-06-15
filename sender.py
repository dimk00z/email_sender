import re
import os
from pathlib import Path
import smtplib
import yagmail
from random import randrange
from time import sleep
from yagmail.error import YagInvalidEmailAddress, YagConnectionClosed, YagAddressError


SENDER_EMAIL = '**'
PASSWORD = '***'
SUBJECT = 'Обновление плана ЕГЭ 2021'
PLAN_FILE = Path.joinpath(Path.cwd(), 'EGE_2021.zip')
UNSENDED_FILE = Path.joinpath(Path.cwd(), 'unsended.txt')
EMAIL_TEMPLATE = '''Дорогой подписчик!
Недавно я обновила "План подготовки к ЕГЭ", который ты получил с этим письмом.
В нем:
1) Убрала из списка литературы справочник Бодоньи по словообразованию, потому что он очень сложный для 11-классника. Необходимое словообразование есть в пособии, которое идет следующим пунктом.
2) Это пособие Громовой и Орловой "ЕГЭ-2020. Английский язык. Разделы «Письмо» и «Говорение»", которое внесла в список литературы, рекомендованной к приобретению. В нем содержатся отлично проработанные лексические темы, необходимые для успешной сдачи экзамена.
3) Также в план добавила ссылки на страницы из своей "Грамматика ЕГЭ" для вашего удобства.
4) Дополнила и поменяла местами некоторые темы, которые мне показались логичными.
5) Убрала список эссе по темам, потому что многие темы уже так не формулируются + этот список доступен в книге Громовой и Орловой и есть у меня в плане, разбитый по темам.
На этом все! Больше план редактировать не собираюсь, это - его финальная версия.

Всем удачи в подготовке к экзаменам!

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
                           #    host='smtp.yandex.ru', port=465,
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
            file.writelines(receiver_address+'\n')


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
    for id, email in enumerate(emails[514:]):
        send_email(email, id+514)
        sleep(randrange(5, 20))


if __name__ == '__main__':
    main()
