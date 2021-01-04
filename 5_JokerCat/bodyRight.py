from reportlab.lib import colors

from reportlab.platypus import Table
from reportlab.platypus import TableStyle

# #################>
# Our code imports
from styles import styles

##########################################
# Called in: body.py - genBodyTable 
# width = 50% of MT_WIDTH and height = 80% of MT_HEIGHT
def genBodyRColTable(width, height):

    rowsHeight = [
        height * 15 / 100, # Crimes table - 15% of height
        height * 35 / 100, # Crimes chart - 45% of height
        height * 30 / 100, # Danger Stay Alert - 30% of height
        height * 20 / 100, # Super Mario - 10% of height
    ]

    # Title to be used in crimes table and crimes chart
    title = 'Crimes per month'

    # generate a list of list with month prefix + random number of crimes
    from datetime import datetime
    from random import randrange
    # Data to be used in crimes table and crimes chart
    data = [
        [   # Months prefixes
            datetime(2019, x, 1).strftime('%b') # %b - Abbreviated month name
                for x in range(1,13)
        ],
        [   # Random values between 20 and 500 for 12 months
            randrange(20, 500) 
                for x in range(0,12)
        ]
    ]

    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
    res = Table([   # Tables inside tables
        [genCrimesTable(
            width, rowsHeight[0], title, data
        )],
        [genCrimesChart(
            width, rowsHeight[1], title, data
        )],
        [genDangerStayAlert(
            width, rowsHeight[2]
        )],
        [genSuperMario(
            width, rowsHeight[3]
        )]
    ], 
    width, rowsHeight)

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL, # useful for debug
        styles.LEFT_PADDING_ZERO_ALL, # from styles.py
        styles.BOTTOM_PADDING_ZERO_ALL,

        # super mario row
        ('BOTTOMPADDING', (0,3), (0,3), rowsHeight[3]/4), # height of mario's row divided by 4       
    ])

    return res

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BR Table - crimes table
# Called in: genBodyRColTable
# Crimes Table will only use 50% of available space
# so we can push it up with bottom padding = 30
def genCrimesTable(width, height, title, data):
    
    titleHeight = height * 20 / 100 # 20% of height
    dataHeight = height * 30 / 100  # 30% of height

    # Title row have 3 columns
    emptyCellWidth = width * 16 / 100           # 16% of width
    titleCellWidth = width - 2 * emptyCellWidth # 100% - 2*16% of width
    widthList = [
        emptyCellWidth,
        titleCellWidth,
        emptyCellWidth
    ]

    # the empty cells actually are the ones with the text :D
    titleTable = Table(
        [[title, '', title]], widthList, titleHeight
    )   
    # see colors at: https://www.w3schools.com/colors/colors_names.asp
    borderColor = colors.darkgreen
    backColor = colors.darkcyan

    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
    titleTable.setStyle([
        styles.LEFT_PADDING_ZERO_ALL,
        styles.TEXT_ALIGN_CENTER_ALL, 

        # 1st column - the shadow
        ('BOTTOMPADDING', (0,0), (0,0), 4),
        ('FONTNAME', (0,0), (0,0), 'fontSPB'),
        ('FONTSIZE', (0,0), (0,0), 14),
        ('LEFTPADDING', (0,0), (0,0), 226), 
        ('TEXTCOLOR', (0,0), (0,0), colors.black),

        # 3rd column - the text
        ('BOTTOMPADDING', (2,0), (2,0), 6),
        ('FONTNAME', (2,0), (2,0), 'fontSPB'),
        ('FONTSIZE', (2,0), (2,0), 14),
        ('LEFTPADDING', (2,0), (2,0), -210),
        ('TEXTCOLOR', (2,0), (2,0), colors.orange),

        # top border line
        ('LINEABOVE',(1,0),(1,0),2,borderColor),
        # left border line
        ('LINEBEFORE',(1,0),(1,0),2,borderColor),
        # right border line
        ('LINEAFTER',(1,0),(1,0),2,borderColor),

        ('BACKGROUND',(1,0),(1,0),backColor),
    ])

    dataTable = Table(
        data,
        width / len(data[0]), 
        dataHeight / len(data)
    )
    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
    dataTable.setStyle([
        #styles.GRID_BLACK_T1_ALL,

        styles.LEFT_PADDING_ZERO_ALL,
        styles.BOTTOM_PADDING_ZERO_ALL,

        # row with the months abbreviations
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),

        # row with the months abbreviations
        ('LEFTPADDING',(0,0),(-1,0),2),
        # row with the values
        ('LEFTPADDING', (0,1), (-1,-1), 3),

        # top border line - first 2 columns of months abbreviations row
        ('LINEABOVE',(0,0),(1,0),2,borderColor),
        # top border line - last 2 columns of months abbreviations row
        ('LINEABOVE',(10,0),(11,0),2,borderColor),
        # left border line - first column
        ('LINEBEFORE',(0,0),(0,1),2,borderColor),
        # right border line - last column
        ('LINEAFTER',(11,0),(11,1),2,borderColor),
        # bottom border line - last row
        ('LINEBELOW',(0,1),(-1,-1),2,borderColor),

        ('BACKGROUND',(0,0),(-1,-1),backColor), 
    ])

    res = Table([
        [titleTable],   # title
        [dataTable]     # months abbreviations + random numbers
    ], width, [titleHeight, dataHeight])

    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
    res.setStyle([
        #styles.GRID_RED_T1_ALL, # useful for debug

        styles.LEFT_PADDING_ZERO_ALL, # from styles.py
        ('BOTTOMPADDING', (0,0), (-1,-1), 30),
    ])    

    return res

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BR Table - crimes chart
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Rect
from reportlab.graphics.shapes import String
from reportlab.graphics.charts.linecharts import(
    HorizontalLineChart3D
)
# Called in: genBodyRColTable
def genCrimesChart(width, height, title, data):

    # Title

    # This will draw a background to the text
    # 'Crimes per month - 3D Line Chart'    
    backgroundRect = Rect(
        -2, height - 24,    # x and y start position
        width + 5, 22,      # width and height
        4,                  # radius x to round corners
        stroke=1, fill=1,
        fillColor=colors.mediumpurple
    )

    # title shadow
    title1 = String(
        2, height - 19, # x and y start position
        f'{title} - 3D Line Chart', 
        fontSize = 16,
        fontName='Helvetica-Bold',
        fillColor=colors.black
    )

    # title text
    title2 = String(
        0, height - 18, # x and y start position
        f'{title} - 3D Line Chart', 
        fontSize = 16,
        fontName='Helvetica-Bold',
        fillColor=colors.white
    ) 

    # Chart
    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Charts: https://youtu.be/FcZ9wTGmMrw
    chart = HorizontalLineChart3D()
    chart.data = [data[1]]
    chart.x = 5     # position at x
    chart.y = 20    # position at y
    chart.height = height - backgroundRect.height - 30 
    chart.width = width - 5 - 10

    # x axis - Months names abbreviated
    chart.categoryAxis.categoryNames = data[0]  	

    # y axis minimum value
    chart.valueAxis.valueMin = 0
    # y axis maximum value
    chart.valueAxis.valueMax = 500
    # y axis, from 0 to 500 step 100, i.e. 0, 100, 200, 300, 400 and 500
    chart.valueAxis.valueStep = 100

    chart.lines[0].strokeWidth = 3.5
    chart.lines[0].strokeColor = colors.red

    drawing = Drawing()
    drawing.add(backgroundRect)
    drawing.add(title1)
    drawing.add(title2)
    drawing.add(chart)

    res = Table([
        [drawing]
    ], width, height)

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL,

        styles.LEFT_PADDING_ZERO_ALL,
        styles.BOTTOM_PADDING_ZERO_ALL,
    ])

    return res

