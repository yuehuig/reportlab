from reportlab.lib import colors

from reportlab.platypus import Table
from reportlab.platypus import Image

from datetime import datetime

# #################>
# Our code imports
from styles import styles

JC_PICTURE = './res/jokerCat.jpg'

# Called in: report.py - line 60 
# width = MT_WIDTH and height = 15% of MT_HEIGHT
def genHeaderTable(width, height):
    
    columnsWidth = [
        width * 80 / 100, # 80% of width (MT_WIDTH)
        width * 20 / 100  # 20% of width (MT_WIDTH)
    ]

    info = genInfoTable(columnsWidth[0],height)

    image = Image(JC_PICTURE)
    # resize to 3% of the image size
    image.drawWidth = image.drawWidth * 3 / 100
    image.drawHeight = image.drawHeight * 3 / 100
    
    res = Table(
        [[info, image]], # info is a table!
        columnsWidth,
        height
    )

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL, # useful for debug

        # For a better understanding of this code please see:
        # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
        ('BOTTOMPADDING',(0,0),(-1,-1), 30), 

        # info table
        ('LEFTPADDING',(0,0),(0,0), 0),
         
        # image
        ('LEFTPADDING',(1,0),(1,0), 30),
    ])

    return res

# width = 80% of MT_WIDTH and height = 15% of MT_HEIGHT
def genInfoTable(width, height): 

    text1 = ['Name:','Joker Cat']
    text2 = ['Age:','3 years old']
    text3 = ['Note:','Extremely Dangerous']

    columnsWidth = [
        width * 18 / 100, # 18% of width
        width * 30 / 100, # 30% of width
    ]

    res = Table(
        [
            [ text1[0], text1[1] ], 
            [ text2[0], text2[1] ], 
            [ text3[0], text3[1] ]
        ],
        columnsWidth,
        height * 15 / 100 # 15% of height
    )

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL, # useful for debug

        # For a better understanding of this code please see:
        # Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
        # Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
        ('LEFTPADDING',(0,0),(0,-1), 10),      # 1st column
        ('BOTTOMPADDING',(0,0),(-1,-1), 15),   # all table cells

        # 1st column
        ('FONTNAME', (0,0), (0,-1), 'fontSPB'), #fontSPB - report.py line 24
        ('FONTSIZE', (0,0), (0,-1), 14),

        # 2nd column
        ('FONTNAME', (1,0), (1,-1), 'fontSE'), #fontSE - report.py line 21
        ('FONTSIZE', (1,0), (1,-1), 15),
    ])

    return res