from reportlab.pdfgen import canvas

# ###################################
# Help
def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')








# ###################################
# Content
fileName = 'MyDoc.pdf'
documentTitle = 'Document title!'
title = 'Tasmanian devil'
subTitle = 'The largest carnivorous marsupial'

textLines = [
'The Tasmanian devil (Sarcophilus harrisii) is',
'a carnivorous marsupial of the family',
'Dasyuridae.'
]

image = 'tasmanianDevil.jpg'


# ###################################
# 0) Create document
pdf = canvas.Canvas(fileName)
pdf.setTitle(title)

drawMyRuler(pdf)

# 获取已经有的font
for font in pdf.getAvailableFonts():
    print(font)

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('abc', 'SakBunderan.ttf'))
pdf.setFont('abc', 36)
# pdf.drawString(270, 770, title)
pdf.drawCentredString(300, 770, title)

pdf.setFillColorRGB(0, 0, 255)
pdf.setFont('Courier-Bold', 24)
pdf.drawCentredString(290, 720, subTitle)

pdf.line(30, 710, 550, 710)

from reportlab.lib import colors

text = pdf.beginText(40, 680)
text.setFont('Courier', 18)
text.setFillColor(colors.red)

for line in textLines:
    text.textLine(line)

pdf.drawText(text)

pdf.drawInlineImage(image, 130, 400)

pdf.save()