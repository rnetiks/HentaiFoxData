# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinderProgram.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import json
import os

with open("data.json","r")as f:
    data = json.load(f)

tag_galleries = {}
tag_list = []

class Ui_MuliSearch(object):
    def setupUi(self, MuliSearch):
        MuliSearch.setObjectName("MuliSearch")
        MuliSearch.resize(777, 345)
        self.centralwidget = QtWidgets.QWidget(MuliSearch)
        self.centralwidget.setObjectName("centralwidget")
        self.Progress = QtWidgets.QProgressBar(self.centralwidget)
        self.Progress.setGeometry(QtCore.QRect(260, 270, 501, 21))
        self.Progress.setProperty("value", 0)
        self.Progress.setObjectName("Progress")
        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddButton.setGeometry(QtCore.QRect(330, 100, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.AddButton.setFont(font)
        self.AddButton.setObjectName("AddButton")
        self.PossibleList = QtWidgets.QListWidget(self.centralwidget)
        self.PossibleList.setGeometry(QtCore.QRect(30, 60, 291, 161))
        self.PossibleList.setObjectName("PossibleList")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(40, 270, 191, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.StartButton.setFont(font)
        self.StartButton.setObjectName("StartButton")
        self.EnterdList = QtWidgets.QListWidget(self.centralwidget)
        self.EnterdList.setGeometry(QtCore.QRect(430, 60, 291, 161))
        self.EnterdList.setObjectName("EnterdList")
        self.ChooseType = QtWidgets.QComboBox(self.centralwidget)
        self.ChooseType.setGeometry(QtCore.QRect(40, 20, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.ChooseType.setFont(font)
        self.ChooseType.setObjectName("ChooseType")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.ChooseType.addItem("")
        self.RemoveButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveButton.setGeometry(QtCore.QRect(330, 140, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.RemoveButton.setFont(font)
        self.RemoveButton.setObjectName("RemoveButton")
        MuliSearch.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MuliSearch)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 22))
        self.menubar.setObjectName("menubar")
        MuliSearch.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MuliSearch)
        self.statusbar.setObjectName("statusbar")
        MuliSearch.setStatusBar(self.statusbar)

        self.retranslateUi(MuliSearch)
        QtCore.QMetaObject.connectSlotsByName(MuliSearch)

        self.ChooseType.activated.connect(self.update_list)
        self.AddButton.clicked.connect(self.add_item)
        self.RemoveButton.clicked.connect(self.remove_item)
        self.StartButton.clicked.connect(self.start_pressed)

    def retranslateUi(self, MuliSearch):
        _translate = QtCore.QCoreApplication.translate
        MuliSearch.setWindowTitle(_translate("MuliSearch", "MultiSearch"))
        self.AddButton.setText(_translate("MuliSearch", "Add"))
        self.PossibleList.setSortingEnabled(False)
        self.StartButton.setText(_translate("MuliSearch", "Search"))
        self.ChooseType.setItemText(0, _translate("MuliSearch", "-- Choose Type --"))
        self.ChooseType.setItemText(1, _translate("MuliSearch", "Tags"))
        self.ChooseType.setItemText(2, _translate("MuliSearch", "Parodies"))
        self.ChooseType.setItemText(3, _translate("MuliSearch", "Characters"))
        self.ChooseType.setItemText(4, _translate("MuliSearch", "Artists"))
        self.ChooseType.setItemText(5, _translate("MuliSearch", "Groups"))
        self.ChooseType.setItemText(6, _translate("MuliSearch", "Categories"))
        self.RemoveButton.setText(_translate("MuliSearch", "Remove"))

    def update_list(self):
        types = ["parodies","characters","tags","artists","groups","categories"]
        self.PossibleList.clear()
        if self.ChooseType.currentText() == "-- Choose Type --":
            for type in types:
                for abc in data[type]:
                    self.PossibleList.addItem(f"{abc}")
        if self.ChooseType.currentText() == "Tags":
            for abc in data["tags"]:
                self.PossibleList.addItem(f"{abc} (tags)")
        if self.ChooseType.currentText() == "Parodies":
            for abc in data["parodies"]:
                self.PossibleList.addItem(f"{abc} (parodies)")
        if self.ChooseType.currentText() == "Characters":
            for abc in data["characters"]:
                self.PossibleList.addItem(f"{abc} (characters)")
        if self.ChooseType.currentText() == "Artists":
            for abc in data["artists"]:
                self.PossibleList.addItem(f"{abc} (artists)")
        if self.ChooseType.currentText() == "Groups":
            for abc in data["groups"]:
                self.PossibleList.addItem(f"{abc} (groups)")
        if self.ChooseType.currentText() == "Categories":
            for abc in data["categories"]:
                self.PossibleList.addItem(f"{abc} (categories)")

    def add_item(self):
        current = self.PossibleList.currentItem()
        if current != None:
            item = self.PossibleList.takeItem(self.PossibleList.row(self.PossibleList.currentItem()))
            self.EnterdList.addItem(item)
            tag_list.append(item.text())

    def remove_item(self):
        current = self.EnterdList.currentItem()
        if current != None:
            item = self.EnterdList.takeItem(self.EnterdList.row(self.EnterdList.currentItem()))
            tag_list.remove(item.text())

    def start_pressed(self):
        filename1 = ""
        for item in tag_list:
            abc = item[:item.find(" (")]
            filename1 = filename1 + f"{abc}-"
        filename = filename1[:-1].replace(" ","_")
        round = 1
        rounds = len(tag_list)
        for item in tag_list:
            type = item[item.find("(")+1:item.find(")")]
            abc = item[:item.find(" (")]
            with open(f"{type}/{abc}.json","r") as f:
                data = json.load(f)
            length = len(data)
            push_val = 100/rounds/length
            if round == 1:
                tag_galleries["1"] = []
                for gallery in data["galleries"]:
                    tag_galleries["1"].append(gallery)
            if round != 1:
                if round <= rounds:
                    tag_galleries[str(round)] = []
                    for gallery in data["galleries"]:
                        val = self.Progress.value() + push_val
                        self.Progress.setValue(int(val))
                        if gallery in tag_galleries[str(round-1)]:
                            tag_galleries[str(round)].append(gallery)
                    if round == rounds:
                        msg = QMessageBox()
                        msg.setWindowTitle("Finished")
                        if len(tag_galleries[str(round)]) > 0:
                            if os.path.exists(f"./results"):
                                pass
                            else:
                                os.mkdir(f"./results")
                            with open(f"results/{filename}.txt", "w+") as d:
                                num = 0
                                for gallery in tag_galleries[str(round)]:
                                    d.write(f"https://hentaifox.com/gallery/{gallery}/\n")
                                    num += 1
                                self.Progress.setValue(100)
                                msg.setText(f"Wrote the URL(s) of {num} results into\nresults/{filename}.txt\n")
                        else:
                            msg.setText(f"Sorry no results for that combination.")
                        x=msg.exec_()
            round += 1





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MuliSearch = QtWidgets.QMainWindow()
    ui = Ui_MuliSearch()
    ui.setupUi(MuliSearch)
    MuliSearch.show()
    sys.exit(app.exec_())
