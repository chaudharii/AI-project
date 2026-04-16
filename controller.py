import pyautogui

pyautogui.FAILSAFE = False

def press(key):
    pyautogui.keyDown(key)

def release(key):
    pyautogui.keyUp(key)
