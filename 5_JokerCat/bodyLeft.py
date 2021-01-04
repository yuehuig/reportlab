from reportlab.lib import colors

from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.platypus import Image

# #################>
# Our code imports
from styles import styles

##########################################
# Called in: body.py - genBodyTable 
# width = 50% of MT_WIDTH and height = 80% of MT_HEIGHT
def genBodyLColTable(width, height):
    
    rowsHeight = [
        height * 10 / 100, # title - 10% of height
        height * 25 / 100, # text 1 - 25% of height
        height * 25 / 100, # text 2 - 25% of height
        height * 35 / 100, # image - teenage joker cat - 35% of height
        height * 5 / 100,  # text - teenage joker cat - 5% of height
    ]
    
    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
    res = Table([ # Tables inside tables
        [genTitle()],
        [genText1(width, rowsHeight[1])],
        [genText2(width, rowsHeight[2])],
        [genImage()],
        [genLegend()],
    ], width, rowsHeight)

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL, # useful for debug

        # For a better understanding of this code please see:
        # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
        styles.LEFT_PADDING_ZERO_ALL,

        # main title
        ('BOTTOMPADDING',(0,0),(0,0),40), 

        # text 1 and text 2
        ('BOTTOMPADDING',(0,1),(0,2),0), 
        ('LEFTPADDING',(0,1),(0,2),0), 

        # teenager joker cat picture
        ('LEFTPADDING',(0,3),(0,3),60),
        
        # teenager joker cat picture legend
        ('BOTTOMPADDING',(0,4),(0,4),20),    
    ])

    return res

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BL Table - title
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Called in: genBodyLColTable
def genTitle():

    titleP1 = 'Fear the '
    titleP2 = 'Joker Cat'
    titleP3 = '!'
    # multiline f-string
    # Example of a template string with syntax similar to HTML
    template = (
f"""
    <font name="fontSE" size="20">
        {titleP1}
    </font>
    <font name="fontSPB" size="16" color="red">
        <u>{titleP2}</u>
    </font>
    <font name="fontSPB" size="20">
        {titleP3}
    </font>
"""       
    )

    style = ParagraphStyle(
        name='title', alignment=TA_CENTER
    )
    res = Paragraph(template, style=style)

    return res

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BL Table - text columns

# width = 50% of MT_WIDTH and height = 25% of height (height = 80% of MT_HEIGHT)
# Called in: genBodyLColTable
def genText1(width, height):

    title = 'Evil has a new face!'
    text = 'Citizens of the world have to deal with a new threat! Joker Cat is now unstopable destroying sofas all around the planet!'

    return genTextCol(width, height, title, text)

# width = 50% of MT_WIDTH and height = 25% of height (height = 80% of MT_HEIGHT)
# Called in: genBodyLColTable
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Rect
from reportlab.graphics.shapes import Circle
def genText2(width, height):

    # Text background
    rWidth = width * 89 / 100
    rHeight = height * 95 / 100
    backgroundRect = Rect(
        x=0, y=0, # Start point
        width=rWidth, height=rHeight, 
        #rx=2, # controls round corners
        strokeWidth=3, strokeColor=colors.orange,
        fillColor=colors.ivory,    
    )
    # bottom left circle
    circle1 = Circle(
        cx=0, cy=0, # x and y for center
        r=4, # radius
        fillColor=colors.red,
    )
    # bottom right circle
    circle2 = Circle(
        cx=rWidth, cy=0, # x and y for center
        r=4, # radius
        fillColor=colors.red,
    ) 
    # top left circle 
    circle3 = Circle(
        cx=0, cy=rHeight, # x and y for center
        r=4, # radius
        fillColor=colors.red,
    )  
    # top right circle
    circle4 = Circle(
        cx=rWidth, cy=rHeight, # x and y for center
        r=4, # radius
        fillColor=colors.red,
    )   

    drawing = Drawing()
    drawing.add(backgroundRect)
    drawing.add(circle1)
    drawing.add(circle2)
    drawing.add(circle3)
    drawing.add(circle4)    

    # Text
    title = 'Terror has just began!'
    text = 'Sofas are now in extinction and if we don\'t stop him... He will destroy sofas at ISS (International Space Station) and even on Mars!!!'

    tableText = genTextCol(width, height, title, text)

    res = Table([
        [drawing, tableText]
    ], [0, width], height)

    res.setStyle([
        styles.LEFT_PADDING_ZERO_ALL,
        styles.BOTTOM_PADDING_ZERO_ALL,
    ])

    return res

# Called in: genText1 & genText2
def genTextCol(width, height, title, text):

    rowsHeight = [
        height * 5 / 100,
        height * 85 / 100
    ]

    res = Table([
        [title],
        [toMultilineStr(text, 30)]
    ], width, rowsHeight)

    res.setStyle([
        # Cell at 0,0
        ('BOTTOMPADDING',(0,0),(0,0),0),
        # Cell at 0,1 
        ('BOTTOMPADDING',(0,1),(0,1),10), 

        ('FONTNAME',(0,0),(0,0), 'fontLG'),
        ('FONTSIZE',(0,0),(0,0), 18),

        ('FONTNAME',(0,1),(0,1), 'fontSE'),
        ('FONTSIZE',(0,1),(0,1), 15),       
    ])

    return res

# This is a workaround, not the perfect solution!
# size - number of chars allowed in a row.
# Called in: genTextCol
def toMultilineStr(text, size):
    res = ''

    splitedText = text.split(' ')

    count = 0
    for word in splitedText:
        count += len(word) + 1
        if count >= size:
            res += '\n\n'
            count = len(word) + 1
        else:
            if len(res) != 0:
                res += ' '
        
        res += word
    
    return res

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BL Table - rotated picture
TeenJC_PICTURE = r'./res/teenagerJokerCat.jpeg'

# Called in: genBodyLColTable
def genImage():
    res = RotatedImage(TeenJC_PICTURE, 10)
    res.drawWidth = res.drawWidth * 35 / 100
    res.drawHeight = res.drawHeight * 35 / 100

    return res

# Extends from Image class
class RotatedImage(Image):

    def __init__(self, filename, degrees):
        self.deg = degrees
        super().__init__(filename)

    # Override draw method
    def draw(self):
        self.canv.rotate(self.deg)
        Image.draw(self)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BL Table - rotated text  

# Called in: genBodyLColTable      
def genLegend():
    style = ParagraphStyle(
        name='legend', alignment=TA_CENTER,
        fontName='fontSC',
        fontSize=8,
    )

    text = 'Teenage Joker Cat'
    return RotatedParagraph(text, style, -5)

# Extends Paragraph class
class RotatedParagraph(Paragraph):

    def __init__(self, text, style, degrees):
        self.deg = degrees
        super().__init__(text, style)

    # Override draw method
    def draw(self):
        self.canv.rotate(self.deg)
        Paragraph.draw(self)  
