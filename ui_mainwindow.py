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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from imageview import ImageView
from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 673)
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

        self.resetMaskButton = QPushButton(self.groupBox)
        self.resetMaskButton.setObjectName(u"resetMaskButton")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.resetMaskButton)

        self.maskCheckBox = QCheckBox(self.groupBox)
        self.maskCheckBox.setObjectName(u"maskCheckBox")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.maskCheckBox)

        self.burnButton = QPushButton(self.groupBox)
        self.burnButton.setObjectName(u"burnButton")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.burnButton)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.SpanningRole, self.label_3)

        self.zeroPhaseButton = QPushButton(self.groupBox)
        self.zeroPhaseButton.setObjectName(u"zeroPhaseButton")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.zeroPhaseButton)

        self.randomPhaseButton = QPushButton(self.groupBox)
        self.randomPhaseButton.setObjectName(u"randomPhaseButton")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.FieldRole, self.randomPhaseButton)

        self.iterSpinBox = QSpinBox(self.groupBox)
        self.iterSpinBox.setObjectName(u"iterSpinBox")
        self.iterSpinBox.setMinimum(1)
        self.iterSpinBox.setMaximum(1000)
        self.iterSpinBox.setSingleStep(10)
        self.iterSpinBox.setValue(100)

        self.formLayout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.iterSpinBox)

        self.reconstructPhaseButton = QPushButton(self.groupBox)
        self.reconstructPhaseButton.setObjectName(u"reconstructPhaseButton")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.FieldRole, self.reconstructPhaseButton)

        self.tabWidget = QTabWidget(self.groupBox)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.formLayout_3 = QFormLayout(self.tab)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.brushSizeSpinBox = QSpinBox(self.tab)
        self.brushSizeSpinBox.setObjectName(u"brushSizeSpinBox")
        self.brushSizeSpinBox.setMinimum(0)
        self.brushSizeSpinBox.setMaximum(25)
        self.brushSizeSpinBox.setValue(2)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.brushSizeSpinBox)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.ampSpinBox = QDoubleSpinBox(self.tab)
        self.ampSpinBox.setObjectName(u"ampSpinBox")
        self.ampSpinBox.setDecimals(1)
        self.ampSpinBox.setMinimum(-1.000000000000000)
        self.ampSpinBox.setMaximum(1.000000000000000)
        self.ampSpinBox.setSingleStep(0.100000000000000)
        self.ampSpinBox.setValue(0.500000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.ampSpinBox)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.formLayout_2 = QFormLayout(self.tab_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.npersegSpinBox = QSpinBox(self.tab_2)
        self.npersegSpinBox.setObjectName(u"npersegSpinBox")
        self.npersegSpinBox.setMinimum(1)
        self.npersegSpinBox.setMaximum(2048)
        self.npersegSpinBox.setValue(1024)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.npersegSpinBox)

        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.overlapSpinBox = QDoubleSpinBox(self.tab_2)
        self.overlapSpinBox.setObjectName(u"overlapSpinBox")
        self.overlapSpinBox.setDecimals(2)
        self.overlapSpinBox.setMaximum(0.990000000000000)
        self.overlapSpinBox.setSingleStep(0.100000000000000)
        self.overlapSpinBox.setValue(0.500000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.overlapSpinBox)

        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.tabWidget.addTab(self.tab_2, "")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.tabWidget)

        self.topFreqSpinBox = QSpinBox(self.groupBox)
        self.topFreqSpinBox.setObjectName(u"topFreqSpinBox")
        self.topFreqSpinBox.setMinimum(1)
        self.topFreqSpinBox.setMaximum(256)
        self.topFreqSpinBox.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.topFreqSpinBox.setValue(5)

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.topFreqSpinBox)

        self.topFreqButton = QPushButton(self.groupBox)
        self.topFreqButton.setObjectName(u"topFreqButton")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.topFreqButton)

        self.reloadButton = QPushButton(self.groupBox)
        self.reloadButton.setObjectName(u"reloadButton")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.reloadButton)

        self.regenerateButton = QPushButton(self.groupBox)
        self.regenerateButton.setObjectName(u"regenerateButton")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.regenerateButton)

        self.reconstructButton = QPushButton(self.groupBox)
        self.reconstructButton.setObjectName(u"reconstructButton")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.reconstructButton)

        self.cmapComboBox = QComboBox(self.groupBox)
        self.cmapComboBox.setObjectName(u"cmapComboBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cmapComboBox)

        self.scaleComboBox = QComboBox(self.groupBox)
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.setObjectName(u"scaleComboBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.scaleComboBox)

        self.histogramCheckBox = QCheckBox(self.groupBox)
        self.histogramCheckBox.setObjectName(u"histogramCheckBox")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.histogramCheckBox)

        self.lockCheckBox = QCheckBox(self.groupBox)
        self.lockCheckBox.setObjectName(u"lockCheckBox")
        self.lockCheckBox.setChecked(True)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lockCheckBox)

        self.playButton = QPushButton(self.groupBox)
        self.playButton.setObjectName(u"playButton")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.FieldRole, self.playButton)

        self.loopButton = QPushButton(self.groupBox)
        self.loopButton.setObjectName(u"loopButton")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.LabelRole, self.loopButton)


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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Spectral", None))
        self.groupBox.setTitle("")
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4c2 Open", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f4be Export", None))
        self.resetMaskButton.setText(QCoreApplication.translate("MainWindow", u"reset mask", None))
        self.maskCheckBox.setText(QCoreApplication.translate("MainWindow", u"mask", None))
        self.burnButton.setText(QCoreApplication.translate("MainWindow", u"burn mask", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Phase", None))
        self.zeroPhaseButton.setText(QCoreApplication.translate("MainWindow", u"zero", None))
        self.randomPhaseButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.reconstructPhaseButton.setText(QCoreApplication.translate("MainWindow", u"reconstruct", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Brush size", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Amplitude", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Brush", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"nperseg", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"overlap", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"STFT", None))
        self.topFreqButton.setText(QCoreApplication.translate("MainWindow", u"top freq", None))
        self.reloadButton.setText(QCoreApplication.translate("MainWindow", u"\u21b6 Reload", None))
        self.regenerateButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f504 Refresh", None))
        self.reconstructButton.setText(QCoreApplication.translate("MainWindow", u"\u2705 Apply", None))
        self.scaleComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Linear", None))
        self.scaleComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Log", None))
        self.scaleComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Mel", None))

        self.histogramCheckBox.setText(QCoreApplication.translate("MainWindow", u"histogram", None))
        self.lockCheckBox.setText(QCoreApplication.translate("MainWindow", u"lock view", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"\u25b6\ufe0f Play", None))
        self.loopButton.setText(QCoreApplication.translate("MainWindow", u"\U0001f501 Loop", None))
    # retranslateUi

