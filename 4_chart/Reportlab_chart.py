from reportlab.graphics.charts.legends import Legend
from reportlab.lib.validators import Auto
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import (
    VerticalBarChart
)
from reportlab.platypus import Table

fileName = 'pdfTable.pdf'

pdf = SimpleDocTemplate(fileName, pageSize = letter)

def getVerticalBarChart():
    data = [
        (3, 18, 20),
        (14, 12, 21)
    ]

    chart = VerticalBarChart()
    chart.data = data

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 25
    chart.valueAxis.valueStep = 5

    chart.x = 5
    chart.y = 5

    chart.width = 240
    chart.height = 100

    chart.strokeColor = colors.black
    chart.fillColor = colors.yellow

    chart.groupSpacing = 0
    chart.categoryAxis.categoryNames = [
        'A', 'B', 'C'
    ]

    title = String(
        50, 110,
        'Vertical Bar Chart',
        fontSize = 14
    )

    drawing = Drawing(240, 120)
    drawing.add(title)
    drawing.add(chart)

    return drawing

from reportlab.graphics.charts.piecharts import (
    Pie
)

def getPieChart():
    data = [3, 18, 20]
    chart = Pie()
    chart.data = data
    chart.x = 50
    chart.y = 5

    chart.labels = [
        'A', 'B', 'C'
    ]
    title = String(
        50, 110,
        'Pie Chart',
        fontSize = 14
    )

    chart.sideLabels = True
    chart.slices[0].fillColor = colors.red
    chart.slices[0].popout = 8

    legend = Legend()
    legend.x = 180
    legend.y = 80
    legend.alignment = 'right'
    legend.colorNamePairs = Auto(obj=chart)

    drawing = Drawing(240, 120)
    drawing.add(title)
    drawing.add(chart)
    drawing.add(legend)
    return drawing

from reportlab.graphics.charts.linecharts import (
    HorizontalLineChart
)
def getLineChart():
    data = [
        (4, 2, 7),
        (7, 8, 6)
    ]

    chart = HorizontalLineChart()
    chart.data = data
    chart.x = 5
    chart.y = 5
    chart.width = 240
    chart.height = 100

    chart.categoryAxis.categoryNames = [
        'A', 'B', 'C'
    ]
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 10
    chart.valueAxis.valueStep = 2

    chart.lines[0].strokeWidth = 3.5
    chart.lines[1].strokeWidth = 1
    chart.lines[0].strokeColor = colors.purple

    title = String(
        50, 110,
        'Line Chart',
        fontSize = 14
    )

    drawing = Drawing(240, 120)
    drawing.add(title)
    drawing.add(chart)
    return drawing

from reportlab.graphics.charts.lineplots import (
    LinePlot
)
from reportlab.graphics.widgets.markers import (
    makeMarker
)

def getLineChartWithMarkers():
    data = [
        ((2, 3), (3, 2), (5, 3)),
        ((2, 6), (3, 4), (4, 3), (5, 1))
    ]

    chart = LinePlot()
    chart.data = data
    chart.x = 5
    chart.y = 5
    chart.width = 240
    chart.height = 100

    chart.fillColor = colors.yellowgreen

    chart.lines[0].strokeWidth = 3.5
    chart.lines[1].strokeWidth = 1
    chart.lines[0].strokeColor = colors.brown

    chart.xValueAxis.valueMin = 1
    chart.xValueAxis.valueMax = 6
    chart.yValueAxis.valueMin = 1
    chart.yValueAxis.valueMax = 7

    chart.lines[0].symbol = makeMarker('Diamond')
    chart.lines[0].symbol.fillColor = colors.pink
    chart.lines[1].symbol = makeMarker(
        'EU_Flag',  # 'Triangle',
        fillColor=colors.red
    )

    title = String(
        50, 110,
        'Line Plot Chart',
        fontSize=14
    )

    drawing = Drawing(240, 120)
    drawing.add(title)
    drawing.add(chart)
    return drawing

barChart = getVerticalBarChart()
pieChart = getPieChart()
lineChart = getLineChart()
lineChartMarkers = getLineChartWithMarkers()

table = Table([
    [barChart, pieChart],
    [lineChart, lineChartMarkers]
], 270, 150)

table.setStyle([
    ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
    ('VALIGN', (0, 0), (-1, -1), "CENTER"),
    ('ALIGN', (0, 0), (-1, -1), "CENTER"),
])

elements = []
elements.append(table)

pdf.build(elements)