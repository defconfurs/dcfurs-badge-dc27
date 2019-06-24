## Here's all the stuff to make your badge's hardware operate normally.
import pyb
import dcfurs
import settings
from pyb import Pin
from pyb import Timer
from pyb import ExtInt
from pyb import I2C
from pyb import UART
from lis2de12 import lis2de12

# The I2C bus used for all the off-chip stuff.
bus = I2C(3, I2C.MASTER, baudrate=100000)

##-----------------------------------------------
## LED Matrix Drivers
##-----------------------------------------------
import micropython
micropython.alloc_emergency_exception_buf(100)

## Bring up the LED matrix
pwmclk = Timer(8, freq=125000)
dcfurs.init(pwmclk)
dcfurs.clear()

##-----------------------------------------------
## Pushbutton Class
##-----------------------------------------------
class switch(Pin):
    def __init__(self, pin):
        self.pin = pin
        self.prev = self.pin.value()
    
    ## Returns 1 on a rising edge, or 0 on no change.
    def event(self):
        if not self.prev:
            self.prev = self.pin.value()
            return self.prev
        else:
            self.prev = self.pin.value()
            return 0

right = switch(Pin('SW1', Pin.IN))
left = switch(Pin('SW2', Pin.IN))

##-----------------------------------------------
## Capacative Touch Controller
##-----------------------------------------------
## TODO: Implement Me!
class capsense:
    def event(self):
        return False

boop = capsense()

##-----------------------------------------------
## Motion Detection / Accelerometer
##-----------------------------------------------
imu = lis2de12(bus)

##-----------------------------------------------
## Low Power Sleep
##-----------------------------------------------
## Check for low power states, or do nothing.
def trysuspend():
    return False