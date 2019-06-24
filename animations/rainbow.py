## Scrolling rainbow
import dcfurs

class rainbow:
    color_map = [
        0xe0, # Red
        0xe8, # Orange
        0xfc, # Yellow
        0x1c, # Green
        0x03, # Blue
        0x43  # Purple
    ]

    def __init__(self):
        self.shift = 0
        self.interval = 100
        self.leftright = True
    
    def draw(self):
        for row in range(0,dcfurs.nrows):
            for col in range(0, dcfurs.ncols/2):
                color = ((self.shift - col - row) // 4) % len(self.color_map)
                dcfurs.set_pixel(col, row, self.color_map[color])
                dcfurs.set_pixel(dcfurs.ncols - col - 1, row, self.color_map[color])
        self.shift += 1
