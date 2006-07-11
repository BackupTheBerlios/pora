
import sys
import wx

#class FText(wx.EvtHandler):
class FText(wx.PyControl):
    def __init__(self, parent, x, y, text, textFont = None):
        wx.PyControl.__init__(self, parent, -1, style = wx.BORDER_NONE)

        self.x = x
        self.y = y
        self.text = text

        self.SetPosition((self.x, self.y))

        if textFont is None:
            self.textFont = wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL)
        else:
            self.textFont = textFont

        self.textBgColor1 = wx.TheColourDatabase.FindColour("BLACK")
        self.textBgColor2 = wx.TheColourDatabase.FindColour("GRAY")
        self.textColor = wx.TheColourDatabase.FindColour("WHITE")

        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self._CursorHand = wx.StockCursor(wx.CURSOR_HAND)

    def onMouseOver(self, flag):
        if flag:
            self.textColor = wx.TheColourDatabase.FindColour("ORANGE")
        else:
            self.textColor = wx.TheColourDatabase.FindColour("WHITE")
        self.Refresh(False)

    def OnMouseMove(self, evt):
        evt

    def OnMouseEvent(self, event):
        if event.Leaving():
            self.SetCursor(wx.NullCursor)
            self.onMouseOver(False)
        else:            
            self.SetCursor(self._CursorHand)
            self.onMouseOver(True)

    def OnMotion(self, evt):
        evt

    def OnSize(self, evt):
        #self.Refresh(False)
        evt.Skip()

    def OnPaint(self, event):
        pdc = wx.PaintDC(self)
        self.Draw(pdc)
        #print 'new paintz'

    #def OnDraw(self, evt):
    #    print 'OnDraw'

    def Draw(self, pdc):

        dc = wx.MemoryDC()
        maxWidth, maxHeight = dc.GetTextExtent(self.text)
        self.bmp = wx.EmptyBitmap(maxWidth + 100, maxHeight)
        dc.SelectObject(self.bmp)
        dc.Clear()
        dc.BeginDrawing()

        dc.SetFont(self.textFont)

        rect = self._Draw(dc)
        dc.EndDrawing()

        xstart = ystart = 0
        pdc.Blit(xstart, ystart, 300, 300, dc, xstart, ystart)

        #print dir(rect)
        #self.SetPosition( (self.x+100, self.y) )
        self.SetSize(rect.GetSize())

        return rect

    def _Draw(self, dc, textTrailer = 0, stripes = True):
        twidth, theight = dc.GetTextExtent(self.text)
        #print 'theight', theight

        self.x = 0
        self.y = 0

        x1 = self.x
        y1 = self.y

        x2 = self.x
        y2 = self.y

        xc = self.x
        yc = self.y + theight

        color1 = self.textBgColor1
        color2 = self.textBgColor2

        dc.SetPen(wx.TRANSPARENT_PEN)

        dc.SetPen(wx.Pen(self.textBgColor1, 1))
        dc.SetBrush(wx.Brush(self.textBgColor1))
        ht2 = theight / 2
        dc.DrawArc(x1+ht2, y1/2, x2+ht2, y2/2, xc+ht2, yc/2)

        rect = wx.Rect(x1+ht2, y1/2, twidth + (twidth / 5), theight + textTrailer)
        self.DrawHorizontalGradient(dc, rect, color1, color2)

        if stripes:
            color3 = wx.Color(255, 255, 255)
            ii_tmp = 0
            for ii in range(0, theight, 2):
                ii_tmp = ii
                rect = wx.Rect(x1 + twidth + (twidth / 5), (y1/2) + ii, 5, 2)
                #print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

                rect = wx.Rect(x1 + twidth + (twidth / 5), (y1/2) + ii, 15, 1)
                #print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

            while (y1/2) + ii_tmp + 2 < y1/2 + theight:
                #print "adjust", ii_tmp, theight
                rect = wx.Rect(x1 - 3 + twidth + (twidth / 5), (y1/2) + ii_tmp, 15, 1)
                #print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

                ii_tmp += 2


        color = self.textColor
        dc.SetTextForeground(color)

        dc.DrawText(self.text, xc+ht2, self.y/2)

        return wx.Rect(x1, y1, x1 - 3 + twidth + (twidth / 5) + 15, (y1/2) + ii_tmp + 3)

    def DrawHorizontalGradient(self, dc, rect, col1, col2):

        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)

        # calculate gradient coefficients
        #col2 = self._style.GetSecondColour()
        #col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.width)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0
        
        for x in range(rect.x, rect.x + rect.width):
            currCol = (r1 + rf, g1 + gf, b1 + bf)
                
            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(rect.x + (x - rect.x), rect.y, 1, rect.height)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep


