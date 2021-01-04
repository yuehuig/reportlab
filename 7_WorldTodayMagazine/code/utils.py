from reportlab.graphics.shapes import String

class utils:
    # Gets width of a string
    # Note: Don't work perfectly with some imported fonts!
    def getStringWidth(text):
        dummyChar = String(0, 0, text)
        # returns:
        # (x0, y0, x1, y1)
        # x0 and y0 start point
        # x1 and y1 end point
        bounds = dummyChar.getBounds()
        xPosStart = bounds[0]
        xPosEnd = bounds[2]

        return xPosEnd - xPosStart