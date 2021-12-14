# WindowsKeyHook

Windows key combination hook by Python  3 in a system(global) wide . The amount of code for this project is small, which makes it easy to change or add features. 

I started this project just because I found the following projects are buggy to use or lack the features I need at the time of 2021-12-14, and it is also complicated for me to contribute code to them:  [boppreh](https://github.com/boppreh)/**[keyboard](https://github.com/boppreh/keyboard)** , [moses-palmer](https://github.com/moses-palmer)/**[pynput](https://github.com/moses-palmer/pynput)**,   [pywinauto](https://github.com/pywinauto)/**[pywinauto](https://github.com/pywinauto/pywinauto)** ,    [Answeror](https://github.com/Answeror)/**[pyhook_py3k](https://github.com/Answeror/pyhook_py3k)**. 

As for sending key combination, I still use [boppreh](https://github.com/boppreh)/**[keyboard](https://github.com/boppreh/keyboard#keyboard.send)**.
## Installation
Download [WindowsKeyHook.py](https://github.com/redstoneleo/WindowsKeyHook/blob/main/WindowsKeyHook.py) and put it somewhere you can import.

##  Usage 
 Change the `if __name__ == "__main__"` block at the bottom of  [WindowsKeyHook.py](https://github.com/redstoneleo/WindowsKeyHook/blob/main/WindowsKeyHook.py) to give a try. An usage example :

    WindowsKeyHook.hook({
        ('left shift', ): [lambda: print('left shift'), False], 
        ('right shift',): [lambda: print('right shift'), False],        
        ('left ctrl', 'c'): [lambda: print('left ctrl c'), False],
        #('left menu', 'x'): [lambda: print('alt x'), True],#The way to unhook a key combination  
    })

The parameter to `hook()` is a dict object, every dict key is tuple of key combination , and the corresponding value is a list with the first item the callable corresponding to the key combination, it is run **asynchronously** in a Python  thread, and the second item a boolen value to specify [whether](https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644985%28v=vs.85%29) preventing the system from passing the key combination message to the rest of the hook chain or the target window procedure.

If you want to **unhook** a key  combination, just comment or delete it from the above hook dict.

 The legal key names are also specified in this file,  notably, some key names used in program may not be the same as that have been printed on keys in your computer keyboard .  For example , the code name for  key with the printed name `Alt` in keyboard is `left menu`(key code:0xa4) or `right menu`(key code:0xa5) in program , [it is officially specified by Microsoft](https://docs.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN). To save user from being confused by this divergence, `WindowsKeyHook` will print a message like `pressed key code : xxxx` or `released key code : xxxx` if a key is pressed or released , then you can search the key code in `WindowsKeyHook.py` to find the correct code name for the key you need to use. 
 
 
If you press the key combination that has been hooked without releasing for a little while , `WindowsKeyHook` won't run the callback repeatedly.
