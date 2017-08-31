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
  commandout |= 0x18  # start bit + single-ended bit
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

# Current sensor connected to adc #0 & #1
potentiometer_adc = 1;

last_read = 0 # this keeps track of the last potentiometer value
tolerance = 5 # to keep from being jittery we'll only change
counter = 0
try:
   while counter < 90:
     # we'll assume that the pot didn't move
     ACS758_changed = False
     
     # read the analog pin
     ACS758 = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
     # how much has it changed since the last read?
     dawn = abs(ACS758 - last_read)
     
     if ( dawn > tolerance ):
       ACS758_changed = True

     if (ACS758 - 520 < 0 ):
       ACS758 = 0

     if ( ACS758_changed and ACS758 > 5):
       ampre = (ACS758-520)*50/520.0
       print ACS758, '{:.2f}'.format(ampre)
     
     # save the potentiometer reading for the next loop
     last_read = ACS758
     counter += 1
     time.sleep(1)

except KeyboardInterrupt:
  print 'CTRL+C'

except:
  print 'whazup'

finally:
  GPIO.cleanup()

