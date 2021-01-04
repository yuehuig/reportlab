# Other videos:
# Generate PDF with Python - Reportlab: https://youtu.be/ZDR7-iSuwkQ
# Generate PDF with Python - Reportlab - Create Table: https://youtu.be/B3OCXBL4Hxs
# Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
# Generate PDF with Python - Reportlab - Create Charts: https://youtu.be/FcZ9wTGmMrw
# Generate PDF with Python - Reportlab - Joker Cat Report demo: https://youtu.be/SDeOPyhO26M
# Generate PDF with Python - Reportlab - Secret Services Survey - Preview: https://youtu.be/AviWgFXFTls
# Generate PDF with Python - Reportlab - Secret Services Survey Demo - https://youtu.be/-7T1UitpBsw
# 
# Run Python Script from Excel VBA: https://youtu.be/Z4SC53VZh-w
# Run Python Script from Excel VBA - Part 2: https://youtu.be/4Z9via5_q9k
# Run Python Script from Excel VBA - Part 3.1: https://youtu.be/PoEnWr6c1cM
# Run Python Script from Excel VBA - Part 3.2: https://youtu.be/Tkk0aedRyU4
# 
# Run Python Script from SQL Server - Hello World - https://youtu.be/QEMKYY3dgcg
# Run Python Script from SQL Server - Parameters - https://youtu.be/RMtT-yVY1TQ
# Run Python Script from SQL Server - Pandas Example - https://youtu.be/yJnAgE2RSVs
# Run Python Script from SQL Server - Plot Example - https://youtu.be/fdELWosVom8
# Python - Rolling Mean and Standard Deviation - Part 1 - https://youtu.be/vksOaLODyj8
# Python - Rolling Mean and Standard Deviation - Part 2 - https://youtu.be/eVfsiRkv2E8

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
# RESTful Web Service - Hello World - Java Spring: https://youtu.be/RXkLlq8YxeM
# 
# ASP.NET Web API intro and Hello World - https://youtu.be/RJpBix5s3BY
# ASP.NET Web API - Controllers - https://youtu.be/nlFVQddx1wc
# ASP.NET Web API - Routing - https://youtu.be/2GvX8puS2is
# ASP.NET Web API - Parameter Binding - https://youtu.be/LuFoVFeEBPw
# ASP.NET Web API - File Uploading - https://youtu.be/MzDQALXH-SI
# ASP.NET Web API - Client Console App - https://youtu.be/Ry45EkZQ2CM
# ASP.NET Web API - BSON - https://youtu.be/BXnfCMcERaw
# ASP.NET Web API - Action Results - https://youtu.be/W80Vflesu8s
# ASP.NET Web API - Content Negotiation - https://youtu.be/vdKF1WTYVq0
# ASP.NET Web API - Media Type Formatters - https://youtu.be/SGeudFDlvCI
# ASP.NET Web API - Action Filters - https://youtu.be/x7kZJf416J4
# ASP.NET Web API - Model Validation - https://youtu.be/sN3qYlxr_vA
# ASP.NET Web API - Save File in SQL Server with ADO.NET - https://youtu.be/LixIRqhzUNQ
# ASP.NET Web API - File Downloading - https://youtu.be/bS_bXsT0kq4
# ASP.NET Web API - Get File from SQL Server with ADO.NET - https://youtu.be/zxPVmGpX07I
# ASP.NET Web API - Save File in SQL Server with Entity Framework - https://youtu.be/JYPaOO_fCug
# ASP.NET Web API - Get File from SQL Server with Entity Framework - https://youtu.be/QxOeuuosgH4
# ASP.NET Web API - Exception Filters - https://youtu.be/1x0s0K3w3Z4
# 
# Playlists:
# Python Pandas: https://www.youtube.com/playlist?list=PLOGAj7tCqHx_c5uWrZX4ykdujODcqczmQ
# Numpy Exercises: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9eQjST2RV-_Py3EJHqRq0C
# Swift: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9C08vyhSMciLtkMSPiirYr
# JavaScript: https://www.youtube.com/playlist?list=PLOGAj7tCqHx_grLMl0A0yC8Ts_ErJMJft
# c#: https://www.youtube.com/playlist?list=PLOGAj7tCqHx9H5dGNA4TGkmjKGOfiR4gk
# Java: https://www.youtube.com/playlist?list=PLOGAj7tCqHx-ey9xikbXOfGdbvcOielRw

from reportlab.lib.pagesizes import A4, landscape

from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

# #################>
# Our code imports
from styles import styles           # from styles.py
from header import genHeaderTable   # from header.py
from body import genBodyTable       # from body.py
from footer import genFooterTable   # from footer.py

# ##########################
# Register fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(
    TTFont('barText', './fonts/SaucerBB.ttf')
)
pdfmetrics.registerFont(
    TTFont('chartTitle', './fonts/PG_Roof Runners_active.ttf')
)

# #################
# Create PDF
pdf = canvas.Canvas('report.pdf', pagesize=landscape(A4))

pdf.setTitle('World Today Magazine')

width = A4[1]
height = A4[0]

# draw top black portion of page
# For a better understand of this coordinates please see code guide
pdf.ellipse(
    width / 2 * -1, height - height / 3, # x1 and y1 coordinates of enclosing rectangle
    width + 50, height + height / 4,     # x2 and y2 coordinates of enclosing rectangle
    stroke=1, fill=1
)

# #################
# document margins
MARGIN_LEFT = MARGIN_RIGHT = 40
MARGIN_TOP = MARGIN_BOTTOM = 20

# mainTable sizes
MT_WIDTH = A4[1] - (MARGIN_LEFT + MARGIN_RIGHT)
MT_HEIGHT = A4[0] - (MARGIN_TOP + MARGIN_BOTTOM)

heightList = [
    MT_HEIGHT * 20 / 100,   # 20% of MT_HEIGHT
    MT_HEIGHT * 75 / 100,   # 75% of MT_HEIGHT
    MT_HEIGHT * 5 / 100,    # 5% of MT_HEIGHT
]

# For a better understanding of this code please see:
# Generate PDF with Python - Reportlab - Create Table - Part 2: https://youtu.be/r--iZCQbxzE
mainTable = Table([
    [genHeaderTable(MT_WIDTH, heightList[0])],  # from header.py
    [genBodyTable(MT_WIDTH, heightList[1])],    # from body.py
    [genFooterTable(MT_WIDTH, heightList[2])],  # from footer.py
],
MT_WIDTH,
heightList)

mainTable.setStyle([
    #styles.GRID_RED_ALL, # useful for debug

    styles.BOTTOM_PADDING_ZERO_ALL,
    styles.LEFT_PADDING_ZERO_ALL,
])

mainTable.wrapOn(pdf, 0, 0)
mainTable.drawOn(pdf, MARGIN_LEFT, MARGIN_BOTTOM)

# save the document
pdf.save()