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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(319, 274)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.posStartLabel = QLabel(self.centralwidget)
        self.posStartLabel.setObjectName(u"posStartLabel")

        self.gridLayout.addWidget(self.posStartLabel, 1, 1, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.posEndLabel = QLabel(self.centralwidget)
        self.posEndLabel.setObjectName(u"posEndLabel")

        self.gridLayout.addWidget(self.posEndLabel, 2, 1, 1, 1)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.bobberColorLabel = QLabel(self.centralwidget)
        self.bobberColorLabel.setObjectName(u"bobberColorLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bobberColorLabel.sizePolicy().hasHeightForWidth())
        self.bobberColorLabel.setSizePolicy(sizePolicy)
        self.bobberColorLabel.setMinimumSize(QSize(20, 20))
        self.bobberColorLabel.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.bobberColorLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.hexColorLabel = QLabel(self.centralwidget)
        self.hexColorLabel.setObjectName(u"hexColorLabel")

        self.horizontalLayout_3.addWidget(self.hexColorLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.thresholdBobberSpinBox = QSpinBox(self.centralwidget)
        self.thresholdBobberSpinBox.setObjectName(u"thresholdBobberSpinBox")
        sizePolicy.setHeightForWidth(self.thresholdBobberSpinBox.sizePolicy().hasHeightForWidth())
        self.thresholdBobberSpinBox.setSizePolicy(sizePolicy)
        self.thresholdBobberSpinBox.setMinimumSize(QSize(120, 0))
        self.thresholdBobberSpinBox.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout_2.addWidget(self.thresholdBobberSpinBox)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.thresholdCatchSpinBox = QSpinBox(self.centralwidget)
        self.thresholdCatchSpinBox.setObjectName(u"thresholdCatchSpinBox")
        sizePolicy.setHeightForWidth(self.thresholdCatchSpinBox.sizePolicy().hasHeightForWidth())
        self.thresholdCatchSpinBox.setSizePolicy(sizePolicy)
        self.thresholdCatchSpinBox.setMinimumSize(QSize(120, 0))
        self.thresholdCatchSpinBox.setMaximumSize(QSize(120, 16777215))

        self.verticalLayout_2.addWidget(self.thresholdCatchSpinBox)

        self.castKeyLabel = QLabel(self.centralwidget)
        self.castKeyLabel.setObjectName(u"castKeyLabel")

        self.verticalLayout_2.addWidget(self.castKeyLabel)

        self.castKeyEdit = QLineEdit(self.centralwidget)
        self.castKeyEdit.setObjectName(u"castKeyEdit")
        sizePolicy.setHeightForWidth(self.castKeyEdit.sizePolicy().hasHeightForWidth())
        self.castKeyEdit.setSizePolicy(sizePolicy)
        self.castKeyEdit.setMinimumSize(QSize(60, 0))
        self.castKeyEdit.setMaximumSize(QSize(60, 16777215))
        self.castKeyEdit.setMaxLength(20)

        self.verticalLayout_2.addWidget(self.castKeyEdit)

        self.jumpToBobberCheck = QCheckBox(self.centralwidget)
        self.jumpToBobberCheck.setObjectName(u"jumpToBobberCheck")

        self.verticalLayout_2.addWidget(self.jumpToBobberCheck)

        self.verboseCheck = QCheckBox(self.centralwidget)
        self.verboseCheck.setObjectName(u"verboseCheck")

        self.verticalLayout_2.addWidget(self.verboseCheck)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(350, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")

        self.verticalLayout.addWidget(self.startButton)

        self.areaButton = QPushButton(self.centralwidget)
        self.areaButton.setObjectName(u"areaButton")

        self.verticalLayout.addWidget(self.areaButton)

        self.colorButton = QPushButton(self.centralwidget)
        self.colorButton.setObjectName(u"colorButton")

        self.verticalLayout.addWidget(self.colorButton)

        self.openConfigFolderButton = QPushButton(self.centralwidget)
        self.openConfigFolderButton.setObjectName(u"openConfigFolderButton")

        self.verticalLayout.addWidget(self.openConfigFolderButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GetTheFish", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
        self.posStartLabel.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.posEndLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Fishing Area", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Bobber Color", None))
        self.bobberColorLabel.setText("")
        self.hexColorLabel.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Threshold Bobber", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Threshold Catch", None))
        self.castKeyLabel.setText(QCoreApplication.translate("MainWindow", u"Cast Key", None))
#if QT_CONFIG(tooltip)
        self.castKeyEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Key bound to the Fishing spell in the game, e.g. 0, f, f1, num0", None))
#endif // QT_CONFIG(tooltip)
        self.jumpToBobberCheck.setText(QCoreApplication.translate("MainWindow", u"Jump to Bobber", None))
        self.verboseCheck.setText(QCoreApplication.translate("MainWindow", u"verbose", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.areaButton.setText(QCoreApplication.translate("MainWindow", u"Set Area", None))
        self.colorButton.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.openConfigFolderButton.setText(QCoreApplication.translate("MainWindow", u"Open Config/Logs Folder", None))
    # retranslateUi
