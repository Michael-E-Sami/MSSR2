#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import os
# from PyQt5.QtDataVisualization import (Q3DSurface, Q3DScatter, Q3DTheme, QAbstract3DGraph,
#        QHeightMapSurfaceDataProxy, QSurface3DSeries, QSurfaceDataItem,
#        QSurfaceDataProxy, QValue3DAxis, QScatter3DSeries, QAbstract3DSeries, QScatterDataItem,QLogValue3DAxisFormatter)
from appv3 import *
import threading


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setMaximumSize(QtCore.QSize(88888, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.listWidget.setProperty("isWrapping", True)
        self.listWidget.setLayoutMode(QtWidgets.QListWidget.SinglePass)
        self.listWidget.setObjectName("listView")
        # item = QtWidgets.QListWidgetItem()
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("ground_foreground.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # item.setIcon(icon)
        # self.listWidget.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_start = QtWidgets.QPushButton(Dialog)
        self.button_start.setObjectName("button_start")
        self.button_start.clicked.connect(self.startWindow)
        self.horizontalLayout_2.addWidget(self.button_start)
        self.button_load = QtWidgets.QPushButton(Dialog)
        self.button_load.setObjectName("button_load")
        self.horizontalLayout_2.addWidget(self.button_load)
        self.button_cancel = QtWidgets.QPushButton(Dialog)
        self.button_cancel.setObjectName("button_cancel")
        self.button_cancel.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.horizontalLayout_2.addWidget(self.button_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.x = 0

    def startWindow(self):
        print('a window should start')

        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow(robots_connected = self.arranged_list)
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
        Dialog.close()


    def on_combobox_changed(self, value):
        # print(os.path.dirname(__file__))
        self.listWidget.clear()
        self.x = 0
        # if (value == 'None'):
        #    import random_keyStrokes
        if (value == 'Physical'):
            from rostopic_names import final_list,arranged_list
            self.arranged_list = arranged_list
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.dirname(__file__) + "/Physical2.jpg"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            for list_itm in final_list:
                item = QtWidgets.QListWidgetItem()

                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setIcon(icon)

                self.listWidget.addItem(item)
                self.listWidget.setIconSize(QtCore.QSize(50, 50))
                _translate = QtCore.QCoreApplication.translate
                item = self.listWidget.item(self.x)
                item.setText(_translate("Dialog", list_itm))

                self.x += 1
            # rospy.init_node('talker', anonymous=True)
            # t = threading.Thread(target=talker)
            # t.start()
        if (value == 'Simulation'):
            from rostopic_names import final_list, arranged_list
            self.arranged_list = arranged_list
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.dirname(__file__) + "/Simulation2.jpg"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            for list_itm in final_list:
                item = QtWidgets.QListWidgetItem()

                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setIcon(icon)

                self.listWidget.addItem(item)
                self.listWidget.setIconSize(QtCore.QSize(50, 50))
                _translate = QtCore.QCoreApplication.translate
                item = self.listWidget.item(self.x)
                item.setText(_translate("Dialog", list_itm))

                self.x += 1
                # print(value)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MSSR"))
        self.label.setText(_translate("Dialog", "Hello and welcome to MSSR application!"))
        self.label_2.setText(_translate("Dialog", "Please choose the next session type"))
        self.comboBox.setItemText(0, _translate("Dialog", "None"))
        self.comboBox.setItemText(1, _translate("Dialog", "Simulation"))
        self.comboBox.setItemText(2, _translate("Dialog", "Physical"))
        self.label_3.setText(_translate("Dialog", "Connected to / Is active:"))
        self.button_start.setText(_translate("Dialog", "Start"))
        self.button_load.setText(_translate("Dialog", "Load"))
        self.button_cancel.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
