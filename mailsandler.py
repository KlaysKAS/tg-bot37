import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from platform import python_version


def getHash(string):
    p = 1
    code = 0
    for i in string:
        code += int((ord(i) * p)) % 900000 + 100000
        p *= 36
        p = p % 1e10
    return code % 900000 + 100000


class MailSandler(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.server = 'smtp.mail.ru'

    def sendMail(self, recipient):
        code = getHash(recipient)

        sender = self.user
        subject = 'Подтвердите свою регистрацию на курсах по цифровой безопасности'
        h2 = 'Это CyberSecurityTeacherBot!'
        text = 'Здравствуйте, вы отправили запрос на прохождение курсов по защите данных,' \
               '<br> <b>ваш код: {}.</b> Пришлите его мне в telegram.'.format(code)
        html = '<html><head></head><body><h2>' + h2 + '</h2><p>' + text + '</p><img src="cid:image1" /></body></head>'

        fp = open('CyberBot.jpg', 'rb')  # Read image
        msgImage = MIMEImage(fp.read())
        fp.close()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'CyberTeacher <' + sender + '>'
        msg['To'] = recipient
        msg['Reply-To'] = sender
        msg['Return-Path'] = sender
        msg['X-Mailer'] = 'Python/' + (python_version())

        part_text = MIMEText(text, 'plain')
        part_html = MIMEText(html, 'html')

        msg.attach(part_text)
        msg.attach(part_html)
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        mail = smtplib.SMTP_SSL(self.server)
        mail.login(self.user, self.password)
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()
        return str(code)
