"""Northern Lights"""
import dcfurs
import settings
import math
import random
import badge

gamma_table = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
    115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
    144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
    177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
    215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]


class northernlights:
    def __init__(self):
        self.interval = 25
        self.shift = 0
        self._set_random_params()

    def _set_random_params(self):
        self.xscale = random.randint(5,30)
        self.yscale = random.randint(5,30)
        self.hscale = random.randint(5,30)

        self.xshift_scale = random.randint(100,500)
        self.yshift_scale = random.randint(100,500)
        self.hshift_scale = random.randint(100,500)
      
        self.xshift_speed = random.randint(1000,5000)
        self.yshift_speed = random.randint(1000,5000)
        self.hshift_speed = random.randint(1000,5000)

        self.xoffset = random.randint(1,10)
        self.yoffset = random.randint(1,10)
        self.hoffset = random.randint(1,10)

        print(
            self.xscale, self.yscale, 
            self.xshift_scale, self.yshift_scale, 
            self.xshift_speed, self.yshift_speed, 
            self.xoffset, self.yoffset
        )


    def draw(self):
        self.shift += 1

        xshift = self.xshift_scale * math.sin(self.shift/self.xshift_speed)
        yshift = self.yshift_scale * math.sin(self.shift/self.yshift_speed)
	hshift = self.hshift_scale * math.sin(self.shift/self.hshift_speed)

        for x in range(dcfurs.ncols):
            for y in range(dcfurs.nrows):
                colbright = math.sin(math.sin(x/self.xscale + self.xoffset) + xshift) * \
                            math.sin(math.sin(y/self.yscale + self.yoffset) + yshift)
                hue = math.sin(math.sin(x/self.hscale + self.hoffset) + hshift) * \
		      math.sin(math.sin(y/self.hscale + self.hoffset) + hshift)
                #dcfurs.set_pix_rgb(x, y, gamma_table[int(colbright*255)])
                dcfurs.set_pix_rgb(x, y, badge.hue2rgb(int(hue * 360), val=gamma_table[int(colbright*255)]))
		#dcfurs.set_rgb565(x, y, (gamma_table[int(colbright*255)] << 3) & 0x7E0)
		#self.screen[y][x] = gamma_table[int(colbright*255)]

    def boop(self):
        self._set_random_params()
        
