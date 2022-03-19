import os
import threading
from ctypes import *
from time import sleep

myLib = CDLL(os.path.join(os.path.dirname(__file__),"ds5w_x64.dll"))


def makePlayerLed(fade,bitmask,brightness):
    assert fade in [0,1]
    assert bitmask in [1,2,4,8,16]
    assert brightness in [0,1,2]
    return fade + bitmask * 2 + brightness * 64

def makeEffect(type,start,end):
    assert type in [0x00,0x01,0x02,0x26,0xfc]
    assert 0 <= start <= 0xff
    assert 0 <= end <= 0xff
    return type * 256 * 256  + start *256  + end


class DSW():
    def __init__(self,index,onEvent):#手柄编号
        if myLib.testControllerInit(index) != 0:
            count = myLib.getConnectedControllerCount()
            raise Exception(f"connect to controller_{index} failed , total {count} controller found")
        Class_ctor_wrapper = myLib.CreateDS5WInstance
        Class_ctor_wrapper.restype = c_void_p
        self.instance = c_void_p(Class_ctor_wrapper(index))
        self.onEvent = onEvent

    def run(self):
        HANDELERCFUNCTYPE = CFUNCTYPE(c_int, c_int, c_int,c_int)
        handeler_func = HANDELERCFUNCTYPE(self.handeler)
        thread = threading.Thread(target=myLib.StartDS5WInstance,args=(self.instance,handeler_func)) 
        thread.start()
        return thread


    def handeler(self,type,code,value):
        self.onEvent(type,code,value)
        return 0

    def controller(self,type,code,value):
        myLib.DS5_interface_controller(self.instance,type,code,value)

    def destroy(self):
        myLib.DeleteDS5WInstance(self.instance)





if __name__ == "__main__":
    try:
        ds5_1 = DSW(1)
        ds5_1.run()

        # count = 1
        # while True:
        #     count += 1
        #     if count % 2 == 0:
        #         ds5_1.controller(0x11,0x08,0)
        #     else:
        #         ds5_1.controller(0x11,0x08,1)
        #     ds5_1.controller(0,0,0)
        #     sleep(0.5)   

        # count = 1
        # while True:
        #     count += 1
        #     if count % 2 == 0:
        #         ds5_1.controller(0x11,0x20,0x000000ff)
        #     else:
        #         ds5_1.controller(0x11,0x20,0xd90051ff)
        #     ds5_1.controller(0,0,0)
        #     sleep(0.5)   

        # for i in [0,1]:
        #     for j in [1,2,4,8,16]:
        #         for k in [0,1,2]:
        #             ds5_1.controller(0x11,0x30,makePlayerLed(i,j,k))
        #             print(makePlayerLed(i,j,k))
        #             sleep(0.5)


        # for i in range(256):
        #     ds5_1.controller(0x03,0x31,i)
        #     sleep(0.01)
        #     print(i)

        # ds5_1.controller(0x03,0x31,0)
        
        # for i in range(256):
        #     ds5_1.controller(0x03,0x32,i)
        #     sleep(0.01)
        #     print(i)
        # ds5_1.controller(0x03,0x32,0)


        # for et in [0x00,0x01,0x02,0x26,0xfc]:
        #     end = 0
        #     for start in range(256):
        #         ds5_1.controller(0x03,0x41,makeEffect(et,start,end))
        #         print(makeEffect(et,start,end))
        #         sleep(1)



        # while True:
        #     for i in range(0,255):
        #         ds5_1.controller(0x03,0x41,makeEffect(0x1,0 , i))
        #         sleep(0.01)
        # ds5_1.controller(0x03,0x41,makeEffect(0x00,0,0))



        state = 0
        a = 255
        r = 255
        g = 0
        b = 0
        while True:
            if state == 0:
                g += 1
                if g == 255:
                    state = 1

            if state == 1:
                r -= 1
                if r == 0:
                    state = 2

            if state == 2:
                b += 1
                if b == 255:
                    state = 3

            if state == 3:
                g -= 1
                if g == 0:
                    state = 4
            if state == 4:
                r += 1
                if r == 255:
                    state = 5
            if state == 5:
                b -= 1
                if b == 0:
                    state = 0
            num = (r << 24) + (g << 16) + (b << 8) + (a)
            ds5_1.controller(0x11,0x20, num)
            sleep(0.003)   
                
        ds5_1.destroy()

    except KeyboardInterrupt:
        ds5_1.destroy()
        print("destroy")
















# ds5_1.controller(1,1,1)
# ds5_1.controller(2,2,2)
# ds5_1.controller
# sleep(1)
# ds5_1.destroy()


# ds5_1.controller(0,0,0)


