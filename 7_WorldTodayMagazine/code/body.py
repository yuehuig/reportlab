from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import (
    TA_RIGHT, TA_LEFT
)

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import String
from reportlab.graphics.charts.barcharts import(
	VerticalBarChart, 
    Rect
)

# #################>
# Our code imports
from styles import styles # styles.py
from utils import utils # utils.py

# this function is called in report.py line 134
def genBodyTable(width, height):

    widthList = [
        width * 40 / 100,   # 40% of width
        width * 60 / 100,   # 60% of width
    ]

    res = Table([
        [genLeftParagraph(), genRightTable(widthList[1], height)]
    ], 
    widthList, height)

    res.setStyle([
        #styles.GRID_RED_ALL, # useful for debug

        styles.LEFT_PADDING_ZERO_ALL,
        styles.BOTTOM_PADDING_ZERO_ALL,

        # 1st column - chart left text
        ('VALIGN', (0,0), (0,0), 'MIDDLE'),

        # 2nd column - chart and bottom text
        ('VALIGN', (1,0), (1,-1), 'TOP'),
    ])

    return res

def genLeftParagraph():

    text = '''
    <font size="16">
    JC has exposed to the world the true<br/>
    meaning of evil! His campaigns on<br/>
    destroying sofas around the globe<br/>
    are significantly increasing the need<br/>
    for a greater hero! GISS continuously<br/>
    search for a solution, being Mad Dog<br/>
    the trump they expect to be the most<br/>
    promising one!
    </font>
    '''

    textParaStyle = ParagraphStyle(
        name = 'chartLeftText',
        leading = 28,   # space between lines
        alignment = TA_RIGHT,
    )

    textPara = Paragraph(text, textParaStyle)

    return textPara

def genRightTable(width, height):

    heightList = [
        height * 80 / 100, # 80% of width
        height * 20 / 100  # 20% of width
    ]

    res = Table([
        [genChart(width, heightList[0])],
        [genBottomParagraph()]
    ], 
    width, heightList)

    res.setStyle([
        #styles.GRID_RED_ALL,

        # ('GRID', (0,0), (0,0), 1, colors.orange),
        # ('GRID', (0,1), (0,1), 1, colors.blue),

        # 2nd row - chart bottom text
        ('VALIGN', (0,1), (0,1), 'TOP'),
        ('LEFTPADDING', (0,1), (0,1), 35),
    ])

    return res

def genChart(width, height): 

    chart = VerticalBarChart()
    chart.data = [ (12, 11, 9, 6, 2, 22, 7) ]

    # Vertical axis - Y axis
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 25
    chart.valueAxis.visible = 0 # hide
    
    # Horizontal axis - X axis
    chart.categoryAxis.categoryNames = [
        'Asia', 'Africa', 'North America', 
        'South America', 'Antarctica', 
        'Europe', 'Australia'
    ]
    # We could hide X axis like we did with Y axis:
    #   example: chart.categoryAxis.visible = 0
    # Hidding the X axis will hide all the elements of X axis
    # and we want to see the labels!
    #   example: chart.categoryAxis.labels.visible = 1 # by default they are visible
    # So we just hide what we don't want to see!
    chart.categoryAxis.visibleAxis = 0      # hide line
    chart.categoryAxis.visibleTicks = 0     # hide line ticks
    chart.categoryAxis.labels.angle = 90    # rotate labels
    chart.categoryAxis.labels.dx = -30      # adjust labels position at x
    chart.categoryAxis.labels.dy = 30       # adjust labels position at y

    # Numbers above each bar    
    chart.barLabelFormat = '%s' # contains the provived string
    chart.barLabels.nudge = 15 # space between the bar and the text
    chart.barLabels.angle = -20 # rotate the text
    chart.barLabels.fontName = 'barText' # registered font at report.py line 91
    chart.barLabels.fontSize = 20
    chart.barLabels.fillColor = colors.red

    chart.barWidth = 5 
    chart.barSpacing = 8 # space between each bar
    # NOTE: bar list doesn't work like we could expect,
    # the first element apparently sets the configuration for all!
    chart.bars[0].fillColor = colors.toColor('hsl(240, 100%, 20%)')
    chart.bars[0].strokeColor = colors.white

    chart.x = width * 5 / 100           # starts at 5% of width space
    chart.y = height * 5 / 100          # starts at 5% of height space
    chart.width = width * 90 / 100      # uses 90% of width
    chart.height = height * 80 / 100    # uses 80% of height
    

    titleShadow = String(
        19, height * 60 / 100 - 1, # x and y start point
        'Average JC attacks by continent',
        fontSize = 20,
        fontName = 'chartTitle', # registered font at report.py line 94
        fillColor = colors.red
    )

    title = String(
        20, height * 60 / 100, # x and y start point
        'Average JC attacks by continent',
        fontSize = 20,
        fontName = 'chartTitle', # registered font at report.py line 94
        fillColor = colors.orange
    )

    bounds = title.getBounds() # returns a tuple with (x1,y1,x2,y2)
    
    rectangle = Rect(
        bounds[0] - 3, bounds[1],       # x1 and y1
        bounds[2] - bounds[0] + 3, 20   # x2 and y2
    )
    rectangle.fillColor = colors.black

    drawing = Drawing()
    drawing.add(rectangle)
    drawing.add(titleShadow)
    drawing.add(title)
    drawing.add(chart)

    # Bars bottom 'labels'
    # For a better understand of this coordinates please 
    # see code guide
    charWidth = utils.getStringWidth('A')
    dataLen = len(chart.data[0]) # 7 elements

    startPoint = chart.getBounds()[0]
    barAndLabelWidth = chart.width / dataLen # total width / 7 elements
    center = barAndLabelWidth / 2 - charWidth / 2

    yPos = chart.y - 10

    # Example:
    # drawing.add(String(startPoint + barAndLabelWidth * 0 + center, chart.y - 10, 'A'))
    # drawing.add(String(startPoint + barAndLabelWidth * 1 + center, chart.y - 10, 'B'))
    # ...
    # drawing.add(String(startPoint + barAndLabelWidth * 6 + center, chart.y - 10, 'G'))
    for index, char in enumerate('ABCDEFG', start=0):
        xPos = startPoint + barAndLabelWidth * index + center

        drawing.add(String(xPos, yPos, char))

    return drawing

def genBottomParagraph():

    text = '''
    <font size="9" color="#8d9698">
    Note: Data here is not accurate since there are some reports from anonymous citizens<br/>
    that are not taken into account! People are afraid to be the next target!<br/>
    Antarctica is where the leading resistance and HQ (headquarters) of GISS are located...<br/>
    There the data is accurate and they already suffered 2 major attacks! Joker Cat is unstoppable!!!
    </font>
    '''

    textParaStyle = ParagraphStyle(
        name = 'chartLeftText',
        leading = 10, # space between lines
        alignment = TA_LEFT, # from reportlab.lib.enums
    )

    textPara = Paragraph(text, textParaStyle)

    return textPara