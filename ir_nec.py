import time
import uqueue

NEC_HEAD=13500#(9000,4500)
NEC_LOGIC_0=1120#(560,560)
NEC_LOGIC_1=2250#(560,1690)
NEC_HOLD=11250#(9000,2250)

class IR:
    def __init__(self,ir_pin):
        self.ir_pin=ir_pin
        self.ir_pin.init(ir_pin.IN)
        self.ir_pin.irq(
            trigger=ir_pin.IRQ_FALLING|ir_pin.IRQ_RISING,
            handler=self._io_callback,
            )
        self.event_queue=uqueue.Queue()
        self.t0=-1

        self.signal_buf=0

        self.addr_buf=0
        self.cmd_buf=0
        self.check_addr_buf=0
        self.check_cmd_buf=0
        self.bit_cnt=0

        self.last_data=None
        self.last_hold_signal_time=0

    def _data(self,bit):
        if self.bit_cnt<8:
            self.addr_buf+=(bit*2**self.bit_cnt)
        elif 8<=self.bit_cnt<16:
            self.check_addr_buf+=((1-bit)*2**(self.bit_cnt-8))
        elif 16<=self.bit_cnt<24:
            self.cmd_buf+=(bit*2**(self.bit_cnt-16))
        elif 24<=self.bit_cnt<32:
            self.check_cmd_buf+=((1-bit)*2**(self.bit_cnt-24))
            if self.bit_cnt==31:
                if self.check_addr_buf==self.addr_buf and self.check_cmd_buf==self.cmd_buf:
                    self.event_queue.put((self.addr_buf,self.cmd_buf))
                    self.last_data=(self.addr_buf,self.cmd_buf)
                self._data_cls()
                return
        self.bit_cnt+=1
    
    def _data_cls(self):
        self.addr_buf=0
        self.cmd_buf=0
        self.check_addr_buf=0
        self.check_cmd_buf=0
        self.bit_cnt=0

    def _io_callback(self,irq_pin):
        t=time.ticks_us()
        if self.t0<0:
            self.t0=t
        else:
            dt=t-self.t0
            if 0<dt<120000:
                if irq_pin.value():
                    self.signal_buf=dt
                else:
                    total=self.signal_buf+dt
                    if self._eq(NEC_HEAD,total):
                        self._data_cls()
                    elif self._eq(NEC_HOLD,total):
                        self.last_hold_signal_time=t
                        pass
                    elif self._eq(NEC_LOGIC_0,total):
                        self._data(0)
                    elif self._eq(NEC_LOGIC_1,total):
                        self._data(1)
                    else:
                        if self._eq(560,self.signal_buf):
                            #print("")
                            pass
                        else:
                            #print("err")
                            pass
            self.t0=t
    
    def _eq(self,a,b):
        return 1 if abs(a-b)<400 else 0

    def get_event_queue(self):
        return self.event_queue
    
    def get_holding(self):
        dt=time.ticks_us()-self.last_hold_signal_time
        if dt>150000:
            return None
        elif dt<0:
            self.last_hold_signal_time=0
            self.last_data=None
        else:
            return self.last_data
