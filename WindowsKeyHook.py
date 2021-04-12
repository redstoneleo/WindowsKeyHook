import atexit
import threading
from ctypes import *

from ctypes import wintypes
from ctypes import c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, WINFUNCTYPE, POINTER
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, HMODULE, LPCWSTR, HINSTANCE, HWND


WH_KEYBOARD_LL = 13  # 全局hook都要用_LL，非WH_KEYBOARD
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

WM_SYSKEYDOWN = 0x104  # Used for ALT key
WM_SYSKEYUP = 0x105

WH_MOUSE_LL = 14
WH_MOUSE = 7
ALL_Threads = 0  # DWORD(0)

# https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
keyNameToKeyCode =  {
 'control-break processing':   0x03,
 'backspace':   0x08,
 'tab':   0x09,
'clear':   0x0c,
 'enter':   0x0d,
 'ctrl':   0x11,
 'alt':   0x12,
 'pause':   0x13,
 'caps lock':   0x14,
 'ime kana mode':   0x15,
 'ime hanguel mode':   0x15,
 'ime hangul mode':   0x15,
 'ime junja mode':   0x17,
 'ime final mode':   0x18,
 'ime hanja mode':   0x19,
 'ime kanji mode':   0x19,
 'esc':   0x1b,
'ime convert':   0x1c,
 'ime nonconvert':   0x1d,
 'ime accept':   0x1e,
'ime mode change request':   0x1f,
 'spacebar':   0x20,
 'page up':   0x21,
 'page down':   0x22,
 'end':   0x23,
 'home':   0x24,
 'left':   0x25,
 'up':   0x26,
 'right':   0x27,
 'down':   0x28,
 'select':   0x29,
 'print':   0x2a,
 'execute':   0x2b,
'print screen':   0x2c,
 'insert':   0x2d,
 'delete':   0x2e,
'help':   0x2f,
 '0':   0x30,
 '1':   0x31,
 '2':   0x32,
 '3':   0x33,
 '4':   0x34,
 '5':   0x35,
 '6':   0x36,
 '7':   0x37,
 '8':   0x38,
 '9':   0x39,
 'a':   0x41,
 'b':   0x42,
 'c':   0x43,
 'd':   0x44,
 'e':   0x45,
 'f':   0x46,
 'g':   0x47,
 'h':   0x48,
 'i':   0x49,
 'j':   0x4a,
 'k':   0x4b,
'l':   0x4c,
 'm':   0x4d,
 'n':   0x4e,
'o':   0x4f,
 'p':   0x50,
 'q':   0x51,
 'r':   0x52,
 's':   0x53,
 't':   0x54,
 'u':   0x55,
 'v':   0x56,
 'w':   0x57,
 'x':   0x58,
 'y':   0x59,
 'z':   0x5a,
 'left windows':   0x5b,
'right windows':   0x5c,
 'applications':   0x5d,
'sleep':   0x5f,
 '0':   0x60,
 '1':   0x61,
 '2':   0x62,
 '3':   0x63,
 '4':   0x64,
 '5':   0x65,
 '6':   0x66,
 '7':   0x67,
 '8':   0x68,
 '9':   0x69,
 '*':   0x6a,
 '+':   0x6b,
'separator':   0x6c,
 '-':   0x6d,
 'decimal':   0x6e,
'/':   0x6f,
 'f1':   0x70,
 'f2':   0x71,
 'f3':   0x72,
 'f4':   0x73,
 'f5':   0x74,
 'f6':   0x75,
 'f7':   0x76,
 'f8':   0x77,
 'f9':   0x78,
 'f10':   0x79,
 'f11':   0x7a,
 'f12':   0x7b,
'f13':   0x7c,
 'f14':   0x7d,
 'f15':   0x7e,
'f16':   0x7f,
 'f17':   0x80,
 'f18':   0x81,
 'f19':   0x82,
 'f20':   0x83,
 'f21':   0x84,
 'f22':   0x85,
 'f23':   0x86,
 'f24':   0x87,
 'num lock':   0x90,
 'scroll lock':   0x91,
 'left shift':   0xa0,
 'right shift':   0xa1,
 'left ctrl':   0xa2,
 'right ctrl':   0xa3,
 'left menu':   0xa4,
 'right menu':   0xa5,
 'browser back':   0xa6,
 'browser forward':   0xa7,
 'browser refresh':   0xa8,
 'browser stop':   0xa9,
 'browser search key':   0xaa,
 'browser favorites':   0xab,
'browser start and home':   0xac,
 'volume mute':   0xad,
 'volume down':   0xae,
'volume up':   0xaf,
 'next track':   0xb0,
 'previous track':   0xb1,
 'stop media':   0xb2,
 'play/pause media':   0xb3,
 'start mail':   0xb4,
 'select media':   0xb5,
 'start application 1':   0xb6,
 'start application 2':   0xb7,
 '+':   0xbb,
 ':':   0xbc,
 '-':   0xbd,
 '.':   0xbe,
 'ime process':   0xe5,
'attn':   0xf6,
'crsel':   0xf7,
'exsel':   0xf8,
'erase eof':   0xf9,
'play':   0xfa,
'zoom':   0xfb,
'reserved ':   0xfc,
'pa1':   0xfd,
'clear':   0xfe,
}



# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *

# class ThreadRunning2(QThread):  # 用 threading.Thread 的时候，英酷词典主窗口调用 Ctrl+C的时候会卡死，不知道为什么
#     # implementing new slots in a QThread subclass is error-prone and discouraged.

#     def __init__(self, func, *args, **kwargs):
#         super().__init__()
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         self.result = 0
#         # self.finished.connect(lambda: threadSet.discard(self))
#         self.start()

#     def run(self):
#         self.func(*self.args)
#         threadSet.discard(self)

#         # print('threadSet-------------',threadSet)
#         # try:
#         #     self.result = self.func(*self.args)  # deleteLater
#         # except Exception as e:
#         #     raise e
#         # print('ThreadRunning--------------{}---'.format(self.func.__name__), e)
#         # logging.error('ThreadRunning---------------')

#         # _, value, traceback = sys.exc_info()
#         # print(type(e).__name__, e.args, sys.exc_info())
#         # print('Error opening %s: %s' % (value.filename, value.strerror))

class ThreadRunning(threading.Thread):  # 用 threading.Thread 的时候，英酷词典主窗口调用 Ctrl+C的时候会卡死，不知道为什么
    # implementing new slots in a QThread subclass is error-prone and discouraged.

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = 0
        # self.finished.connect(lambda: threadSet.discard(self))
        self.start()

    def run(self):
        self.func(*self.args)
        threadSet.discard(self)


pressedKeyCodeList = []
threadSet=set()#否则thread会被gc

def lowLevelKeyboardHandler(nCode, wParam, lParam):
    '''
    ncode : A code the hook procedure uses to determine how to process the message. If nCode is less than zero, the hook procedure must pass the message to the windll.user32.CallNextHookEx function without further processing and should return the value returned by windll.user32.CallNextHookEx.
    wParam：The identifier of the keyboard message. This parameter can be one of the following messages: WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, or WM_SYSKEYUP.
    lParam：A pointer to a KBDLLHOOKSTRUCT structure.
    '''

    if nCode < 0:
        return windll.user32.CallNextHookEx(ALL_Threads, nCode, wParam, lParam)

    virtualKeyCode =  lParam.contents.vk_code#lParam[0]
    # print(f"{'pressed' if wParam in {WM_KEYDOWN, WM_SYSKEYDOWN} else 'released'} key code :{hex(virtualKeyCode),virtualKeyCode}")
    if wParam in {WM_KEYDOWN, WM_SYSKEYDOWN} and virtualKeyCode not in pressedKeyCodeList:  # 防止一直按住时的多次触发
        pressedKeyCodeList.append(virtualKeyCode)
        handlerInfo = registeredKeyCodeList2handlerInfo.get(tuple(pressedKeyCodeList))
        # print(hex(virtualKeyCode),tuple(pressedKeyCodeList),handlerInfo)
        if handlerInfo:
            # print(handlerInfo,tuple(pressedKeyCodeList))
            func, suppress = handlerInfo
            threadSet.add(ThreadRunning(func)) # 用threading.Thread(target=lambda: print(i))的话你看不到exception信息
            
            if suppress:
                return 1  # If the hook procedure processed the message, it may return a nonzero value to prevent the system from passing the message to the rest of the hook chain or the target window procedure.

    elif wParam in {WM_KEYUP, WM_SYSKEYUP}:  # 释放的时候
        try:
            pressedKeyCodeList.remove(virtualKeyCode)
        except ValueError as e:  # remove raises ValueError when x is not found in s.
            pass

        # print('onKeyReleased key set', pressedKeyCodeList)

    return windll.user32.CallNextHookEx(ALL_Threads, nCode, wParam, lParam)  # Calling the windll.user32.CallNextHookEx function to chain to the next hook procedure is optional, but it is highly recommended; otherwise, other applications that have installed hooks will not receive hook notifications and may behave incorrectly as a result. You should call windll.user32.CallNextHookEx unless you absolutely need to prevent the notification from being seen by other applications.



