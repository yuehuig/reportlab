from reportlab.platypus import Table
from reportlab.platypus import TableStyle

# #################>
# Our code imports
from styles import styles               # styles.py
from bodyLeft import genBodyLColTable   # bodyLeft.py
from bodyRight import genBodyRColTable  # bodyRight.py

# Called in: report.py - line 61
# width = MT_WIDTH and height = 80% of MT_HEIGHT
def genBodyTable(width, height):
    
    colWidth = width / 2 # 50% each column

    # For a better understanding of this code please see:
    # Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
    res = Table(
        [   # Tables inside tables
            [ 
            genBodyLColTable(colWidth,height),  # from bodyLeft.py
            genBodyRColTable(colWidth,height)   # from bodyRight.py
            ], 
        ],
        colWidth,
        height
    )

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL, # useful for debug
        styles.LEFT_PADDING_ZERO_ALL, # from styles.py
        styles.BOTTOM_PADDING_ZERO_ALL,
    ])

    return res
