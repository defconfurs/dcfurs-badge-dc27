## Cylon visor animation
import dcfurs

class cylon:
    def __init__(self):
        self.column = 0
        self.interval = 75
        self.leftright = True
    
    def draw(self):
        dcfurs.clear()
        for row in range(0, 7):
            dcfurs.set_pixel(self.column-1, row, 1)
            dcfurs.set_pixel(self.column, row, 200)
            dcfurs.set_pixel(self.column+1, row, 1)
        if self.leftright:
           self.column += 1
           if self.column >= 17:
               self.leftright = False 
        else:
            self.column -= 1
            if self.column <= 0:
                self.leftright = True
