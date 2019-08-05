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
from bluetooth import bluetooth

# The I2C bus used for all the off-chip stuff.
bus = I2C(3, I2C.MASTER, baudrate=100000)

##-----------------------------------------------
## LED Matrix Drivers
##-----------------------------------------------
import micropython
micropython.alloc_emergency_exception_buf(100)

## Bring up the LED matrix
pwmclk = Timer(8, freq=500000)
dcfurs.init(pwmclk)
dcfurs.clear()

##-----------------------------------------------
## Bluetooth Module
##-----------------------------------------------
ble = None
try:
    if (bus.mem_read(8, 0x42, 0)):
        ble = bluetooth(bus)
        ble.write(ble.REG_COOLDOWN, settings.cooldown)
except Exception as e:
    ble = None

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
boop = dcfurs.boop(settings.boopselect)
tmr = Timer(2, freq=100)
tmr.callback(lambda t: boop.start())

##-----------------------------------------------
## Motion Detection / Accelerometer
##-----------------------------------------------
class dummy:
    def x(self):
        return 0
    
    def y(self):
        return 0
    
    def z(self):
        return 0
    
    def read(self, addr):
        return 0
    
    def filtered_xyz(self):
        return (0, 0, 0)

# Wrap in a try/except in case we are running on
# a prototype with a bad accelerometer.
try:
    imu = lis2de12(bus)
except:
    imu = dummy()

##-----------------------------------------------
## Low Power Sleep
##-----------------------------------------------
## Check for low power states, or do nothing.
def trysuspend():
    return False

##-----------------------------------------------
## Hue/Value to RGB888 conversion
##-----------------------------------------------
def hue2rgb(hue, val=255):
    sextant = hue // 60
    remainder = hue % 60
    p = 0 # full saturation always results in zero.
    q = (val * (60 - remainder)) // 60
    t = (val * remainder) // 60
    
    if (sextant == 0):
        r = val
        g = t
        b = p
    elif (sextant == 1):
        r = q
        g = val
        b = p
    elif (sextant == 2):
        r = p
        g = val
        b = t
    elif (sextant == 3):
        r = p
        g = q
        b = val
    elif (sextant == 4):
        r = t
        g = p
        b = val
    else:
        r = val
        g = p
        b = q
   
    return (r << 16) | (g << 8) | b 

