#!/usr/bin/env python

__author__ = 'Baumfaust'

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import QRect, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QColor

from ui_main import Ui_MainWindow
from getthefish import GetTheFish

class ThreadRunner(QThread):
    def __init__(self, object):
        QThread.__init__(self)
        self.fish = object

    def run(self):
        self.fish.run = True
        self.fish.fishing()

    def stopFishing(self):
        self.fish.run = False

class ScreenshotWidget(QWidget):
    colorPicked = pyqtSignal()

    def __init__(self):
        super(ScreenshotWidget, self).__init__()
        layout = QHBoxLayout()
        label = QLabel()
        pixmap = QPixmap("img.png")
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    def getBobberColor(self):
        return self.color

    def mousePressEvent(self, event):
        pos = event.pos()
        pm = self.grab(QRect(pos.x(), pos.y(), 1, 1))
        i = pm.toImage()
        self.color = QColor(i.pixel(0, 0))
        self.colorPicked.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.screenshotWidget = None
        color = QColor(72, 41, 12).name(QColor.HexRgb)
        self.ui.hexColorLabel.setText(color)
        self.ui.bobberColorLabel.setStyleSheet("QLabel { background-color : " + color + "; }")

        self.fish = GetTheFish()
        self.fish.gui = True
        self.thread = ThreadRunner(self.fish)
        self.ui.colorButton.clicked.connect(self.openScreenshot)
        self.ui.startButton.clicked.connect(self.toggleFishing)
        self.ui.thresholdBobberSpinBox.valueChanged.connect(self.guiUpdated)
        self.ui.thresholdCatchSpinBox.valueChanged.connect(self.guiUpdated)
        self.ui.jumpToBobberCheck.stateChanged.connect(self.guiUpdated)
        self.ui.verboseCheck.stateChanged.connect(self.guiUpdated)
        self.updateGui()


    def updateGui(self):
        self.ui.thresholdBobberSpinBox.setValue(self.fish.fishConfig.thresholdBobber)
        self.ui.thresholdCatchSpinBox.setValue(self.fish.fishConfig.thresholdCatch)
        print("updateGui " + str(self.fish.fishConfig.jumpToBobber))
        self.ui.jumpToBobberCheck.setChecked(self.fish.fishConfig.jumpToBobber)
        self.ui.verboseCheck.setChecked(self.fish.fishConfig.verbose)

    def guiUpdated(self):
        self.fish.fishConfig.thresholdBobber = self.ui.thresholdBobberSpinBox.value()
        self.fish.fishConfig.thresholdCatch = self.ui.thresholdCatchSpinBox.value()
        self.fish.fishConfig.jumpToBobber = self.ui.jumpToBobberCheck.isChecked()
        self.fish.fishConfig.verbose = self.ui.verboseCheck.isChecked()
        self.fish.save()

    def toggleFishing(self):
        if self.thread.isRunning():
            self.thread.stopFishing()
            self.ui.startButton.setText("Start")
        else:
            self.thread.start()
            self.ui.startButton.setText("Stop")

    def bobberColorPicked(self):
        color = QColor( self.screenshotWidget.getBobberColor()).name(QColor.HexRgb)
        self.ui.hexColorLabel.setText(color)
        self.ui.bobberColorLabel.setStyleSheet("QLabel { background-color : " + color + "; }")

    def openScreenshot(self):
        self.screenshotWidget = ScreenshotWidget()
        self.screenshotWidget.colorPicked.connect(self.bobberColorPicked)




    # def mousePressEvent(self, event):
    #     self.origin = event.pos()
    #     if not self.rubberBand:
    #         self.rubberBand = QRubberBand(QRubberBand.Rectangle, None)
    #     self.rubberBand.setGeometry(QRect(self.origin, QSize()))
    #     self.rubberBand.show()
    #
    # def mouseMoveEvent(self, event):
    #     if self.rubberBand:
    #         self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

        #super(PieView, self).mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     #super(PieView, self).mouseReleaseEvent(event)
    #
    #     if self.rubberBand:
    #         self.rubberBand.hide()


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    try:
        sys.exit(app.exec_())
    except:
        pass
