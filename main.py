from keyboard import is_pressed
import pyautogui
import time
import ctypes
from PIL import Image,ImageGrab
import os
import mss
from colorama import Fore, Style, init
import json

S_HEIGHT, S_WIDTH = (ImageGrab.grab().size)
#判定する色なんだけど
COLOR_R = [250,250,250]#赤 紫 黄
COLOR_G = [90,100, 250]
COLOR_B = [90,250, 90]


TOLERANCE = 35#色の許容範囲
GRABZONE = 4#範囲
TRIGGER_KEY = "F2"#切り替え
BUNNY_KEY = "F3"#バニホキー
SWITCH_KEY = "F4"#武器切り替え
COLOR_CHANGE_KEY = "F5"#色変え
HOLD_KEY = "shift"#ホールドキー
COLOR=0

GRABZONE_KEY_UP = "up"#範囲上げ
GRABZONE_KEY_DOWN = "down"#範囲下げ

mods = ["オペ/マーシャル", "ガーディアン", "ヴァンダル"]
stCOLOR = ["赤","紫","黄"]

pyautogui.FAILSAFE = False

def LoadConfig():#Config読み込み
    global TOLERANCE,GRABZONE,TRIGGER_KEY,BUNNY_KEY,SWITCH_KEY,COLOR_CHANGE_KEY,HOLD_KEY,COLOR
    try: 
        with open('config.json', 'r',-1,"UTF-8") as config_file:
            config = json.load(config_file)
        
        TOLERANCE = config["TOLERANCE"]#色の許容範囲
        GRABZONE = config["GRABZONE"]#範囲
        TRIGGER_KEY = config["TRIGGER_KEY"]#切り替え
        BUNNY_KEY = config['BUNNY_KEY']#バニホキー
        SWITCH_KEY = config['SWITCH_KEY']#武器切り替え
        COLOR_CHANGE_KEY = config['COLOR_CHANGE_KEY']#色変え
        HOLD_KEY = config['HOLD_KEY']#ホールドキー
        if config["ENEMY_COLOR"] =="赤":COLOR=0
        elif config["ENEMY_COLOR"] =="紫":COLOR =1
        else:COLOR=2
        if GRABZONE <1 or GRABZONE > 10: GRABZONE=4
    except:
        pass

def SaveConfig():
    nowconfig = {
        "TRIGGER_KEY": TRIGGER_KEY, 
        "BUNNY_KEY": BUNNY_KEY, 
        "SWITCH_KEY": SWITCH_KEY, 
        "COLOR_CHANGE_KEY": COLOR_CHANGE_KEY, 
        "HOLD_KEY": HOLD_KEY,
        "GRABZONE": GRABZONE,
        "ENEMY_COLOR" : stCOLOR[COLOR],
        "TOLERANCE" : TOLERANCE
    }
    with open('config.json', 'w',encoding="UTF-8") as config_file:
        json.dump(nowconfig, config_file,ensure_ascii=False, indent=4)



class FoundEnemy(Exception):
    pass

class notteiBot():
    def __init__(self) -> None:
        self.toggled = False
        self._bunny = False
        self.mode = 1
        self.last_reac = 0
        
    def toggle(self) -> None: self.toggled = not self.toggled
        
    def bunnyy(self) -> None: self._bunny = not self._bunny

    def switch(self):
        if self.mode != 2: self.mode += 1
        else: self.mode = 0

    def click(self) -> None:
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # sol bas
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # sol bırak
        
    def approx(self, r, g ,b) -> bool: return COLOR_R[COLOR] - TOLERANCE < r < COLOR_R[COLOR] + TOLERANCE and COLOR_G[COLOR] - TOLERANCE < g < COLOR_G[COLOR] + TOLERANCE and COLOR_B[COLOR] - TOLERANCE < b < COLOR_B[COLOR] + TOLERANCE
    
    def grab(self) -> None:
        with mss.mss() as sct:
            bbox=(int(S_HEIGHT/2-GRABZONE), int(S_WIDTH/2-GRABZONE), int(S_HEIGHT/2+GRABZONE), int(S_WIDTH/2+GRABZONE))
            sct_img = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self) -> None:
        start_time = time.time()
        pmap = self.grab()
        
        try:
            for x in range(0, GRABZONE*2):
                for y in range(0, GRABZONE*2):
                    r, g, b = pmap.getpixel((x,y))
                    if self.approx(r, g, b): raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time)*1000)
            self.click()
            if self.mode == 0: time.sleep(0.5)
            if self.mode == 1: time.sleep(0.25)
            if self.mode == 2: time.sleep(0.2)
            print_banner(self)

    def bunny(self) -> None:
        while True:
            if is_pressed("space"): pyautogui.press("space")
            else: break
