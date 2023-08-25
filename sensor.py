from DHT_data import DHT_data
from bh1750 import *
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time

def safe_exit(signum, frame):
    exit(1) 

dht = DHT_data()
lcd = LCD()

temp_state = 0
lux_state = 0
humid_state = 0

while True:
    try:    
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        temp, humid = dht.getDataDHT()
        lux = readLight(DEVICE)
        
        # temperature room condition
        if (temp >= 20 and temp <=28):
            lcd.text("temperature: normal",1)
            temp_state = 0
        elif (temp < 20):
            lcd.text("temperature: cold",1)
            temp_state = -1
        elif (temp > 28):
            lcd.text("temperature: hot",1)
            temp_state = 1
        
        # humidity room condition
        if (humid >= 40 and humid <= 60):
            lcd.text("humidity: normal", 2)
            humid_state = 0
        elif (humid < 40):
            lcd.text("humidity: dry", 2)
            humid_state = -1
        elif (humid > 60):
            lcd.text("humidity: humid", 2)
            humid_state = 1
        
        # lux room condition       
        if (lux >= 100):
            lcd.text("lumen: normal",3)
            lux_state = 0
        elif (lux < 100):
            lcd.text("lumen: dark",3)
            lux_state = 1
        
        # when standard is not met
        if temp_state == 1 or humid_state == 1 or lux_state == 1:
            for i in range(0,5):
                lcd.backlight(False)
                time.sleep(0.1)
                # print("i true: {}".format(i))
            
            for i in range(0,5):
                lcd.backlight(True)
                time.sleep(0.1)
                # print("i false: {}".format(i))
        
        elif temp_state == -1 or humid_state == -1:
            for i in range(0,10):
                lcd.backlight(False)
                time.sleep(0.5)
            
            for i in range(0,10):
                lcd.backlight(True)
                time.sleep(0.5)
        
        # lcd.text("temperature: {:.2f}".format(temp),1)
        # lcd.text("humidity: {:.2f}%".format(humid),2)
        # lcd.text("lux: {:.2f}".format(lux),3)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        continue

lcd.clear()