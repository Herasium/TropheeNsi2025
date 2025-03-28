import ctypes as ct
import winsound

class Popup():
    def __init__(self,text,title,icon):
        self.text = text
        self.title = title

        self.user32 = ct.WinDLL('user32', use_last_error=True)
        self.MessageBox = self.user32.MessageBoxW

        if icon == 0:
            self.MessageBox(0,self.text, self.title,0x000020000)
        if icon == 1:
            self.MessageBox(0,self.text, self.title,0x000020010)
        if icon == 2:
            self.MessageBox(0,self.text, self.title,0x000020020)
        if icon == 3:
            self.MessageBox(0,self.text, self.title,0x000020030)
        if icon == 4:
            self.MessageBox(0,self.text, self.title,0x000020040)
   

