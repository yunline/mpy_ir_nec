# Micropython IR NEC Decoder #
An NEC protocol decoder with an event queue based on [micropython](https://github.com/micropython/micropython).  

It is advised that the CPU frequency should be high ( e.g.  `machine.freq(160000000)` on Esp8266 ) for higher timing accuracy.

e.g.

```python
#./main.py
from machine import Pin
from ir_nec import IR
import time
from uqueue import QueueEmptyError

ir=IR(Pin(14))
event_queue=ir.get_event_queue()

while 1:#Mainloop.
    time.sleep(0.1)
    if not event_queue.empty():
        print(event_queue.get())#Get event.
        #The event data format is (NEC_addr,NEC_cmd)
    
    holding=ir.get_holding()#Get holding
    #When you are holding a key down on your remote controller, 
    #the value of holding will be (NEC_addr,NEC_cmd), 
    #or it will be None.
    if holding:
        print("holding",holding)
```