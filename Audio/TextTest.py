from turtle import right
import win32api, win32con, win32gui, win32ui

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


def createMessage(hdc,left,bottom,right,top,text):

    win32gui.DrawText(
        hdc,
        text,
        -1,
        (left,bottom,right,top),
        win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
    )



def wndProc(hWnd, message, wParam, lParam):
    if message == win32con.WM_PAINT:

        hdc, paintStruct = win32gui.BeginPaint(hWnd)

        dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
        fontSize = 80

        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Times New Roman"
        lf.lfHeight = int(round(dpiScale * fontSize))
        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hdc, hf)
        win32gui.SetBkColor(hdc, win32api.RGB(200,0,0))
        win32gui.SetBkMode(hdc, win32con.OPAQUE)

        for i in range(0,n_words):
            print(arr[4 + i * 5])
            createMessage(hdc,arr[0 + i * 5],arr[1 + i * 5],arr[2 + i * 5],arr[3 + i * 5],arr[4 + i * 5])
        
        win32gui.EndPaint(hWnd, paintStruct)
        
        return 0

    elif message == win32con.WM_DESTROY:
        print ("Closing the window")
        win32gui.PostQuitMessage(0)
        return 0

    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)



if __name__ == '__main__':

    n_words=2

    arr = [500,400,100,100,"text", 600,400,400,300,"loo"]

    createWindow()

