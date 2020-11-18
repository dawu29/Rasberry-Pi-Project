import RPi.GPIO as GPIO
import smbus
import time

address = 0x48 #I2C address for PCF8591
bus=smbus.SMBus(1)

channel3=0x43 #3 analog input channel(AIN1, AIN2, AIN3) of RGB on PCF8591 
channel2=0x42
channel1=0x41

red = 22      #pins of RGBLED
green = 27
blue = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(red,GPIO.OUT)      
GPIO.setup(green,GPIO.OUT)
GPIO.setup(blue,GPIO.OUT)
    
p_Red = GPIO.PWM(red,1000)    #configure PMW to 3 pins of RGBLED
p_Red.start(0)
p_Green = GPIO.PWM(green,1000)
p_Green.start(0)
p_Blue = GPIO.PWM(blue,1000)
p_Blue.start(0)

def analogValue(channel):    #read ADC value
    bus.write_byte(address,channel)
    value = bus.read_byte(address)
    return value
    

def destroy():
    bus.close()
    GPIO.cleanup()

    
if __name__ == '__main__':
    try:
        while True:     
            value_Red = analogValue(channel1)       #read ADC value of 3 potentiometers
            value_Green = analogValue(channel2)
            value_Blue = analogValue(channel3)
            p_Red.ChangeDutyCycle(value_Red*100/255)  #map the value of potentiometers(0-255) into PWM value
            p_Green.ChangeDutyCycle(value_Green*100/255)
            p_Blue.ChangeDutyCycle(value_Blue*100/255)

            print ('Red '+str(value_Red)+' Green '+str(value_Green)+' Blue '+str(value_Blue))
            time.sleep(0.01)
        
    except KeyboardInterrupt:
        destroy()

        
    
