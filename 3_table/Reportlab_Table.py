from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import Image

import datetime

class Pin:
	title = ''
	refNo = ''
	PIN = ''
	serialNo = ''
	date = datetime.datetime.now()
	picPath = ''

def getPins():
    pin1 = Pin()
    pin1.title = 'Popeye'
    pin1.refNo = 'wer-2'
    pin1.PIN = '5498-6438-9951-91435'
    pin1.serialNo = '07347153284647310'
    pin1.date = datetime.datetime(2019, 12, 31, 22, 38, 44, 100000)
    pin1.picPath = './resources/popeye.jpg'

    pin2 = Pin()
    pin2.title = 'He-Man'
    pin2.refNo = 'wer-6'
    pin2.PIN = '7131-6411-8451-92495'
    pin2.serialNo = '21047053904655310'
    pin2.date = datetime.datetime(2019, 7, 23, 20, 12, 37, 100000)
    pin2.picPath = './resources/heman.jpg'

    pin3 = Pin()
    pin3.title = 'Johnny Bravo'
    pin3.refNo = 'wer-5'
    pin3.PIN = '0029-6435-7422-42940'
    pin3.serialNo = '87027653903475601'
    pin3.date = datetime.datetime(2019, 8, 7, 17, 52, 18, 100000)
    pin3.picPath = './resources/johnnyBravo.jpg'

    pin4 = Pin()
    pin4.title = 'Son Goku'
    pin4.refNo = 'wer-9'
    pin4.PIN = '0536-4441-3422-83701'
    pin4.serialNo = '38122657903475000'
    pin4.date = datetime.datetime(2019, 6, 13, 19, 31, 39, 100000)
    pin4.picPath = './resources/songoku.jpg'

    return [pin1,pin2,pin3,pin4]

fileName = 'pdfTable.pdf'

pdf = SimpleDocTemplate(fileName, pageSize = letter)

fonts = canvas.Canvas('abc').getAvailableFonts()
for font in fonts:
    print(font)

def genPinTable(pin):
    pinElemTable = None
    pinElemWidth = 250

    titleTable = Table([
        [pin.title]
    ], pinElemWidth)

    refNoTable = Table([
        ['Ref.No:', pin.refNo, 'N 100'],
    ], [60, 120, 70])

    pinTable = Table([
        ['PIN', pin.PIN],
    ], [60, 190])

    serialTable = Table([
        ['Serial No.:', pin.serialNo],
    ], [60])

    dateTable = Table([
        [
            'Date:',
            pin.date.strftime('%m/%d/%Y'),
            pin.date.strftime('%I:%M:%S %p'),
        ]
    ], [60])

    serialDateTable = Table([
        [serialTable],
        [dateTable]
    ])

    picture = Image(pin.picPath)
    picture.drawWidth = 30
    picture.drawHeight = 30
    pictureTable = Table([
        [picture]
    ], 30, 30)

    serialDatePictureTable = Table([
        [serialDateTable, pictureTable]
    ], [190, 50])

    pinElemTable = Table([
        [titleTable],
        [refNoTable],
        [pinTable],
        [serialDatePictureTable]
    ], pinElemWidth)

#tablestyle
    titleTableStyle = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 0),
    ])
    titleTable.setStyle(titleTableStyle)

    refNoTableStyle = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 0),
    ])
    refNoTable.setStyle(refNoTableStyle)

    pinTableStyle = TableStyle([
        ('FONTSIZE', (1, 0), (-1, 0), 13),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, 0), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 0),
    ])
    pinTable.setStyle(pinTableStyle)

    serialTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 0),
    ])
    serialTable.setStyle(serialTableStyle)

    dateTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 2),
    ])
    dateTable.setStyle(dateTableStyle)

    serialDateTableStyle = TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTOOMPADDING', (0, 0), (-1, -1), 0),

        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ])
    serialDateTable.setStyle(serialDateTableStyle)

    picTableStyle = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 15),

        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ])
    pictureTable.setStyle(picTableStyle)

    serialDatePicTableStyle = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),

        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    serialDatePictureTable.setStyle(serialDatePicTableStyle)

    pinElemTableStyle = TableStyle([
        ('BOX', (0, 0), (-1, -1), 3, colors.black),

        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ])
    pinElemTable.setStyle(pinElemTableStyle)

    return pinElemTable

elements = []
pins = getPins()
pinTb0 = genPinTable(pins[0])
pinTb1 = genPinTable(pins[1])
pinTb2 = genPinTable(pins[2])
pinTb3 = genPinTable(pins[3])
mainTable = Table([
    [pinTb0, pinTb1],
    [pinTb2, pinTb3]
])
elements.append(mainTable)

pdf.build(elements)