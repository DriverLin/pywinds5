import threading

import vgamepad as vg
from vgamepad import XUSB_BUTTON

from utils.ds5_events import *
from utils.mouse_keyboard_controller import *
from utils.pywinds5 import pywinds5

X360_BTN_MAP = {
    BTN_CROSS: XUSB_BUTTON.XUSB_GAMEPAD_A,
    BTN_CIRCLE: XUSB_BUTTON.XUSB_GAMEPAD_B,
    BTN_SQUARE: XUSB_BUTTON.XUSB_GAMEPAD_X,
    BTN_TRIANGLE: XUSB_BUTTON.XUSB_GAMEPAD_Y,
    BTN_DPAD_DOWN: XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    BTN_DPAD_LEFT: XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    BTN_DPAD_RIGHT: XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    BTN_DPAD_UP: XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    BTN_L1: XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    # BTN_L2:
    BTN_L3: XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    BTN_R1: XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    # BTN_R2:
    BTN_R3: XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    BTN_SELECT: XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    BTN_START: XUSB_BUTTON.XUSB_GAMEPAD_START,
    BTN_PS: XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,

}


class vgamepad_controller:
    def __init__(self) -> None:
        self.ds5 = pywinds5(
            index=0,
            onBTN=self.onBTN,
            onLT=self.onLT,
            onRT=self.onRT,
            onLeftStick=self.onLeftStick,
            onRightStick=self.onRightStick,
            onGyroscope=self.onGyro,
            onAccelerometer=self.onAcc,
            onTouchPad_1=self.onTouchPad_1,
        )

        self.vx360 = vg.VX360Gamepad()
        self.vx360.register_notification(callback_function=self.callBack)

        self.rs_x = 0
        self.rs_y = 0
        self.rs_add_x = 0
        self.rs_add_y = 0

        self.touchPoint_1_down = False
        self.touchPoint_1_last = (-1, -1)

    def onBTN(self, btn, down):
        if btn in X360_BTN_MAP:
            self.vx360.press_button(
                X360_BTN_MAP[btn]) if down else self.vx360.release_button(X360_BTN_MAP[btn])
            self.vx360.update()

        if btn == TOUCH_POINT_1:
            self.touchPoint_1_down = down
            if down == False:
                self.touchPoint_1_last = (-1, -1)

    def onLT(self, value):
        self.vx360.left_trigger(value)
        # self.ds5.stateController.setLightBar_RGB(g = value * 200 / 255 + 55)
        self.vx360.update()

    def onRT(self, value):
        self.vx360.right_trigger(value)
        # self.ds5.stateController.setLightBar_RGB(r = value * 200 / 255 + 55 )
        self.vx360.update()

    def onLeftStick(self, x, y):
        self.vx360.left_joystick(x*256, y*256)
        self.vx360.update()

    def setRS(self):
        mixed_x = self.rs_x + self.rs_add_x
        mixed_y = self.rs_y + self.rs_add_y
        if mixed_x < -127:
            mixed_x = -127
        if mixed_x > 127:
            mixed_x = 127
        if mixed_y < -127:
            mixed_y = -127
        if mixed_y > 127:
            mixed_y = 127
        self.vx360.right_joystick(mixed_x * 256, mixed_y * 256)
        # print(mixed_x, mixed_y)
        self.vx360.update()

    def onRightStick(self, x, y):
        self.rs_x = x
        self.rs_y = y
        self.setRS()

    def onGyro(self, x, y, z):
        # self.ds5.stateController.setGyroscope(x, y, z)
        # print(f"Gyroscope: {x}, {y}, {z}")
        pass

    def onAcc(self, x, y, z):
        self.rs_add_y = int(x / 16)  # c_short
        self.rs_add_x = int(- y / 4)
        self.setRS()
        # print(f"Accelerometer: {int(x / 0x7F)}, {int(y / 0x7f)}, {int(z/0x7f)}")
        pass

    def onTouchPad_1(self, x, y):
        if self.touchPoint_1_down:
            if self.touchPoint_1_last == (-1, -1):
                self.touchPoint_1_last = (x, y)
            else:
                offset_x, offset_y = x - \
                    self.touchPoint_1_last[0], y-self.touchPoint_1_last[1]
                self.touchPoint_1_last = (x, y)
                # mouse_move(int(offset_x/4), int(offset_y / 4))
                mouse_wheel(int(offset_y))
        else:
            pass

    def callBack(self, client, target, large_motor, small_motor, led_number, user_data):
        self.ds5.stateController.setRightRumble(small_motor)
        self.ds5.stateController.setLeftRumble(large_motor)
        # self.ds5.stateController.setLightBar("#d90051")
        print(f"Received notification for client {client}, target {target}")
        print(f"large motor: {large_motor}, small motor: {small_motor}")
        print(f"led number: {led_number}")

    def run(self):
        return self.ds5.run()


vgamepad_controller().run().join()
