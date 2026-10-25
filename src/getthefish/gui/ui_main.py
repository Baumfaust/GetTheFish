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

from getthefish.gui.widgets import (BiteMeter, RoundHistory, StatusLed)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
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

        self.statusLed = StatusLed(self.centralwidget)
        self.statusLed.setObjectName(u"statusLed")

        self.headerLayout.addWidget(self.statusLed)

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

        self.leftSpacer = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.leftColumn.addItem(self.leftSpacer)

        self.leftColumn.setStretch(3, 1)

        self.fullLayout.addLayout(self.leftColumn)

        self.rightColumn = QVBoxLayout()
        self.rightColumn.setSpacing(4)
        self.rightColumn.setObjectName(u"rightColumn")
        self.sessionGroup = QGroupBox(self.fullPage)
        self.sessionGroup.setObjectName(u"sessionGroup")
        self.sessionLayout = QVBoxLayout(self.sessionGroup)
        self.sessionLayout.setSpacing(10)
        self.sessionLayout.setObjectName(u"sessionLayout")
        self.statsLayout = QGridLayout()
        self.statsLayout.setSpacing(6)
        self.statsLayout.setObjectName(u"statsLayout")
        self.castsCaption = QLabel(self.sessionGroup)
        self.castsCaption.setObjectName(u"castsCaption")
        self.castsCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.castsCaption, 0, 1, 1, 1)

        self.castsValue = QLabel(self.sessionGroup)
        self.castsValue.setObjectName(u"castsValue")
        self.castsValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.castsValue, 1, 1, 1, 1)

        self.todayCastsValue = QLabel(self.sessionGroup)
        self.todayCastsValue.setObjectName(u"todayCastsValue")
        self.todayCastsValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayCastsValue, 2, 1, 1, 1)

        self.totalCastsValue = QLabel(self.sessionGroup)
        self.totalCastsValue.setObjectName(u"totalCastsValue")
        self.totalCastsValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalCastsValue, 3, 1, 1, 1)

        self.catchesCaption = QLabel(self.sessionGroup)
        self.catchesCaption.setObjectName(u"catchesCaption")
        self.catchesCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.catchesCaption, 0, 2, 1, 1)

        self.catchesValue = QLabel(self.sessionGroup)
        self.catchesValue.setObjectName(u"catchesValue")
        self.catchesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.catchesValue, 1, 2, 1, 1)

        self.todayCatchesValue = QLabel(self.sessionGroup)
        self.todayCatchesValue.setObjectName(u"todayCatchesValue")
        self.todayCatchesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayCatchesValue, 2, 2, 1, 1)

        self.totalCatchesValue = QLabel(self.sessionGroup)
        self.totalCatchesValue.setObjectName(u"totalCatchesValue")
        self.totalCatchesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalCatchesValue, 3, 2, 1, 1)

        self.missesCaption = QLabel(self.sessionGroup)
        self.missesCaption.setObjectName(u"missesCaption")
        self.missesCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.missesCaption, 0, 3, 1, 1)

        self.missesValue = QLabel(self.sessionGroup)
        self.missesValue.setObjectName(u"missesValue")
        self.missesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.missesValue, 1, 3, 1, 1)

        self.todayMissesValue = QLabel(self.sessionGroup)
        self.todayMissesValue.setObjectName(u"todayMissesValue")
        self.todayMissesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayMissesValue, 2, 3, 1, 1)

        self.totalMissesValue = QLabel(self.sessionGroup)
        self.totalMissesValue.setObjectName(u"totalMissesValue")
        self.totalMissesValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalMissesValue, 3, 3, 1, 1)

        self.rateCaption = QLabel(self.sessionGroup)
        self.rateCaption.setObjectName(u"rateCaption")
        self.rateCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.rateCaption, 0, 4, 1, 1)

        self.rateValue = QLabel(self.sessionGroup)
        self.rateValue.setObjectName(u"rateValue")
        self.rateValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.rateValue, 1, 4, 1, 1)

        self.todayRateValue = QLabel(self.sessionGroup)
        self.todayRateValue.setObjectName(u"todayRateValue")
        self.todayRateValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayRateValue, 2, 4, 1, 1)

        self.totalRateValue = QLabel(self.sessionGroup)
        self.totalRateValue.setObjectName(u"totalRateValue")
        self.totalRateValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalRateValue, 3, 4, 1, 1)

        self.perHourCaption = QLabel(self.sessionGroup)
        self.perHourCaption.setObjectName(u"perHourCaption")
        self.perHourCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.perHourCaption, 0, 5, 1, 1)

        self.perHourValue = QLabel(self.sessionGroup)
        self.perHourValue.setObjectName(u"perHourValue")
        self.perHourValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.perHourValue, 1, 5, 1, 1)

        self.todayPerHourValue = QLabel(self.sessionGroup)
        self.todayPerHourValue.setObjectName(u"todayPerHourValue")
        self.todayPerHourValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayPerHourValue, 2, 5, 1, 1)

        self.totalPerHourValue = QLabel(self.sessionGroup)
        self.totalPerHourValue.setObjectName(u"totalPerHourValue")
        self.totalPerHourValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalPerHourValue, 3, 5, 1, 1)

        self.elapsedCaption = QLabel(self.sessionGroup)
        self.elapsedCaption.setObjectName(u"elapsedCaption")
        self.elapsedCaption.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.elapsedCaption, 0, 6, 1, 1)

        self.elapsedValue = QLabel(self.sessionGroup)
        self.elapsedValue.setObjectName(u"elapsedValue")
        self.elapsedValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.elapsedValue, 1, 6, 1, 1)

        self.todayElapsedValue = QLabel(self.sessionGroup)
        self.todayElapsedValue.setObjectName(u"todayElapsedValue")
        self.todayElapsedValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.todayElapsedValue, 2, 6, 1, 1)

        self.totalElapsedValue = QLabel(self.sessionGroup)
        self.totalElapsedValue.setObjectName(u"totalElapsedValue")
        self.totalElapsedValue.setProperty(u"statValue", True)

        self.statsLayout.addWidget(self.totalElapsedValue, 3, 6, 1, 1)

        self.sessionLabel = QLabel(self.sessionGroup)
        self.sessionLabel.setObjectName(u"sessionLabel")
        self.sessionLabel.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.sessionLabel, 1, 0, 1, 1)

        self.todayLabel = QLabel(self.sessionGroup)
        self.todayLabel.setObjectName(u"todayLabel")
        self.todayLabel.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.todayLabel, 2, 0, 1, 1)

        self.totalLabel = QLabel(self.sessionGroup)
        self.totalLabel.setObjectName(u"totalLabel")
        self.totalLabel.setProperty(u"caption", True)

        self.statsLayout.addWidget(self.totalLabel, 3, 0, 1, 1)


        self.sessionLayout.addLayout(self.statsLayout)

        self.roundsLayout = QHBoxLayout()
        self.roundsLayout.setSpacing(8)
        self.roundsLayout.setObjectName(u"roundsLayout")
        self.roundsLabel = QLabel(self.sessionGroup)
        self.roundsLabel.setObjectName(u"roundsLabel")
        self.roundsLabel.setProperty(u"caption", True)

        self.roundsLayout.addWidget(self.roundsLabel)

        self.roundHistory = RoundHistory(self.sessionGroup)
        self.roundHistory.setObjectName(u"roundHistory")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.roundHistory.sizePolicy().hasHeightForWidth())
        self.roundHistory.setSizePolicy(sizePolicy1)

        self.roundsLayout.addWidget(self.roundHistory)


        self.sessionLayout.addLayout(self.roundsLayout)


        self.rightColumn.addWidget(self.sessionGroup)

        self.meterGroup = QGroupBox(self.fullPage)
        self.meterGroup.setObjectName(u"meterGroup")
        self.meterLayout = QVBoxLayout(self.meterGroup)
        self.meterLayout.setObjectName(u"meterLayout")
        self.biteMeter = BiteMeter(self.meterGroup)
        self.biteMeter.setObjectName(u"biteMeter")
        self.biteMeter.setMinimumSize(QSize(0, 120))

        self.meterLayout.addWidget(self.biteMeter)


        self.rightColumn.addWidget(self.meterGroup)

        self.logGroup = QGroupBox(self.fullPage)
        self.logGroup.setObjectName(u"logGroup")
        self.logLayout = QVBoxLayout(self.logGroup)
        self.logLayout.setObjectName(u"logLayout")
        self.logView = QPlainTextEdit(self.logGroup)
        self.logView.setObjectName(u"logView")
        self.logView.setReadOnly(True)
        self.logView.setMaximumBlockCount(500)

        self.logLayout.addWidget(self.logView)

        self.logButtonLayout = QHBoxLayout()
        self.logButtonLayout.setObjectName(u"logButtonLayout")
        self.logButtonSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logButtonLayout.addItem(self.logButtonSpacer)

        self.openConfigFolderButton = QPushButton(self.logGroup)
        self.openConfigFolderButton.setObjectName(u"openConfigFolderButton")

        self.logButtonLayout.addWidget(self.openConfigFolderButton)


        self.logLayout.addLayout(self.logButtonLayout)


        self.rightColumn.addWidget(self.logGroup)

        self.rightColumn.setStretch(2, 1)

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

        self.compactRoundHistory = RoundHistory(self.compactPage)
        self.compactRoundHistory.setObjectName(u"compactRoundHistory")
        sizePolicy1.setHeightForWidth(self.compactRoundHistory.sizePolicy().hasHeightForWidth())
        self.compactRoundHistory.setSizePolicy(sizePolicy1)

        self.compactLayout.addWidget(self.compactRoundHistory)

        self.compactStatsLayout = QGridLayout()
        self.compactStatsLayout.setSpacing(2)
        self.compactStatsLayout.setObjectName(u"compactStatsLayout")
        self.compactCaughtCaption = QLabel(self.compactPage)
        self.compactCaughtCaption.setObjectName(u"compactCaughtCaption")
        self.compactCaughtCaption.setProperty(u"caption", True)
        self.compactCaughtCaption.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactCaughtCaption, 0, 1, 1, 1)

        self.compactRateCaption = QLabel(self.compactPage)
        self.compactRateCaption.setObjectName(u"compactRateCaption")
        self.compactRateCaption.setProperty(u"caption", True)
        self.compactRateCaption.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactRateCaption, 0, 2, 1, 1)

        self.compactTimeCaption = QLabel(self.compactPage)
        self.compactTimeCaption.setObjectName(u"compactTimeCaption")
        self.compactTimeCaption.setProperty(u"caption", True)
        self.compactTimeCaption.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTimeCaption, 0, 3, 1, 1)

        self.compactSessionLabel = QLabel(self.compactPage)
        self.compactSessionLabel.setObjectName(u"compactSessionLabel")
        self.compactSessionLabel.setProperty(u"caption", True)

        self.compactStatsLayout.addWidget(self.compactSessionLabel, 1, 0, 1, 1)

        self.compactSessionCatches = QLabel(self.compactPage)
        self.compactSessionCatches.setObjectName(u"compactSessionCatches")
        self.compactSessionCatches.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactSessionCatches, 1, 1, 1, 1)

        self.compactSessionRate = QLabel(self.compactPage)
        self.compactSessionRate.setObjectName(u"compactSessionRate")
        self.compactSessionRate.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactSessionRate, 1, 2, 1, 1)

        self.compactSessionTime = QLabel(self.compactPage)
        self.compactSessionTime.setObjectName(u"compactSessionTime")
        self.compactSessionTime.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactSessionTime, 1, 3, 1, 1)

        self.compactTodayLabel = QLabel(self.compactPage)
        self.compactTodayLabel.setObjectName(u"compactTodayLabel")
        self.compactTodayLabel.setProperty(u"caption", True)

        self.compactStatsLayout.addWidget(self.compactTodayLabel, 2, 0, 1, 1)

        self.compactTodayCatches = QLabel(self.compactPage)
        self.compactTodayCatches.setObjectName(u"compactTodayCatches")
        self.compactTodayCatches.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTodayCatches, 2, 1, 1, 1)

        self.compactTodayRate = QLabel(self.compactPage)
        self.compactTodayRate.setObjectName(u"compactTodayRate")
        self.compactTodayRate.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTodayRate, 2, 2, 1, 1)

        self.compactTodayTime = QLabel(self.compactPage)
        self.compactTodayTime.setObjectName(u"compactTodayTime")
        self.compactTodayTime.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTodayTime, 2, 3, 1, 1)

        self.compactTotalLabel = QLabel(self.compactPage)
        self.compactTotalLabel.setObjectName(u"compactTotalLabel")
        self.compactTotalLabel.setProperty(u"caption", True)

        self.compactStatsLayout.addWidget(self.compactTotalLabel, 3, 0, 1, 1)

        self.compactTotalCatches = QLabel(self.compactPage)
        self.compactTotalCatches.setObjectName(u"compactTotalCatches")
        self.compactTotalCatches.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTotalCatches, 3, 1, 1, 1)

        self.compactTotalRate = QLabel(self.compactPage)
        self.compactTotalRate.setObjectName(u"compactTotalRate")
        self.compactTotalRate.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTotalRate, 3, 2, 1, 1)

        self.compactTotalTime = QLabel(self.compactPage)
        self.compactTotalTime.setObjectName(u"compactTotalTime")
        self.compactTotalTime.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.compactStatsLayout.addWidget(self.compactTotalTime, 3, 3, 1, 1)

        self.compactStatsLayout.setColumnStretch(0, 1)
        self.compactStatsLayout.setColumnStretch(1, 1)
        self.compactStatsLayout.setColumnStretch(2, 1)
        self.compactStatsLayout.setColumnStretch(3, 1)

        self.compactLayout.addLayout(self.compactStatsLayout)

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
        self.thresholdBobberSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Per-channel RGB tolerance when searching for the bobber colour", None))
