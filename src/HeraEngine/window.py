from __future__ import unicode_literals
import sys
import ctypes as ct
import ctypes.wintypes as w
import time
import threading
from HeraEngine.types.Vec2 import Vec2


def MAKEINTRESOURCE(x):
    return w.LPCWSTR(x)

CW_USEDEFAULT = ct.c_int(0x80000000).value
IDI_APPLICATION = MAKEINTRESOURCE(32512)



CS_HREDRAW = 2
CS_VREDRAW = 1
IDC_ARROW = MAKEINTRESOURCE(32512)
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

#Windows messages, used for having mouse position and keys and stuff
WM_PAINT        = 15
WM_DESTROY      = 0x0002
WM_CLOSE        = 0x0010
WM_QUIT         = 0x0012
WM_MOUSEMOVE    = 0x0200
WM_KEYDOWN      = 0x0100
WM_KEYUP        = 0x0101
WM_CHAR         = 0x0102
WM_RBUTTONDOWN  = 0x0204
WM_LBUTTONDOWN  = 0x0201

#Windows types, useful for fullscreen
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_THICKFRAME = 0x00040000
WS_MAXIMIZEBOX = 0x00010000
WS_POPUP       = 0x80000000
WS_NOT_RESIZABLE =  WS_OVERLAPPEDWINDOW & ~(WS_THICKFRAME | WS_MAXIMIZEBOX)

SM_CXSCREEN    = 0 
SM_CYSCREEN    = 1

LRESULT = ct.c_int64
HCURSOR = ct.c_void_p
WNDPROC = ct.WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)

class WNDCLASS(ct.Structure):
    _fields_ = (('style', w.UINT),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', ct.c_int),
                ('cbWndExtra', ct.c_int),
                ('hInstance', w.HINSTANCE),
                ('hIcon', w.HICON),
                ('hCursor', HCURSOR),
                ('hbrBackground', w.HBRUSH),
                ('lpszMenuName', w.LPCWSTR),
                ('lpszClassName', w.LPCWSTR))

class PAINTSTRUCT(ct.Structure):
    _fields_ = (('hdc', w.HDC),
                ('fErase', w.BOOL),
                ('rcPaint', w.RECT),
                ('fRestore', w.BOOL),
                ('fIncUpdate', w.BOOL),
                ('rgbReserved', w.BYTE * 32))

class BITMAPINFOHEADER(ct.Structure):
    _fields_ = [
        ("biSize", w.DWORD),
        ("biWidth", ct.c_long),
        ("biHeight", ct.c_long),
        ("biPlanes", w.WORD),
        ("biBitCount", w.WORD),
        ("biCompression", w.DWORD),
        ("biSizeImage", w.DWORD),
        ("biXPelsPerMeter", ct.c_long),
        ("biYPelsPerMeter", ct.c_long),
        ("biClrUsed", w.DWORD),
        ("biClrImportant", w.DWORD),
    ]

class RGBQUAD(ct.Structure):
    _fields_ = [
        ("rgbBlue", w.BYTE),
        ("rgbGreen", w.BYTE),
        ("rgbRed", w.BYTE),
        ("rgbReserved", w.BYTE),
    ]

class RECT(ct.Structure):
    _fields_ = [
        ("left", ct.c_long),
        ("top", ct.c_long),
        ("right", ct.c_long),
        ("bottom", ct.c_long),
    ]

class BITMAPINFO(ct.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1),  
    ]




