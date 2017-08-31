import RPi.GPIO as GPIO
from time import sleep

relay=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay,GPIO.OUT)
GPIO.output(relay,1)
for i in range(0,21):
  if i % 2 > 0:
    GPIO.output(relay,1)    
  else:
    GPIO.output(relay,0)
  sleep(3)
GPIO.cleanup()
