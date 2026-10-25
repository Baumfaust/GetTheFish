# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

from getthefish.gui.widgets import (BiteMeter, PreviewView)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1040, 680)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(8)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(12, 12, 12, 12)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(8)
        self.headerLayout.setObjectName(u"headerLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerLayout.addWidget(self.titleLabel)

        self.stateLabel = QLabel(self.centralwidget)
        self.stateLabel.setObjectName(u"stateLabel")

        self.headerLayout.addWidget(self.stateLabel)

        self.headerSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.themeButton = QPushButton(self.centralwidget)
        self.themeButton.setObjectName(u"themeButton")
        self.themeButton.setFlat(True)
        self.themeButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.headerLayout.addWidget(self.themeButton)

        self.viewButton = QPushButton(self.centralwidget)
        self.viewButton.setObjectName(u"viewButton")
        self.viewButton.setFlat(True)
        self.viewButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.headerLayout.addWidget(self.viewButton)


        self.mainLayout.addLayout(self.headerLayout)

        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName(u"pages")
        self.fullPage = QWidget()
        self.fullPage.setObjectName(u"fullPage")
        self.fullLayout = QHBoxLayout(self.fullPage)
        self.fullLayout.setSpacing(12)
        self.fullLayout.setObjectName(u"fullLayout")
        self.fullLayout.setContentsMargins(0, 0, 0, 0)
        self.leftColumn = QVBoxLayout()
        self.leftColumn.setSpacing(4)
        self.leftColumn.setObjectName(u"leftColumn")
        self.setupGroup = QGroupBox(self.fullPage)
        self.setupGroup.setObjectName(u"setupGroup")
        self.setupGroup.setMinimumSize(QSize(320, 0))
        self.setupGroup.setMaximumSize(QSize(320, 16777215))
        self.setupLayout = QGridLayout(self.setupGroup)
        self.setupLayout.setSpacing(8)
        self.setupLayout.setObjectName(u"setupLayout")
        self.areaLabel = QLabel(self.setupGroup)
        self.areaLabel.setObjectName(u"areaLabel")

        self.setupLayout.addWidget(self.areaLabel, 0, 0, 1, 1)

        self.areaLayout = QHBoxLayout()
        self.areaLayout.setObjectName(u"areaLayout")
        self.posStartLabel = QLabel(self.setupGroup)
        self.posStartLabel.setObjectName(u"posStartLabel")

        self.areaLayout.addWidget(self.posStartLabel)

        self.areaArrowLabel = QLabel(self.setupGroup)
        self.areaArrowLabel.setObjectName(u"areaArrowLabel")

        self.areaLayout.addWidget(self.areaArrowLabel)

        self.posEndLabel = QLabel(self.setupGroup)
        self.posEndLabel.setObjectName(u"posEndLabel")

        self.areaLayout.addWidget(self.posEndLabel)

        self.areaSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.areaLayout.addItem(self.areaSpacer)


        self.setupLayout.addLayout(self.areaLayout, 0, 1, 1, 1)

        self.areaButton = QPushButton(self.setupGroup)
        self.areaButton.setObjectName(u"areaButton")

        self.setupLayout.addWidget(self.areaButton, 0, 2, 1, 1)

        self.bobberLabel = QLabel(self.setupGroup)
        self.bobberLabel.setObjectName(u"bobberLabel")

        self.setupLayout.addWidget(self.bobberLabel, 1, 0, 1, 1)

        self.colorLayout = QHBoxLayout()
        self.colorLayout.setObjectName(u"colorLayout")
        self.bobberColorLabel = QLabel(self.setupGroup)
        self.bobberColorLabel.setObjectName(u"bobberColorLabel")
        self.bobberColorLabel.setMinimumSize(QSize(18, 18))
        self.bobberColorLabel.setMaximumSize(QSize(18, 18))

        self.colorLayout.addWidget(self.bobberColorLabel)

        self.hexColorLabel = QLabel(self.setupGroup)
        self.hexColorLabel.setObjectName(u"hexColorLabel")

        self.colorLayout.addWidget(self.hexColorLabel)

        self.colorSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.colorLayout.addItem(self.colorSpacer)


        self.setupLayout.addLayout(self.colorLayout, 1, 1, 1, 1)

        self.colorButton = QPushButton(self.setupGroup)
        self.colorButton.setObjectName(u"colorButton")

        self.setupLayout.addWidget(self.colorButton, 1, 2, 1, 1)

        self.castKeyLabel = QLabel(self.setupGroup)
        self.castKeyLabel.setObjectName(u"castKeyLabel")

        self.setupLayout.addWidget(self.castKeyLabel, 2, 0, 1, 1)

        self.castKeyEdit = QLineEdit(self.setupGroup)
        self.castKeyEdit.setObjectName(u"castKeyEdit")
        self.castKeyEdit.setMaxLength(20)

        self.setupLayout.addWidget(self.castKeyEdit, 2, 1, 1, 2)


        self.leftColumn.addWidget(self.setupGroup)

        self.tuningGroup = QGroupBox(self.fullPage)
        self.tuningGroup.setObjectName(u"tuningGroup")
        self.tuningGroup.setMinimumSize(QSize(320, 0))
        self.tuningGroup.setMaximumSize(QSize(320, 16777215))
        self.tuningLayout = QGridLayout(self.tuningGroup)
        self.tuningLayout.setSpacing(8)
        self.tuningLayout.setObjectName(u"tuningLayout")
        self.thresholdBobberLabel = QLabel(self.tuningGroup)
        self.thresholdBobberLabel.setObjectName(u"thresholdBobberLabel")

        self.tuningLayout.addWidget(self.thresholdBobberLabel, 0, 0, 1, 1)

        self.thresholdBobberSpinBox = QSpinBox(self.tuningGroup)
        self.thresholdBobberSpinBox.setObjectName(u"thresholdBobberSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thresholdBobberSpinBox.sizePolicy().hasHeightForWidth())
        self.thresholdBobberSpinBox.setSizePolicy(sizePolicy)
        self.thresholdBobberSpinBox.setMinimumSize(QSize(120, 0))
        self.thresholdBobberSpinBox.setMaximumSize(QSize(120, 16777215))

        self.tuningLayout.addWidget(self.thresholdBobberSpinBox, 0, 1, 1, 1)

        self.thresholdCatchLabel = QLabel(self.tuningGroup)
        self.thresholdCatchLabel.setObjectName(u"thresholdCatchLabel")

        self.tuningLayout.addWidget(self.thresholdCatchLabel, 1, 0, 1, 1)

        self.thresholdCatchSpinBox = QSpinBox(self.tuningGroup)
        self.thresholdCatchSpinBox.setObjectName(u"thresholdCatchSpinBox")
        sizePolicy.setHeightForWidth(self.thresholdCatchSpinBox.sizePolicy().hasHeightForWidth())
        self.thresholdCatchSpinBox.setSizePolicy(sizePolicy)
        self.thresholdCatchSpinBox.setMinimumSize(QSize(120, 0))
        self.thresholdCatchSpinBox.setMaximumSize(QSize(120, 16777215))

        self.tuningLayout.addWidget(self.thresholdCatchSpinBox, 1, 1, 1, 1)

        self.jumpToBobberCheck = QCheckBox(self.tuningGroup)
        self.jumpToBobberCheck.setObjectName(u"jumpToBobberCheck")

        self.tuningLayout.addWidget(self.jumpToBobberCheck, 2, 0, 1, 2)

        self.verboseCheck = QCheckBox(self.tuningGroup)
        self.verboseCheck.setObjectName(u"verboseCheck")

        self.tuningLayout.addWidget(self.verboseCheck, 3, 0, 1, 2)


        self.leftColumn.addWidget(self.tuningGroup)

        self.startLayout = QVBoxLayout()
        self.startLayout.setObjectName(u"startLayout")
        self.startLayout.setContentsMargins(-1, 12, -1, -1)
        self.startButton = QPushButton(self.fullPage)
        self.startButton.setObjectName(u"startButton")

        self.startLayout.addWidget(self.startButton)


        self.leftColumn.addLayout(self.startLayout)

        self.logGroup = QGroupBox(self.fullPage)
        self.logGroup.setObjectName(u"logGroup")
        self.logGroup.setMinimumSize(QSize(320, 0))
        self.logGroup.setMaximumSize(QSize(320, 16777215))
        self.logLayout = QVBoxLayout(self.logGroup)
        self.logLayout.setObjectName(u"logLayout")
        self.logView = QPlainTextEdit(self.logGroup)
        self.logView.setObjectName(u"logView")
        self.logView.setReadOnly(True)
        self.logView.setMaximumBlockCount(500)

        self.logLayout.addWidget(self.logView)

        self.openConfigFolderButton = QPushButton(self.logGroup)
        self.openConfigFolderButton.setObjectName(u"openConfigFolderButton")

        self.logLayout.addWidget(self.openConfigFolderButton)


        self.leftColumn.addWidget(self.logGroup)

        self.leftColumn.setStretch(3, 1)

        self.fullLayout.addLayout(self.leftColumn)

        self.rightColumn = QVBoxLayout()
        self.rightColumn.setSpacing(4)
        self.rightColumn.setObjectName(u"rightColumn")
        self.sessionGroup = QGroupBox(self.fullPage)
        self.sessionGroup.setObjectName(u"sessionGroup")
        self.statsLayout = QHBoxLayout(self.sessionGroup)
        self.statsLayout.setSpacing(8)
        self.statsLayout.setObjectName(u"statsLayout")
        self.castsLayout = QVBoxLayout()
        self.castsLayout.setSpacing(0)
        self.castsLayout.setObjectName(u"castsLayout")
        self.castsValue = QLabel(self.sessionGroup)
        self.castsValue.setObjectName(u"castsValue")
        self.castsValue.setProperty(u"statValue", True)

        self.castsLayout.addWidget(self.castsValue)

        self.castsCaption = QLabel(self.sessionGroup)
        self.castsCaption.setObjectName(u"castsCaption")
        self.castsCaption.setProperty(u"caption", True)

        self.castsLayout.addWidget(self.castsCaption)


        self.statsLayout.addLayout(self.castsLayout)

        self.catchesLayout = QVBoxLayout()
        self.catchesLayout.setSpacing(0)
        self.catchesLayout.setObjectName(u"catchesLayout")
        self.catchesValue = QLabel(self.sessionGroup)
        self.catchesValue.setObjectName(u"catchesValue")
        self.catchesValue.setProperty(u"statValue", True)

        self.catchesLayout.addWidget(self.catchesValue)

        self.catchesCaption = QLabel(self.sessionGroup)
        self.catchesCaption.setObjectName(u"catchesCaption")
        self.catchesCaption.setProperty(u"caption", True)

        self.catchesLayout.addWidget(self.catchesCaption)


        self.statsLayout.addLayout(self.catchesLayout)

        self.missesLayout = QVBoxLayout()
        self.missesLayout.setSpacing(0)
        self.missesLayout.setObjectName(u"missesLayout")
        self.missesValue = QLabel(self.sessionGroup)
        self.missesValue.setObjectName(u"missesValue")
        self.missesValue.setProperty(u"statValue", True)

        self.missesLayout.addWidget(self.missesValue)

        self.missesCaption = QLabel(self.sessionGroup)
        self.missesCaption.setObjectName(u"missesCaption")
        self.missesCaption.setProperty(u"caption", True)

        self.missesLayout.addWidget(self.missesCaption)


        self.statsLayout.addLayout(self.missesLayout)

        self.rateLayout = QVBoxLayout()
        self.rateLayout.setSpacing(0)
        self.rateLayout.setObjectName(u"rateLayout")
        self.rateValue = QLabel(self.sessionGroup)
        self.rateValue.setObjectName(u"rateValue")
        self.rateValue.setProperty(u"statValue", True)

        self.rateLayout.addWidget(self.rateValue)

        self.rateCaption = QLabel(self.sessionGroup)
        self.rateCaption.setObjectName(u"rateCaption")
        self.rateCaption.setProperty(u"caption", True)

        self.rateLayout.addWidget(self.rateCaption)


        self.statsLayout.addLayout(self.rateLayout)

        self.perHourLayout = QVBoxLayout()
        self.perHourLayout.setSpacing(0)
        self.perHourLayout.setObjectName(u"perHourLayout")
        self.perHourValue = QLabel(self.sessionGroup)
        self.perHourValue.setObjectName(u"perHourValue")
        self.perHourValue.setProperty(u"statValue", True)

        self.perHourLayout.addWidget(self.perHourValue)

        self.perHourCaption = QLabel(self.sessionGroup)
        self.perHourCaption.setObjectName(u"perHourCaption")
        self.perHourCaption.setProperty(u"caption", True)

        self.perHourLayout.addWidget(self.perHourCaption)


        self.statsLayout.addLayout(self.perHourLayout)

        self.elapsedLayout = QVBoxLayout()
        self.elapsedLayout.setSpacing(0)
        self.elapsedLayout.setObjectName(u"elapsedLayout")
        self.elapsedValue = QLabel(self.sessionGroup)
        self.elapsedValue.setObjectName(u"elapsedValue")
        self.elapsedValue.setProperty(u"statValue", True)

        self.elapsedLayout.addWidget(self.elapsedValue)

        self.elapsedCaption = QLabel(self.sessionGroup)
        self.elapsedCaption.setObjectName(u"elapsedCaption")
        self.elapsedCaption.setProperty(u"caption", True)

        self.elapsedLayout.addWidget(self.elapsedCaption)


        self.statsLayout.addLayout(self.elapsedLayout)


        self.rightColumn.addWidget(self.sessionGroup)

        self.previewGroup = QGroupBox(self.fullPage)
        self.previewGroup.setObjectName(u"previewGroup")
        self.previewLayout = QVBoxLayout(self.previewGroup)
        self.previewLayout.setObjectName(u"previewLayout")
        self.previewView = PreviewView(self.previewGroup)
        self.previewView.setObjectName(u"previewView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.previewView.sizePolicy().hasHeightForWidth())
        self.previewView.setSizePolicy(sizePolicy1)

        self.previewLayout.addWidget(self.previewView)

        self.previewInfoLayout = QHBoxLayout()
        self.previewInfoLayout.setObjectName(u"previewInfoLayout")
        self.previewInfoLabel = QLabel(self.previewGroup)
        self.previewInfoLabel.setObjectName(u"previewInfoLabel")

        self.previewInfoLayout.addWidget(self.previewInfoLabel)

        self.previewInfoSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.previewInfoLayout.addItem(self.previewInfoSpacer)

        self.previewCheck = QCheckBox(self.previewGroup)
        self.previewCheck.setObjectName(u"previewCheck")
        self.previewCheck.setChecked(True)

        self.previewInfoLayout.addWidget(self.previewCheck)


        self.previewLayout.addLayout(self.previewInfoLayout)

        self.previewLayout.setStretch(0, 1)

        self.rightColumn.addWidget(self.previewGroup)

        self.meterGroup = QGroupBox(self.fullPage)
        self.meterGroup.setObjectName(u"meterGroup")
        self.meterLayout = QVBoxLayout(self.meterGroup)
        self.meterLayout.setObjectName(u"meterLayout")
        self.biteMeter = BiteMeter(self.meterGroup)
        self.biteMeter.setObjectName(u"biteMeter")
        self.biteMeter.setMinimumSize(QSize(0, 130))

        self.meterLayout.addWidget(self.biteMeter)


        self.rightColumn.addWidget(self.meterGroup)

        self.rightColumn.setStretch(1, 1)

        self.fullLayout.addLayout(self.rightColumn)

        self.fullLayout.setStretch(1, 1)
        self.pages.addWidget(self.fullPage)
        self.compactPage = QWidget()
        self.compactPage.setObjectName(u"compactPage")
        self.compactLayout = QVBoxLayout(self.compactPage)
        self.compactLayout.setSpacing(8)
        self.compactLayout.setObjectName(u"compactLayout")
        self.compactLayout.setContentsMargins(0, 0, 0, 0)
        self.compactStartButton = QPushButton(self.compactPage)
        self.compactStartButton.setObjectName(u"compactStartButton")

        self.compactLayout.addWidget(self.compactStartButton)

        self.compactStatsLabel = QLabel(self.compactPage)
        self.compactStatsLabel.setObjectName(u"compactStatsLabel")
        self.compactStatsLabel.setProperty(u"caption", True)

        self.compactLayout.addWidget(self.compactStatsLabel)

        self.compactMeter = BiteMeter(self.compactPage)
        self.compactMeter.setObjectName(u"compactMeter")
        self.compactMeter.setMinimumSize(QSize(0, 80))

        self.compactLayout.addWidget(self.compactMeter)

        self.pages.addWidget(self.compactPage)

        self.mainLayout.addWidget(self.pages)

        self.mainLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GetTheFish", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"GetTheFish", None))
        self.stateLabel.setText(QCoreApplication.translate("MainWindow", u"IDLE", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Light", None))
#if QT_CONFIG(tooltip)
        self.themeButton.setToolTip(QCoreApplication.translate("MainWindow", u"Switch between light and dark mode", None))
#endif // QT_CONFIG(tooltip)
        self.viewButton.setText(QCoreApplication.translate("MainWindow", u"Compact", None))
#if QT_CONFIG(tooltip)
        self.viewButton.setToolTip(QCoreApplication.translate("MainWindow", u"Switch between the full and the compact view", None))
#endif // QT_CONFIG(tooltip)
        self.setupGroup.setTitle(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.areaLabel.setText(QCoreApplication.translate("MainWindow", u"Area", None))
        self.posStartLabel.setText("")
        self.areaArrowLabel.setText(QCoreApplication.translate("MainWindow", u"\u2192", None))
        self.posEndLabel.setText("")
        self.areaButton.setText(QCoreApplication.translate("MainWindow", u"Set Area", None))
#if QT_CONFIG(tooltip)
        self.areaButton.setToolTip(QCoreApplication.translate("MainWindow", u"Drag a rectangle over the water where the bobber lands", None))
#endif // QT_CONFIG(tooltip)
        self.bobberLabel.setText(QCoreApplication.translate("MainWindow", u"Bobber", None))
        self.bobberColorLabel.setText("")
        self.hexColorLabel.setText("")
        self.colorButton.setText(QCoreApplication.translate("MainWindow", u"Pick Color", None))
#if QT_CONFIG(tooltip)
        self.colorButton.setToolTip(QCoreApplication.translate("MainWindow", u"Click the bobber in a frozen screenshot", None))
#endif // QT_CONFIG(tooltip)
        self.castKeyLabel.setText(QCoreApplication.translate("MainWindow", u"Cast Key", None))
#if QT_CONFIG(tooltip)
        self.castKeyEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Key bound to the Fishing spell in the game, e.g. 0, f, f1, num0", None))
#endif // QT_CONFIG(tooltip)
        self.tuningGroup.setTitle(QCoreApplication.translate("MainWindow", u"Tuning", None))
        self.thresholdBobberLabel.setText(QCoreApplication.translate("MainWindow", u"Threshold Bobber", None))
#if QT_CONFIG(tooltip)
        self.thresholdBobberSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Per-channel RGB tolerance when searching the bobber (pink pixels in the preview)", None))
#endif // QT_CONFIG(tooltip)
        self.thresholdCatchLabel.setText(QCoreApplication.translate("MainWindow", u"Threshold Catch", None))
#if QT_CONFIG(tooltip)
        self.thresholdCatchSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Colour change of the watched pixel that counts as a bite (dashed line in the meter)", None))
#endif // QT_CONFIG(tooltip)
        self.jumpToBobberCheck.setText(QCoreApplication.translate("MainWindow", u"Jump to Bobber", None))
        self.verboseCheck.setText(QCoreApplication.translate("MainWindow", u"Verbose Log", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.logGroup.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.openConfigFolderButton.setText(QCoreApplication.translate("MainWindow", u"Open Config/Logs Folder", None))
        self.sessionGroup.setTitle(QCoreApplication.translate("MainWindow", u"Session", None))
        self.castsValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.castsCaption.setText(QCoreApplication.translate("MainWindow", u"Casts", None))
        self.catchesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.catchesCaption.setText(QCoreApplication.translate("MainWindow", u"Catches", None))
        self.missesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.missesCaption.setText(QCoreApplication.translate("MainWindow", u"Misses", None))
        self.rateValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.rateCaption.setText(QCoreApplication.translate("MainWindow", u"Catch rate", None))
        self.perHourValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.perHourCaption.setText(QCoreApplication.translate("MainWindow", u"Fish / hour", None))
        self.elapsedValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.elapsedCaption.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.previewGroup.setTitle(QCoreApplication.translate("MainWindow", u"Preview", None))
#if QT_CONFIG(tooltip)
        self.previewView.setToolTip(QCoreApplication.translate("MainWindow", u"Check your area and colour before fishing: pink pixels match the bobber colour, the circle is where the bobber would be found", None))
#endif // QT_CONFIG(tooltip)
        self.previewInfoLabel.setText("")
        self.previewCheck.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.meterGroup.setTitle(QCoreApplication.translate("MainWindow", u"Bite meter", None))
        self.compactStartButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.compactStatsLabel.setText("")
    # retranslateUi

