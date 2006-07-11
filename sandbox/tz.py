"""
  * the use of foreground and background program-generated images;
  * the use of cursor keys to move an image;
  * the automatic scrolling of windows;
  * double-buffering of images using "built-in" bufferedDC's.
Using the arrow-keys, we move a simple image (circle) on a checkered
background inside a scrolled-window, scrolling automatically as needed to
keep the circle always visible.
"""

import  wx

custom_buffer = False

class CheckeredBackground(object):
  """Checkered-like image pattern defined so that we can better
  visualise the moving canvas."""
  # Note: there is no real need to define this as a class; it could
  # have been simply defined as a function of MyCanvas below.
  # Note 2: default values are provided but not used in this program.

  def __init__(self, width=600, height=480, side=40):
    
      #-- prepare to create bitmap image
      self.image = wx.EmptyBitmap(width, height)

      # Before we can "draw", we need to specify what the context will be.
      #-- Device context (DC) will be computer memory
      offDC = wx.MemoryDC()

      #-- prepare to work with the image
      offDC.SelectObject(self.image)

      #-- select a background colour
      offDC.SetBackground(wx.Brush("WHEAT"))

      #-- "paint" over the entire object with the background colour
      offDC.Clear()

      #-- create the pattern in "separate" memory
      nb_col = width//side
      nb_row = height//side
      squares = []
      for i in range(0, nb_col, 2):
          for j in range(0, nb_row, 2):
              x = i*side
              y = j*side
              squares.append( (x, y, side, side) )
      for i in range(1, nb_col, 2):
          for j in range(1, nb_row, 2):
              x = i*side
              y = j*side
              squares.append( (x, y, side, side) )

      #-- Choose square outline colour
      offDC.SetPen(wx.Pen("PALE GREEN", side/8))

      #-- Choose square interior (fill) colour
      offDC.SetBrush(wx.Brush("LIGHT STEEL BLUE"))

      #-- "draw" the squares in DC memory
      offDC.DrawRectangleList(squares)

      #-- release bitmap image from drawing context.  This amounts,
      # as I understand, to undoing SelectObject().
      del offDC

class MovingCircle(object):
  """Creates a simple circle on transparent background"""
  # Note: there is no real need to define this as a class.
  # It is done here for later re-use in other examples.
  # Note 2: default values are provided but not used in this program.

  def __init__(self, radius = 10, string_colour = "RED"):

      #-- prepare to create bitmap image
      self.image = wx.EmptyBitmap(2*radius, 2*radius)
    
      #-- Device context (DC) will be computer memory
      offDC = wx.MemoryDC()

      #-- prepare to work with the image
      offDC.SelectObject(self.image)
    
      """ Preparing to draw a shape with a transparent background.
          I thought that choosing a wx.Brush with a TRANSPARENT_BRUSH
          colour, and clearing the DC with it would work - but it
          does not.  What does work is to select an "unused" colour
          for the background and set up a mask with it."""
      #-- choose an "unusual" background colour ...
      offDC.SetBackground(wx.Brush(wx.Colour(2,2,2), wx.SOLID))

      #-- ... and set it everywhere
      offDC.Clear()

      #-- different colour for object
      offDC.SetPen(wx.Pen(string_colour, 1)) # outline
      offDC.SetBrush(wx.Brush(string_colour)) # interior

      offDC.DrawCircle(radius, radius, radius)# center: (x, y) and radius.
    
      #-- release bitmap image from drawing context to process it further
      del offDC

      #-- set up a mask with our "unusual" colour
      mask = wx.Mask(self.image, wx.Colour(2,2,2))
      self.image.SetMask(mask)
      #-- only regions where colour != wx.Colour(2,2,2) survives.


