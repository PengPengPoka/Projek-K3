import time
import board
import adafruit_dht

class DHT_data:
    def getDataDHT(self):
        dhtDevice = adafruit_dht.DHT22(board.D4,use_pulseio=False)
        temp_c = dhtDevice.temperature
        humid = dhtDevice.humidity
        
        if not temp_c and not humid:
            temp_c = 0
            humid = 0
            return temp_c, humid
        
        # time.sleep(2.0)
        return temp_c, humid
    