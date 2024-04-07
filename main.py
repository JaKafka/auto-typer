from pynput import keyboard
from pynput.keyboard import Controller, Key
from threading import Thread, Event

# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm

import pytesseract

# importing OpenCV
import cv2

from PIL import ImageGrab

pipe = ''

def on_press(key):
    command = Controller()
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['home','end']:  # keys of interest
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # Provide path to Tesseract
        cap = ImageGrab.grab(bbox=(300, 200, 1850, 900))
        px = cap.load()
        height,width = cap.size
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = px[loop1, loop2]
                rem = 0
                if r == 149 and g == 197 and b == 144:
                    rem = 1
                elif r == 237 and g == 247 and b == 231:
                    rem = 1
                elif r == 255 and g == 220 and b == 217:
                    rem = 1
                elif r == 213 and g == 91 and b == 96:
                    rem = 1
                if rem:
                    px[loop1, loop2] = (255,255,255)
        tesstr = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
            lang='eng')
        tesstr = tesstr.strip()
        tesstr = " ".join(tesstr.split())
        tesstr = tesstr + " "
        command.type(tesstr)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys