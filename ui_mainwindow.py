# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

from imageview import ImageView
from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.openButton = QPushButton(self.groupBox)
        self.openButton.setObjectName(u"openButton")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.openButton)

        self.exportButton = QPushButton(self.groupBox)
        self.exportButton.setObjectName(u"exportButton")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.exportButton)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.brushSizeSpinBox = QSpinBox(self.groupBox)
        self.brushSizeSpinBox.setObjectName(u"brushSizeSpinBox")
        self.brushSizeSpinBox.setMinimum(0)
        self.brushSizeSpinBox.setMaximum(25)
        self.brushSizeSpinBox.setValue(2)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.brushSizeSpinBox)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.ampSpinBox = QDoubleSpinBox(self.groupBox)
        self.ampSpinBox.setObjectName(u"ampSpinBox")
        self.ampSpinBox.setDecimals(1)
        self.ampSpinBox.setMinimum(-1.000000000000000)
        self.ampSpinBox.setMaximum(1.000000000000000)
        self.ampSpinBox.setSingleStep(0.100000000000000)
        self.ampSpinBox.setValue(0.500000000000000)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.ampSpinBox)

        self.reconstructButton = QPushButton(self.groupBox)
        self.reconstructButton.setObjectName(u"reconstructButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.reconstructButton)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.label_3)

        self.zeroPhaseButton = QPushButton(self.groupBox)
        self.zeroPhaseButton.setObjectName(u"zeroPhaseButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.zeroPhaseButton)

        self.randomPhaseButton = QPushButton(self.groupBox)
        self.randomPhaseButton.setObjectName(u"randomPhaseButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.randomPhaseButton)

        self.iterSpinBox = QSpinBox(self.groupBox)
        self.iterSpinBox.setObjectName(u"iterSpinBox")
        self.iterSpinBox.setMinimum(1)
        self.iterSpinBox.setMaximum(1000)
        self.iterSpinBox.setSingleStep(10)
        self.iterSpinBox.setValue(100)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.iterSpinBox)

        self.reconstructPhaseButton = QPushButton(self.groupBox)
        self.reconstructPhaseButton.setObjectName(u"reconstructPhaseButton")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.reconstructPhaseButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(8, QFormLayout.ItemRole.LabelRole, self.verticalSpacer)

        self.playButton = QPushButton(self.groupBox)
        self.playButton.setObjectName(u"playButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.playButton)

        self.histogramCheckBox = QCheckBox(self.groupBox)
        self.histogramCheckBox.setObjectName(u"histogramCheckBox")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.SpanningRole, self.histogramCheckBox)


        self.horizontalLayout.addWidget(self.groupBox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.imageView = ImageView(self.centralwidget)
        self.imageView.setObjectName(u"imageView")

        self.verticalLayout.addWidget(self.imageView)

        self.plotView = PlotWidget(self.centralwidget)
        self.plotView.setObjectName(u"plotView")

        self.verticalLayout.addWidget(self.plotView)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Spectral", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Control", None))
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Brush size", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Amplitude", None))
        self.reconstructButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Phase", None))
        self.zeroPhaseButton.setText(QCoreApplication.translate("MainWindow", u"zero", None))
        self.randomPhaseButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.reconstructPhaseButton.setText(QCoreApplication.translate("MainWindow", u"reconstruct", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.histogramCheckBox.setText(QCoreApplication.translate("MainWindow", u"histogram", None))
    # retranslateUi

