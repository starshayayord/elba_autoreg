#! /usr/bin/env python
# -*- coding: utf-8 -*-

import email
import re
import smtplib
from shutil import move
from email.mime.text import MIMEText
from os import listdir
from os.path import isfile, join


def getEmailContentFromFile(emailFile):
    fp = open(emailFile, 'r')
    content = fp.read()
    fp.close()
    msg = email.message_from_string(content)
    message = ''
    if msg.is_multipart():
        for payload in msg.get_payload():
            message += payload.get_payload(decode=True)
    else:
        message = msg.get_payload(decode=True)
    return message


def parseEmailAddress(content):
    abonentEmail = re.search('<mailto:(.*?)>', content)
    if abonentEmail:
        #try to find link
        return abonentEmail.group(1)
    else:
        #try to find plain
        abonentEmail = re.search(r"Электронная почта:\s{0,}([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", content)
        if abonentEmail:
            return abonentEmail.group(1).strip()
        else:
            return False

def sendSpecialEmail(repsonseFile, fromAddress, toAddress, smtpServer, subject):
    # get email content
    fp = open(repsonseFile, 'rb')
    filecontent = fp.read()
    fp.close()
    # create mail message
    msg = MIMEText(filecontent, 'html', 'utf-8')
    msg['To'] = toAddress
    msg['From'] = fromAddress
    msg['Subject'] = subject
    s = smtplib.SMTP(smtpServer)
    s.sendmail(fromAddress, [toAddress], msg.as_string(()))
    s.quit()


mailbox = '/home/autoreg/Maildir/new'
outbody = '/home/autoreg/body.html'
processed_folder = '/home/autoreg/Maildir/old'
err_folder = '/home/autoreg/Maildir/err'
fromAddress = 'info@e-kontur.ru'
smtpServer = 'localhost'
toAddressError = 'dev-elba@kontur.ru'
emailFiles = [f for f in listdir(mailbox) if isfile(join(mailbox, f))]
for emailFile in emailFiles:
    content = getEmailContentFromFile(join(mailbox, emailFile))
    abonentEmail = parseEmailAddress(content)
    if abonentEmail:
        sendSpecialEmail(outbody, fromAddress, abonentEmail, smtpServer, 'Заявка на регистрацию в Эльбе')
        move((join(mailbox, emailFile)), (join(processed_folder, emailFile)))
    else:
        sendSpecialEmail(join(mailbox, emailFile), fromAddress, toAddressError, smtpServer, 'Ошибка обработки регистрационного письма!')
        move((join(mailbox, emailFile)), (join(err_folder, emailFile)))


