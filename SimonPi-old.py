#Written By Gee Bartlett 

#Simon Says Mini backpack Kit For Raspberry Pi
#Setup to use only for 4 GPIO it achieves this by reading inputs when Lights are inactive.



#Musical Note Notes
#A4	     440.00
#A#4/Bb4   466.16	
#B4	     493.88	
#C5	     523.25	
#C#5/Db5   554.37
#D5	     587.33
#D#5/Eb5   622.25
#E5	     659.25
#F5	     698.46
#F#5/Gb5   739.99
#G5	     783.99
#G#5/Ab5   830.61

#Insert Tune here  [('note',duration)]
Tune1 = [('a',1),('a#',1)],[('b',1)]

import os
from socket import socket, AF_INET, SOCK_STREAM 
import threading
import RPi.GPIO as GPIO   
from time import sleep as delay

#Setup GPIO
GPIO.setmode(GPIO.BCM)

#Start socket instance 
sck = socket(AF_INET, SOCK_STREAM)

#load Pure Data with tone sketch
print(os.system("pd -nogui tonegenerator.pd &"))
print('now you wait ...........')
delay(1.5)

#Start socket connection for communicating with Pure Data sketch 
sck.connect(("127.0.0.1",3000))

#settings 

gameActive = False
outputs = [22,23,24,25] #GPIO ports to use Change As Required
light_speed = 0.1 #Speed setting for intro light sequence

#Lookup table for Notes to Hz
Notes = {'a':440, 'a#':466.16, 'b':493.88, 'c': 523.25, 'c#':554.37, 'd':587.33, 'd#':622.25, 'e':659.25, 'f':698.46, 'f#':739.99, 'g':783.99, 'g#':830.61} 

#Lookup for notes light location 
Lights = {'a':outputs[0], 'a#':outputs[1], 'b':outputs[2], 'c': outputs[3], 'c#':outputs[0], 'd':outputs[1], 'd#':outputs[2], 'e':outputs[3], 'f':outputs[0], 'f#':outputs[1], 'g':outputs[2], 'g#':outputs[3]}

#Send Note to Pure Data 
def playNote(f,d):
   sck.send("tone  " + str(f) + ";")
   sck.send("power 1;")
   delay(d)
   sck.send("power 0;")

#PLay to string 
def playTune(tune):
   for i in range(len(Tune1)):
      note = Tune1[i]
      
#Function to lookup notes hz value      
def convertHz(f,d):
   f=Notes.get(f) 
   return (f,d)

#print(convertHz(Tune1[0]))

def button1(channel):
   print channel
   print("button 1 pressed")
   playNote(440,0.4)
   return

def button2(channel):
   print("button 2 pressed")
   playNote(330,0.4)
   return


def button3(channel): 
   gameActive = True
   fail()


def fail():
   playNote(220,3)
   gameActive = True
   #lights(0.2)



for i in range(len(outputs)):
   GPIO.setup(outputs[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
   

#button interupt activate
def attachInt(button,IOport):
   if ( button == 0):
      GPIO.add_event_detect(IOport, GPIO.FALLING, callback=button1, bouncetime=300)
   elif( button == 1):
      GPIO.add_event_detect(IOport, GPIO.FALLING, callback=button2, bouncetime=300)
   elif( button == 2):
      GPIO.add_event_detect(IOport, GPIO.FALLING, callback=button3, bouncetime=300)
   elif( button == 3):
      GPIO.add_event_detect(IOport, GPIO.FALLING, callback=button2, bouncetime=300)
   return 0



#Begining Light Show
def lights(speed):
   
#Cycles through leds  
   while (gameActive == False):
      for i in range(len(outputs)):

         GPIO.remove_event_detect(outputs[i])
         GPIO.setup(outputs[i], GPIO.OUT)
         GPIO.output(outputs[i], True)
         delay(speed)
         GPIO.setup(outputs[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
         attachInt(i,outputs[i]) 
         delay(speed)   

#Not sure if i'm keep the threading 
t = threading.Thread(target = lights, args = [light_speed])
t.deamon = False
t.start()


while 1:   
   try:

      print("stuff")
      
      delay(1)
 
#catch keyboard interrupt      
   except KeyboardInterrupt:
        
      os.system('sudo killall pd')
      GPIO.cleanup()
      os.system('sudo killall python')
      break
