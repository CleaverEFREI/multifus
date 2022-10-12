from tkinter.tix import Tree
import pynput.mouse as mouse
import pynput.keyboard as kb
import asyncio
import win32gui
import win32api
import win32con
from time import sleep, time
import pygetwindow
import keyboard


def window_size(hwnd, debug = 0):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = 2560
    h = 1440
    if debug ==1:
        print("\tLocation: (%d, %d)" % (x, y))
        print("\tSize: (%d, %d)" % (w, h))
    return x,y,w,h

def do_click(hwnd, x, y):
    lParam = win32api.MAKELONG(x,y)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

def hook():        
    # Scan des fenetres ouvertes
    screen_name = []
    print("Waiting for dofus ...")
    while len(screen_name) == 0:
        screen_tiles_name = pygetwindow.getAllTitles()
        for i in screen_tiles_name:
            if "Dofus 2." in i:        
                # Si on trouve dofus
                print("Hooked on : "+i)
                screen_name.append(i)
    hwnd_list = []
    for i in screen_name:
        hwnd = win32gui.FindWindow(None, i)
        hwnd = [hwnd,i.split(" ")[0]]
        hwnd_list.append(hwnd)
    return hwnd_list

def on_click(m,table_acc_size):
    try:
        if m.button.name == "left":
            for acc in table_acc_size:
                sleep(0.3)
                do_click(acc[-1], m.x, m.y)
    except Exception:
        pass

"""
def on_press(m,table_acc_size):
    pass
"""
async def checkMouseEvents(table_acc_size):
    with mouse.Events() as mouseEvents:
        mouseEvent = mouseEvents.get(0.1)
        if mouseEvent != None:
            on_click(mouseEvent, table_acc_size)
"""
async def checkKeyboardEvents(table_acc_size):
    with kb.Events() as keyboardEvents:
        keyboardEvent = keyboardEvents.get(0.01)
        if keyboardEvent != None:
            on_press(keyboardEvent, table_acc_size)
"""
async def main(table_acc_size):
    # Schedule two calls *concurrently*:
    await asyncio.gather(checkMouseEvents(table_acc_size))#checkKeyboardEvents(table_acc_size),



if __name__ == "__main__":
    hwnd = hook()
    table_acc_size = []
    cpt = 0
    for hw in hwnd:
        x,y,w,h = window_size(hw[0])
        table_acc_size.append([x,y,w,h,hw[1],hw[0]])
        print("Compte ",cpt,":")
        print(x,y,w,h,hw[1],hw[0])
        cpt += 1
    print("Select a leader")
    # select account with an input and delete it for the list
    l = input()
    table_acc_size.pop(int(l))
    while True:
        if keyboard.is_pressed('-'): 
            print('You quit!')
            break
        if keyboard.is_pressed('*'): 
            print('Pause!')
            sleep(1)
            while True:
                if keyboard.is_pressed('/'):
                    print('Resume!')
                    break

        asyncio.run(main(table_acc_size))
    
