import win32api
import win32con
import win32gui
import time
import threading
from collections import deque



messagePrompt = ' :'
userAndMessage = deque()

def queue(message):
    userAndMessage.append(message)

def getQueue():
    return userAndMessage

def dequeue():
    return userAndMessage.popleft()

def cleanMessage(message):
    return message.split("\r\n")[0]

def showMessages():
    return userAndMessage[0] + "\n" + userAndMessage[1] + "\n" + userAndMessage[2] + "\n" + userAndMessage[3] + "\n" + userAndMessage[4]


#Code example modified from:
#Christophe Keller
#Hello World in Python using Win32

# New code: Define globaL
def main():
    #get instance handle
    hInstance = win32api.GetModuleHandle()
    # the class name
    className = 'SimpleWin32'

    # create and initialize window class
    wndClass                = win32gui.WNDCLASS()
    wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc    = wndProc
    wndClass.hInstance      = hInstance
    wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName  = className

    # register window class
    wndClassAtom = None
    try:
        wndClassAtom = win32gui.RegisterClass(wndClass)
    except Exception as e:
        print (e)
        raise e

    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

    hWindow = win32gui.CreateWindowEx(
        exStyle,
        wndClassAtom,
        None, # WindowName
        style,
        20, # x
        900, # y
        1920, # width
        600, # height
        None, # hWndParent
        None, # hMenu
        hInstance,
        None # lpParam
    )

    # Show & update the window
    win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, 
win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
    win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
win32con.SWP_SHOWWINDOW)

    win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
    win32gui.UpdateWindow(hWindow)

    thr = threading.Thread(target=customDraw, args=(hWindow,))
    thr.setDaemon(False)
    thr.start()

    # Dispatch messages
    win32gui.PumpMessages()

def customDraw(hWindow):
    win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE | 
win32con.RDW_ERASE)



queue(("Dave: ", "Daves message was important"))
queue(("Chris: ", "Chris is asleep again"))
queue(("Suzy: ", "Suzy has had way to much cake"))
queue(("Sarah: ", "Sarah is shockingly beautiful"))
queue(("Steve: ", "Steve likes to eat dog treats")) 


def wndProc(hWnd, message, wParam, lParam):
    textFormat = win32con.DT_NOCLIP | win32con.DT_VCENTER | win32con.DT_EXPANDTABS
    if message == win32con.WM_PAINT:
        hDC, paintStruct = win32gui.BeginPaint(hWnd)
        fontSize = 20

        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Times New Roman"
        lf.lfHeight = fontSize
        lf.lfWeight = 300

        lf.lfQuality = win32con.NONANTIALIASED_QUALITY
        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hDC, hf)

        if len(userAndMessage) > 4:
            win32gui.SetTextColor(hDC,win32api.RGB(255,0,0))
            rect = win32gui.GetClientRect(hWnd)
            drawRect = win32gui.DrawText(hDC,userAndMessage[0][0],-1, rect, 
win32con.DT_CALCRECT); 
            win32gui.DrawText(hDC, userAndMessage[0][0], -1, rect, textFormat)

            win32gui.SetTextColor(hDC,win32api.RGB(240,240,240))
            drawrect = win32gui.DrawText(hDC, userAndMessage[0][1], -1, rect, 
win32con.DT_CALCRECT);
            rect = (drawRect[1][0] + drawRect[1][2], drawRect[1][1], drawRect[1][2], 
drawRect[1][3])
            win32gui.DrawText(hDC, userAndMessage[0][1], -1, rect, textFormat)


#####################################################################################
            win32gui.SetTextColor(hDC,win32api.RGB(255,0,0))
            rect = (0, drawRect[1][1] + drawRect[1][3], drawRect[1][2], drawRect[1] 
[3])
            drawRect = win32gui.DrawText(hDC,userAndMessage[1][0],-1, rect, 
win32con.DT_CALCRECT); 
            win32gui.DrawText(hDC, userAndMessage[1][0], -1, rect, textFormat)

            win32gui.SetTextColor(hDC,win32api.RGB(240,240,240))
            drawrect = win32gui.DrawText(hDC, userAndMessage[1][1], -1, rect, 
win32con.DT_CALCRECT);
            rect = (drawRect[1][0] + drawRect[1][2], drawRect[1][1], drawRect[1][2], 
drawRect[1][3])
            win32gui.DrawText(hDC, userAndMessage[1][1], -1, rect, textFormat)


#####################################################################################
            win32gui.SetTextColor(hDC,win32api.RGB(255,0,0))
            rect = (0, drawRect[1][1] + (drawRect[1][3] // 2), drawRect[1][2], 
drawRect[1][3])
            drawRect = win32gui.DrawText(hDC,userAndMessage[2][0],-1, rect, 
win32con.DT_CALCRECT); 
            win32gui.DrawText(hDC, userAndMessage[2][0], -1, rect, textFormat)

            win32gui.SetTextColor(hDC,win32api.RGB(240,240,240))
            drawrect = win32gui.DrawText(hDC, userAndMessage[2][1], -1, rect, 
win32con.DT_CALCRECT)
            rect = (drawRect[1][0] + drawRect[1][2], drawRect[1][1], drawRect[1][2], 
drawRect[1][3])
            win32gui.DrawText(hDC, userAndMessage[2][1], -1, rect, textFormat)

        #####################################################################################
            win32gui.SetTextColor(hDC,win32api.RGB(255,0,0))
            rect = (0, drawRect[1][1] + (drawRect[1][3] // 3), drawRect[1][2], 
drawRect[1][3])
            drawRect = win32gui.DrawText(hDC,userAndMessage[3][0],-1, rect, 
win32con.DT_CALCRECT); 
            win32gui.DrawText(hDC, userAndMessage[3][0], -1, rect, textFormat)

            win32gui.SetTextColor(hDC,win32api.RGB(240,240,240))
            drawrect = win32gui.DrawText(hDC, userAndMessage[3][1], -1, rect, 
win32con.DT_CALCRECT);
            rect = (drawRect[1][0] + drawRect[1][2], drawRect[1][1], drawRect[1][2], 
drawRect[1][3])
            win32gui.DrawText(hDC, userAndMessage[3][1], -1, rect, textFormat)


#####################################################################################
            win32gui.SetTextColor(hDC,win32api.RGB(255,0,0))
            rect = (0, drawRect[1][1] + (drawRect[1][3] // 4), drawRect[1][2], 
drawRect[1][3])
            drawRect = win32gui.DrawText(hDC,userAndMessage[4][0],-1, rect, 
win32con.DT_CALCRECT); 
            win32gui.DrawText(hDC, userAndMessage[4][0], -1, rect, textFormat)

            win32gui.SetTextColor(hDC,win32api.RGB(240,240,240))
            drawrect = win32gui.DrawText(hDC, userAndMessage[4][1], -1, rect, 
win32con.DT_CALCRECT);
            rect = (drawRect[1][0] + drawRect[1][2], drawRect[1][1], drawRect[1][2], 
drawRect[1][3])
            win32gui.DrawText(hDC, userAndMessage[4][1], -1, rect, textFormat)

            win32gui.EndPaint(hWnd, paintStruct)
            return 0

    elif message == win32con.WM_DESTROY:
        print('Being destroyed')
        win32gui.PostQuitMessage(0)
        return 0

    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

if __name__ == '__main__':
    main()