from utils.events import *
from utils.interface import *
from utils.mouse_keyboard_controller import *


class Mapper:
    def __init__(self) -> None:
        self.ds5w = DSW(1,self.onEvent)
        self.ds5w.run()
        self.t1x = -1
        self.t1y = -1

        self.maxACC = -1
        
        self.gyroValueX = 0
        self.gyroValueY = 0

        self.tlValue = 0
        self.trValue = 0
        

        self.ls_x = 0
        self.ls_y = 0

        self.rs_x = 0
        self.rs_y = 0

        # threading.Thread(target=self.gyroView).start()
        threading.Thread(target=self.rsView).start()
        threading.Thread(target=self.lsWheel).start()

    def gyroView(self):
        while True:
            x = int(-self.gyroValueY / 100)
            y = int(-self.gyroValueX /100)
            if x == 0 and y == 0:
                pass
            else:
                mouse_move(x,y)
                sleep(0.01)

    def rsView(self):
        while True:
            x = int(self.rs_x / 7)
            y = int(-self.rs_y / 7)
            if x == 0 and y == 0:
                pass
            else:
                mouse_move(x,y)
                sleep( 1 / 250 )

    def lsWheel(self):
        while True:
            wheel = int(self.ls_y / 8)
            sleep(1 / 60)
            mouse_wheel(wheel * 3)




    def onEvent(self,type,code,value):
        if type == EV_ABS and code == ABS_TOUCHPOINT_1_X:
            if self.t1x == -1:
                self.t1x = value
            else:
                if self.t1x != value:
                    offsetX = value - self.t1x
                    self.t1x = value
                    mouse_move(offsetX,0)
        if type == EV_ABS and code == ABS_TOUCHPOINT_1_Y:
            if self.t1y == -1:
                self.t1y = value
            else:
                if self.t1y != value:
                    offsetY = value - self.t1y
                    self.t1y = value
                    mouse_move(0,offsetY)
        if type == EV_KEY and code == BTN_TOUCHPOINT_1:
            if value == 0:
                self.t1x = -1
                self.t1y = -1

        if type == EV_REL and code == REL_ACCELEROMETER_X:
            self.gyroValueX = value

        if type == EV_REL and code == REL_ACCELEROMETER_Y:
            self.gyroValueY = value

        if type == EV_ABS and code == ABS_RX:
            if self.tlValue <= 24 and value > 24:
                mouse_press(MOUSE_BTN_RIGHT)
            if self.tlValue >= 24 and value < 24:
                mouse_release(MOUSE_BTN_RIGHT)
            self.tlValue = value


        if type == EV_ABS and code == ABS_RY:
            if self.trValue <= 24 and value > 24:
                mouse_press(MOUSE_BTN_LEFT)
            if self.trValue >= 24 and value < 24:
                mouse_release(MOUSE_BTN_LEFT)
            self.trValue = value


        if type == EV_ABS and code == ABS_X:
            self.ls_x = value
        if type == EV_ABS and code == ABS_Y:
            self.ls_y = value
        if type == EV_ABS and code == ABS_Z:
            self.rs_x = value
        if type == EV_ABS and code == ABS_RZ:
            self.rs_y = value

        if type == EV_KEY and code == BTN_DPAD_DOWN:
            if value == 0:
                key_press(40)
            else:
                key_relese(40)

        if type == EV_KEY and code == BTN_DPAD_UP:
            if value == 0:
                key_press(38)
            else:
                key_relese(38)

        if type == EV_KEY and code == BTN_DPAD_LEFT:
            if value == 0:
                key_press(37)
            else:
                key_relese(37)

        if type == EV_KEY and code == BTN_DPAD_RIGHT:
            if value == 0:
                key_press(39)
            else:
                key_relese(39)





        return 0

              



if __name__ == "__main__":
    try:
        Mapper()
    except Exception as e:
        print(e)
        exit(1)

    # for i in range(37,41):
    #     print(i)
    #     key_press(i)
    #     sleep(0.02)
    #     key_relese(i)
    #     sleep(0.5)
        