#endif // QT_CONFIG(tooltip)
        self.thresholdCatchLabel.setText(QCoreApplication.translate("MainWindow", u"Threshold Catch", None))
#if QT_CONFIG(tooltip)
        self.thresholdCatchSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Colour change of the watched pixel that counts as a bite (dashed line in the meter)", None))
#endif // QT_CONFIG(tooltip)
        self.jumpToBobberCheck.setText(QCoreApplication.translate("MainWindow", u"Jump to Bobber", None))
        self.verboseCheck.setText(QCoreApplication.translate("MainWindow", u"Verbose Log", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.sessionGroup.setTitle(QCoreApplication.translate("MainWindow", u"Statistics", None))
        self.castsCaption.setText(QCoreApplication.translate("MainWindow", u"Casts", None))
        self.castsValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayCastsValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalCastsValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.catchesCaption.setText(QCoreApplication.translate("MainWindow", u"Catches", None))
        self.catchesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayCatchesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalCatchesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.missesCaption.setText(QCoreApplication.translate("MainWindow", u"Misses", None))
        self.missesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayMissesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalMissesValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.rateCaption.setText(QCoreApplication.translate("MainWindow", u"Catch rate", None))
        self.rateValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayRateValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalRateValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.perHourCaption.setText(QCoreApplication.translate("MainWindow", u"Fish / hour", None))
        self.perHourValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayPerHourValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalPerHourValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.elapsedCaption.setText(QCoreApplication.translate("MainWindow", u"Fishing time", None))
        self.elapsedValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.todayElapsedValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.totalElapsedValue.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.sessionLabel.setText(QCoreApplication.translate("MainWindow", u"Session", None))
        self.todayLabel.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.totalLabel.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.roundsLabel.setText(QCoreApplication.translate("MainWindow", u"Last rounds", None))
        self.meterGroup.setTitle(QCoreApplication.translate("MainWindow", u"Bite meter", None))
        self.logGroup.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.openConfigFolderButton.setText(QCoreApplication.translate("MainWindow", u"Open Config/Logs Folder", None))
        self.compactStartButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.compactCaughtCaption.setText(QCoreApplication.translate("MainWindow", u"Caught", None))
        self.compactRateCaption.setText(QCoreApplication.translate("MainWindow", u"Rate", None))
        self.compactTimeCaption.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.compactSessionLabel.setText(QCoreApplication.translate("MainWindow", u"Session", None))
        self.compactSessionCatches.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactSessionRate.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactSessionTime.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTodayLabel.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.compactTodayCatches.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTodayRate.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTodayTime.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTotalLabel.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.compactTotalCatches.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTotalRate.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
        self.compactTotalTime.setText(QCoreApplication.translate("MainWindow", u"\u2013", None))
    # retranslateUi

