# WindowsKeyboardHook

Windows key combination hook by Python  3 in a system(global) wide .

I started this project just because I found the following projects are bugy to use or lack the features I need  at the time of 2020-12-21, and it is also complicated for me to contribute code to them:  [boppreh](https://github.com/boppreh)/**[keyboard](https://github.com/boppreh/keyboard)** ,  [pywinauto](https://github.com/pywinauto)/**[pywinauto](https://github.com/pywinauto/pywinauto)** ,  [moses-palmer](https://github.com/moses-palmer)/**[pynput](https://github.com/moses-palmer/pynput)**,   [Answeror](https://github.com/Answeror)/**[pyhook_py3k](https://github.com/Answeror/pyhook_py3k)**. 

As for sending key combination, I still use [boppreh](https://github.com/boppreh)/**[keyboard](https://github.com/boppreh/keyboard)**.

## Installation
1. pip install --upgrade pyqt5
2. download [WindowsKeyboardHook.py](https://github.com/redstoneleo/WindowsKeyboardHook/blob/main/WindowsKeyboardHook.py) and put it somewhere you can import.

	Currently,  `WindowsKeyboardHook` runs the callback corresponding to the key combination in an individual PyQt5 QThread, it is possible  to get rid of it by replacing it with `threading.Thread` of Python, so porting contributions are welcome  !
##  Usage 
 Change the `if __name__ == "__main__"` block at the bottom of  [WindowsKeyboardHook.py](https://github.com/redstoneleo/WindowsKeyboardHook/blob/main/WindowsKeyboardHook.py) to give a try. An usage example :

    WindowsKeyboardHook.hook({
        ('left shift', ): [lambda: print('left shift'), False], 
        ('right shift',): [lambda: print('right shift'), False],        
        ('left ctrl', 'c'): [lambda: print('left ctrl c'), False],
        ('left menu', 'x'): [lambda: print('alt x'), True],
    })#Alt + X

The parameter to `hook()` is a dict object, every dict key is tuple of key combination , and the corresponding value is a list with the first item the callable corresponding to the key combination and the second item a boolen value to specify whether preventing the system from passing the key combination message to the rest of the hook chain or not.  

An `unhook` example :

    WindowsKeyboardHook.unhook({      
        ('left ctrl', 'c'): [lambda: print('left ctrl c'), False],
        ('left menu', 'x'): [lambda: print('alt x'), True],
    })    

Those passed to `unhook()` would be unhooked.

 The legal key names are also specified in this file,  notably, some key names used in program may not be the same as that have been printed on keys in your computer keyboard .  For example , the code name for  key with the printed name `Alt` in keyboard is `left menu`(key code:0xa4) or `right menu`(key code:0xa5) in program , [it is officially specified by Microsoft](https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN). To save user from being confused by this divergence, `WindowsKeyboardHook` will print a message like `pressed key code : xxxx` if a key is pressed , then you can search the key code in `WindowsKeyboardHook.py` to find the correct code name for the key you need to use. 
 

If you press the key combination that has been hooked without releasing for a little while , `WindowsKeyboardHook` won't run the callback repeatedly.
