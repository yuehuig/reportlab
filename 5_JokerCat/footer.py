from reportlab.lib import colors

from reportlab.platypus import Table
from reportlab.platypus import Image
from reportlab.platypus import TableStyle

# #################>
# Our code imports
from styles import styles

def getOrdinalSuffix(day):
    return 'th' if 11<=day<=13 else {1:'st',2:'nd',3:'rd'}.get(day%10, 'th')

from datetime import datetime as dt

# Called in: report.py - line 62
# width = MT_WIDTH and height = 5% of MT_HEIGHT
def genFooterTable(width, height):
    
    columnsWidth = [
        width * 80 / 100, # 80% of width (MT_WIDTH)
        width * 20 / 100  # 20% of width (MT_WIDTH)
    ]

    text1 = 'If you see him please contact secret services at secretServicesJokerCat@secret.com '

    date = dt.now()
    suffix = getOrdinalSuffix(date.day)
    # note: %#d - removes leading zero on windows
    # For unix based systems should be: %-d
    text2 = date.strftime(f'%B %#d{suffix}, %Y')

    res = Table(
        [[text1, text2]],
        columnsWidth,
        height
    )

    res.setStyle([
        #styles.GRID_BLACK_T1_ALL,

        ('ALIGN', (1,0), (1,0), 'RIGHT')
    ])

    return res