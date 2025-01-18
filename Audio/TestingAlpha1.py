import pyaudio
import wave
import keyboard  
import logging
import threading
import time
import speech_recognition as sr
from os import path
import numpy as np
import sounddevice as sd
import wave
import io
import win32api, win32con, win32gui, win32ui


import pyautogui
import cv2
import pytesseract
import numpy as np
import time
from pytesseract import Output


p = pyaudio.PyAudio()


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44000
CHUNK = 1048
RECORD_SECONDS = 5

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'  

for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    pass

device_id =4
device_info = p.get_device_info_by_index(device_id)
channels = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
# https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
stream = p.open(format=FORMAT,
                channels=channels,
                rate=int(device_info["defaultSampleRate"]),
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_info["index"],
                as_loopback=True
                )

r = sr.Recognizer()
Transfer_frames = bytearray()
i=0
texto="place"
font_size = 20
h_wnd = ""
translateFlag = 0
arr=[]
h_handle = 0
frames = bytearray()
   
def processChunk(process_frames):

    wav_file = io.BytesIO()
    wav_writer = wave.open(wav_file, "wb")
    wav_writer.setframerate(RATE)
    wav_writer.setsampwidth(2)
    wav_writer.setnchannels(2)
    wav_writer.writeframes(process_frames)
    wav_file.seek(0)


    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)  
         
    
    text = r.recognize_google(audio,language="en-US")
    return text



def createWindow():
    hInstance = win32api.GetModuleHandle()
    className = 'MyWindowClassName'

    wndClass                = win32gui.WNDCLASS()
    wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc    = wndProc
    wndClass.hInstance      = hInstance
    wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName  = className
    wndClassAtom = win32gui.RegisterClass(wndClass)

    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

    style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

    hWindow = win32gui.CreateWindowEx(
        exStyle,
        wndClassAtom,
        None, # WindowName
        style,
        0, # x
        0, # y
        win32api.GetSystemMetrics(win32con.SM_CXSCREEN), # width
        win32api.GetSystemMetrics(win32con.SM_CYSCREEN), # height
        None, # hWndParent
        None, # hMenu
        hInstance,
        None # lpParam
    )
   
    win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)


    win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

    win32gui.PumpMessages()



def wndProc(hWnd, message, wParam, lParam):
    if message == win32con.WM_PAINT:

        hdc, paintStruct = win32gui.BeginPaint(hWnd)
        global h_handle 
        global h_wnd
        h_wnd = hWnd
        h_handle = hdc
        dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
        fontSize = arr[5]

        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Times New Roman"
        lf.lfHeight = int(round(dpiScale * fontSize))

        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hdc, hf)
        win32gui.SetBkColor(hdc, win32api.RGB(0,255,0))
        win32gui.SetBkMode(hdc, win32con.OPAQUE)
        print(len(arr))
        for i in range(0,int(len(arr)/6)):

            win32gui.DrawText(
                hdc,
                arr[4+ i*6],
                -1,
                (arr[0 + i*6],arr[1+ i*6],arr[2+ i*6],arr[3+ i*6]),
                win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
            )
    


        
        win32gui.EndPaint(hWnd, paintStruct)
        return 0

    elif message == win32con.WM_DESTROY:
        print ("Closing the window")
        win32gui.PostQuitMessage(0)
        return 0

    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)


def processAndDisplay(frames):
    texto= processChunk(frames)
    global arr
    arr = [1000,1000,900,1000,str(texto),font_size]
    
    win32gui.RedrawWindow(h_wnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    



def translateImage():
    global translateFlag
    translateFlag=1
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  

    data = pytesseract.image_to_data(image, output_type='dict')
    global arr

    boxes = len(data['level'])
    #print(data)

    for i in range(boxes ):
        if ( data['text'][i].isalpha() and float(data['conf'][i]) > 70 and len(data['text'][i]) > 1):
            texto = data['text'][i]
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

            #Draw box        
            arr.append(x)
            arr.append(y)
            arr.append(x+w)
            arr.append(y+h)
            arr.append(data['text'])
            arr.append(font_size)

    win32gui.RedrawWindow(h_wnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)

    translateFlag = 0


if __name__ == "__main__":

    arr = [1000,1000,900,1000,str(texto),font_size]

    threading.Thread(target= createWindow).start()
    for i in range(0,RATE):
        data = stream.read(CHUNK)
        frames.extend(data)  
        if i % 200 == 0 and i > 1:

            threading.Thread(target= processAndDisplay ,args=(frames,)).start()
            frames = bytearray()

        if keyboard.is_pressed("p") and translateFlag == 0:
            threading.Thread(target=translateImage).start()

            print("comecou")
            # tirar foto



    

            


 