class Window():
    def __init__(self,core,size,cursor,keyboard):
        self.core = core
        self.keyboard = keyboard
        self.cursor = cursor

        self.kernel32 = ct.WinDLL('kernel32', use_last_error=True)
        self.GetModuleHandle = self.kernel32.GetModuleHandleW
        self.GetModuleHandle.argtypes = w.LPCWSTR,
        self.GetModuleHandle.restype = w.HMODULE
        self.GetModuleHandle.errcheck = self.errcheck

        self.user32 = ct.WinDLL('user32', use_last_error=True)
        self.CreateWindowEx = self.user32.CreateWindowExW
        self.CreateWindowEx.argtypes = w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD, ct.c_int, ct.c_int, ct.c_int, ct.c_int, w.HWND, w.HMENU, w.HINSTANCE, w.LPVOID
        self.CreateWindowEx.restype = w.HWND
        self.CreateWindowEx.errcheck = self.errcheck
        self.LoadIcon = self.user32.LoadIconW
        self.LoadIcon.argtypes = w.HINSTANCE, w.LPCWSTR
        self.LoadIcon.restype = w.HICON
        self.LoadIcon.errcheck = self.errcheck
        self.LoadCursor = self.user32.LoadCursorW
        self.LoadCursor.argtypes = w.HINSTANCE, w.LPCWSTR
        self.LoadCursor.restype = HCURSOR
        self.LoadCursor.errcheck = self.errcheck
        self.RegisterClass = self.user32.RegisterClassW
        self.RegisterClass.argtypes = ct.POINTER(WNDCLASS),
        self.RegisterClass.restype = w.ATOM
        self.RegisterClass.errcheck = self.errcheck
        self.ShowWindow = self.user32.ShowWindow
        self.ShowWindow.argtypes = w.HWND, ct.c_int
        self.ShowWindow.restype = w.BOOL
        self.UpdateWindow = self.user32.UpdateWindow
        self.UpdateWindow.argtypes = w.HWND,
        self.UpdateWindow.restype = w.BOOL
        self.UpdateWindow.errcheck = self.errcheck
        self.GetMessage = self.user32.GetMessageW
        self.GetMessage.argtypes = ct.POINTER(w.MSG), w.HWND, w.UINT, w.UINT
        self.GetMessage.restype = w.BOOL
        self.GetMessage.errcheck = self.minusonecheck
        self.TranslateMessage = self.user32.TranslateMessage
        self.TranslateMessage.argtypes = ct.POINTER(w.MSG),
        self.TranslateMessage.restype = w.BOOL
        self.DispatchMessage = self.user32.DispatchMessageW
        self.DispatchMessage.argtypes = ct.POINTER(w.MSG),
        self.DispatchMessage.restype = LRESULT
        self.BeginPaint = self.user32.BeginPaint
        self.BeginPaint.argtypes = w.HWND, ct.POINTER(PAINTSTRUCT)
        self.BeginPaint.restype = w.HDC
        self.GetClientRect = self.user32.GetClientRect
        self.GetClientRect.argtypes = w.HWND, ct.POINTER(w.RECT)
        self.GetClientRect.restype = w.BOOL
        self.GetClientRect.errcheck = self.errcheck
        self.EndPaint = self.user32.EndPaint
        self.EndPaint.argtypes = w.HWND, ct.POINTER(PAINTSTRUCT)
        self.EndPaint.restype = w.BOOL
        self.PostQuitMessage = self.user32.PostQuitMessage
        self.PostQuitMessage.argtypes = ct.c_int,
        self.PostQuitMessage.restype = None
        self.DefWindowProc = self.user32.DefWindowProcW
        self.DefWindowProc.argtypes = w.HWND, w.UINT, w.WPARAM, w.LPARAM
        self.DefWindowProc.restype = LRESULT

        self.SetWindowPos = self.user32.SetWindowPos
        self.SetWindowPos.argtypes = w.HWND, w.HWND, ct.c_int, ct.c_int, ct.c_int, ct.c_int, w.UINT
        self.SetWindowPos.restype = w.BOOL

        self.gdi32 = ct.WinDLL('gdi32', use_last_error=True)
        self.SetPixel = self.gdi32.SetPixel
        self.SetPixel.argtypes = w.HDC, ct.c_int, ct.c_int, w.COLORREF
        self.SetPixel.restype = w.COLORREF
        self.GetStockObject = self.gdi32.GetStockObject
        self.GetStockObject.argtypes = ct.c_int,
        self.GetStockObject.restype = w.HGDIOBJ

        self.Title = "Default Window"
        self.Size = size
        self.past_size = None
        self.fullscreen = False
        self.ready = False
        self.kill = False

    def errcheck(self, result, func, args):
        if result is None or result == 0:
            a = ct.get_last_error()
            raise ct.WinError(a)
        return result

    def minusonecheck(self, result, func, args):
        if result == -1:
            a = ct.get_last_error()
            raise ct.WinError(a)
        return result

    def WndProc(self, hwnd, message, wParam, lParam):
        ps = PAINTSTRUCT()
        rect = w.RECT()

        if message == WM_PAINT:
            hdc = self.BeginPaint(hwnd, ct.byref(ps))
            self.GetClientRect(hwnd, ct.byref(rect))
            self.EndPaint(hwnd, ct.byref(ps))
            return 0
        elif message == WM_DESTROY:
            self.PostQuitMessage(0)
            return 0
        elif message == WM_KEYDOWN:
            self.keyboard.window_register_action("vk_key_down",keycode=wParam)
            return 0
        elif message == WM_KEYUP:
            return 0
        elif message == WM_CHAR:
            char = chr(wParam)
            return 0
        elif message == WM_MOUSEMOVE:
            x = ct.c_short(lParam & 0xffff).value
            y = ct.c_short((lParam >> 16) & 0xffff).value
            self.cursor.window_register_action("move",x=x,y=y)

            return 0

        elif message == WM_RBUTTONDOWN:
            self.cursor.window_register_action("rbuttondown")

            return 0
        
        elif message == WM_LBUTTONDOWN:
            self.cursor.window_register_action("lbuttondown")

            return 0

        return self.DefWindowProc(hwnd, message, wParam, lParam)

    def SetPixelColor(self, x, y, color):
        if self.ready:
            self.buffer[int(y * self.Size.x + x)] = color 
            

    def GetFullscreenSize(self):
        return self.user32.GetSystemMetrics(SM_CXSCREEN),self.user32.GetSystemMetrics(SM_CYSCREEN)

    def SetWindowSize(self, size):
        if not isinstance(size,Vec2):
            raise TypeError("Window size must be a Vec2")
        self.Size = size

    def clear_buffer(self):
        if self.ready:
            self.buffer = (ct.c_uint32 * (self.Size.y*self.Size.x))()



    def update(self):
        if not self.ready:
            return
        
        if self.past_size != self.Size and not self.fullscreen:
            self.past_size = self.Size
            self.SetWindowPos(self.hwnd, None, 0, 0, self.Size.y+16, self.Size.x+39, 0)

        hdc = self.user32.GetDC(self.hwnd)
        hdc_mem = self.gdi32.CreateCompatibleDC(hdc)

        rect = w.RECT()
        self.GetClientRect(self.hwnd, ct.byref(rect))
        width = rect.right
        height = rect.bottom

        bitmap_info = BITMAPINFO()
        bitmap_info.bmiHeader.biSize = ct.sizeof(BITMAPINFOHEADER)
        bitmap_info.bmiHeader.biWidth = width
        bitmap_info.bmiHeader.biHeight = -height 
        bitmap_info.bmiHeader.biPlanes = 1
        bitmap_info.bmiHeader.biBitCount = 32  
        bitmap_info.bmiHeader.biCompression = 0 
        bitmap_info.bmiHeader.biSizeImage = 0
        bitmap_info.bmiHeader.biXPelsPerMeter = 0
        bitmap_info.bmiHeader.biYPelsPerMeter = 0
        bitmap_info.bmiHeader.biClrUsed = 0
        bitmap_info.bmiHeader.biClrImportant = 0

        pixel_data = ct.POINTER(ct.c_uint32)()
        hbm_mem = self.gdi32.CreateDIBSection(hdc, ct.byref(bitmap_info), 0, ct.byref(pixel_data), None, 0)

        self.gdi32.SelectObject(hdc_mem, hbm_mem)

        ct.memmove(pixel_data, self.buffer, len(self.buffer) * ct.sizeof(ct.c_uint32))


        self.gdi32.BitBlt(hdc, 0, 0, width, height, hdc_mem, 0, 0, 0x00CC0020)
        self.user32.ReleaseDC(self.hwnd, hdc)

        self.gdi32.DeleteObject(hbm_mem)
        self.gdi32.DeleteDC(hdc_mem)

    def keep_alive(self,msg):
        while self.GetMessage(ct.byref(msg), None, 0, 0) != 0 and not self.kill:
            self.TranslateMessage(ct.byref(msg))
            self.DispatchMessage(ct.byref(msg))


    def MainWin(self):
        self.wndclass = WNDCLASS()
        self.wndclass.style         = CS_HREDRAW | CS_VREDRAW
        self.wndclass.lpfnWndProc   = WNDPROC(self.WndProc)
        self.wndclass.cbClsExtra    = 0
        self.wndclass.cbWndExtra    = 0
        self.wndclass.hInstance     = self.GetModuleHandle(None)
        self.wndclass.hIcon         = self.LoadIcon(None, IDI_APPLICATION)
        self.wndclass.hCursor       = self.LoadCursor(None, IDC_ARROW)
        self.wndclass.hbrBackground = self.GetStockObject(WHITE_BRUSH)
        self.wndclass.lpszMenuName  = None
        self.wndclass.lpszClassName = 'Window'

        self.RegisterClass(ct.byref(self.wndclass))

        self.hwnd = self.CreateWindowEx(0,
                            self.wndclass.lpszClassName,
                            self.Title,
                            WS_POPUP if self.fullscreen else WS_NOT_RESIZABLE,
                            CW_USEDEFAULT,
                            CW_USEDEFAULT,
                            CW_USEDEFAULT,
                            CW_USEDEFAULT,
                            None,
                            None,
                            self.wndclass.hInstance,
                            None)

        if self.fullscreen:
            self.SetWindowPos(self.hwnd, None, 0, 0,
                            self.user32.GetSystemMetrics(SM_CXSCREEN),
                            self.user32.GetSystemMetrics(SM_CYSCREEN),
                            0)
            
            self.Size = Vec2(*self.GetFullscreenSize())
        self.buffer = (ct.c_uint32 * (self.Size.x*self.Size.y))()

        self.user32.ShowWindow(self.hwnd, SW_SHOWNORMAL)
        self.user32.UpdateWindow(self.hwnd)
        msg = w.MSG()
        self.ready = True
        self.keep_alive(msg)
        
        return msg.wParam

