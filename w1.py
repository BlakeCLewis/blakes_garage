import time as t
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import numpy as np

bigSwitch=17 # 120V On/Off 48V transformer.

#------- setup relay & turn on main power -------
GPIO.setmode(GPIO.BCM)
GPIO.setup(bigSwitch,GPIO.OUT)
GPIO.output(bigSwitch,1)

#------- setup DS18B20 temp sensor---------------
# pin 4 is 1w default when 1w kernel mod is loaded
# devices readings show up at /sys/bus/w1/devices/28-xxxxxxxxxxxx/1w_slave
def gettemp(id): #reads one device
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 99999
    f.close()
    return int(mytemp[1])
  except:
    return 99999

def gettemps(): #calls gettemp to read each device
  np.set_printoptions(formatter={'float': '{:.0f}'.format}) # integer part for display 
  # need to move sensor ids, correction values and sensor names to a configuration file
  ids=['28-000008c941ac','28-000008c97c4e','28-000008ca191c','28-000008ca4422','28-000008ca8a1b']
  # need to create config file with names(mix,hot,r1,r2.in.out attatch to ids
  cor=np.array([0,0,0,0,0])
  # calibrated correction value should come from config file
  temps=np.array([0.0,0.0,0.0,0.0,0.0])
  alpha=0.7
  for i in range(0,len(ids)):
    temp=float(gettemp(ids[i]))
    temps[i]=temp
  x=np.array (temps+cor)/1000
  return str(x)  # should return numpy array and formated for printing by output module

#------- setup display --------------------------
RST = None     # on the PiOLED this pin isnt used
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1',(width,height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()
z = 0
#------- run loop -------------------------------
try:
  while z < 50:
      # Draw a black filled box to clear the image.
      draw.rectangle((0,0,width,height), outline=0, fill=0)
 
      # labels should come from config file, 4 lines of text on the 128x64 display
      draw.text((x, top),     "[HT MX R1 R2 IN OT]", font=font, fill=255) 
      draw.text((x, top+8),   gettemps(),            font=font, fill=255)
      #draw.text((x, top+16),  blah1,                 font=font, fill=255)
      #draw.text((x, top+25),  blah2,                 font=font, fill=255)
      if z%2 > 0:
        GPIO.output(bigSwitch,1)
      else:
        GPIO.output(bigSwitch,0) 
      # Display image.
      disp.image(image)
      disp.display()
      t.sleep(1)
      z+=1
except KeyboardInterrupt:
  print 'CTRL+C'

except:
  print 'whazup'

finally:
  GPIO.cleanup()