class MyCanvas(wx.ScrolledWindow):
  def __init__(self, parent, id = -1, size = wx.DefaultSize):
      wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size,
                              style=wx.SUNKEN_BORDER)
      # sets dimensions so that image will be larger than window,
      # and scrolling can occur.
      self.maxWidth = 1200
      self.maxHeight = 800

      # Set the size of the total window, of which only a small part
      # will be displayed; apparently SetVirtualSize needs
      # a single (tuple) argument, which explains the double (( )).
      self.SetVirtualSize((self.maxWidth, self.maxHeight))

      # Set the scrolling rate; use same value in both horizontal and
      scrollRate = 20  # vertical directions.
      self.SetScrollRate(scrollRate, scrollRate)

      # Create the background image
      side = 40
      self.background = CheckeredBackground(self.maxWidth,
                                            self.maxHeight, side)
    
      # Create small foreground images; normally, such an image might
      # be imported from a file
      self.radius = 40
      self.red_circle = MovingCircle(self.radius, "RED")
    
      # sets its position (used later)
      self.circle_x = 0  # position of top left corner of enclosing box
      self.circle_y = 0

      # bind the key events that will be used to move the small image
      self.bindEvents()
    
      # Initialize the buffer bitmap.  No real DC is needed at this point.
      self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
      self.drawImage()
    
  def bindEvents(self):
      # use the old style [still works!] instead of self.Bind(evt, fn)
      wx.EVT_PAINT(self, self.OnPaint)
      wx.EVT_CHAR(self, self.MyArrowKeys)

##-- onPaint() and drawImage() are the two methods I'd like to know how
##-- to do with custom-based buffered DCs.

  def OnPaint(self, event):
      if custom_buffer:
          pass
          # I haven't been able to figure out how to do this
      else:
          dc = wx.BufferedPaintDC(self, self.buffer)
    
  def drawImage(self):
      if custom_buffer:
          pass
          # I haven't been able to figure out how to do this.
      else:
          dc = wx.BufferedDC(None, self.buffer)
      dc.Clear()
      dc.BeginDrawing()
      # First copy the background image onto the buffer
      dc.DrawBitmap(self.background.image, 0, 0, True)
      # Next, superimpose the foreground image
      dc.DrawBitmap(self.red_circle.image, self.circle_x,
                    self.circle_y, True)
      dc.EndDrawing()
      del dc      

  def MoveCircle(self, x, y):
      self.circle_x += x
      self.circle_y += y

      #-- Prevent the circle from moving out of bounds
      # (of the full background image, not the visible part.)
# SAM
#      if self.circle_x < circle_x =" 0" circle_y =" 0"> self.maxWidth - 2*self.radius:
#          self.circle_x = self.maxWidth - 2*self.radius
      if self.circle_y > self.maxHeight - 2*self.radius:
          self.circle_y = self.maxHeight - 2*self.radius      
    
      hidden = 40  # approximate space hidden under scrollbars
    
      # determine the position of top left visible window in
      # "scrollrate" units
      xView, yView = self.GetViewStart()

      # corresponding amount of pixel per "scroll"
      xDelta, yDelta = self.GetScrollPixelsPerUnit()

      # size of wisible window
      width, height = self.GetSizeTuple()

      #-- Determine if window needs to be scrolled so that object
      # remains visible.  Assume that the object fits entirely
      # in the visible view.

#      if self.circle_x < xview =" max(0,"> xView*xDelta + width:
#          xView = (self.circle_x + 2*self.radius + hidden - width)/xDelta

#      if self.circle_y < yview =" max(0,"> yView*yDelta + height:
#          yView = (self.circle_y + 2*self.radius + hidden - height)/yDelta

      self.Scroll(xView, yView)

      self.drawImage()
      self.Refresh(False)
            
  def MyArrowKeys(self, event):
      code = event.KeyCode()
      if code == wx.WXK_UP:
          self.MoveCircle(0, -10) # up on screen is negative y-direction
      elif code == wx.WXK_LEFT:
          self.MoveCircle(-10, 0)
      elif code == wx.WXK_RIGHT:
          self.MoveCircle(10, 0)
      elif code == wx.WXK_DOWN:
          self.MoveCircle(0, 10)
      else:
          pass   # ignore all other keys pressed
    
   
class AnimationFrame(wx.Frame):
  def __init__(self, parent):
      wx.Frame.__init__(self, parent, -1, "Animation Frame", size=(400, 300),
                       style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
      doodle = MyCanvas(self, -1)

#----------------------------------------------------------------------

if __name__ == '__main__':
  app = wx.PySimpleApp()
  frame = AnimationFrame(None)
  frame.Show(True)
  app.MainLoop()