def print_banner(bot: notteiBot) -> None:
    os.system("cls")
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
    print(" ┬    ┌┬┐┬┌─┐┌─┐    ┬ ┬  \n │    ││││└─┐└─┐    │ │ \n ┴    ┴ ┴┴└─┘└─┘    └─┘")
    print(Style.NORMAL +Fore.MAGENTA+"========= Key =========")
    
    print(Fore.LIGHTWHITE_EX+"トリガーキー   :",Fore.LIGHTCYAN_EX +TRIGGER_KEY + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"ホールドキー   :",Fore.LIGHTCYAN_EX +HOLD_KEY + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"バニホキー     :", Fore.LIGHTCYAN_EX + BUNNY_KEY + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"武器           :", Fore.LIGHTCYAN_EX +SWITCH_KEY + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"敵色           :", Fore.LIGHTCYAN_EX + COLOR_CHANGE_KEY + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"範囲           :", Fore.LIGHTCYAN_EX +GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print(Fore.WHITE +       "保存           :", Fore.GREEN+"F10")
    print(Fore.MAGENTA+"========= Info =========")
    
    print(Fore.LIGHTWHITE_EX+"トリガーボット :" , (Fore.GREEN if bot.toggled else Fore.RED) + ("有効" if bot.toggled else "無効") + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"バニーホップ   :", (Fore.GREEN if bot._bunny else Fore.RED) + ("有効" if bot._bunny else "無効") + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"武器モード     :", Fore.CYAN + mods[bot.mode] + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"敵色           :", ( Fore.MAGENTA if COLOR == 1 else Fore.RED if COLOR is not 2 else Fore.YELLOW ) + stCOLOR[COLOR] + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"識別/許容範囲  :", Fore.CYAN + str(GRABZONE) + "x" + str(GRABZONE) +"|"+str(TOLERANCE)+ Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX+"反応速度       :", Fore.CYAN + str(bot.last_reac) + Style.RESET_ALL + " ms ("+str((bot.last_reac)/(GRABZONE*GRABZONE))+"ms/pix)")
    
    print(Fore.MAGENTA+"========================")
    print(Fore.CYAN + "Created by Nottei \n " + "          ver: 2.1")
if __name__ == '__main__':
    #config読み込み
    LoadConfig()
    bot = notteiBot()
    print_banner(bot) 
    while True:
        if is_pressed(SWITCH_KEY): #武器切り替え
            bot.switch() 
            print_banner(bot) 
            time.sleep(0.3)
            continue
        if is_pressed(GRABZONE_KEY_UP): #判定上げ
            if GRABZONE <10:
                GRABZONE += 1   
                print_banner(bot) 
            time.sleep(0.3)
            continue
        if is_pressed(GRABZONE_KEY_DOWN):#判定下げ
            if GRABZONE >1:
                GRABZONE -= 1    
                print_banner(bot)   
            time.sleep(0.3)   
            continue
        if is_pressed(TRIGGER_KEY): #切り替え
            bot.toggle()
            print_banner(bot) 
            time.sleep(0.3)
            continue
        if is_pressed(BUNNY_KEY): #バニホ
            bot.bunnyy()       
            print_banner(bot)  
            time.sleep(0.3)
            continue
        if is_pressed(COLOR_CHANGE_KEY): #色変え
            if COLOR !=2:COLOR+=1
            else:COLOR =0  
            print_banner(bot) 
            time.sleep(0.3)
            continue
        if is_pressed(HOLD_KEY): #切り替え
            bot.scan()
            time.sleep(0.3)
            continue
        if is_pressed("F10"):
            SaveConfig()
            time.sleep(10)
            continue
        if bot.toggled: 
            bot.scan()
        if bot._bunny:
            if is_pressed("space"): 
                bot.bunny()
        time.sleep(0.0025)