#!/usr/bin/env python

import sys
import smtplib
import sqlite3
from datetime import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import requests
from bs4 import BeautifulSoup

from config import db_name, server, username, password, from_address, logger

def send_notification(url, page, last_modified, to_address):
    content = BeautifulSoup(page.content)
    title = content.title.getText()
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = title + ' was updated on ' + str(last_modified)
    msg.attach(MIMEText(url, 'plain'))
    s = smtplib.SMTP(server)
    s.starttls()
    s.login(username, password)
    s.sendmail(msg['From'], to_address, msg.as_string())
    s.close

try:
    url = sys.argv[1]
    to_address = sys.argv[2]
    logger.info('Checking ' + url)
    page = requests.get(url)
    last_modified = datetime.strptime(page.headers['last-modified'], "%a, %d %b %Y %H:%M:%S %Z")
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT last_modified FROM page WHERE url = ?", (url,))
    prev_last_modified = cur.fetchone()
    if not prev_last_modified:
        cur.execute("INSERT INTO page (url, last_modified) VALUES (?, ?)", (url, last_modified))
        send_notification(url, page, last_modified, to_address)
        logger.info('New page')
    elif last_modified > datetime.strptime(prev_last_modified[0], "%Y-%m-%d %H:%M:%S"):
        send_notification(url, page, page.headers['last-modified'], to_address)
        cur.execute("UPDATE page SET last_modified = ? WHERE url = ?", (last_modified, url))
        logger.info('Page changed - notification sent to ' + to_address)
    else:
        logger.info('Page has not changed')
    conn.commit()

except:
    logger.exception("Error encountered - Could be bad args")
