#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import csv
import random
import time
import datetime
from datetime import timedelta, date
import os, os.path

tomorrow = date.today() - timedelta(days=1)
pic_title = tomorrow.strftime('%Y-%m-%d')
title_date = tomorrow.strftime('%d.%m.')
mp3_folder = tomorrow.strftime('%Y%m%d')

#select random quotation for moral support
line_number = random.randint(1, 7)    
with open("/home/pi/noise/etc/quotes.csv") as f:
    mycsv = csv.reader(f)
    mycsv = list(mycsv)
    quote = mycsv[line_number][0]
    autor = mycsv[line_number][1]

#count recordings, *2 because of 2 min pieces
numfiles = str(len([f for f in os.listdir("/home/pi/noise/mp3/"+mp3_folder) if os.path.isfile(os.path.join("/home/pi/noise/mp3/"+mp3_folder, f)) and f[0] != '.'])*2)

me = "raspberry@.com"
you = "you@.com"
you2 = "you@.com"

#For multiple receiver use
#you = 'he@gmail.com,she@gmail.com'
#you2 =  ['he@gmail.com', 'she@gmail.com']

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "noise level protocol"
msg['From'] = me
msg['To'] = you

# html message
html = """\
<html>
  <head></head>
  <body>
    Good morning,<br>
I have created a noise level protocol of """+title_date+""" and """+numfiles+""" min recorded.<br>
Best regards<br>
<br>
Raspberry Spy<br>
<br>
<table style="text-align: left; width: 100%;" border="0"
 cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td style="width: 49%;">
      <hr style="height:1px; border:none; color:#000; background-color:#000;"></td>
      <td style="width: 2%;">
      <img style="width: 30px; height: 30px;" alt="&ldquo;" src="cid:image1"></td>
      <td style="width: 49%;">
      <hr style="height:1px; border:none; color:#000; background-color:#000;"></td>
    </tr>
    <tr>
      <td style="width: 100%; text-align: center;" colspan="3"
 rowspan="1">""" + quote + """<br><span style="font-style: italic;">- """ + autor + """</span></td>
    </tr>
    <tr>
      <td style="width: 49%;">
      <hr style="height:1px; border:none; color:#000; background-color:#000;"></td>
      <td style="width: 2%;">
      <img style="width: 30px; height: 30px;" alt="&rdquo;" src="cid:image2"></td>
      <td style="width: 49%;">
      <hr style="height:1px; border:none; color:#000; background-color:#000;"></td>
    </tr>

  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
fp = open('/home/pi/noise/etc/q3.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

fp = open('/home/pi/noise/etc/q4.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image2>')
msg.attach(msgImage)

fp = open('/home/pi/noise/pic/'+pic_title+'.png', 'rb')
img = MIMEImage(fp.read())
fp.close()
img.add_header('Content-Disposition', 'attachment', filename=(pic_title+".png"))
msg.attach(img)

msg.attach(part2)
# Send the message via local SMTP server.
mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('raspberry@.com', 'password')
mail.sendmail(me, you2, msg.as_string())
mail.quit()