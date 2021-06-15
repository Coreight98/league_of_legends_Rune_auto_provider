import win32gui
import numpy as np
from PIL import ImageGrab
from selenium import webdriver
import cv2
from tkinter import *
import requests
import csv
from api import appkey #kakao apikey

windows = ''

def find_lune(result):
    with open('lol_data.csv',newline='',encoding="utf-8-sig") as csvfile:
        finder = csv.DictReader(csvfile)
        for row in finder:
            if row['이름'] in result:
                driver = webdriver.Chrome()
                driver.get(row['url'])


def kakao_ocr(screen, appkey: str):
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'
    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}
    image = screen
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})
def okClick():
    result = ''
    handle = win32gui.FindWindow(None, r'League of Legends')
    win32gui.SetForegroundWindow(handle)
    rect = win32gui.GetWindowRect(handle)
    x, y = rect[0], rect[1]
    w, h = rect[2] - x, rect[3] - y
    size_sc = [x + w // 3 + w // 10, y + h // 2 + h // 8, x + w // 2 + w // 12, y + h // 2 + h // 6 + 6]
    window.geometry("100x100+" + str(x + w) + "+" + str(y))
    screen = np.array(ImageGrab.grab(bbox=(size_sc[0], size_sc[1], size_sc[2], size_sc[3])))
    output = kakao_ocr(cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY), appkey).json()
    try:
        for _ in output['result']:
            result += (_['recognition_words'][0]) + ' '
    except:
        pass
    find_lune(result)
    return

window = Tk()
size_sc = [0, 0, 100, 100]
window.title("A")
window.geometry("100x100+100+100")
btn = Button(window, text="OK", command=okClick, height=50, width=50)
btn.pack()
window.mainloop()
