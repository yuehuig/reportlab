from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# #################>
# Our code imports
from styles import styles # styles.py

# this function is called in report.py line 133
def genHeaderTable(width, height):

    # for more colors see: https://htmlcolorcodes.com/color-names/
    titleText = '''
    <font color="#7CB9E8" size="34">
    <b>
    People are more scared than ever<br/>
    increasing Joker Cat attacks are devastating
    </b>
    </font>
    '''

    titleParaStyle = ParagraphStyle(
        name = 'headingTitle',
        leading = 40, # space between lines
        alignment = TA_CENTER, # horizontal align
    )

    titlePara = Paragraph(titleText, titleParaStyle)

    res = Table([
        [titlePara]
    ], 
    width, height)

    res.setStyle([
        #styles.GRID_RED_ALL, # useful for debug

        styles.LEFT_PADDING_ZERO_ALL, # from styles.py
        styles.BOTTOM_PADDING_ZERO_ALL,

        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), # vertical align
    ])

    return res