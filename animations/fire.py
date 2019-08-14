"""Fire animation, by Uck!"""

import dcfurs
import random

# Colors, from top to bottom of the fire.
colors = [0, 0x1f0f0f, 0x3f0000, 0xff0000, 0xff7f00, 0xffff00, 0x1f007f,
          0x0000ff, 0xffffff]

# Bitmask values copied from emote.boop().
boop_mask = [
    0x0e48e,
    0x12b52,
    0x12b52,
    0x0eb4e,
    0x02492,
    0x02012,
    0x0200e
]
    

class fire(object):
    """A simple fire animation, inspired by the classic demo fire effect."""

    def __init__(self):
        # Allocate our internal buffer.  Values in this buffer range from 0
        # to len(colors) - 1.  As the fire values move upward on the screen,
        # these values fall toward 0 (which is black, in the colors array).
        #
        # There's an extra row at the bottom that's filled with random values.
        # That row isn't displayed on the LEDs.
        self.buffer = [[0] * dcfurs.ncols for y in range(dcfurs.nrows + 1)]
        self.interval = 25
        self.boop_remaining = 0

    def draw(self):
        self.update_fire()
        self.update_boop()

        if self.boop_remaining:
            # Render at 1/4 brightness unless it's the Boop text.
            for y, row_mask in enumerate(boop_mask):
                for x in range(dcfurs.ncols):
                    color = colors[self.buffer[y][x]]
                    if (1 << x) & row_mask == 0:
                        # Non-boop pixel.
                        color = (color >> 2) & 0x3f3f3f
                    dcfurs.set_pix_rgb(x, y, color)
        else:
            for y in range(dcfurs.nrows):
                for x in range(dcfurs.ncols):
                    dcfurs.set_pix_rgb(x, y, colors[self.buffer[y][x]])

    def update_fire(self):
        """Update our internal fire buffer, moving the flames upward."""
        # Fill the bottom (invisible) row with random values.
        for x in range(dcfurs.ncols):
            self.buffer[dcfurs.nrows][x] = random.randint(0, len(colors) - 1)

        # Propagate the fire colors upward, averaging from the pixels below
        # and decreasing the value toward 0.
        for y in range(dcfurs.nrows):
            for x in range(1, dcfurs.ncols - 1):
                value = (self.buffer[y + 1][x - 1] +
                         self.buffer[y + 1][x] +
                         self.buffer[y + 1][x + 1]) // 3
                if random.randint(0, 2) == 0:
                    value -= 1
                self.buffer[y][x] = min(len(colors) - 1, max(0, value))

    def boop(self):
        """Nose Boop start, reset our internal Boop timer."""
        self.boop_remaining = 500 / self.interval

    def update_boop(self):
        """Check if we need to add Boop to the flames."""
        if self.boop_remaining:
            self.add_boop()
            self.boop_remaining -= 1

    def add_boop(self):
        """Add Boop to the fire, so it interacts with the flames."""
        for y, row_mask in enumerate(boop_mask):
            for x in range(dcfurs.ncols):
                if (1 << x) & row_mask:
                    self.buffer[y][x] = len(colors) - 1
