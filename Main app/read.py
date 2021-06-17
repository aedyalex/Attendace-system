#!/usr/bin/env python

import RPi.GPIO as GPIO
import I2C_LCD_driver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import requests
import json
from servo_driver import *
from mfrc522 import SimpleMFRC522
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
reader = SimpleMFRC522()
lcd = I2C_LCD_driver.lcd()
servo = Servo_driver(7)

# for LEDs
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

# for email
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

valid_entries = ["Cody"]

id = 0
text = ""
server_address = 'http://192.168.0.108:5000'
headers = {'Content-type': 'application/json', 'Accept':'text/plain'}

def send_email(content):

    server.login('lockdoor.monitoring@gmail.com','Aiwprton.1')
    server.sendmail('lockdoor.monitoring@gmail.com','eduard-alexandru.codau@student.tuiasi.ro',content.as_string())

def send_post_to_server(json_text):
    requests.post(server_address,data=json_text, headers=headers)
    
    
def display_waiting_text():
    global id
    global text
    while id == 0 and text == "":
        lcd.lcd_display_string("Waiting for card")
        lcd.lcd_clear()
        
        lcd.lcd_display_string("Waiting for card.")
        sleep(0.5)
        lcd.lcd_clear()
        
        lcd.lcd_display_string("Waiting for card..")
        sleep(0.5)
        lcd.lcd_clear()
        
        lcd.lcd_display_string("Waiting for card...")
        sleep(0.5)
        
def read():
    global id
    global text

    t = threading.Thread(target=display_waiting_text)
    t.start()
  
    id, text = reader.read()
    t.join()
    
    print(id)
    print(text)
    
    if str(text.split(" ")[0]) in valid_entries:
        GPIO.output(13, GPIO.HIGH)
        
        lcd.lcd_display_string("Acces granted: " + text,1)
        json_text = json.dumps({"name": str(text.split(" ")[0]), "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status":"granted"})
        t1 = threading.Thread(target=send_post_to_server,args=(json_text,))
        t1.start()
        
        message = MIMEMultipart()
        message['From'] = 'lockdoor.monitoring@gmail.com'
        message['To'] = 'eduard-alexandru.codau@student.tuiasi.ro'
        message['Subject'] = 'Monitoring notification'
        email = "La data de " + str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + " utilizatorul " + str(text.split(" ")[0]) + " a incercat sa acceseze sistemul. Rezultat: granted"
        message.attach(MIMEText(email,'plain'))
        
        t2 = threading.Thread(target=send_email,args=(message,))
        t2.start()
        
        servo.unlock()
        sleep(5)
        GPIO.output(13, GPIO.LOW)
        servo.lock()
    else:
        print(text)
        GPIO.output(11, GPIO.HIGH)
        lcd.lcd_display_string("Acces denied: " + text,1)
        json_text = json.dumps({"name": str(text.split(" ")[0]), "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status":"denied"})
        t1 = threading.Thread(target=send_post_to_server, args=(json_text,))
        t1.start();
        
        message = MIMEMultipart()
        message['From'] = 'lockdoor.monitoring@gmail.com'
        message['To'] = 'eduard-alexandru.codau@student.tuiasi.ro'
        message['Subject'] = 'Monitoring notification'
        email = "La data de " + str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + " utilizatorul " + str(text.split(" ")[0]) + " a incercat sa acceseze sistemul. Rezultat: denied"
        message.attach(MIMEText(email,'plain'))
        
        t2 = threading.Thread(target=send_email,args=(message,))
        t2.start()
        sleep(3)
        GPIO.output(11, GPIO.LOW)

    id = 0
    text = ""

