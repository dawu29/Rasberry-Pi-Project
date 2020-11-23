import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
loop =0 #this will be used as a global variable inside runRed and runGreen function 

number = {0:[1,1,1,1,1,1,0],1:[0,1,1,0,0,0,0],2:[1,1,0,1,1,0,1],3:[1,1,1,1,0,0,1],
          4:[0,1,1,0,0,1,1],5:[1,0,1,1,0,1,1],6:[1,0,1,1,1,1,1],7:[1,1,1,0,0,0,0],
          8:[1,1,1,1,1,1,1],9:[1,1,1,1,0,1,1]} #GPIO on/off sequence for the 7 segements from number 0 to 9
      
red = 17 #red LED
yellow = 27 #yellow LED
green = 22 #green LED
pb = 14 #push button
seglist = [5,8,12,16,13,6,7] #for pin A B C D E F G of the 7 segments
def setup():
    for i in seglist:
        GPIO.setup(i,GPIO.OUT)

    GPIO.setup(red,GPIO.OUT)
    GPIO.setup(yellow,GPIO.OUT)
    GPIO.setup(green,GPIO.OUT)
    GPIO.setup(pb,GPIO.IN,pull_up_down=GPIO.PUD_UP)



def runRed(): #red LED countdown
    global loop
    GPIO.output(green,0)
    GPIO.output(yellow,0)
    GPIO.output(red,1)
    for i in range(9,-1,-1): #countdown from 9 to 0 second
        for j in range(7): #7segment displplay update everyone second
            GPIO.output(seglist[j],number[i][j])
        time.sleep(1)
        if GPIO.input(pb)== False: #when the push bottun is pressed, RED led countdown will stop and greenLED countdown will start
            runGreen()
            break
    loop +=1 #update the global variable for the while loop
    
def runGreen(): #green LED countdown
    global loop
    GPIO.output(yellow,0)
    GPIO.output(red,0) 
    GPIO.output(green,1) 
    for i in range(9,3,-1): #countdown from 9 to 4 second
        for j in range(7): #7segment display update everyone second
            GPIO.output(seglist[j],number[i][j])
        time.sleep(1)
        
    for i in range(3,-1,-1): #coundown from 3 to 0 second
        for j in range(7): #7 segment display
            GPIO.output(seglist[j],number[i][j])        
        #yellow light starts flashing and buzzer starts beeping as well, buzzer shares the same GPIO.OUT as the yelllow LED
        GPIO.output(yellow,1)
        time.sleep(0.2)
        GPIO.output(yellow,0)
        time.sleep(0.1)
        GPIO.output(yellow,1)
        time.sleep(0.2)
        GPIO.output(yellow,0)
        time.sleep(0.5)
    loop +=1 #update the global variable for the while loop
    
    
setup()
while True:    #the LED countdown alternates between red and green 
    if GPIO.input(pb)== True and loop%2 == 0:        
        runRed()
    if GPIO.input(pb)== True and loop%2 == 1:
        runGreen()




GPIO.cleanup()
