import ugfx
import buttons
import pyb

ugfx.init()
buttons.init()

class Pages:
    def __init__(self, pagelist):
        self.list = pagelist
        self.current = 0

    def print_random(self):
        self.current = pyb.rng() % len(self.list)
        self.print_current()

    def print_current(self):
        self.list[self.current].print_page()

class Page1:
    def print_page(self):
        self.content = ["xxxxxxxxxxxxxxxxxxx             xxxxxxxxx       xxxxxxxxx",
                        "xxxxxxxxxxxx      x               x     x         x     x",
                        "xxxxxxxxxxxx  xxxxx xxxxxxxxxxxxx x  xxxx xxxxxxx x  x  x xxxxxxxxxxxxxxxxxxxxxx",
                        "xxxxxxxxxxxx    xxx x    xxx    x x    xx x     x x     x x  x  xxxxxxxxxxxxxxxx",
                        "xxxxxxxxxxxx  xxxxx x  x  x  x  x x  xxxx x  xxxx x  x  x x  x  xxxxxxxxxxxxxxxx",
                        "xxxxxxxxxxxx      x x  xx   xx  x x  xxxx x    xx x  x  x xx   xxxxxxxxxxxxxxxxx",
                        "xxxxxxxxxxxxxxxxxxx x  xxxxxxx  x xxxxxxx x  xxxx xxxxxxx x  x  xxxxxxxxxxxxxxxx",
                        "                    x  xxxxxxx  x         x  xxxx         x  x  xxxxxxxxxxxxxxxx",
                        "                  xxxxxxxxxxxxxxx       xxxxxxxxx       xxxxxxxxxxxxxxxxxxxxxxxx"]

        ugfx.clear(ugfx.BLACK)
        ugfx.area(0, 5, 320, 45, ugfx.BLUE)
        
        for i,line in enumerate(self.content):
            for j,c in enumerate(line):
                if c=="x":
                    ugfx.area(4*j, 5*i+5, 4, 5, ugfx.YELLOW)
        
        ugfx.area(0, 220, 320, 15, ugfx.YELLOW)
        ugfx.text(35, 221, "EMFFAX: The World at Your Fingertips", ugfx.BLUE)

class Page2:
    def print_page(self):
        ugfx.clear(ugfx.BLACK)
        ugfx.area(0, 5, 320, 45, ugfx.BLUE)
        
        ugfx.area(0, 220, 320, 15, ugfx.YELLOW)
        ugfx.text(35, 221, "EMFFAX: The World at Your Fingertips", ugfx.BLUE)

from imu import IMU

imu = IMU()

pages = Pages([Page1(),Page2()])

counter = 10000
orient = 0

while True:
    pyb.wfi()
    if buttons.is_pressed("BTN_MENU"):
        break

    counter += 1
    if counter >= 10000:
        pages.print_random()
        counter = 0
    ival = imu.get_acceleration()
    if ival['y'] < 0:
        if orient != 0:
            ugfx.orientation(0)
            orient = 0
            pages.print_current()
    elif orient != 180:
        ugfx.orientation(180)
        orient = 180
        pages.print_current()
