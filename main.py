from machine import Pin
from ir_nec import IR
import time
from uqueue import QueueEmptyError

i=IR(Pin(14,Pin.IN))
light=0

while 1:
    time.sleep(0.1)
    try:
        d=i.event_queue.pop()
        print(d)
        if d==(0,1):
            light=1-light
            Pin(2,Pin.OUT).value(light)
    except QueueEmptyError:
        pass
    h=i.get_holding()
    if h:
        print("holding",h)