from reportlab.graphics.widgets.signsandsymbols import(
    DangerSign
) 
from reportlab.graphics.widgetbase import TwoFaces
# Called in: genBodyRColTable
def genDangerStayAlert(width, height):

    danger = DangerSign()
    danger.x = width/2 - danger.size/2
    danger.y = height/2 - danger.size/2

    text1 = 'Danger!'
    title = String(
        danger.x + danger.size/len(text1), danger.y + danger.size + 5, 
        text1, 
        fontSize = 18,
        fontName='fontLG',
        fillColor=colors.black
    )
    title2 = String(
        danger.x, danger.y - 20, 
        'Stay Alert!', 
        fontSize = 18,
        fontName='fontLG',
        fillColor=colors.black
    )

    faces = TwoFaces()
    faces.faceOne.size = 50
    faces.faceTwo.size = 50
    faces.faceOne.x = danger.x - faces.faceOne.size / 2
    faces.faceTwo.x = danger.x + danger.size - faces.faceTwo.size / 2
    faces.faceOne.y = danger.y + danger.size / 2
    faces.faceTwo.y = danger.y + danger.size / 2
    # faces.faceOne.skinColor = colors.green
    # faces.faceTwo.skinColor = colors.blueviolet
    # faces.faceOne.eyeColor = colors.red
    # faces.faceTwo.eyeColor = colors.red
    faces.faceOne.mood = 'ok'

    drawing = Drawing()
    drawing.add(title)
    drawing.add(danger)
    drawing.add(faces)
    drawing.add(title2)

    return drawing

