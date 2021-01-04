# For a better understanding of this code please see:
# Generate PDF with Python - Reportlab: https://youtu.be/ZDR7-iSuwkQ
# Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
# Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
# Generate PDF with Python - Reportlab - Create Charts: https://youtu.be/FcZ9wTGmMrw

# Other cool videos
# Run Python Script from Excel VBA: https://youtu.be/Z4SC53VZh-w
# Run Python Script from Excel VBA - Part 2: https://youtu.be/4Z9via5_q9k
# Run Python Script from Excel VBA - Part 3.1: https://youtu.be/PoEnWr6c1cM
# Run Python Script from Excel VBA - Part 3.2: https://youtu.be/Tkk0aedRyU4
# 
# 
# Basic Python KeyLogger: https://youtu.be/AS4PnrWv-f4
# Convert .py into .exe: https://youtu.be/CftCQYNb7B4
# Image to Text with Python - pytesseract: https://youtu.be/4DrCIVS5U3Y
# Speech to Text with Python: https://youtu.be/If2HJ23zP2U
# Weather Forecast with Python: https://youtu.be/O9G4vBsiV40
# Search Movie with Python - IMDbPY: https://youtu.be/vzOdCPV7zvs
# Generate and Read QR Code with Python: https://youtu.be/2QK942FPCw0
# Run JavaScript from Python: https://youtu.be/ByjpBvpPp8Q
# Run Python in Browser - Brython: https://youtu.be/dFNXwq5kmNk
# Hide Text in Image with Python - Stegano: https://youtu.be/IhXbJfLCst0
# HTML to PDF with Python: https://youtu.be/m3u3oLgDcJI
# Web Scraping with Python - BeautifulSoup: https://youtu.be/Jnn2kIqPH7o
# Generate Excel with Python - OpenPyXL: https://youtu.be/KNdqnIpl2UE
# Translate Text with Python - googletrans: https://youtu.be/yRFkI8miPHA
# Convert Python 2 to Python 3 Code - 2to3: https://youtu.be/t0v4F396_nc
# Face Detection with Python - OpenCV: https://youtu.be/FeUAmWZ7Clw
# Run Python Script in LibreOffice: https://youtu.be/3Ef_ordyWQs
# Generate Excel with Python - xlwings: https://youtu.be/sGvMLmLOH5g
# 
# and Playlists:
# Python Pandas: https://www.youtube.com/playlist?list=PLOGAj7tCqHx_c5uWrZX4ykdujODcqczmQ
# Python and SQL Server: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9Add6MWzl_5Wbix9V1OjSx
# Numpy Exercises: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9eQjST2RV-_Py3EJHqRq0C
# ASP.NET Web API C#: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9n-_d3YKwLJr-uHkmKZyih

from reportlab.lib.pagesizes import A4

from reportlab.platypus import Table
from reportlab.platypus import TableStyle

from reportlab.pdfgen import canvas

# #################>
# Our code imports
from header import genHeaderTable
from body import genBodyTable
from footer import genFooterTable
from styles import styles

# ##########################
# Register fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# register imported fonts
pdfmetrics.registerFont(
    TTFont('fontSE', './fonts/SpecialElite.ttf')
)
pdfmetrics.registerFont(
    TTFont('fontSPB', './fonts/SansPosterBold.ttf')
)
pdfmetrics.registerFont(
    TTFont('fontSC', './fonts/Sin City.ttf')
)
pdfmetrics.registerFont(
    TTFont('fontLG', './fonts/LuckiestGuy.ttf')
)

# #################
# Create PDF
pdf = canvas.Canvas('report.pdf')
# Set the size of a A4 page
pdf.pagewidth = A4[0]
pdf.pageheight = A4[1]

pdf.setTitle('Joker Cat Report')

# #################
# document margins
MARGIN_LEFT = MARGIN_RIGHT = 40
MARGIN_TOP = MARGIN_BOTTOM = 20

# mainTable sizes
MT_WIDTH = A4[0] - (MARGIN_LEFT + MARGIN_RIGHT)
MT_HEIGHT = A4[1] - (MARGIN_TOP + MARGIN_BOTTOM)

HT_HEIGHT = MT_HEIGHT * 15 / 100 # 15% of MT_HEIGHT
BT_HEIGHT = MT_HEIGHT * 80 / 100 # 80% of MT_HEIGHT
FT_HEIGHT = MT_HEIGHT * 5 / 100  # 5% of MT_HEIGHT

# For a better understanding of this code please see:
# Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
mainTable = Table(
    [   # Tables inside tables
        [genHeaderTable(MT_WIDTH, HT_HEIGHT)], # from header.py
        [genBodyTable(MT_WIDTH, BT_HEIGHT)],   # from body.py
        [genFooterTable(MT_WIDTH, FT_HEIGHT)], # from footer.py
    ],
    MT_WIDTH,
    [HT_HEIGHT, BT_HEIGHT, FT_HEIGHT]
)

# For a better understanding of this code please see:
# Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
# Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
mainTable.setStyle([
    #styles.GRID_BLACK_T1_ALL,

    styles.LEFT_PADDING_ZERO_ALL, # from styles.py
    styles.BOTTOM_PADDING_ZERO_ALL,
])

mainTable.wrapOn(pdf, 0, 0)
mainTable.drawOn(pdf, MARGIN_LEFT, MARGIN_BOTTOM)

# ##########################
# Draw lines
from reportlab.lib import colors

pdf.setStrokeColor(colors.cadetblue)
pdf.setLineWidth(10)

# top horizontal line
pdf.line(
    0,                  # x1 - start point
    pdf.pageheight - 10,# y1 - start point
    pdf.pagewidth,      # x2 - end point
    pdf.pageheight - 10,# y2 - end point
)
# left vertical line
pdf.line(
    10, 
    0, 
    10,
    pdf.pageheight,
)
pdf.setStrokeColor(colors.yellow)
# right vertical line
pdf.line(
    pdf.pagewidth - 10, 
    0, 
    pdf.pagewidth - 10,
    pdf.pageheight,
)
# bottom horizontal line
pdf.line(
    0, 
    10, 
    pdf.pagewidth,
    10,
)

pdf.save()