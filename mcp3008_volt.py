
#  co   grn       yel      org      brn
#  3008 13        12       11       10
#  rpi  18        23       24       25
#       SPICLK,   SPIMOSI, SPIMISO, SPICS
#  py   clockpin, mosipin, misopin, cspin

import time as t
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
  commandout |= 0x18  # start bit & single ended indicator
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

for i in range(300):
  print i
  vi = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
  v0 = "%5.2f"% (4.25 * vi / 1024)
  print v0
  vj = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
  v1 = "%5.2f"% (4.25 * vj / 1024)
  print v1
  vk = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
  v2 = "%5.2f"% (4.25 * vk / 1024)
  print v2
  vl = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
  v3 = "%5.2f"% (4.25 * vl / 1024)
  print v3
  vm = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
  v4 = "%5.2f"% (4.25 * vm / 1024)
  print v4
  Vt = "%5.2f"% (4.25 * (vi+vj+vk+vl+vm) / 1024)
  print Vt
  print  '-----------------'
  t.sleep(10)

GPIO.cleanup() 