class WGUI(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size = size,
                                  style = wx.SUNKEN_BORDER)
        self.SetBackgroundColour("WHITE")

        self.tile_narrow = 1
        self.tile_wide = 1
        self.maxWidth = 500
        self.maxHeight = 500

        self.ft = FText(self, 100, 54, 'asdasdasd')
        self.ft2 = FText(self, 10, 4, 'asdasdasd')

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        scrollRate = self.tile_narrow + self.tile_wide
        self.SetScrollRate(scrollRate, scrollRate)

        self.SetScrollbars(1, 1, self.maxWidth,
            self.maxHeight, yPos = 0)

        self.bmp = wx.EmptyBitmap(self.maxWidth, self.maxHeight)

        #self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.textBgColor1 = wx.TheColourDatabase.FindColour("BLACK")
        self.textBgColor2 = wx.TheColourDatabase.FindColour("GRAY")
        self.textColor = wx.TheColourDatabase.FindColour("WHITE")

    def OnPaint1(self, event):
        """ Handles The wx.EVT_PAINT Event For PieCtrl. """

        pdc = wx.PaintDC(self)
        #self.Draw(pdc)

    def Draw1(self, pdc):

        if 1:
            print 'paint new'
            #wx.ScrolledWindow.Draw(self, pdc)
            rect = self.ft.Draw(pdc)
            print rect
        else:
            print 'paint'
            dc = wx.MemoryDC()
            dc.SelectObject(self.bmp)
            dc.Clear()
            dc.BeginDrawing()

            dc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

            self.d(dc, 10,5,'asdasdasd')
            dc.EndDrawing()

            xstart, ystart = self.CalcUnscrolledPosition(0,0)
            pdc.Blit(xstart, ystart, 300, 300, dc, xstart, ystart)

    def d1(self, dc, x, y, text):
        twidth, theight = dc.GetTextExtent(text)

        #dc.DrawArc(20,20,40,20,20,30) 

        x1 = y1 = x2 = y2 = xc = yc = theight
        yc += yc

        # full
        #dc.DrawArc(20,20, 20,20, 20,30) 
        dc.DrawArc(x1, y1/2, x2, y2/2, xc, yc/2)
        dc.DrawText("abcd", xc / 2, y2 / 2)

    def DrawHorizontalGradient(self, dc, rect, col1, col2):

        if rect.height < 1 or rect.width < 1:
            return

        dc.SetPen(wx.TRANSPARENT_PEN)

        # calculate gradient coefficients
        #col2 = self._style.GetSecondColour()
        #col1 = self._style.GetFirstColour()

        r1, g1, b1 = int(col1.Red()), int(col1.Green()), int(col1.Blue())
        r2, g2, b2 = int(col2.Red()), int(col2.Green()), int(col2.Blue())

        flrect = float(rect.width)

        rstep = float((r2 - r1)) / flrect
        gstep = float((g2 - g1)) / flrect
        bstep = float((b2 - b1)) / flrect

        rf, gf, bf = 0, 0, 0
        
        for x in range(rect.x, rect.x + rect.width):
            currCol = (r1 + rf, g1 + gf, b1 + bf)
                
            dc.SetBrush(wx.Brush(currCol, wx.SOLID))
            dc.DrawRectangle(rect.x + (x - rect.x), rect.y, 1, rect.height)
            rf = rf + rstep
            gf = gf + gstep
            bf = bf + bstep


    def d2(self, dc, x, y, text, textTrailer = 0, stripes = True):
        twidth, theight = dc.GetTextExtent(text)

        x1 = y1 = x2 = y2 = xc = yc = theight
        yc += yc

        color1 = self.textBgColor1
        color2 = self.textBgColor2

        dc.SetPen(wx.TRANSPARENT_PEN)
        pc = wx.Color(color1.Red() + 30,color1.Green() + 30, color1.Blue() + 30)
        dc.SetBrush(wx.Brush(pc))
        #dc.DrawArc(x1-2, y1/2, x2-2, y2/2, xc - 2, yc/2)

        dc.SetPen(wx.Pen("black", 1))
        dc.SetBrush(wx.Brush("black"))
        dc.DrawArc(x1, y1/2, x2, y2/2, xc, yc/2)

        rect = wx.Rect(x1 - 3, y1/2, twidth, y1 + textTrailer)
        self.DrawHorizontalGradient(dc, rect, color1, color2)

        color = self.textColor
        dc.SetTextForeground(color)

        dc.DrawText(text, xc - (xc/3) + 1, y2 / 2 - 1)

    def d(self, dc, x, y, text, textTrailer = 0, stripes = True):
        twidth, theight = dc.GetTextExtent(text)

        x1 = x
        y1 = y

        x2 = x
        y2 = y

        xc = x
        yc = y + theight
        #yc += yc

        color1 = self.textBgColor1
        color2 = self.textBgColor2

        dc.SetPen(wx.TRANSPARENT_PEN)
        #pc = wx.Color(color1.Red() + 30,color1.Green() + 30, color1.Blue() + 30)
        #dc.SetBrush(wx.Brush(pc))
        #dc.DrawArc(x1-2, y1/2, x2-2, y2/2, xc - 2, yc/2)

        dc.SetPen(wx.Pen("black", 1))
        dc.SetBrush(wx.Brush("black"))
        dc.DrawArc(x1, y1/2, x2, y2/2, xc, yc/2)

        rect = wx.Rect(x1 - 3, y1/2, twidth + (twidth / 5), theight + textTrailer)

        self.DrawHorizontalGradient(dc, rect, color1, color2)

        if stripes:
            color3 = wx.Color(255, 255, 255)
            ii_tmp = 0
            for ii in range(0, theight, 2):
                ii_tmp = ii
                rect = wx.Rect(x1 - 3 + twidth + (twidth / 5), (y1/2) + ii, 5, 2)
                print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

                rect = wx.Rect(x1 - 3 + twidth + (twidth / 5), (y1/2) + ii, 15, 1)
                print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

            while (y1/2) + ii_tmp + 2 < y1/2 + theight:
                print "adjust", ii_tmp, theight
                rect = wx.Rect(x1 - 3 + twidth + (twidth / 5), (y1/2) + ii_tmp, 15, 1)
                print rect
                self.DrawHorizontalGradient(dc, rect, color2, color3)

                ii_tmp += 2


        color = self.textColor
        dc.SetTextForeground(color)

        dc.DrawText(text, xc, y/2)

class TopFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
            pos=(350, 750), size=(350, 200))

        #p = wx.Panel(self, -1)
        #p = TestPanel(self, sys.stdout)
        p = WGUI(self)


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



# ---

