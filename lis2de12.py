from pyb import I2C
from pyb import Pin

class lis2de12:
    I2C_ADDR_LOW = const(0x18)
    I2C_ADDR_HIGH = const(0x19)

    # Register addresses
    STATUS_REG_AUX = const(0x07)
    OUT_TEMP_L = const(0x0C)
    OUT_TEMP_H = const(0x0D)
    WHO_AM_I = const(0x0F)
    CTRL_REG0 = const(0x1E)
    TEMP_CFG_REG = const(0x1F)
    CTRL_REG1 = const(0x20)
    CTRL_REG2 = const(0x21)
    CTRL_REG3 = const(0x22)
    CTRL_REG4 = const(0x23)
    CTRL_REG5 = const(0x24)
    CTRL_REG6 = const(0x25)
    REFERENCE = const(0x26)
    STATUS_REG = const(0x27)
    FIFO_READ_START = const(0x28)
    OUT_X_H = const(0x29)
    OUT_Y_H = const(0x2B)
    OUT_Z_H = const(0x2D)
    FIFO_CTRL_REG = const(0x2E)
    FIFO_SRC_REG = const(0x2F)
    INT1_CFG = const(0x30)
    INT1_SRC = const(0x31)
    INT1_THS = const(0x32)
    INT1_DURATION = const(0x33)
    INT2_CFG = const(0x34)
    INT2_SRC = const(0x35)
    INT2_THS = const(0x36)
    INT2_DURATION = const(0x37)
    CLICK_CFG = const(0x38)
    CLICK_SRC = const(0x39)
    CLICK_THS = const(0x3A)
    TIME_LIMIT = const(0x3B)
    TIME_LATENCY = const(0x3C)
    TIME_WINDOW = const(0x3D)
    ACT_THS = const(0x3E)
    ACT_DUR = const(0x3F)

    def __init__(self, bus, addr=I2C_ADDR_HIGH):
        self.addr = addr
        self.bus = bus

        self.filter_index = 0
        self.filter_x = [0, 0, 0, 0]
        self.filter_y = [0, 0, 0, 0]
        self.filter_z = [0, 0, 0, 0]

        self.irq = Pin('INT_WKUP', Pin.IN)

        # Configure and enable the acceleromter
        self.write(self.CTRL_REG1, 0x5F)    # Enable the device and configure 100Hz sampling.
        self.write(self.CTRL_REG2, 0x07)    # Enable high-pass filters for AOI and click.
        self.write(self.CTRL_REG3, 0x40)    # Enable AOI interrupt on pin INT1.
        self.write(self.CTRL_REG4, 0x00)    # +/- 2g full scale mode.
        self.write(self.CTRL_REG5, 0x08)    # Latch INT1 sources until read by software.
        self.write(self.INT1_CFG,  0x2A)    # Enable high interrupts on X, Y and Z
        self.write(self.INT1_THS,  64)      # Configure interrupt thresholds at ~1g
        self.write(self.INT1_DURATION, 10)  # High condition must exist for 10ms to trigger.
        self.write(self.CLICK_CFG, 0x15)    # Enable single-tap detection.
    
    def read(self, reg):
        result = self.bus.mem_read(1, self.addr, reg)
        return result[0]
    
    def read16(self, reg):
        result = self.bus.mem_read(2, self.addr, reg)
        return result[0] + (result[1] << 8)
    
    def write(self, reg, value):
        self.bus.mem_write(bytearray([value]), self.addr, reg)
    
    def x(self):
        # Invert X axis to match the DC26 badge orientation.
        xraw = self.read(self.OUT_X_H)
        if (xraw > 127):
            return (256 - xraw)
        else:
            return -xraw
    
    def y(self):
        # Invert Y axis to match the DC26 badge orientation.
        yraw = self.read(self.OUT_Y_H)
        if (yraw > 127):
            return (256 - yraw)
        else:
            return -yraw
    
    def z(self):
        zraw = self.read(self.OUT_Z_H)
        if (zraw > 127):
            return -(256 - zraw)
        else:
            return zraw

    def filtered_xyz(self):
        # Take a new measurement and filter it.
        self.filter_x[self.filter_index] = self.x()
        self.filter_y[self.filter_index] = self.y()
        self.filter_z[self.filter_index] = self.z()
        self.filter_index = (self.filter_index + 1) % 4

        result =  (sum(self.filter_x), sum(self.filter_y), sum(self.filter_z))
        return result
    
    def status(self):
        if (self.irq.value()):
            print("Wakeup Pin High")
        else:
            print("Wakeup Pin Low")

        print("STATUS_REG   = " + hex(self.read(self.STATUS_REG)))
        print("OUT_TEMP_L   = " + hex(self.read(self.OUT_TEMP_L)))
        print("OUT_TEMP_H   = " + hex(self.read(self.OUT_TEMP_H)))
        print("WHO_AM_I     = " + hex(self.read(self.WHO_AM_I)))
        print("CTRL_REG0    = " + hex(self.read(self.CTRL_REG0)))
        print("TEMP_CFG_REG = " + hex(self.read(self.TEMP_CFG_REG)))
        print("CTRL_REG1    = " + hex(self.read(self.CTRL_REG1)))
        print("CTRL_REG2    = " + hex(self.read(self.CTRL_REG2)))
        print("CTRL_REG3    = " + hex(self.read(self.CTRL_REG3)))
        print("CTRL_REG4    = " + hex(self.read(self.CTRL_REG4)))
        print("CTRL_REG5    = " + hex(self.read(self.CTRL_REG5)))
        print("CTRL_REG6    = " + hex(self.read(self.CTRL_REG6)))
        print("REFERENCE    = " + hex(self.read(self.REFERENCE)))
        print("STATUS_REG   = " + hex(self.read(self.STATUS_REG)))
        print("OUT_X_H      = " + hex(self.read(self.OUT_X_H)))
        print("OUT_Y_H      = " + hex(self.read(self.OUT_Y_H)))
        print("OUT_Z_H      = " + hex(self.read(self.OUT_Z_H)))
        print("FIFO_CTRL_REG= " + hex(self.read(self.FIFO_CTRL_REG)))
        print("FIFO_SRC_REG = " + hex(self.read(self.FIFO_SRC_REG)))
        print("INT1_CFG     = " + hex(self.read(self.INT1_CFG)))
        print("INT1_SRC     = " + hex(self.read(self.INT1_SRC)))
        print("INT1_THS     = " + hex(self.read(self.INT1_THS)))
        print("INT1_DURATION= " + hex(self.read(self.INT1_DURATION)))
        print("INT2_CFG     = " + hex(self.read(self.INT2_CFG)))
        print("INT2_SRC     = " + hex(self.read(self.INT2_SRC)))
        print("INT2_THS     = " + hex(self.read(self.INT2_THS)))
        print("INT2_DURATION= " + hex(self.read(self.INT2_DURATION)))
        print("CLICK_CFG    = " + hex(self.read(self.CLICK_CFG)))
        print("CLICK_SRC    = " + hex(self.read(self.CLICK_SRC)))
        print("CLICK_THS    = " + hex(self.read(self.CLICK_THS)))
        print("TIME_LIMIT   = " + hex(self.read(self.TIME_LIMIT)))
        print("TIME_LATENCY = " + hex(self.read(self.TIME_LATENCY)))
        print("TIME_WINDOW  = " + hex(self.read(self.TIME_WINDOW)))
        print("ACT_THS      = " + hex(self.read(self.ACT_THS)))
        print("ACT_DUR      = " + hex(self.read(self.ACT_DUR)))

