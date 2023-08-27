from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
# from rpi_backlight import Backlight

lcd = LCD()
# backlight = Backlight()

def safe_exit(signum, frame):
    exit(1) 
    
state = False
try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text("Apakah,", 1)
    lcd.text("Raspberry Pi!", 2)
    
    while True:
        for i in range(0,10):
            state = True
            if state == True:
                lcd.text(str(state),3)
                lcd.text(str(i),4)
                lcd.backlight(True)
                time.sleep(1)
        state = False
        lcd.backlight(False)
        time.sleep(1)
    
    pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()