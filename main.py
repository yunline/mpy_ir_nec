#Based on esp8266
from machine import Pin
from ir_nec import IR
import time
from uqueue import QueueEmptyError

ir=IR(Pin(14,Pin.IN))

while 1:#Mainloop.
    time.sleep(0.1)
    try:
        print(ir.event_queue.pop())#Get event.
    except QueueEmptyError:
        pass
    hold=ir.get_holding()#Get holding
    if hold:
        print("holding",hold)