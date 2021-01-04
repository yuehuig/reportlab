# List of Lists
data = [
    ['Dedicated Hosting', 'VPS Hosting', 'Sharing Hosting', 'Reseller Hosting'],
    ['€200/Month', '€100/Month', '€20/Month', '€50/Month'],
    ['Free Domain', 'Free Domain', 'Free Domain', 'Free Domain'],
    ['2GB DDR2', '20GB Disc Space', 'Unlimited Email', 'Unlimited Email']
]

fileName = 'pdfTable.pdf'

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

pdf = SimpleDocTemplate(fileName, pageSize=letter)

from reportlab.platypus import Table

table = Table(data)

from reportlab.platypus import TableStyle
from reportlab.lib import colors

style = TableStyle([
    ('BACKGROUND', (0, 0), (3, 0), colors.green),
    ('TEXTCOLOR', (0, 0), (3, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
])

table.setStyle(style)

runNumb = len(data)
for i in range(1, runNumb):
    if i % 2 == 0:
        bc = colors.burlywood
    else:
        bc = colors.beige

    ts = TableStyle([
        ('BACKGROUND', (0, i), (-1, i), bc),
        ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),
        ('GRID', (0, 1), (-1, -1), 2, colors.black),
    ])
    table.setStyle(ts)

# 添加边框
ts = TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)])
table.setStyle(ts)

elements = []
elements.append(table)

pdf.build(elements)