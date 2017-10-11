
#  co   grn       yel      org      brn
#  3008 13        12       11       10
#  rpi  18        23       24       25
#       SPICLK,   SPIMOSI, SPIMISO, SPICS
#  py   clockpin, mosipin, misopin, cspin

import time
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
    return -1

  GPIO.output(cspin, True)
  GPIO.output(clockpin, False)  # start clock low
  GPIO.output(cspin, False)     # bring CS low
  commandout = adcnum
  commandout |= 0x10  # start bit & differemtial indicator
  commandout <<= 3    # we only need to send 5 bits here

  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
    commandout <<= 1
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)

  adcout = 0

  # read in one empty bit, one null bit and 10 ADC bits
  for i in range(12):
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
    adcout <<= 1
    if (GPIO.input(misopin)):
      adcout |= 0x1

  GPIO.output(cspin, True)
  adcout >>= 1       # first bit is 'null' so drop it
  return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK,  GPIO.OUT)
GPIO.setup(SPICS,   GPIO.OUT)

blah1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
blah3 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
blah5 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)

print blah1
print blah3
print blah5

GPIO.cleanup() 
