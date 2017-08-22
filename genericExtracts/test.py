#!/usr/bin/ python

import os
import sys
import yaml
import time
import APIMethod as APIFile
import csv
import math
import smtplib

import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

from email.utils import COMMASPACE, formatdate


# Main function
if __name__ == '__main__':

    filePath =  "K:/Git Code/Python/Output/request1.csv"
    print(filePath)

    if os.path.isfile(filePath):

        ctype, encoding = mimetypes.guess_type(filePath)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

    composedMessage = MIMEMultipart()
    composedMessage['Subject'] = 'Requested Information'
    composedMessage['To'] = "srikrishna.bingi@exusia.com"
    composedMessage['From'] = "srikrishna.bingi@gmail.com"

    ctype, encoding = mimetypes.guess_type(filePath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)


    if maintype == 'text':
        with open(filePath, newline='') as fp:
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filePath) as fp:
            msg = MIMEImage(fp.read())
    elif maintype == 'audio':
        with open(filePath) as fp:
            msg = MIMEAudio(fp.read())
    else:
        with open(filePath) as fp:
            msg = MIMEBase(maintype)
            msg.set_payload(fp.read())
        encoders.encode_base64(msg)


    #attachment = open(filePath, "rb")


    msg.add_header("Content-Disposition", "attachment", filename='request1.csv')
    composedMessage.attach(msg)

    #print(composedMessage.as_string())

    mailObject = smtplib.SMTP('smtp.gmail.com', 587)
    mailObject.starttls()
    mailObject.login('srikrishna.bingi@gmail.com','Sri13krishna')
    mailObject.sendmail("srikrishna.bingi@gmail.com","srikrishna.bingi@exusia.com",composedMessage.as_string())
    print('Done sending Mail')
    mailObject.close()