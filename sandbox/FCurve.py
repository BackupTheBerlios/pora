
#
# $Id: FCurve.py,v 1.1 2006/07/12 15:21:48 lightdruid Exp $
#

import sys
import wx

class FCurve(wx.PyControl):
    def __init__(self, parent):
        wx.PyControl.__init__(self, parent, -1, style = wx.BORDER_NONE)


class TopFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
            pos=(350, 750), size=(350, 200))

        p = wx.ScrolledWindow(self, -1, (0, 0), style = wx.SUNKEN_BORDER)


def main(args = []):
    class NanoApp(wx.App):
        def OnInit(self):
            frame = TopFrame(None, "")
            self.SetTopWindow(frame)
            frame.Show(True)
            return True

    wx.InitAllImageHandlers()
    app = NanoApp(redirect = False)
    app.MainLoop()

if __name__ == '__main__':
    main(sys.argv[1:])



