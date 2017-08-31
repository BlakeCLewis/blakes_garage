#!/usr/bin/python
from time import sleep
import numpy as np
def gettemp(id):
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
 
if __name__ == '__main__':
  np.set_printoptions(formatter={'float': '{:.2f}'.format})
  ids=['28-000008c941ac','28-000008c97c4e','28-000008ca191c','28-000008ca4422','28-000008ca8a1b']
  cor=np.array([0,0,0,0,0])
  temps=np.array([0.0,0.0,0.0,0.0,0.0])
  alpha=0.7
  for i in range(0,len(ids)):
    temp=float(gettemp(ids[i]))
    temps[i]=temp
  x=np.array (temps+cor)/1000*9/5+32
  print str(x)
