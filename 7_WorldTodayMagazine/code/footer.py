from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# #################>
# Our code imports
from styles import styles # styles.py

# this function is called in report.py line 135
def genFooterTable(width, height):

    text = 'THE ASSOCIATION OF <b>WORLD TODAY MAGAZINE</b>'

    textParaStyle = ParagraphStyle(
        name = 'footer',
        leading = 10, # space between lines
        alignment = TA_CENTER, # horizontal align
    )

    textPara = Paragraph(text, textParaStyle)

    res = Table([
        [textPara]
    ], 
    width, height)

    res.setStyle([
        #styles.GRID_RED_ALL,

        styles.LEFT_PADDING_ZERO_ALL,
        styles.BOTTOM_PADDING_ZERO_ALL,

        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), # vertical align
    ])

    return res