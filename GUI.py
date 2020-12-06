from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor
from PyQt5.QtCore import Qt, QPoint


class Window(QMainWindow):

    def __init__(self, data, glob):
        super().__init__()
        self.title = "CHUJ"

        self.data = data
        self.glob = glob

        self.top = 150
        self.left = 150
        self.width = 1550
        self.height = 1100

        self.setStyleSheet("background-color: #211e1e;")

        self.InitWindow()

    def InitWindow(self):
        '''Initialization the size and name of the window'''
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        '''Inserting objects into window'''
        painter = QPainter(self)

        painter.setBrush(QBrush(QColor(227, 91, 0),  Qt.SolidPattern))
        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        painter.drawRect(80, 400, 140, 100)

        painter.drawRect(580, 400, 140, 100)
        painter.drawRect(830, 400, 140, 100)

        painter.drawRect(1330, 400, 140, 100)
        painter.drawRect(1080, 400, 140, 100)
        painter.drawRect(330, 200, 140, 100)
        painter.drawRect(1080, 200, 140, 100)
        painter.drawRect(705, 10, 140, 100)
        painter.drawRect(705, 200, 140, 100)
        painter.drawRect(330, 400, 140, 100)

        painter.drawRect(1210, 600, 140, 100)
        painter.drawRect(705, 600, 140, 100)
        painter.drawRect(205, 600, 140, 100)

        painter.drawRect(1210, 710, 140, 100)
        painter.drawRect(705, 710, 140, 100)
        painter.drawRect(205, 710, 140, 100)

        painter.drawRect(705, 880, 140, 100)

        painter.drawLine(400, 300, 150, 400)
        painter.drawLine(775, 300, 650, 400)
        painter.drawLine(1150, 300, 1150, 400)
        painter.drawLine(775, 300, 900, 400)
        painter.drawLine(1150, 300, 1400, 400)
        painter.drawLine(400, 200, 775, 110)
        painter.drawLine(775, 200, 775, 110)
        painter.drawLine(1150, 200, 775, 110)
        painter.drawLine(400, 300, 400, 400)

        painter.drawLine(275, 710, 275, 700)
        painter.drawLine(775, 710, 775, 700)
        painter.drawLine(1280, 710, 1280, 700)

        painter.drawLine(775, 880, 275, 810)
        painter.drawLine(775, 880, 775, 810)
        painter.drawLine(775, 880, 1275, 810)

        painter.drawLine(650, 500, 775, 600)
        painter.drawLine(1150, 500, 1275, 600)
        painter.drawLine(150, 500, 275, 600)

        painter.drawLine(900, 500, 775, 600)
        painter.drawLine(1400, 500, 1275, 600)
        painter.drawLine(400, 500, 275, 600)

        self.drawText(event, painter)

    def drawText(self, event, painter):
        '''Inserting text and computing values into window'''

        painter.setFont(QFont('Arial', 11))

        painter.drawText(QPoint(710, 72), 'P(H): ' + str(self.data.iloc[0, 3]))

        painter.drawText(QPoint(335, 260), 'P(E_x): ' + str(self.data.iloc[0, 0]))
        painter.drawText(QPoint(710, 260), 'P(E_p): ' + str(self.data.iloc[1, 0]))
        painter.drawText(QPoint(1085, 260), 'P(E_t): ' + str(self.data.iloc[2, 0]))

        painter.drawText(QPoint(85, 462), 'P(H|E_x): ' + str(self.data.iloc[0, 1]))
        painter.drawText(QPoint(335, 462), 'P(H|~E_x): ' + str(self.data.iloc[0, 2]))

        painter.drawText(QPoint(585, 462), 'P(H|E_p): ' + str(self.data.iloc[1, 1]))
        painter.drawText(QPoint(835, 462), 'P(H|~E_p): ' + str(self.data.iloc[1, 2]))

        painter.drawText(QPoint(1085, 462), 'P(H|E_t): ' + str(self.data.iloc[2, 1]))
        painter.drawText(QPoint(1335, 462), 'P(H|~E_t): ' + str(self.data.iloc[2, 2]))

        painter.drawText(QPoint(210, 662), 'P(E|E`x): ' + str(self.data.iloc[0, 7]))
        painter.drawText(QPoint(710, 662), 'P(E|E`p): ' + str(self.data.iloc[1, 7]))
        painter.drawText(QPoint(1215, 662), 'P(E|E`t): ' + str(self.data.iloc[2, 7]))

        painter.drawText(QPoint(210, 770), 'P(H|E`x): ' + str(self.data.iloc[0, 8]))
        painter.drawText(QPoint(710, 770), 'P(H|E`p): ' + str(self.data.iloc[1, 8]))
        painter.drawText(QPoint(1215, 770), 'P(H|E`t): ' + str(self.data.iloc[2, 8]))

        painter.drawText(QPoint(710, 942), 'GLOB: ' + str(self.glob))



