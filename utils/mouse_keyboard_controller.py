import ctypes
from time import sleep, time, time_ns

import win32api
import win32con

_MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA

MOUSE_BTN_LEFT = 1
MOUSE_BTN_RIGHT = 2
MOUSE_BTN_MIDDLE = 3

def key_press(num):
    win32api.keybd_event(num, _MapVirtualKey(num, 0), 0, 0)

def key_relese(num):
    win32api.keybd_event(num, _MapVirtualKey(num, 0), win32con.KEYEVENTF_KEYUP, 0)

def key_event(num,down):
    if down:
        key_press(num)
    else:
        key_relese(num)



def mouse_press(btn):
    if btn == MOUSE_BTN_LEFT:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    elif btn == MOUSE_BTN_RIGHT:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    elif btn == MOUSE_BTN_MIDDLE:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)


def mouse_release(btn):
    if btn == MOUSE_BTN_LEFT:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif btn == MOUSE_BTN_RIGHT:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    elif btn == MOUSE_BTN_MIDDLE:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
    
def mouse_wheel(delta):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,delta,0)

def mouse_move(offset_x,offset_y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,offset_x,offset_y,0,0)
