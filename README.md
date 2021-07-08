# mpy_ir_nec #

An NEC protocol decoder. 

e.g.

```python
#./main.py
#Based on esp8266
import machine
from machine import Pin
from ir_nec import IR
import time
from uqueue import QueueEmptyError

#machine.freq(160000000)

i=IR(Pin(14,Pin.IN))

light=0

while 1:#Mainloop.
    time.sleep(0.1)
    try:
        data=i.event_queue.pop()#Get event.
        print(data)
        if data==(0,1):#If the received data matches the data you set here ...
            light=1-light
            #... the built-in LED will turn on or off.
            Pin(2,Pin.OUT).value(light)#ESP12f LED Pin.
    except QueueEmptyError:
        pass
    h=i.get_holding()#Get holding
    if h:
        print("holding",h)
```