def genSuperMario(width, height):

    ps = 4 # point size

    # this will draw from bottom-up, left-right
    background = Rect(
        0, 0,           # x and y start position
        15*ps, 18*ps,   # width and height  
        strokeWidth=0, strokeColor=colors.cadetblue,
        fill=1, fillColor=colors.cadetblue
    )

    bootLeft1 = Rect(
        ps, ps,       # x and y start position
        ps, ps,       # width and height
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )
    bootLeft2 = Rect(
        2*ps, ps,       # x and y start position
        3*ps, 2*ps,       # width and height
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )   

    startBR2 = bootLeft1.width + bootLeft2.width + ps * 4 + ps
    bootRight2 = Rect(
        startBR2, ps,      
        3*ps, 2*ps,       
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )  
    bootRight1 = Rect(
        startBR2 + bootRight2.width, ps,
        ps, ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )

    handLeft2 = Rect(
        ps, 4*ps,
        2*ps, 3*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    ) 
    handLeft1 = Rect(
        handLeft2.width + ps, 5*ps,
        ps, ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    )

    startHR1_x = handLeft2.width + handLeft1.width + 6*ps + ps
    handRight1 = Rect(
        startHR1_x, 5*ps,
        ps, ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    )
    handRight2 = Rect(
        startHR1_x + handRight1.width, 4*ps,
        2*ps, 3*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    )

    monkeySuit1 = Rect(
        3*ps, 3*ps,
        3*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.steelblue,
        fill=1, fillColor=colors.steelblue
    )
    monkeySuit2 = Rect(
        monkeySuit1.y + monkeySuit1.width + 2*ps, 3*ps,
        3*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.steelblue,
        fill=1, fillColor=colors.steelblue
    )
    monkeySuit3 = Rect(
        monkeySuit1.y + monkeySuit1.width, 4*ps,
        2*ps, 4*ps,      
        strokeWidth=0, strokeColor=colors.steelblue,
        fill=1, fillColor=colors.steelblue
    )
    monkeySuit4 = Rect(
        4*ps, 5*ps,
        6*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.steelblue,
        fill=1, fillColor=colors.steelblue
    )
    monkeySuit5 = Rect(
        5*ps, 7*ps,
        4*ps, 3*ps,      
        strokeWidth=0, strokeColor=colors.steelblue,
        fill=1, fillColor=colors.steelblue
    )  

    shirt1 = Rect(
        6*ps, 8*ps,
        2*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    )
    shirt2 = Rect(
        8*ps, 9*ps,
        2*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    )
    shirt3 = Rect(
        9*ps, 7*ps,
        3*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    )
    shirt4 = Rect(
        10*ps, 6*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 
    shirt5 = Rect(
        12*ps, 7*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    )   
    shirt6 = Rect(
        3*ps, 7*ps,
        2*ps, 3*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 
    shirt7 = Rect(
        3*ps, 6*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 
    shirt8 = Rect(
        2*ps, 7*ps,
        1*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 
    shirt9 = Rect(
        ps, 7*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 

    button1 = Rect(
        5*ps, 6*ps,
        ps, ps,      
        strokeWidth=0, strokeColor=colors.yellow,
        fill=1, fillColor=colors.yellow
    )
    button2 = Rect(
        8*ps, 6*ps,
        ps, ps,      
        strokeWidth=0, strokeColor=colors.yellow,
        fill=1, fillColor=colors.yellow
    )

    faceSkin1 = Rect(
        4*ps, 10*ps,
        8*ps, 4*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    )
    faceSkin2 = Rect(
        3*ps, 12*ps,
        1*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    ) 
    faceSkin3 = Rect(
        12*ps, 12*ps,
        1*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    )
    faceSkin4 = Rect(
        13*ps, 12*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    ) 
    faceSkin5 = Rect(
        6*ps, 14*ps,
        5*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.bisque,
        fill=1, fillColor=colors.bisque
    ) 

    moustache1 = Rect(
        9*ps, 11*ps,
        4*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.black,
        fill=1, fillColor=colors.black
    ) 
    moustache2 = Rect(
        10*ps, 12*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.black,
        fill=1, fillColor=colors.black
    ) 

    eyes = Rect(
        9*ps, 13*ps,
        1*ps, 2*ps,      
        strokeWidth=0, strokeColor=colors.black,
        fill=1, fillColor=colors.black
    )

    hair1 = Rect(
        2*ps, 11*ps,
        1*ps, 3*ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )  
    hair2 = Rect(
        3*ps, 11*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )   
    hair3 = Rect(
        4*ps, 12*ps,
        2*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    )
    hair4 = Rect(
        4*ps, 13*ps,
        1*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    ) 
    hair5 = Rect(
        3*ps, 14*ps,
        3*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.brown,
        fill=1, fillColor=colors.brown
    ) 

    cap1 = Rect(
        3*ps, 15*ps,
        10*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    ) 
    cap2 = Rect(
        4*ps, 16*ps,
        6*ps, 1*ps,      
        strokeWidth=0, strokeColor=colors.red,
        fill=1, fillColor=colors.red
    )   

    text = String(
        80, 30, 
        'We need a hero',
        fontSize = 12,
        fontName='fontSC',
        fillColor=colors.black
    )     

    drawing = Drawing()
    #background
    drawing.add(background)
    # left boot
    drawing.add(bootLeft1)
    drawing.add(bootLeft2)
    # right boot
    drawing.add(bootRight2)
    drawing.add(bootRight1)    
    #left hand
    drawing.add(handLeft2)
    drawing.add(handLeft1)
    #right hand
    drawing.add(handRight1)
    drawing.add(handRight2)
    #monkey suit
    drawing.add(monkeySuit1)
    drawing.add(monkeySuit2)
    drawing.add(monkeySuit3)
    drawing.add(monkeySuit4)
    drawing.add(monkeySuit5)
    #shirt
    drawing.add(shirt1)
    drawing.add(shirt2)
    drawing.add(shirt3)
    drawing.add(shirt4)
    drawing.add(shirt5)
    drawing.add(shirt6)
    drawing.add(shirt7)
    drawing.add(shirt8)
    drawing.add(shirt9)
    #yellow buttons
    drawing.add(button1)
    drawing.add(button2)
    #face skin
    drawing.add(faceSkin1)
    drawing.add(faceSkin2)
    drawing.add(faceSkin3)
    drawing.add(faceSkin4)
    drawing.add(faceSkin5)
    #moustache
    drawing.add(moustache1)
    drawing.add(moustache2)
    #eyes
    drawing.add(eyes)
    #hair
    drawing.add(hair1)
    drawing.add(hair2)
    drawing.add(hair3)
    drawing.add(hair4)
    drawing.add(hair5)
    #cap
    drawing.add(cap1)
    drawing.add(cap2)

    #text
    drawing.add(text)

    return drawing