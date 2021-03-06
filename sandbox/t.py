import wx

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Am I transparent?")
        self.amount = 255
        self.delta = -1

        p = wx.Panel(self)
        self.st = wx.StaticText(p, -1, str(self.amount), (25,25))
        self.st.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.timer = wx.Timer(self)
        self.timer.Start(1)
        self.Bind(wx.EVT_TIMER, self.AlphaCycle)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def AlphaCycle(self, evt):
        self.amount += self.delta
        if self.amount == 0 or self.amount == 255:
            self.delta = -self.delta
        self.MakeTransparent(self.amount)
        self.st.SetLabel(str(self.amount))


    def OnCloseWindow(self, evt):
        self.timer.Stop()
        del self.timer
        self.Destroy()


    def MakeTransparent(self, amount):
        hwnd = self.GetHandle()
        try:
            import ctypes
            _winlib = ctypes.windll.user32
            style = _winlib.GetWindowLongA(hwnd, 0xffffffecL)
            style |= 0x00080000
            _winlib.SetWindowLongA(hwnd, 0xffffffecL, style)
            _winlib.SetLayeredWindowAttributes(hwnd, 0, amount, 2)

        except ImportError:
            import win32api, win32con, winxpgui
            _winlib = win32api.LoadLibrary("user32")
            pSetLayeredWindowAttributes = win32api.GetProcAddress(
                _winlib, "SetLayeredWindowAttributes")
            if pSetLayeredWindowAttributes == None:
                return
            exstyle = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if 0 == (exstyle & 0x80000):
                win32api.SetWindowLong(hwnd,
                                       win32con.GWL_EXSTYLE,
                                       exstyle | 0x80000)
            winxpgui.SetLayeredWindowAttributes(hwnd, 0, amount, 2)



app = wx.App(False)
frm = Frame()
frm.Show()
app.MainLoop()