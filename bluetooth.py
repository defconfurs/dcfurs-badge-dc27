from pyb import I2C

class bluetooth:
    I2C_ADDR = const(0x42)

    # Register Addresses
    REG_DEVID       = const(0x00)
    REG_SERIAL      = const(0x08)
    REG_STATE       = const(0x0a)
    REG_FLAGS       = const(0x0b)
    REG_COLOR       = const(0x0c)
    REG_DURATION    = const(0x0e)
    REG_RSSI        = const(0x10)
    REG_TTL         = const(0x11)
    REG_ORIGN       = const(0x12)
    REG_EMOTE       = const(0x14)

    # Writeable Addresses
    REG_ADVNAME     = const(0x1c)
    REG_TXLEN       = const(0x2e)
    REG_TXMAGIC     = const(0x2f)
    REG_TXDATA      = const(0x30)

    # Supported Flags
    FLAG_EMOTE      = const(0x01)
    FLAG_COLOR      = const(0x02)

    def __init__(self, bus, addr=I2C_ADDR):
        self.addr = addr
        self.bus = bus

    def read(self, reg):
        result = self.bus.mem_read(1, self.addr, reg)
        return result[0]
    
    def read16(self, reg):
        result = self.bus.mem_read(2, self.addr, reg)
        return result[0] + (result[1] << 8)
    
    def write(self, reg, value):
        self.bus.mem_write(bytearray([value]), self.addr, reg)

    def write16(self, reg, value):
        buf = bytearray([(value & 0x00ff) >> 0, (value & 0xff00) >> 8])
        self.bus.mem_write(buf, self.addr, reg)
    
    def transmit(self, magic, payload=None):
        buf = bytearray([0, magic])
        if payload:
            buf[0] = len(payload)
            buf += payload
        self.bus.mem_write(buf, self.addr, self.REG_TXLEN)
    
    def flags(self):
        return self.read(self.REG_FLAGS)

    def color(self):
        result = self.bus.mem_read(3, self.addr, self.REG_FLAGS)
        flags = result[0]
        rgb16 = result[1] + (result[2] << 8)
        if result[0] & self.FLAG_COLOR:
            # Convert to rgb-888 because after two badges, I'm still undecided on color encoding.
            return ((rgb16 & 0xf800) << 8) | ((rgb16 & 0x07e0) << 5) | ((rgb16 & 0x001F) << 3)
        else:
            return None
