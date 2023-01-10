from cefpython3     import cefpython as cef
from SDK.localSDK   import localSDK
from Handlers       import *
from BrowserFrame   import *
from MainFrame      import MainFrame
from DB.DataService    import DataService
import threading    as thread
import tkinter      as tk
import sys

def main():
    running = True
    # Create MorphCast SDK
    sdk = localSDK()
    global freePort; freePort = sdk.returnFreePort()
    
    sdkThread = thread.Thread(target=sdk.start)
    sdkThread.start()

    # Sqlite
    dataService = DataService(1)
    def sqlLoop():
        if running: 
            thread.Timer(5.0, sqlLoop).start()
            dataService.calculate()

    sys.excepthook = cef.ExceptHook
    root = tk.Tk()
    app  = MainFrame(root, freePort, dataService)
    cef.Initialize(commandLineSwitches = {"enable-media-stream": " "})
    
    # =============
    thread.Timer(10.0, sqlLoop).start()
    app.mainloop()
    
    # =============

    cef.Shutdown()
    sdk.httpd.shutdown()

if __name__ == '__main__':
    main()