#Based on esp8266
from machine import Pin,PWM
from ir_nec import IR
import time
from uqueue import QueueEmptyError

POWER=(0,1)#Set keys here.
ADD=(0,4)
SUB=(0,0)

ir=IR(Pin(14))
event_queue=ir.get_event_queue()
led=PWM(Pin(2,Pin.OUT))#ESP12f LED Pin.
duty=512
off=1
led.freq(1000)
led.duty(1023)

def set_duty(duty):
    led.duty(duty)
    print("Duty: %d."%duty)

def change_duty(data):
    global duty
    if data==ADD:
        duty=duty-32 if duty>0 else duty
        set_duty(duty)
    elif data==SUB:
        duty=duty+32 if duty<1023 else duty
        set_duty(duty)

while 1:#Mainloop.
    time.sleep(0.1)
    if not event_queue.empty():
        data=event_queue.get()#Get event.
        if data==POWER:
            off=1-off
            led.duty(1023 if off else duty)
            print("Turned on" if not off else "Turned off")
        change_duty(data)

    holding=ir.get_holding()#Get holding
    if holding and not off:
        change_duty(holding)
