#Based on esp8266
import machine
from machine import Pin,PWM
from ir_nec import IR
import time
from uqueue import QueueEmptyError

POWER=(0,1)#Set keys here.
ADD=(0,4)
SUB=(0,0)

ir=IR(Pin(14,Pin.IN))
led=PWM(Pin(2,Pin.OUT))#ESP12f LED Pin.
duty=512
off=1
led.freq(1000)
led.duty(1023)

while 1:#Mainloop.
    time.sleep(0.1)
    try:
        data=ir.event_queue.pop()#Get event.
        if data==POWER:
            off=1-off
            led.duty(1023 if off else duty)
            print("Turned on" if not off else "Turned off")
    except QueueEmptyError:
        pass

    hold=ir.get_holding()#Get holding
    if hold and not off:
        if hold==ADD:
            duty=duty-32 if duty>0 else duty
            led.duty(duty)
            print("Duty: %d."%duty)
        elif hold==SUB:
            duty=duty+32 if duty<1023 else duty
            led.duty(duty)
            print("Duty: %d."%duty)