ULONG_PTR = POINTER(DWORD)

class KBDLLHOOKSTRUCT(Structure):#如果不定义的话那么lowLevelKeyboardHandler(nCode, wParam, lParam)的第三个参数就是一个莫名其妙的数字，用不了
    _fields_ = [("vk_code", DWORD),
                ("scan_code", DWORD),
                ("flags", DWORD),
                ("time", c_int),
                ("dwExtraInfo", ULONG_PTR)]

# lowLevelKeyboardProcedureFunctionPrototype = WINFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
lowLevelKeyboardProcedureFunctionPrototype = WINFUNCTYPE(c_int, WPARAM, LPARAM, POINTER(KBDLLHOOKSTRUCT))


windll.user32.SetWindowsHookExW.argtypes = (  # 要指定的，否则QT里call会出现argument 2: <class 'TypeError'>: expected WinFunctionType instance instead of WinFunctionType
    c_int,
    lowLevelKeyboardProcedureFunctionPrototype,
    wintypes.HINSTANCE,
    wintypes.DWORD)

lowLevelKeyboardProcedure = lowLevelKeyboardProcedureFunctionPrototype(lowLevelKeyboardHandler)

windll.user32.CallNextHookEx.argtypes = [c_int , c_int, c_int, POINTER(KBDLLHOOKSTRUCT)] # 要指定的，否则QT里call会出现argument 4: <class 'TypeError'>: wrong type

registeredKeyCodeList2handlerInfo = {}
hookHandle=None

def hook(registeredKeyCombination2handlerInfo):
    for keyCombination in registeredKeyCombination2handlerInfo:
        registeredKeyCodeList2handlerInfo[tuple(map(lambda key: keyNameToKeyCode[key], keyCombination))]=registeredKeyCombination2handlerInfo[keyCombination]

    # print('hook--------------',registeredKeyCodeList2handlerInfo)
    
    hookHandle = windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL, lowLevelKeyboardProcedure,None, ALL_Threads)  # 32为是不是要用 windll.kernel32.GetModuleHandleW(None)？？？ If the function succeeds, the return value is the handle to the hook procedure. If the function fails, the return value is NULL. To get extended error information, call GetLastError.

    if hookHandle:
        atexit.register(windll.user32.UnhookWindowsHookEx, hookHandle)  # Before terminating, an application must call the UnhookWindowsHookEx function to free system resources associated with the hook.


def unhook(registeredKeyCombination2handlerInfo):
    for keyCombination in registeredKeyCombination2handlerInfo:
        registeredKeyCodeList2handlerInfo.pop(tuple(map(lambda key: keyNameToKeyCode[key], keyCombination)),None)#启动的时候如果没有勾选全局翻译就会执行这个，用pop不会出现异常，del则会，所以dict操作尽量pop None

    # print('unhook--------------',registeredKeyCodeList2handlerInfo)

    if not registeredKeyCodeList2handlerInfo and hookHandle:
        windll.user32.UnhookWindowsHookEx(hookHandle)  # Before terminating, an application must call the UnhookWindowsHookEx function to free system resources associated with the hook.



if __name__ == "__main__":
    hook({
        ('left shift', ): [lambda: print('left shift'), False], #按键顺序是有影响的
        ('right shift',): [lambda: print('right shift'), False],        
        ('left ctrl', 'c'): [lambda: print('left ctrl c'), False],
        ('left menu', 'x'): [lambda: print('alt x'), True],
    })

    msg = windll.user32.GetMessageW(None, 0, 0, 0)
    windll.user32.TranslateMessage(byref(msg))
    windll.user32.DispatchMessageW(byref(msg))
