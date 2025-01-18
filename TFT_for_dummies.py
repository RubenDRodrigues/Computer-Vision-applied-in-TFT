from tabnanny import check
from tracemalloc import start
from turtle import width
import pyautogui
import cv2
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
import time
from pytesseract import Output
from skimage.metrics import structural_similarity

width=1920
height=1080
target_champions = [ "Vladimir", "Varus", "Nami", "Skarner", "Aurelion", "Illaoi", "Nidalee"]
target_positions = [ [0,1], [4,0], [4,6], [4,1], [4,7], [0,6], [0,3]  ]
target_locations = []
target_items = [["Shojin"] ]
for i in target_positions:
    target_locations.append( [i[0] * 50 + 300, i[1] * 50 + 1000 ]   )
    
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  
#image = cv2.imread("test.png")

#realtime
#image = pyautogui.screenshot()


# Stretch
# scale_percent = 100 # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# resize image
# resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def whiteOnly(image):
    lower = np.array([160,160,160])  #-- Lower range --
    upper = np.array([255,255,255])  #-- Upper range --
    mask = cv2.inRange(image, lower, upper)
    res = cv2.bitwise_and(image, image, mask= mask)  #-- Contains pixels having the gray color--
    return res

def RollOrLevel():
    return 1

def clickRoll():
    pyautogui.typewrite("f")
   #refresh_coords = (350, 1050) 
    #pyautogui.click(refresh_coords)
    #pyautogui.mouseDown(); 
    #pyautogui.mouseUp()

def clickLevel():
    pyautogui.typewrite("d")
    #level_coords = (350, 950) 
    #pyautogui.click(level_coords)
    #pyautogui.mouseDown(); 
    #pyautogui.mouseUp()

def checkGold(image):
    gold_image = whiteOnly(image[850:930, 850:950])
    gold_value = pytesseract.image_to_string(gold_image)
    print("Ouro Atual: " + gold_value)
    return gold_value


def sell_champ_at(x,y):
    pyautogui.moveTo(x,y)
    pyautogui.press("e")

#Arrastar Champs
def checkBench():
    fixedBorder = width * 0.21
    currentY = height *3/4
    space_between_champ = (width-fixedBorder*2)/9
    index=0
    champIndex= 0 # Nao uses isto

    for i in range(0,9):

        currentX = fixedBorder + i * space_between_champ
        pyautogui.click(currentX, currentY-30)
        pyautogui.mouseDown()
        pyautogui.mouseUp()

        time.sleep(0.1)

        #tirar Foto
        bench_champ_image = pyautogui.screenshot()
        bench_champ_image = cv2.cvtColor(np.array(bench_champ_image), cv2.COLOR_RGB2BGR)        
           

        champ_details_image = bench_champ_image[int(currentY)-100:int(currentY)+100, int(currentX)-100:int(currentX)+400]
        #cv2.imwrite("frame.jpg", champ_details_image)
        #time.sleep(6)
        champ_details = pytesseract.image_to_data(champ_details_image, output_type=Output.DICT)

        print(champ_details['text'])
        for champ in champ_details['text']:
            if(champ in target_champions): 
                champIndex = target_champions.index(champ)
                target_location = target_locations[champIndex]
                dragTo(currentX,currentY,target_location)
            else: 
                sell_champ_at(currentX,currentY)
                  
        index=index+1


def dragTo(x_from, y_from, x_to, y_to):
    pyautogui.moveTo(x_from,y_from)
    pyautogui.click()  
    pyautogui.moveTo(x_to,y_to)
    pyautogui.click()
    pyautogui.mouseDown()  
    pyautogui.mouseUp()  


def findBench(large_image):
    method = cv2.TM_SQDIFF_NORMED
    # Read the images from the file
    small_image = cv2.imread('BenchSide.png')
    result = cv2.matchTemplate(small_image, large_image, method)
    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc
    return MPy

def checkItems(image):
    image = image[700:1030, 0:300]


#Detetar Champs e comprar
def BuyChamps(image):
    champs_image = whiteOnly(image[1030:, 0:])
    champs_data = pytesseract.image_to_data(champs_image, output_type=Output.DICT)
    index=0
    print(champs_data)
    for i in champs_data['text']:
        if i == "" or i == " ":
            index=index+1
            continue
        for target_champion in target_champions:
            if (target_champion in i):
                left = champs_data['left'][index]
                top = champs_data['top'][index] 
                print(top)
                pyautogui.click(left + 30, height - 50,clicks=5,interval=0.25)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                champs_bought = champs_bought + 1
                
        index=index+1

def sell_field(image):
    for i in range(1,9):
        for j in range(1,5):
            x = 400 + i * 100
            y = 300 + j * 90
            sell_champ_at(x,y)

def checkCurrentLevel(image):
    image = image[20:80,730:830]
    cv2.imwrite("lol.png",image)
    current_round = pytesseract.image_to_string(image)
    print("nivel Atual: " + current_round)

def choose_augment(image):
    
    pyautogui.click(800, 600,clicks=3,interval=0.1)


def buy_random_champ(image):

    pyautogui.click(400, 1030,clicks=5,interval=0.25)
    pyautogui.click(600, 1030,clicks=5,interval=0.25)
    pyautogui.click(800, 1030,clicks=5,interval=0.25)
    pyautogui.click(1000, 1030,clicks=5,interval=0.25)
    pyautogui.click(1200, 1030,clicks=5,interval=0.25)

    pyautogui.mouseDown()
    pyautogui.mouseUp()

current_round = ""
champs_bought = 0
while True:
    
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  
    
    #image = cv2.imread("test.jpg")

    #Ver nivel
    checkCurrentLevel(image)

    if "Choose your augment" in pytesseract.image_to_string(image):
        choose_augment(image)
    
    #ronda 1-3
    #time.sleep(100)

    if (current_round=="1-2"):
        sell_field(image)
    
    BuyChamps(image)

    gold = checkGold(image)
    #dragTo(700, 700, 600, 600)
    checkBench()
    clickRoll()





