from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import sys

from bs4 import BeautifulSoup
from zipfile import ZipFile
import concurrent.futures
import requests
import urllib
import os
import shutil
import json
import time

#---get-latest-gallery----------
if True:
    web = requests.get("https://hentaifox.com/")
    html = web.text
    soup = BeautifulSoup(html, "html.parser")
    no1 = str(soup.find("div", attrs={"class":"inner_thumb"}))
    latest_gallery = int(no1[no1.find("/gallery/")+9:no1.find('/"><img')])
#---multi-search-list-setup-----
if True:
    with open("data/data.json","r")as f:
        data = json.load(f)
    tag_galleries = {}
    white_list = {}
    black_list = {}
    item_list={}
    types = ["parodies","characters","tags","artists","groups","categories"]
    for type in types:
        white_list[type] = []
        black_list[type] = []
        item_list[type] = []
        for abc in data[type]:
            item_list[type].append(abc)
#---GUI-------------------------
class Ui_HentaiFoxDesktop(QMainWindow):
    def setupUi(self, HentaiFoxDesktop):
        if True:
            HentaiFoxDesktop.setObjectName("HentaiFoxDesktop")
            HentaiFoxDesktop.resize(1920, 1000)
            self.status = QStatusBar()
            self.setStatusBar(self.status)
            self.centralwidget = QtWidgets.QWidget(HentaiFoxDesktop)
            self.centralwidget.setObjectName("centralwidget")
            self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
            self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
            self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
            self.tabWidget.setObjectName("tabWidget")
            self.browse = QtWidgets.QWidget()
            self.browse.setObjectName("browse")
            self.gridLayout_2 = QtWidgets.QGridLayout(self.browse)
            self.gridLayout_2.setObjectName("gridLayout_2")
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout")
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.setSpacing(5)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.backbutton = QtWidgets.QPushButton(self.browse)
            font14 = QtGui.QFont()
            font14.setFamily("Arial")
            font14.setPointSize(14)
            font14.setWeight(50)
            self.backbutton.setFont(font14)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(".\\Icons/Back_Arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.backbutton.setIcon(icon)
            self.backbutton.setIconSize(QtCore.QSize(25, 25))
            self.backbutton.setFlat(True)
            self.backbutton.setObjectName("backbutton")
            self.horizontalLayout.addWidget(self.backbutton)
            self.forwardbutton = QtWidgets.QPushButton(self.browse)
            self.forwardbutton.setFont(font14)
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(".\\Icons/Forward_Arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.forwardbutton.setIcon(icon1)
            self.forwardbutton.setIconSize(QtCore.QSize(25, 25))
            self.forwardbutton.setFlat(True)
            self.forwardbutton.setObjectName("forwardbutton")
            self.horizontalLayout.addWidget(self.forwardbutton)
            self.reloadbutton = QtWidgets.QPushButton(self.browse)
            self.reloadbutton.setFont(font14)
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap(".\\Icons/Reload_Arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reloadbutton.setIcon(icon2)
            self.reloadbutton.setIconSize(QtCore.QSize(25, 25))
            self.reloadbutton.setFlat(True)
            self.reloadbutton.setObjectName("reloadbutton")
            self.horizontalLayout.addWidget(self.reloadbutton)
            self.homebutton = QtWidgets.QPushButton(self.browse)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.homebutton.sizePolicy().hasHeightForWidth())
            self.homebutton.setSizePolicy(sizePolicy)
            self.homebutton.setFont(font14)
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap(".\\Icons/Home-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.homebutton.setIcon(icon3)
            self.homebutton.setIconSize(QtCore.QSize(25, 25))
            self.homebutton.setFlat(True)
            self.homebutton.setObjectName("homebutton")
            self.horizontalLayout.addWidget(self.homebutton)
            self.urlbar = QtWidgets.QLineEdit(self.browse)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.urlbar.sizePolicy().hasHeightForWidth())
            self.urlbar.setSizePolicy(sizePolicy)
            font10 = QtGui.QFont()
            font10.setFamily("Arial")
            font10.setPointSize(10)
            self.urlbar.setFont(font10)
            self.urlbar.setObjectName("urlbar")
            self.horizontalLayout.addWidget(self.urlbar)
            self.bookmark = QtWidgets.QToolButton(self.browse)
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(".\\Icons/Bookmark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.bookmark.setIcon(icon4)
            self.bookmark.setIconSize(QtCore.QSize(30, 30))
            self.bookmark.setPopupMode(QToolButton.InstantPopup)
            self.bookmark.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            self.bookmark.setAutoRaise(True)
            self.bookmark.setObjectName("toolButton")
            self.horizontalLayout.addWidget(self.bookmark)
            self.downloadbutton = QtWidgets.QPushButton(self.browse)
            font11 = QtGui.QFont()
            font11.setPointSize(11)
            self.downloadbutton.setFont(font11)
            self.downloadbutton.setObjectName("downloadbutton")
            self.horizontalLayout.addWidget(self.downloadbutton)
            self.label_zoom = QtWidgets.QLabel(self.browse)
            font13 = QtGui.QFont()
            font13.setPointSize(13)
            self.label_zoom.setFont(font13)
            self.label_zoom.setObjectName("label_zoom")
            self.horizontalLayout.addWidget(self.label_zoom)
            self.zoomslider = QtWidgets.QSlider(self.browse)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.zoomslider.sizePolicy().hasHeightForWidth())
            self.zoomslider.setSizePolicy(sizePolicy)
            self.zoomslider.setMinimumSize(QtCore.QSize(100, 0))
            self.zoomslider.setMinimum(30)
            self.zoomslider.setMaximum(190)
            self.zoomslider.setProperty("value", 100)
            self.zoomslider.setOrientation(QtCore.Qt.Horizontal)
            self.zoomslider.setObjectName("zoomslider")
            self.horizontalLayout.addWidget(self.zoomslider)
            self.menu_button = QToolButton(self.browse)
            self.menu_button.setIcon(QIcon("icons/menu.png"))
            self.menu_button.setIconSize(QSize(30,30))
            self.menu_button.setPopupMode(QToolButton.InstantPopup)
            self.menu_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.menu_button.setAutoRaise(True)
            self.menu_button.setObjectName("menu_button")
            self.horizontalLayout.addWidget(self.menu_button)
            self.horizontalLayout.setStretch(0, 1)
            self.horizontalLayout.setStretch(1, 1)
            self.horizontalLayout.setStretch(2, 1)
            self.horizontalLayout.setStretch(3, 1)
            self.horizontalLayout.setStretch(4, 50)
            self.horizontalLayout.setStretch(5, 1)
            self.horizontalLayout.setStretch(6, 1)
            self.horizontalLayout.setStretch(7, 1)
            self.horizontalLayout.setStretch(8, 10)
            self.horizontalLayout.setStretch(9, 1)
            self.verticalLayout.addLayout(self.horizontalLayout)
            self.tabs = QTabWidget(self.browse)
            self.tabs.setObjectName("tabs")
            self.tab = QtWidgets.QWidget()
            self.tab.setObjectName("tab")
            self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.tab)
            self.verticalLayout_21.setObjectName("verticalLayout_21")
            self.verticalLayout.addWidget(self.tabs)
            self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
            self.tabWidget.addTab(self.browse, "")
            self.search = QtWidgets.QWidget()
            self.search.setObjectName("search")
            self.gridLayout_3 = QtWidgets.QGridLayout(self.search)
            self.gridLayout_3.setObjectName("gridLayout_3")
            self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_7.setSpacing(20)
            self.horizontalLayout_7.setObjectName("horizontalLayout_7")
            self.verticalLayout_10 = QtWidgets.QVBoxLayout()
            self.verticalLayout_10.setObjectName("verticalLayout_10")
            self.choosetype = QtWidgets.QComboBox(self.search)
            self.choosetype.setMinimumSize(QtCore.QSize(0, 40))
            self.choosetype.setFont(font11)
            self.choosetype.setObjectName("choosetype")
            self.verticalLayout_10.addWidget(self.choosetype)
            self.criterialist = QtWidgets.QListWidget(self.search)
            self.criterialist.setObjectName("criterialist")
            self.verticalLayout_10.addWidget(self.criterialist)
            self.horizontalLayout_7.addLayout(self.verticalLayout_10)
            self.verticalLayout_9 = QtWidgets.QVBoxLayout()
            self.verticalLayout_9.setObjectName("verticalLayout_9")
            self.label = QtWidgets.QLabel(self.search)
            self.label.setFont(font11)
            self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.label.setWordWrap(True)
            self.label.setObjectName("label")
            self.verticalLayout_9.addWidget(self.label)
            self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_6.setSpacing(20)
            self.horizontalLayout_6.setObjectName("horizontalLayout_6")
            self.verticalLayout_8 = QtWidgets.QVBoxLayout()
            self.verticalLayout_8.setObjectName("verticalLayout_8")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout()
            self.verticalLayout_4.setSpacing(10)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_4.setSpacing(20)
            self.horizontalLayout_4.setObjectName("horizontalLayout_4")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout()
            self.verticalLayout_2.setSpacing(10)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.whitelist_arrows_r = QtWidgets.QLabel(self.search)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.whitelist_arrows_r.sizePolicy().hasHeightForWidth())
            self.whitelist_arrows_r.setSizePolicy(sizePolicy)
            font12 = QtGui.QFont()
            font12.setPointSize(12)
            self.whitelist_arrows_r.setFont(font12)
            self.whitelist_arrows_r.setAlignment(QtCore.Qt.AlignCenter)
            self.whitelist_arrows_r.setObjectName("whitelist_arrows_r")
            self.verticalLayout_2.addWidget(self.whitelist_arrows_r)
            self.whitelist_addbutton = QtWidgets.QPushButton(self.search)
            self.whitelist_addbutton.setFont(font11)
            self.whitelist_addbutton.setObjectName("whitelist_addbutton")
            self.verticalLayout_2.addWidget(self.whitelist_addbutton)
            self.whitelist_removebutton = QtWidgets.QPushButton(self.search)
            self.whitelist_removebutton.setFont(font11)
            self.whitelist_removebutton.setObjectName("whitelist_removebutton")
            self.verticalLayout_2.addWidget(self.whitelist_removebutton)
            self.whitelist_arrows_l = QtWidgets.QLabel(self.search)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.whitelist_arrows_l.sizePolicy().hasHeightForWidth())
            self.whitelist_arrows_l.setSizePolicy(sizePolicy)
            self.whitelist_arrows_l.setFont(font12)
            self.whitelist_arrows_l.setAlignment(QtCore.Qt.AlignCenter)
            self.whitelist_arrows_l.setObjectName("whitelist_arrows_l")
            self.verticalLayout_2.addWidget(self.whitelist_arrows_l)
            self.verticalLayout_2.setStretch(0, 1)
            self.verticalLayout_2.setStretch(1, 1)
            self.verticalLayout_2.setStretch(2, 1)
            self.verticalLayout_2.setStretch(3, 1)
            self.horizontalLayout_4.addLayout(self.verticalLayout_2)
            self.whitelist = QtWidgets.QListWidget(self.search)
            self.whitelist.setObjectName("whitelist")
            self.horizontalLayout_4.addWidget(self.whitelist)
            self.horizontalLayout_4.setStretch(0, 10)
            self.horizontalLayout_4.setStretch(1, 15)
            self.verticalLayout_4.addLayout(self.horizontalLayout_4)
            self.line = QtWidgets.QFrame(self.search)
            self.line.setMinimumSize(QtCore.QSize(0, 6))
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setLineWidth(4)
            self.line.setMidLineWidth(0)
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setObjectName("line")
            self.verticalLayout_4.addWidget(self.line)
            self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_5.setSpacing(20)
            self.horizontalLayout_5.setObjectName("horizontalLayout_5")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout()
            self.verticalLayout_3.setSpacing(10)
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.blacklist_arrows_r = QtWidgets.QLabel(self.search)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.blacklist_arrows_r.sizePolicy().hasHeightForWidth())
            self.blacklist_arrows_r.setSizePolicy(sizePolicy)
            self.blacklist_arrows_r.setFont(font12)
            self.blacklist_arrows_r.setAlignment(QtCore.Qt.AlignCenter)
            self.blacklist_arrows_r.setObjectName("blacklist_arrows_r")
            self.verticalLayout_3.addWidget(self.blacklist_arrows_r)
            self.blacklist_addbutton = QtWidgets.QPushButton(self.search)
            self.blacklist_addbutton.setFont(font11)
            self.blacklist_addbutton.setObjectName("blacklist_addbutton")
            self.verticalLayout_3.addWidget(self.blacklist_addbutton)
            self.blacklist_removebutton = QtWidgets.QPushButton(self.search)
            self.blacklist_removebutton.setFont(font11)
            self.blacklist_removebutton.setObjectName("blacklist_removebutton")
            self.verticalLayout_3.addWidget(self.blacklist_removebutton)
            self.blacklist_arrows_l = QtWidgets.QLabel(self.search)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.blacklist_arrows_l.sizePolicy().hasHeightForWidth())
            self.blacklist_arrows_l.setSizePolicy(sizePolicy)
            self.blacklist_arrows_l.setFont(font12)
            self.blacklist_arrows_l.setAlignment(QtCore.Qt.AlignCenter)
            self.blacklist_arrows_l.setObjectName("blacklist_arrows_l")
            self.verticalLayout_3.addWidget(self.blacklist_arrows_l)
            self.verticalLayout_3.setStretch(0, 1)
            self.verticalLayout_3.setStretch(1, 1)
            self.verticalLayout_3.setStretch(2, 1)
            self.verticalLayout_3.setStretch(3, 1)
            self.horizontalLayout_5.addLayout(self.verticalLayout_3)
            self.blacklist = QtWidgets.QListWidget(self.search)
            self.blacklist.setObjectName("blacklist")
            self.horizontalLayout_5.addWidget(self.blacklist)
            self.horizontalLayout_5.setStretch(0, 10)
            self.horizontalLayout_5.setStretch(1, 15)
            self.verticalLayout_4.addLayout(self.horizontalLayout_5)
            self.verticalLayout_8.addLayout(self.verticalLayout_4)
            self.gridLayout = QtWidgets.QGridLayout()
            self.gridLayout.setHorizontalSpacing(20)
            self.gridLayout.setVerticalSpacing(10)
            self.gridLayout.setObjectName("gridLayout")
            self.verticalLayout_7 = QtWidgets.QVBoxLayout()
            self.verticalLayout_7.setSpacing(10)
            self.verticalLayout_7.setObjectName("verticalLayout_7")
            self.verticalLayout_5 = QtWidgets.QVBoxLayout()
            self.verticalLayout_5.setSpacing(0)
            self.verticalLayout_5.setObjectName("verticalLayout_5")
            self.label_choosedoubleclickfunc = QtWidgets.QLabel(self.search)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_choosedoubleclickfunc.sizePolicy().hasHeightForWidth())
            self.label_choosedoubleclickfunc.setSizePolicy(sizePolicy)
            self.label_choosedoubleclickfunc.setFont(font11)
            self.label_choosedoubleclickfunc.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.label_choosedoubleclickfunc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_choosedoubleclickfunc.setObjectName("label_choosedoubleclickfunc")
            self.verticalLayout_5.addWidget(self.label_choosedoubleclickfunc)
            self.check_internal = QtWidgets.QRadioButton(self.search)
            self.check_internal.setFont(font11)
            self.check_internal.setChecked(True)
            self.check_internal.setObjectName("check_internal")
            self.verticalLayout_5.addWidget(self.check_internal)
            self.check_external = QtWidgets.QRadioButton(self.search)
            self.check_external.setFont(font11)
            self.check_external.setObjectName("check_external")
            self.verticalLayout_5.addWidget(self.check_external)
            self.verticalLayout_7.addLayout(self.verticalLayout_5)
            self.verticalLayout_6 = QtWidgets.QVBoxLayout()
            self.verticalLayout_6.setObjectName("verticalLayout_6")
            self.label_amount = QtWidgets.QLabel(self.search)
            self.label_amount.setFont(font11)
            self.label_amount.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.label_amount.setAlignment(QtCore.Qt.AlignCenter)
            self.label_amount.setWordWrap(True)
            self.label_amount.setObjectName("label_amount")
            self.verticalLayout_6.addWidget(self.label_amount)
            self.pagecount = QtWidgets.QLCDNumber(self.search)
            self.pagecount.setSmallDecimalPoint(False)
            self.pagecount.setDigitCount(11)
            self.pagecount.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
            self.pagecount.setObjectName("pagecount")
            self.verticalLayout_6.addWidget(self.pagecount)
            self.label_percentage = QtWidgets.QLabel(self.search)
            self.label_percentage.setFont(font11)
            self.label_percentage.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.label_percentage.setAlignment(QtCore.Qt.AlignCenter)
            self.label_percentage.setWordWrap(True)
            self.label_percentage.setObjectName("label_percentage")
            self.verticalLayout_6.addWidget(self.label_percentage)
            self.percentagecount = QtWidgets.QProgressBar(self.search)
            self.percentagecount.setProperty("value", 24)
            self.percentagecount.setOrientation(QtCore.Qt.Horizontal)
            self.percentagecount.setObjectName("percentagecount")
            self.verticalLayout_6.addWidget(self.percentagecount)
            self.verticalLayout_6.setStretch(0, 1)
            self.verticalLayout_6.setStretch(1, 2)
            self.verticalLayout_6.setStretch(2, 1)
            self.verticalLayout_6.setStretch(3, 1)
            self.verticalLayout_7.addLayout(self.verticalLayout_6)
            self.check_loadfacts = QtWidgets.QCheckBox(self.search)
            self.check_loadfacts.setObjectName("check_loadfacts")
            self.verticalLayout_7.addWidget(self.check_loadfacts)
            self.verticalLayout_7.setStretch(0, 1)
            self.verticalLayout_7.setStretch(1, 2)
            self.gridLayout.addLayout(self.verticalLayout_7, 0, 0, 2, 1)
            self.search_button = QtWidgets.QPushButton(self.search)
            self.search_button.setFont(font14)
            self.search_button.setObjectName("search_button")
            self.gridLayout.addWidget(self.search_button, 0, 1, 1, 1)
            self.diagnostics = QtWidgets.QLabel(self.search)
            self.diagnostics.setFont(font12)
            self.diagnostics.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.diagnostics.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            self.diagnostics.setWordWrap(True)
            self.diagnostics.setObjectName("diagnostics")
            self.gridLayout.addWidget(self.diagnostics, 1, 1, 1, 1)
            self.gridLayout.setColumnStretch(0, 10)
            self.gridLayout.setColumnStretch(1, 15)
            self.gridLayout.setRowStretch(0, 1)
            self.gridLayout.setRowStretch(1, 1)
            self.verticalLayout_8.addLayout(self.gridLayout)
            self.verticalLayout_8.setStretch(0, 10)
            self.verticalLayout_8.setStretch(1, 9)
            self.horizontalLayout_6.addLayout(self.verticalLayout_8)
            self.describtion = QtWidgets.QLabel(self.search)
            self.describtion.setFont(font14)
            self.describtion.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.describtion.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.describtion.setScaledContents(False)
            self.describtion.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            self.describtion.setWordWrap(True)
            self.describtion.setObjectName("describtion")
            self.horizontalLayout_6.addWidget(self.describtion)
            self.horizontalLayout_6.setStretch(0, 10)
            self.horizontalLayout_6.setStretch(1, 6)
            self.verticalLayout_9.addLayout(self.horizontalLayout_6)
            self.verticalLayout_9.setStretch(0, 1)
            self.verticalLayout_9.setStretch(1, 20)
            self.horizontalLayout_7.addLayout(self.verticalLayout_9)
            self.horizontalLayout_7.setStretch(0, 10)
            self.horizontalLayout_7.setStretch(1, 30)
            self.gridLayout_3.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
            self.tabWidget.addTab(self.search, "")
            self.results = QtWidgets.QWidget()
            self.results.setObjectName("results")
            self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.results)
            self.horizontalLayout_11.setObjectName("horizontalLayout_11")
            self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_10.setSpacing(20)
            self.horizontalLayout_10.setObjectName("horizontalLayout_10")
            self.verticalLayout_20 = QtWidgets.QVBoxLayout()
            self.verticalLayout_20.setObjectName("verticalLayout_20")
            self.resultlist = QtWidgets.QListWidget(self.results)
            self.resultlist.setMaximumSize(QtCore.QSize(700, 16777215))
            self.resultlist.setObjectName("resultlist")
            self.verticalLayout_20.addWidget(self.resultlist)
            self.check_preview = QtWidgets.QCheckBox(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.check_preview.sizePolicy().hasHeightForWidth())
            self.check_preview.setSizePolicy(sizePolicy)
            self.check_preview.setMinimumSize(QtCore.QSize(0, 30))
            self.check_preview.setObjectName("check_preview")
            self.verticalLayout_20.addWidget(self.check_preview)
            self.horizontalLayout_10.addLayout(self.verticalLayout_20)
            self.verticalLayout_19 = QtWidgets.QVBoxLayout()
            self.verticalLayout_19.setObjectName("verticalLayout_19")
            self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_9.setSpacing(10)
            self.horizontalLayout_9.setObjectName("horizontalLayout_9")
            self.horizontalLayout_loadfile = QtWidgets.QHBoxLayout()
            self.horizontalLayout_loadfile.setObjectName("verticalLayout_18")
            self.filebrowser = QtWidgets.QListWidget(self.results)
            self.filebrowser.setObjectName("filebrowser")
            self.horizontalLayout_loadfile.addWidget(self.filebrowser)
            self.filebuttons_layout = QtWidgets.QVBoxLayout()
            self.filebuttons_layout.setObjectName("filebuttons_layout")
            self.horizontalLayout_loadfile.addLayout(self.filebuttons_layout)
            self.loadfilebutton = QtWidgets.QPushButton(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.loadfilebutton.sizePolicy().hasHeightForWidth())
            self.loadfilebutton.setSizePolicy(sizePolicy)
            self.loadfilebutton.setMinimumSize(QtCore.QSize(0, 40))
            self.loadfilebutton.setFont(font11)
            self.loadfilebutton.setObjectName("loadfilebutton")
            self.filebuttons_layout.addWidget(self.loadfilebutton)
            self.deletefilebutton = QtWidgets.QPushButton(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.deletefilebutton.sizePolicy().hasHeightForWidth())
            self.deletefilebutton.setSizePolicy(sizePolicy)
            self.deletefilebutton.setMinimumSize(QtCore.QSize(0, 40))
            self.deletefilebutton.setFont(font11)
            self.deletefilebutton.setObjectName("deletefilebutton")
            self.filebuttons_layout.addWidget(self.deletefilebutton)
            self.horizontalLayout_9.addLayout(self.horizontalLayout_loadfile)
            self.line_3 = QtWidgets.QFrame(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
            self.line_3.setSizePolicy(sizePolicy)
            self.line_3.setMinimumSize(QtCore.QSize(5, 0))
            self.line_3.setLineWidth(4)
            self.line_3.setMidLineWidth(0)
            self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_3.setObjectName("line_3")
            self.horizontalLayout_9.addWidget(self.line_3)
            self.label_info = QtWidgets.QLabel(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_info.sizePolicy().hasHeightForWidth())
            self.label_info.setSizePolicy(sizePolicy)
            self.label_info.setFont(font11)
            self.label_info.setAlignment(QtCore.Qt.AlignCenter)
            self.label_info.setWordWrap(True)
            self.label_info.setObjectName("label_info")
            self.horizontalLayout_9.addWidget(self.label_info)
            self.horizontalLayout_9.setStretch(0, 100)
            self.horizontalLayout_9.setStretch(1, 5)
            self.horizontalLayout_9.setStretch(2, 100)
            self.verticalLayout_19.addLayout(self.horizontalLayout_9)
            self.line_2 = QtWidgets.QFrame(self.results)
            self.line_2.setMinimumSize(QtCore.QSize(0, 6))
            self.line_2.setLineWidth(3)
            self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.verticalLayout_19.addWidget(self.line_2)
            self.gridLayout_4 = QtWidgets.QGridLayout()
            self.gridLayout_4.setSpacing(10)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.title = QtWidgets.QLabel(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
            self.title.setSizePolicy(sizePolicy)
            self.title.setMinimumSize(QtCore.QSize(0, 60))
            self.title.setFont(font14)
            self.title.setAlignment(QtCore.Qt.AlignCenter)
            self.title.setObjectName("title")
            self.gridLayout_4.addWidget(self.title, 0, 1, 1, 4)
            self.verticalLayout_14 = QtWidgets.QVBoxLayout()
            self.verticalLayout_14.setObjectName("verticalLayout_14")
            self.lable_tags = QtWidgets.QLabel(self.results)
            self.lable_tags.setFont(font14)
            self.lable_tags.setAlignment(QtCore.Qt.AlignCenter)
            self.lable_tags.setObjectName("lable_tags")
            self.verticalLayout_14.addWidget(self.lable_tags)
            self.tags = QtWidgets.QListWidget(self.results)
            self.tags.setObjectName("tags")
            self.verticalLayout_14.addWidget(self.tags)
            self.gridLayout_4.addLayout(self.verticalLayout_14, 1, 1, 2, 1)
            self.verticalLayout_16 = QtWidgets.QVBoxLayout()
            self.verticalLayout_16.setObjectName("verticalLayout_16")
            self.lable_artistandgroups = QtWidgets.QLabel(self.results)
            self.lable_artistandgroups.setFont(font14)
            self.lable_artistandgroups.setAlignment(QtCore.Qt.AlignCenter)
            self.lable_artistandgroups.setWordWrap(True)
            self.lable_artistandgroups.setObjectName("lable_artistandgroups")
            self.verticalLayout_16.addWidget(self.lable_artistandgroups)
            self.artistsandgroups = QtWidgets.QListWidget(self.results)
            self.artistsandgroups.setObjectName("artistsandgroups")
            self.verticalLayout_16.addWidget(self.artistsandgroups)
            self.gridLayout_4.addLayout(self.verticalLayout_16, 1, 3, 1, 2)
            self.verticalLayout_17 = QtWidgets.QVBoxLayout()
            self.verticalLayout_17.setObjectName("verticalLayout_17")
            self.lable_parodies = QtWidgets.QLabel(self.results)
            self.lable_parodies.setFont(font14)
            self.lable_parodies.setAlignment(QtCore.Qt.AlignCenter)
            self.lable_parodies.setObjectName("lable_parodies")
            self.verticalLayout_17.addWidget(self.lable_parodies)
            self.parodies = QtWidgets.QListWidget(self.results)
            self.parodies.setObjectName("parodies")
            self.verticalLayout_17.addWidget(self.parodies)
            self.gridLayout_4.addLayout(self.verticalLayout_17, 2, 3, 1, 2)
            self.verticalLayout_13 = QtWidgets.QVBoxLayout()
            self.verticalLayout_13.setObjectName("verticalLayout_13")
            self.label_choose_doubleclickfunc2 = QtWidgets.QLabel(self.results)
            font = QtGui.QFont()
            font.setPointSize(10)
            self.label_choose_doubleclickfunc2.setFont(font)
            self.label_choose_doubleclickfunc2.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.label_choose_doubleclickfunc2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_choose_doubleclickfunc2.setObjectName("label_choose_doubleclickfunc2")
            self.verticalLayout_13.addWidget(self.label_choose_doubleclickfunc2)
            self.check_internal2 = QtWidgets.QRadioButton(self.results)
            self.check_internal2.setChecked(True)
            self.check_internal2.setObjectName("check_internal2")
            self.verticalLayout_13.addWidget(self.check_internal2)
            self.check_external2 = QtWidgets.QRadioButton(self.results)
            self.check_external2.setObjectName("check_external2")
            self.verticalLayout_13.addWidget(self.check_external2)
            self.gridLayout_4.addLayout(self.verticalLayout_13, 3, 3, 1, 2)
            self.cover = QtWidgets.QLabel(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.cover.sizePolicy().hasHeightForWidth())
            self.cover.setSizePolicy(sizePolicy)
            self.cover.setMinimumSize(QtCore.QSize(175, 248))
            self.cover.setMaximumSize(QtCore.QSize(350, 496))
            self.cover.setSizeIncrement(QtCore.QSize(350, 496))
            self.cover.setBaseSize(QtCore.QSize(1, 1))
            self.cover.setFrameShape(QtWidgets.QFrame.WinPanel)
            self.cover.setFrameShadow(QtWidgets.QFrame.Raised)
            self.cover.setText("")
            self.cover.setPixmap(QtGui.QPixmap(".\\Icons/images.jpg"))
            self.cover.setAlignment(QtCore.Qt.AlignCenter)
            self.cover.setObjectName("cover")
            self.gridLayout_4.addWidget(self.cover, 0, 0, 3, 1)
            self.internalbrowserbutton = QtWidgets.QPushButton(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.internalbrowserbutton.sizePolicy().hasHeightForWidth())
            self.internalbrowserbutton.setSizePolicy(sizePolicy)
            self.internalbrowserbutton.setMinimumSize(QtCore.QSize(0, 50))
            self.internalbrowserbutton.setFont(font11)
            self.internalbrowserbutton.setObjectName("internalbrowserbutton")
            self.gridLayout_4.addWidget(self.internalbrowserbutton, 3, 1, 1, 1)
            self.externalbrowserbutton = QtWidgets.QPushButton(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.externalbrowserbutton.sizePolicy().hasHeightForWidth())
            self.externalbrowserbutton.setSizePolicy(sizePolicy)
            self.externalbrowserbutton.setMinimumSize(QtCore.QSize(0, 50))
            self.externalbrowserbutton.setFont(font11)
            self.externalbrowserbutton.setObjectName("externalbrowserbutton")
            self.gridLayout_4.addWidget(self.externalbrowserbutton, 3, 2, 1, 1)
            self.verticalLayout_15 = QtWidgets.QVBoxLayout()
            self.verticalLayout_15.setObjectName("verticalLayout_15")
            self.lable_characters = QtWidgets.QLabel(self.results)
            self.lable_characters.setFont(font14)
            self.lable_characters.setAlignment(QtCore.Qt.AlignCenter)
            self.lable_characters.setObjectName("lable_characters")
            self.verticalLayout_15.addWidget(self.lable_characters)
            self.characters = QtWidgets.QListWidget(self.results)
            self.characters.setObjectName("characters")
            self.verticalLayout_15.addWidget(self.characters)
            self.gridLayout_4.addLayout(self.verticalLayout_15, 1, 2, 2, 1)
            self.verticalLayout_12 = QtWidgets.QVBoxLayout()
            self.verticalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.verticalLayout_12.setSpacing(5)
            self.verticalLayout_12.setObjectName("verticalLayout_12")
            self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
            self.horizontalLayout_8.setSpacing(0)
            self.horizontalLayout_8.setObjectName("horizontalLayout_8")
            self.label_pages = QtWidgets.QLabel(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_pages.sizePolicy().hasHeightForWidth())
            self.label_pages.setSizePolicy(sizePolicy)
            font16 = QtGui.QFont()
            font16.setPointSize(16)
            self.label_pages.setFont(font16)
            self.label_pages.setObjectName("label_pages")
            self.horizontalLayout_8.addWidget(self.label_pages)
            self.pagescount2 = QtWidgets.QLCDNumber(self.results)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.pagescount2.sizePolicy().hasHeightForWidth())
            self.pagescount2.setSizePolicy(sizePolicy)
            self.pagescount2.setDigitCount(5)
            self.pagescount2.setObjectName("pagescount2")
            self.horizontalLayout_8.addWidget(self.pagescount2)
            self.horizontalLayout_8.setStretch(0, 1)
            self.horizontalLayout_8.setStretch(1, 2)
            self.verticalLayout_12.addLayout(self.horizontalLayout_8)
            self.category = QtWidgets.QLabel(self.results)
            self.category.setFont(font16)
            self.category.setAlignment(QtCore.Qt.AlignCenter)
            self.category.setObjectName("category")
            self.verticalLayout_12.addWidget(self.category)
            self.gridLayout_4.addLayout(self.verticalLayout_12, 3, 0, 1, 1)
            self.gridLayout_4.setColumnStretch(0, 11)
            self.gridLayout_4.setColumnStretch(1, 10)
            self.gridLayout_4.setColumnStretch(2, 10)
            self.gridLayout_4.setColumnStretch(3, 10)
            self.gridLayout_4.setColumnStretch(4, 1)
            self.verticalLayout_19.addLayout(self.gridLayout_4)
            self.horizontalLayout_10.addLayout(self.verticalLayout_19)
            self.horizontalLayout_10.setStretch(0, 10)
            self.horizontalLayout_10.setStretch(1, 30)
            self.horizontalLayout_11.addLayout(self.horizontalLayout_10)
            self.tabWidget.addTab(self.results, "")
            self.update = QtWidgets.QWidget()
            self.update.setObjectName("update")
            self.gridLayout_5 = QtWidgets.QGridLayout(self.update)
            self.gridLayout_5.setObjectName("gridLayout_5")
            self.gridLayout_6 = QtWidgets.QGridLayout()
            self.gridLayout_6.setObjectName("gridLayout_6")
            self.widget = QtWidgets.QWidget(self.update)
            self.widget.setObjectName("widget")
            self.gridLayout_6.addWidget(self.widget, 1, 0, 1, 1)
            self.label_credits = QtWidgets.QLabel(self.update)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.label_credits.sizePolicy().hasHeightForWidth())
            self.label_credits.setSizePolicy(sizePolicy)
            self.label_credits.setFont(font14)
            self.label_credits.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            self.label_credits.setWordWrap(True)
            self.label_credits.setObjectName("label_credits")
            self.gridLayout_6.addWidget(self.label_credits, 0, 2, 2, 1)
            self.verticalLayout_11 = QtWidgets.QVBoxLayout()
            self.verticalLayout_11.setObjectName("verticalLayout_11")
            self.start = QtWidgets.QLabel(self.update)
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(14)
            self.start.setFont(font)
            self.start.setObjectName("start")
            self.verticalLayout_11.addWidget(self.start)
            self.startslider = QtWidgets.QSlider(self.update)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.startslider.sizePolicy().hasHeightForWidth())
            self.startslider.setSizePolicy(sizePolicy)
            self.startslider.setMinimumSize(QtCore.QSize(0, 50))
            self.startslider.setMinimum(1)
            self.startslider.setSliderPosition(1)
            self.startslider.setOrientation(QtCore.Qt.Horizontal)
            self.startslider.setObjectName("startslider")
            self.verticalLayout_11.addWidget(self.startslider)
            self.stop = QtWidgets.QLabel(self.update)
            font = QtGui.QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(14)
            self.stop.setFont(font)
            self.stop.setObjectName("stop")
            self.verticalLayout_11.addWidget(self.stop)
            self.stopslider = QtWidgets.QSlider(self.update)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.stopslider.sizePolicy().hasHeightForWidth())
            self.stopslider.setSizePolicy(sizePolicy)
            self.stopslider.setMinimumSize(QtCore.QSize(0, 50))
            self.stopslider.setMinimum(1)
            self.stopslider.setSliderPosition(1)
            self.stopslider.setOrientation(QtCore.Qt.Horizontal)
            self.stopslider.setObjectName("stopslider")
            self.verticalLayout_11.addWidget(self.stopslider)
            self.updatebutton = QtWidgets.QPushButton(self.update)
            self.updatebutton.setMinimumSize(QtCore.QSize(0, 50))
            self.updatebutton.setFont(font16)
            self.updatebutton.setObjectName("updatebutton")
            self.verticalLayout_11.addWidget(self.updatebutton)
            self.gridLayout_6.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
            self.line_4 = QtWidgets.QFrame(self.update)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
            self.line_4.setSizePolicy(sizePolicy)
            self.line_4.setMinimumSize(QtCore.QSize(6, 0))
            self.line_4.setLineWidth(3)
            self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_4.setObjectName("line_4")
            self.gridLayout_6.addWidget(self.line_4, 0, 1, 2, 1)
            self.label_version = QtWidgets.QLabel(self.update)
            self.label_version.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
            self.label_version.setObjectName("label_version")
            self.gridLayout_6.addWidget(self.label_version, 2, 2, 1, 1)
            self.gridLayout_6.setColumnStretch(0, 100)
            self.gridLayout_6.setColumnStretch(1, 20)
            self.gridLayout_6.setColumnStretch(2, 300)
            self.gridLayout_6.setRowStretch(0, 1)
            self.gridLayout_6.setRowStretch(1, 5)
            self.gridLayout_5.addLayout(self.gridLayout_6, 0, 0, 1, 1)
            self.tabWidget.addTab(self.update, "")
            self.horizontalLayout_2.addWidget(self.tabWidget)
            HentaiFoxDesktop.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(HentaiFoxDesktop)
            self.statusbar.setObjectName("statusbar")
            HentaiFoxDesktop.setStatusBar(self.statusbar)
            self.tabs.setMovable(True)
            self.tabs.setTabsClosable(True)
            self.tabs.setDocumentMode(True)

            self.retranslateUi(HentaiFoxDesktop)
            self.tabWidget.setCurrentIndex(0)
            self.tabs.setCurrentIndex(0)
            QtCore.QMetaObject.connectSlotsByName(HentaiFoxDesktop)
#---------browser-setup----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.tabWidget.setCurrentIndex(0)
            self.add_new_tab(QUrl('https://hentaifox.com/'), 'Homepage')
            self.urlbar.setText("https://hentaifox.com/")

            self.bookmarkMenu = QMenu()
            with open("data/bookmarks.json","r") as f:
                bookmarks = json.load(f)
            self.bookmarkMenu.clear()
            self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"),"Add Bookmark",self.add_bookmark,QKeySequence("Ctrl+D"))
            self.bookmarkMenu.addSeparator()
            self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"),"Add Bookmark",self.add_bookmark,QKeySequence("Ctrl+D"))
            self.bookmarkMenu.addSeparator()
            for bookmark in bookmarks:
                self.bookmarkMenu.addAction(f"{bookmark}",lambda bookmark=bookmark: self.load_bookmark(bookmark))
            self.refresh_bookmarks()
            self.bookmark.setMenu(self.bookmarkMenu)

            self.browserMenu = QMenu()
            self.browserMenu.addAction(QIcon("icons/Back_Arrow.png"),"Back",lambda: self.tabs.currentWidget().back(),QKeySequence("Ctrl+Left"))
            self.browserMenu.addAction(QIcon("icons/Forward_Arrow.png"),"Forward",lambda: self.tabs.currentWidget().forward(),QKeySequence("Ctrl+Right"))
            self.browserMenu.addAction(QIcon("icons/Reload_Arrow.png"),"Reload",lambda: self.tabs.currentWidget().reload(),QKeySequence("Ctrl+R"))
            self.browserMenu.addAction(QIcon("icons/Home-icon.png"),"Home",self.navigate_home,QKeySequence("Ctrl+H"))
            self.browserMenu.addSeparator()
            self.browserMenu.addAction(QIcon("icons/add_tab.png"),"New Tab",self.add_new_tab,QKeySequence("Ctrl+T"))
            self.browserMenu.addAction(QIcon("icons/remove_tab.png"),"Close Tab",lambda i=self.tabs.currentIndex(): self.close_current_tab(i),QKeySequence("Ctrl+W"))
            self.tabsMenu = self.browserMenu.addMenu(QIcon("icons/tab.png"),"Navigate Tabs")
            self.tabsMenu.addAction("Switch to Tab 1",lambda: self.tabs.setCurrentIndex(0),QKeySequence("Ctrl+1"))
            self.browserMenu.addSeparator()
            self.browserMenu.addAction(QIcon("icons/zoom_in.png"),"Zoom in by 10%",lambda value=0.1:self.zoom_browser2(value=value),QKeySequence("Ctrl++"))
            self.browserMenu.addAction(QIcon("icons/zoom_out.png"),"Zoom out by 10%",lambda value=-0.1:self.zoom_browser2(value=value),QKeySequence("Ctrl+-"))
            self.browserMenu.addAction(QIcon("icons/zoom.png"),"Reset Zoom to 100%",self.reset_zoom,QKeySequence("Ctrl+0"))
            self.browserMenu.addSeparator()
            self.browserMenu.addAction(QIcon("icons/download.png"),"Download current Gallery",self.download,QKeySequence("Ctrl+S"))
            self.menu_button.setMenu(self.browserMenu)
#---------multi-search-setup-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.choosetype.addItem("-- Choose Type --")
            self.choosetype.addItem("tags")
            self.choosetype.addItem("parodies")
            self.choosetype.addItem("characters")
            self.choosetype.addItem("artists")
            self.choosetype.addItem("groups")
            self.choosetype.addItem("categories")
            self.describtion.setText("Select tag to view description")
            self.percentagecount.setValue(0)
#---------update-setup-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.startslider.setMaximum(int(latest_gallery))
            self.startslider.setValue(int(latest_gallery-500))
            self.stopslider.setMaximum(int(latest_gallery))
            self.stopslider.setValue(int(latest_gallery))
            self.start.setText(f"Start searching for gaps and updates at: {latest_gallery-500}")
            self.stop.setText(f"Stop searching for gaps and updates at: {latest_gallery}")
#---------browser-signals--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.backbutton.clicked.connect(lambda: self.tabs.currentWidget().back())
            self.forwardbutton.clicked.connect(lambda: self.tabs.currentWidget().forward())
            self.reloadbutton.clicked.connect(lambda: self.tabs.currentWidget().reload())
            self.homebutton.clicked.connect(self.navigate_home)
            self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
            self.tabs.currentChanged.connect(self.current_tab_changed)
            self.tabs.tabCloseRequested.connect(self.close_current_tab)
            self.zoomslider.sliderMoved.connect(self.zoom_browser)
            self.urlbar.returnPressed.connect(self.navigate_to_url)
            self.downloadbutton.clicked.connect(self.download)
#---------multi-search-signals---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.choosetype.activated.connect(self.update_taglist)
            self.whitelist_addbutton.clicked.connect(self.whitelist_add)
            self.whitelist_removebutton.clicked.connect(self.whitelist_remove)
            self.blacklist_addbutton.clicked.connect(self.blacklist_add)
            self.blacklist_removebutton.clicked.connect(self.blacklist_remove)
            self.criterialist.itemClicked.connect(self.criterialist_update_gallerycounter)
            self.whitelist.itemClicked.connect(self.whitelist_update_gallerycounter)
            self.blacklist.itemClicked.connect(self.blacklist_update_gallerycounter)
            self.criterialist.itemDoubleClicked.connect(self.criterialist_opentaginbrowser)
            self.whitelist.itemDoubleClicked.connect(self.whitelist_opentaginbrowser)
            self.blacklist.itemDoubleClicked.connect(self.blacklist_opentaginbrowser)
            self.search_button.clicked.connect(self.multi_search)
#---------update-signals---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.startslider.valueChanged.connect(self.update_start)
            self.stopslider.valueChanged.connect(self.update_stop)
            self.updatebutton.clicked.connect(self.update_datamap)
#---------result-signals---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if True:
            self.tabWidget.currentChanged.connect(self.load_result_filelist)
            self.loadfilebutton.clicked.connect(self.load_results)
            self.resultlist.currentItemChanged.connect(self.preview)
            self.tags.itemDoubleClicked.connect(self.tags_opentaginbrowser)
            self.characters.itemDoubleClicked.connect(self.characters_opentaginbrowser)
            self.artistsandgroups.itemDoubleClicked.connect(self.artistsandgroups_opentaginbrowser)
            self.parodies.itemDoubleClicked.connect(self.parodies_opentaginbrowser)
            self.internalbrowserbutton.clicked.connect(self.opengalleryinternal)
            self.externalbrowserbutton.clicked.connect(self.opengalleryexternal)
            self.deletefilebutton.clicked.connect(self.deletefile)
#---------set-text---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def retranslateUi(self, HentaiFoxDesktop):
        _translate = QtCore.QCoreApplication.translate
        HentaiFoxDesktop.setWindowTitle(_translate("HentaiFoxDesktop", "HentaiFox Desktop"))
        self.downloadbutton.setText(_translate("HentaiFoxDesktop", "Download Gallery"))
        self.label_zoom.setText(_translate("HentaiFoxDesktop", "Zoom:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.browse), _translate("HentaiFoxDesktop", "Browse"))
        self.label.setText(_translate("HentaiFoxDesktop", "Press \"search\" to search for galleries featuring the whitelisted tags and not featuring the blacklisted tags."))
        self.whitelist_arrows_r.setText(_translate("HentaiFoxDesktop", ">>>>>>>>>>>>>>"))
        self.whitelist_addbutton.setText(_translate("HentaiFoxDesktop", "Add to Whitelist"))
        self.whitelist_removebutton.setText(_translate("HentaiFoxDesktop", "Remove from Whitelist"))
        self.whitelist_arrows_l.setText(_translate("HentaiFoxDesktop", "<<<<<<<<<<<<<<"))
        self.blacklist_arrows_r.setText(_translate("HentaiFoxDesktop", ">>>>>>>>>>>>>>"))
        self.blacklist_addbutton.setText(_translate("HentaiFoxDesktop", "Add to Blacklist"))
        self.blacklist_removebutton.setText(_translate("HentaiFoxDesktop", "Remove from Blacklist"))
        self.blacklist_arrows_l.setText(_translate("HentaiFoxDesktop", "<<<<<<<<<<<<<<"))
        self.label_choosedoubleclickfunc.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Doubleclick Tag to:</p></body></html>"))
        self.check_internal.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.check_external.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.label_amount.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Amount of Galleries containing the selected Tag:</p></body></html>"))
        self.label_percentage.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Percentage of Galleries containing the selected Tag:</p></body></html>"))
        self.check_loadfacts.setText(_translate("HentaiFoxDesktop", "Disable Pagecounter"))
        self.search_button.setText(_translate("HentaiFoxDesktop", "Search"))
        self.diagnostics.setText(_translate("HentaiFoxDesktop", "Search Diagnostics..."))
        self.describtion.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Chloroform, or trichloromethane, is an organic compound with formula CHCl<span style=\" vertical-align:sub;\">3.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search), _translate("HentaiFoxDesktop", "Multi-Search"))
        self.check_preview.setText(_translate("HentaiFoxDesktop", "Disable Preview (less interactions with the website)"))
        self.loadfilebutton.setText(_translate("HentaiFoxDesktop", "Load selected .result file"))
        self.deletefilebutton.setText(_translate("HentaiFoxDesktop", "Delete the selected .result file"))
        self.label_info.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>The Filename is constructed by the white- and blacklisted tags. First the whitelisted tags combined with a &quot;-&quot;, second the blacklisted tags added with a &quot;!&quot;.</p><p>The filetype &quot;.result&quot; is a custom json file containing the results of a Multi-search.</p><p>You can add external .result files by dropping them in the &quot;Results (JSON)&quot; folder. </p><p>You can also find a txt-file containing just the URLs in the &quot;Results (TXT)&quot; folder.</p><p>The delete button will delete both the .result file and the corresponding .txt file.</p></body></html>"))
        self.title.setText(_translate("HentaiFoxDesktop", "Title"))
        self.lable_tags.setText(_translate("HentaiFoxDesktop", "Tags:"))
        self.lable_artistandgroups.setText(_translate("HentaiFoxDesktop", "Artist and Groups:"))
        self.lable_parodies.setText(_translate("HentaiFoxDesktop", "Parodies:"))
        self.label_choose_doubleclickfunc2.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Doubleclick Tag to:</p></body></html>"))
        self.check_internal2.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.check_external2.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.internalbrowserbutton.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.externalbrowserbutton.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.lable_characters.setText(_translate("HentaiFoxDesktop", "Characters:"))
        self.label_pages.setText(_translate("HentaiFoxDesktop", "Pages:"))
        self.category.setText(_translate("HentaiFoxDesktop", "Category"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results), _translate("HentaiFoxDesktop", "Result-Viewer"))
        self.label_credits.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>Credits:</p><p><br/></p><p>Written in Python by Niggo Jächa.</p><p>GUI powerd by PyQt5.</p><p><br/></p><p>This project aims to give Hentaifox.com the last 10% for a 10/10!</p><p><br/></p><p>Im searching for volunteers to write descriptions for all the tags (390) and maybe even a view artists, groups, parodies etc.<br/></p><p>If you have questions join the Hentaifox Discord server:<br/>https://discord.gg/QksFct</p><p><br/></p><p>Contact: </p><p>Discord: N. Jächa#1707</p><p>Email: andre.grabowich@gmail.com</p><p>Thanks to HentaiFox for this great Website!</p></body></html>"))
        self.start.setText(_translate("HentaiFoxDesktop", "Start searching for gaps and updates at: 1"))
        self.stop.setText(_translate("HentaiFoxDesktop", "Stop searching for gaps and updates at: 1"))
        self.updatebutton.setText(_translate("HentaiFoxDesktop", "Update"))
        self.label_version.setText(_translate("HentaiFoxDesktop", "<html><head/><body><p>HF-Desktop v.1.3</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.update), _translate("HentaiFoxDesktop", "Update-Datamap"))
#---------browser-functions------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if True:
        def add_new_tab(self, qurl=None, label="Loading..."):
            if qurl is None:
                qurl = QUrl('https://hentaifox.com/')
            browser = WebEngineView(self)
            browser.setUrl(qurl)
            i = self.tabs.addTab(browser, label)
            self.tabs.setCurrentIndex(i)
            browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
            browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

        def create_new_tab(self, page):
            browser = page
            i = self.tabs.addTab(browser, "loading...")
            self.tabs.setCurrentIndex(i)
            browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
            browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

        def tab_open_doubleclick(self, i):
            if i == -1:
                self.add_new_tab(qurl=QUrl("https://hentaifox.com/"))

        def current_tab_changed(self, i):
            qurl = self.tabs.currentWidget().url()
            self.update_urlbar(qurl, self.tabs.currentWidget())
            self.update_zoom()
            self.refresh_bookmarks()
            self.update_tab_count()

        def update_zoom(self):
            zoomvalue = int(self.tabs.currentWidget().zoomFactor()*100)
            self.zoomslider.setValue(zoomvalue)

        def close_current_tab(self, i):
            if self.tabs.count() < 2:
                return

            self.tabs.removeTab(i)

        def navigate_home(self):
            self.tabs.currentWidget().setUrl(QUrl("https://hentaifox.com/"))

        def navigate_to_url(self):
            q = QUrl(self.urlbar.text())
            if q.scheme() == "":
                q.setScheme("http")
            url_raw = q.url()
            if str(url_raw).startswith("http:"):
                url_raw = str(url_raw).replace("http:","https://")
            if url_raw.startswith("https://hentaifox.com"):
                self.tabs.currentWidget().setUrl(QUrl(url_raw))

        def update_urlbar(self, q, browser=None):
            if browser != self.tabs.currentWidget():
                return

            self.urlbar.setText(q.toString())
            self.urlbar.setCursorPosition(0)
            self.refresh_bookmarks()

            if q.toString() != "":
                if not q.toString().startswith("https://hentaifox.com/"):
                    if browser.history().canGoBack() == True:
                        browser.back()
                    else:
                        self.tabs.removeTab(self.tabs.currentIndex())

        def zoom_browser(self):
            webview = self.tabs.currentWidget()
            zoomfactor = int(self.zoomslider.value())*0.01
            webview.setZoomFactor(zoomfactor)

        def zoom_browser2(self,value):
            if self.tabs.currentWidget().zoomFactor()+0.1 < 2 and value >0:
                zoomfactor = self.tabs.currentWidget().zoomFactor()+value
                self.tabs.currentWidget().setZoomFactor(zoomfactor)
                self.update_zoom()
            if value <0:
                zoomfactor = self.tabs.currentWidget().zoomFactor()+value
                self.tabs.currentWidget().setZoomFactor(zoomfactor)
                self.update_zoom()

        def reset_zoom(self):
            self.tabs.currentWidget().setZoomFactor(1)
            self.update_zoom()

        def download(self):
            url = self.tabs.currentWidget().url().url()
            if url.startswith("https://hentaifox.com/g/"):
                web = requests.get(f"{url}")
                html = web.text
                soup = BeautifulSoup(html, 'html.parser')
                okay = str(soup.find('div',attrs={"class":"browse_buttons"}))
                gal = okay[okay.find('href="')+6:okay.find('">Back')]
                url = f"https://hentaifox.com{gal}"
            if url[:30] == "https://hentaifox.com/gallery/":

                def download(url2,x):
                    resource = requests.get(url2)
                    if str(resource) == "<Response [200]>":
                        output = open(f"{title}\{x}.jpg","wb")
                        output.write(resource.content)
                        output.close()
                        print(f"{x} done")
                    else:
                        url2 = url2[:-3] + "png"
                        resource2 = requests.get(url2)
                        output = open(f"{title}\{x}.png","wb")
                        output.write(resource2.content)
                        output.close()
                        print(f"{x} done")

                web = requests.get(f"{url}")
                html = web.text
                soup = BeautifulSoup(html, 'html.parser')
                okay = soup.find('title')
                title = str(okay.text).replace("|","_").replace(".","")
                if str(okay) != "<title>404 Not Found - HentaiFox</title>":
                    dir = str(html)[str(html).find('input type="hidden" name="load_dir" id="load_dir"')+57:str(html).find('input type="hidden" name="load_dir" id="load_dir"')+60]
                    show_all_id_raw = str(soup.find("input", attrs={"type":"hidden","name":"load_id","id":"load_id"}))
                    show_all_pages_raw = str(soup.find("input", attrs={"type":"hidden","name":"load_pages","id":"load_pages"}))
                    id = show_all_id_raw[show_all_id_raw.find('value="')+7:-3]
                    pages = show_all_pages_raw[show_all_pages_raw.find('value="')+7:-3]
                    msg = QtWidgets.QMessageBox
                    reply = msg.question(self.tabs,"Download",f"Do you really want to download\n{okay.text[:-12]}?",msg.Ok|msg.Cancel)
                    if reply == msg.Ok:
                        try:
                            os.mkdir(f"./{title}")
                        except FileExistsError:
                            print("Warning: Folder already exists")
                            pass
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            for x in range(int(pages)+1):
                                if x > 0:
                                    url2 = f"https://i.hentaifox.com/{dir}/{id}/{x}.jpg"
                                    executor.submit(download, url2, x)

                        with ZipFile(f"Download/{title}.zip", "w") as zip:
                            print("Zipping...")
                            for file in os.listdir(f"./{title}/"):
                                zip.write(f"{title}/{file}")
                            print("Zipping done")
                            shutil.rmtree(f'./{title}/')
                        msg = QtWidgets.QMessageBox(self.tabs)
                        msg.setWindowTitle("Download Finished")
                        msg.setText(f'You can find\n"{title}.zip"\nin the "Download" folder.' )
                        msg.exec_()

        def add_bookmark(self):
            bookmark_actions = []
            for action in self.bookmarkMenu.actions():
                if action.text().startswith("https://"):
                    bookmark_actions.append(action.text())
            url = self.tabs.currentWidget().url().url()
            if url not in bookmark_actions:
                with open("data/bookmarks.json","r") as f:
                    bookmarks = json.load(f)
                if url not in bookmarks:
                    bookmarks.append(url)
                with open("data/bookmarks.json","w") as f:
                    json.dump(bookmarks,f,indent=4)
                self.refresh_bookmarks(mode="remove")

        def remove_bookmark(self):
            bookmark_actions = []
            for action in self.bookmarkMenu.actions():
                if action.text().startswith("https://"):
                    bookmark_actions.append(action.text())
            url = self.tabs.currentWidget().url().url()
            if url in bookmark_actions:
                with open("data/bookmarks.json","r") as f:
                    bookmarks = json.load(f)
                if url in bookmarks:
                    bookmarks.remove(url)
                with open("data/bookmarks.json","w") as f:
                    json.dump(bookmarks,f,indent=4)
                self.refresh_bookmarks(mode="add")

        def refresh_bookmarks(self,mode=None):
            bookmark_actions = []
            for action in self.bookmarkMenu.actions():
                if action.text().startswith("https://"):
                    bookmark_actions.append(action.text())

            url = self.tabs.currentWidget().url().url()

            with open("data/bookmarks.json","r") as f:
                bookmarks = json.load(f)

            if mode == None:
                if url in bookmark_actions:
                    mode = "remove"
                elif url not in bookmark_actions:
                    mode = "add"
            if mode == "remove":
                self.bookmark.setIcon(QIcon("icons/BookmarkSet.png"))
                self.bookmarkMenu.clear()
                self.bookmarkMenu.addAction(QIcon("icons/remove_Bookmark.png"),"Remove Bookmark",self.remove_bookmark,QKeySequence("Ctrl+D"))
                self.bookmarkMenu.addSeparator()
                for bookmark in bookmarks:
                    self.bookmarkMenu.addAction(f"{bookmark}",lambda bookmark=bookmark: self.load_bookmark(bookmark))
            elif mode == "add":
                self.bookmark.setIcon(QIcon("icons/Bookmark.png"))
                self.bookmarkMenu.clear()
                self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"),"Add Bookmark",self.add_bookmark,QKeySequence("Ctrl+D"))
                self.bookmarkMenu.addSeparator()
                for bookmark in bookmarks:
                    self.bookmarkMenu.addAction(f"{bookmark}",lambda bookmark=bookmark: self.load_bookmark(bookmark))

        def load_bookmark(self,bookmark):
            self.add_new_tab(qurl=QUrl(f"{bookmark}"),label="loading...")

        def update_tab_count(self):
            lenght = self.tabs.count()
            self.tabsMenu.clear()
            for x in range(lenght):
                if x <= 8:
                    i = x+1
                    self.tabsMenu.addAction(f"Switch to Tab {i}",lambda x=x: self.tabs.setCurrentIndex(x),QKeySequence(f"Ctrl+{i}"))
#---------multi-search-functions-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if True:

        def update_taglist(self):
            self.criterialist.clear()
            if self.choosetype.currentText() == "tags":
                for abc in item_list["tags"]:
                    self.criterialist.addItem(f"{abc}")
            if self.choosetype.currentText() == "parodies":
                for abc in item_list["parodies"]:
                    self.criterialist.addItem(f"{abc}")
            if self.choosetype.currentText() == "characters":
                for abc in item_list["characters"]:
                    self.criterialist.addItem(f"{abc}")
            if self.choosetype.currentText() == "artists":
                for abc in item_list["artists"]:
                    self.criterialist.addItem(f"{abc}")
            if self.choosetype.currentText() == "groups":
                for abc in item_list["groups"]:
                    self.criterialist.addItem(f"{abc}")
            if self.choosetype.currentText() == "categories":
                for abc in item_list["categories"]:
                    self.criterialist.addItem(f"{abc}")

        def whitelist_add(self):
            current = self.criterialist.currentItem()
            if current != None:
                type = self.choosetype.currentText()
                item = self.criterialist.takeItem(self.criterialist.row(self.criterialist.currentItem()))
                self.whitelist.addItem(f"{item.text()} ({type})")
                white_list[self.choosetype.currentText()].append(item.text())
                item_list[self.choosetype.currentText()].remove(item.text())

        def whitelist_remove(self):
            current = self.whitelist.currentItem()
            if current != None:
                item_raw = self.whitelist.takeItem(self.whitelist.row(self.whitelist.currentItem()))
                item_name = item_raw.text()[:item_raw.text().find(" (")]
                item_type = item_raw.text()[item_raw.text().find("(")+1:item_raw.text().find(")")]
                white_list[item_type].remove(item_name)
                item_list[item_type].append(item_name)
                item_list[item_type].sort()
                self.update_taglist()

        def blacklist_add(self):
            current = self.criterialist.currentItem()
            if current != None:
                type = self.choosetype.currentText()
                item = self.criterialist.takeItem(self.criterialist.row(self.criterialist.currentItem()))
                self.blacklist.addItem(f"{item.text()} ({type})")
                black_list[self.choosetype.currentText()].append(item.text())
                item_list[self.choosetype.currentText()].remove(item.text())

        def blacklist_remove(self):
            current = self.blacklist.currentItem()
            if current != None:
                item_raw = self.blacklist.takeItem(self.blacklist.row(self.blacklist.currentItem()))
                item_name = item_raw.text()[:item_raw.text().find(" (")]
                item_type = item_raw.text()[item_raw.text().find("(")+1:item_raw.text().find(")")]
                black_list[item_type].remove(item_name)
                item_list[item_type].append(item_name)
                item_list[item_type].sort()
                self.update_taglist()

        def update_gallerycounter(self,abc,type):
            if self.check_loadfacts.isChecked() == False:
                try:
                    count = data[type][abc]
                    self.pagecount.display(count)
                    percentage = int(count)/int(latest_gallery)
                    self.percentagecount.setValue(int(percentage*100))
                    with open("data/descriptions.json","r") as d:
                        with open("data/wikientries.json","r") as b:
                            desps = json.load(d)
                            wdes = json.load(b)
                            description = desps[type][abc]
                            if type == "tags":
                                wdescription = wdes["tags"][abc]
                                text = f"Wikidescription (by ehwiki.org):\n{wdescription}\n\nUserdescriptions:\n{description}"
                            else:
                                text = f"{description}"
                            self.describtion.setText(text)
                except:
                    print("Error while loading the description or gallery-counter")

        def criterialist_update_gallerycounter(self):
            current_abc = self.criterialist.currentItem().text()
            current_type = self.choosetype.currentText()
            self.update_gallerycounter(abc=current_abc,type=current_type)

        def whitelist_update_gallerycounter(self):
            current_abc = self.whitelist.currentItem().text()[:self.whitelist.currentItem().text().find(" (")]
            current_type = self.whitelist.currentItem().text()[self.whitelist.currentItem().text().find("(")+1:self.whitelist.currentItem().text().find(")")]
            self.update_gallerycounter(abc=current_abc,type=current_type)

        def blacklist_update_gallerycounter(self):
            current_abc = self.blacklist.currentItem().text()[:self.blacklist.currentItem().text().find(" (")]
            current_type = self.blacklist.currentItem().text()[self.blacklist.currentItem().text().find("(")+1:self.blacklist.currentItem().text().find(")")]
            self.update_gallerycounter(abc=current_abc,type=current_type)

        def opentaginbrowser(self,type,abc):
            if type == "parodies":
                type = "parody"
            else:
                type = type[:-1]
            abc = abc.replace(" ", "-").replace(".","")
            if abc.endswith("-"):
                abc = abc[:-1]
            if self.check_internal.isChecked() == True:
                qurl = QtCore.QUrl(f"https://hentaifox.com/{type}/{abc}/")
                self.tabWidget.setCurrentIndex(0)
                self.add_new_tab(qurl,label="loading...")
            elif self.check_external.isChecked() == True:
                os.system(f"start https://hentaifox.com/{type}/{abc}/")

        def criterialist_opentaginbrowser(self):
            current_abc = self.criterialist.currentItem().text()
            current_type = self.choosetype.currentText()
            self.opentaginbrowser(abc=current_abc,type=current_type)

        def whitelist_opentaginbrowser(self):
            current_abc = self.whitelist.currentItem().text()[:self.whitelist.currentItem().text().find(" (")]
            current_type = self.whitelist.currentItem().text()[self.whitelist.currentItem().text().find("(")+1:self.whitelist.currentItem().text().find(")")]
            self.opentaginbrowser(abc=current_abc,type=current_type)

        def blacklist_opentaginbrowser(self):
            current_abc = self.blacklist.currentItem().text()[:self.blacklist.currentItem().text().find(" (")]
            current_type = self.blacklist.currentItem().text()[self.blacklist.currentItem().text().find("(")+1:self.blacklist.currentItem().text().find(")")]
            self.opentaginbrowser(abc=current_abc,type=current_type)

        def multi_search(self):
            if self.whitelist.count() > 0:
                start_time = time.time()
                duration = 0
                comparisons = 0
                iterations = 0
                jsons = 0
                filename1 = ""
                for type in types:
                    for abc in white_list[type]:
                        filename1 = filename1 + f"{abc}-"
                filename = filename1[:-1].replace(" ","_")

                round = 1
                rounds = 0
                for type in types:
                    for abc in white_list[type]:
                        rounds += 1

                for type in types:
                    for abc in white_list[type]:
                        with open(f"{type}/{abc}.json","r") as f:
                            data = json.load(f)
                            jsons += 1
                        if round == 1:
                            iterations += 1
                            tag_galleries["1"] = []
                            print(f"Loading galleries containing '{abc}'...")
                            for gallery in data["galleries"]:
                                tag_galleries["1"].append(gallery)
                            if rounds == 1:
                                still_results = True
                                break
                        if round != 1:
                            iterations += 1
                            if round <= rounds:
                                tag_galleries[str(round)] = []
                                print(f"Passing galleries containing '{abc}'...")
                                for gallery in data["galleries"]:
                                    comparisons += 1
                                    if gallery in tag_galleries[str(round-1)]:
                                        tag_galleries[str(round)].append(gallery)
                            if round == rounds:
                                if len(tag_galleries[str(round)]) > 0:
                                    still_results = True
                                    break
                                else:
                                    still_results = False
                        round += 1
                if self.blacklist.count() > 0:
                    for type in types:
                        for abc in black_list[type]:
                            iterations += 1
                            print(f"Removing galleries containing '{abc}'...")
                            filename = f"{filename}!{str(abc).replace(' ','_')}"
                            with open(f"{type}/{abc}.json","r") as f:
                                data = json.load(f)
                            for gallery in data["galleries"]:
                                comparisons += 1
                                if gallery in tag_galleries[str(round)]:
                                    tag_galleries[str(round)].remove(gallery)
                            if len(tag_galleries[str(round)]) > 0:
                                still_results = True
                            else:
                                still_results = False
                else:
                    print("Blacklist empty...")
                if still_results == True:
                    with open(f"Results (TXT)/{filename}.txt", "w+") as d:
                        num = 0
                        for gallery in tag_galleries[str(round)]:
                            d.write(f"https://hentaifox.com/gallery/{gallery}/\n")
                            num += 1
                    with open(f"Results (JSON)/{filename}.result","w") as j:
                        data = []
                        for gallery in tag_galleries[str(round)]:
                            data.append(f"https://hentaifox.com/gallery/{gallery}/")
                        json.dump(data,j,indent=4)
                else:
                    print("finished")
                    self.label.setText(f'Sorry no results for the combination \n\n{filename}.')
                    duration = time.time()-start_time
                print("finished")
                self.label.setText(f'Found {num} galleries. You can find "{filename}.txt" in the "Results (TXT)" folder and "{filename}.result" in the "Results (JSON)" folder.')
                duration = time.time()-start_time
                try:
                    self.diagnostics.setText(f"Search Diagnostics:\n\nGalleries found: {num}\nDuration: {duration} seconds\nJson-files loaded: {jsons}\nIterations: {iterations}\nComparisons: {comparisons}")
                except:
                    pass
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText(f'You need to add items to the whitelist.\nFor blacklist only, please use the blacklist feature on the website.')
                msg.exec_()
#---------update-functions-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if True:
        def update_start(self):
            self.start.setText(f"Start searching for gaps and updates at: {self.startslider.value()}")
        def update_stop(self):
            self.stop.setText(f"Stop searching for gaps and updates at: {self.stopslider.value()}")

        def update_datamap(self):
            if self.stopslider.value() > self.startslider.value():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("UPDATE")
                msg.setText(f"About to update the datamap.\nThis may take a while.\nFor progress look at the console.")
                x=msg.exec_()
                parodies = {}
                characters = {}
                tags = {}
                artists = {}
                groups = {}
                categories = {}
                titles = {}
                pagecount = {}
                gals = {}
                found= {}
                not_found= []

                types = ["parodies","characters","tags","artists","groups","categories"]
                for type in types:
                    for file in os.listdir(f"./{type}/"):
                        abc = str(file)[:-5]
                        with open(f"{type}/{abc}.json","r") as g:
                            gals_per_tag = json.load(g)
                            gals[abc] = gals_per_tag["galleries"]
                            print(f"loading: {type}/{abc}")

                start_id = self.startslider.value()
                y = self.stopslider.value()

                for x in range(start_id,int(y+1)):
                    print(f"searching for {x}")
                    found[x]= "not found"
                    for abc in gals:
                        if x in gals[abc]:
                            found[x]= "found"
                            break
                print("writing list of missing galleries...")
                for gal in found:
                    if found[gal] == "found":
                        pass
                    else:
                        not_found.append(gal)
                print("finished writing list of missing galleries. (not_found.json)")

                with open("not_found.json","w") as f:
                    data = not_found
                    json.dump(data,f,indent=4)

                gaps = []
                print("scraping missing galleries...")
                def fetch(x):
                    web = requests.get(f"https://hentaifox.com/gallery/{x}/")
                    print(f"Request finished ({x})")
                    html = web.text
                    soup = BeautifulSoup(html, 'html.parser')
                    okay = soup.find('title')
                    if str(okay) == "<title>404 Not Found - HentaiFox</title>":
                        with open("gaps.txt","a+") as f:
                            f.write(f"\ngap at {x}")
                    else:
                        titles[x] = str(str(okay.text).replace(" - HentaiFox"," ")[:-1])
                        try:
                            pages_raw = soup.find("span", attrs={"class":"i_text pages"}).text
                            pages = pages_raw[pages_raw.find(": ")+2:]
                            pagecount[x] = pages
                        except:
                            pass

                    par_result = soup.find_all('ul', attrs={'class':'parodies'})
                    if par_result != []:
                        par_res = par_result[0]
                        pars_raw = par_res.find_all('a', attrs={'class':'tag_btn'})
                        for par_raw in pars_raw:
                            try:
                                split_tag = par_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            par = par_raw.text[:-len(par_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(par_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                                if str(par) in parodies:
                                    pass
                                else:
                                    parodies[par] = []
                                parodies[par].append(x)

                    char_result = soup.find_all('ul', attrs={'class':'characters'})
                    if char_result != []:
                        char_res = char_result[0]
                        chars_raw = char_res.find_all('a', attrs={'class':'tag_btn'})
                        for char_raw in chars_raw:
                            try:
                                split_tag = char_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            char = char_raw.text[:-len(char_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(char_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                                if str(char) in characters:
                                    pass
                                else:
                                    characters[char] = []
                                characters[char].append(x)

                    tag_result = soup.find_all('ul', attrs={'class':'tags'})
                    if tag_result != []:
                        tag_res = tag_result[0]
                        tags_raw = tag_res.find_all('a', attrs={'class':'tag_btn'})
                        for tag_raw in tags_raw:
                            try:
                                split_tag = tag_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            tag = tag_raw.text[:-len(tag_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(tag_raw.find("span",attrs={'class':'t_badge'}).text) > 100:
                                if str(tag) in tags:
                                    pass
                                else:
                                    tags[tag] = []
                                tags[tag].append(x)

                    art_result = soup.find_all('ul', attrs={'class':'artists'})
                    if art_result != []:
                        art_res = art_result[0]
                        arts_raw = art_res.find_all('a', attrs={'class':'tag_btn'})
                        for art_raw in arts_raw:
                            try:
                                split_tag = art_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            art = art_raw.text[:-len(art_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(art_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                                if str(art) in artists:
                                    pass
                                else:
                                    artists[art] = []
                                artists[art].append(x)

                    grp_result = soup.find_all('ul', attrs={'class':'groups'})
                    if grp_result != []:
                        grp_res = grp_result[0]
                        grps_raw = grp_res.find_all('a', attrs={'class':'tag_btn'})
                        for grp_raw in grps_raw:
                            try:
                                split_tag = grp_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            grp = grp_raw.text[:-len(grp_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(grp_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                                if str(grp) in groups:
                                    pass
                                else:
                                    groups[grp] = []
                                groups[grp].append(x)

                    cat_result = soup.find_all('ul', attrs={'class':'categories'})
                    if cat_result != []:
                        cat_res = cat_result[0]
                        cats_raw = cat_res.find_all('a', attrs={'class':'tag_btn'})
                        for cat_raw in cats_raw:
                            try:
                                split_tag = cat_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            cat = cat_raw.text[:-len(cat_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            if int(cat_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                                if str(cat) in categories:
                                    pass
                                else:
                                    categories[cat] = []
                                categories[cat].append(x)

                    return f"Done ({x})"

                def save():
                    print("saving all")

                    pagecount_copy = dict(pagecount)
                    with open("data/pages.json", "r") as f:
                        data = json.load(f)
                        data.update(pagecount_copy)
                    with open("data/pages.json", "w") as f:
                        json.dump(data,f,indent=4)

                    title_copy = dict(titles)
                    with open("data/titles.json", "r") as f:
                        data = json.load(f)
                        data.update(title_copy)
                    with open("data/titles.json", "w") as f:
                        json.dump(data,f,indent=4)

                    tags_copy = dict(tags)
                    for tag in tags_copy:
                        if os.path.exists(f"tags/{tag}.json"):
                            pass
                        else:
                            with open(f"tags/{tag}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"tags/{tag}.json","r")as f:
                            data = json.load(f)
                            for gal in tags_copy[tag]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"tags/{tag}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"tags/{tag} saved")
                        tags[tag] = []

                    parodies_copy = dict(parodies)
                    for par in parodies_copy:
                        if os.path.exists(f"parodies/{par}.json"):
                            pass
                        else:
                            with open(f"parodies/{par}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"parodies/{par}.json","r")as f:
                            data = json.load(f)
                            for gal in parodies_copy[par]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"parodies/{par}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"parodies/{par} saved")
                        parodies[par] = []

                    characters_copy = dict(characters)
                    for char in characters_copy:
                        if os.path.exists(f"characters/{char}.json"):
                            pass
                        else:
                            with open(f"characters/{char}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"characters/{char}.json","r")as f:
                            data = json.load(f)
                            for gal in characters_copy[char]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"characters/{char}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"parodies/{char} saved")
                        characters[char] = []

                    artists_copy = dict(artists)
                    for art in artists_copy:
                        if os.path.exists(f"artists/{art}.json"):
                            pass
                        else:
                            with open(f"artists/{art}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"artists/{art}.json","r")as f:
                            data = json.load(f)
                            for gal in artists_copy[art]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"artists/{art}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"parodies/{art} saved")
                        artists[art] = []

                    groups_copy = dict(groups)
                    for grp in groups_copy:
                        if os.path.exists(f"groups/{grp}.json"):
                            pass
                        else:
                            with open(f"groups/{grp}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"groups/{grp}.json","r")as f:
                            data = json.load(f)
                            for gal in groups_copy[grp]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"groups/{grp}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"groups/{grp} saved")
                        groups[grp] = []

                    categories_copy = dict(categories)
                    for cat in categories_copy:
                        if os.path.exists(f"categories/{cat}.json"):
                            pass
                        else:
                            with open(f"categories/{cat}.json","w+") as f:
                                f.write('{"galleries": []}')
                        with open(f"categories/{cat}.json","r")as f:
                            data = json.load(f)
                            for gal in categories_copy[cat]:
                                data["galleries"].append(gal)
                                data["galleries"].sort()
                            with open(f"categories/{cat}.json","w")as f:
                                json.dump(data,f,indent=4)
                                print(f"categories/{cat} saved")
                        categories[cat] = []
                    print("finished saving")

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = [executor.submit(fetch, x) for x in not_found]
                    for f in concurrent.futures.as_completed(results):
                        print(f.result())

                save()
                with open("404.txt","w+") as f:
                    for gal in gaps:
                        content = f.read()
                        f.write(f"{content}\n{gal}")

                things = {}

                types = ["parodies","characters","tags","artists","groups","categories"]
                for type in types:
                    things[type] = {}
                    for file in os.listdir(f"./{type}/"):
                        abc = str(file)[:-5]
                        try:
                            with open(f"{type}/{abc}.json","r") as g:
                                gals = json.load(g)
                            things[type][abc] = len(gals["galleries"])
                            print(f"Counting galleries: {type}/{abc}.json")
                        except:
                            print(f"ERROR: {type}/{abc}.json is broken. The created file is not usable.")
                            break

                with open("data/data.json","w") as f:
                    json.dump(things,f,indent=4)
                print("--- datamap update finished ---")
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Finished")
                msg.setText(f"Datamap up to date.\nWrote URLs of gaps into 404.txt\n")
                x=msg.exec_()
#---------result-functions-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if True:

        def load_result_filelist(self):
            self.filebrowser.clear()
            if self.tabWidget.currentIndex() == 2:
                for file in os.listdir("./Results (JSON)/"):
                    if file.endswith(".result"):
                        self.filebrowser.addItem(file)

        def load_results(self):
            self.resultlist.clear()
            if self.filebrowser.currentItem() != None:
                result_file = self.filebrowser.currentItem().text()
                with open(f"Results (JSON)/{result_file}","r") as f:
                    data = json.load(f)
                    for gallery in data:
                        self.resultlist.addItem(gallery)

        def preview(self):
            if self.check_preview.isChecked() == False:
                if self.resultlist.currentItem() != None:
                    self.tags.clear()
                    self.characters.clear()
                    self.artistsandgroups.clear()
                    self.parodies.clear()

                    url = self.resultlist.currentItem().text()
                    web = requests.get(url)
                    html = web.text
                    soup = BeautifulSoup(html, 'html.parser')
                    pages_raw = soup.find("span", attrs={"class":"i_text pages"}).text
                    pages= pages_raw[pages_raw.find(": ")+2:]
                    self.pagescount2.display(pages)
                    title = soup.find('title').text.replace("|","\n").replace("- HentaiFox", "")
                    self.title.setText(title)

                    par_result = soup.find_all('ul', attrs={'class':'parodies'})
                    if par_result != []:
                        par_res = par_result[0]
                        pars_raw = par_res.find_all('a', attrs={'class':'tag_btn'})
                        for par_raw in pars_raw:
                            try:
                                split_tag = par_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            par = par_raw.text[:-len(par_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            self.parodies.addItem(par)


                    char_result = soup.find_all('ul', attrs={'class':'characters'})
                    if char_result != []:
                        char_res = char_result[0]
                        chars_raw = char_res.find_all('a', attrs={'class':'tag_btn'})
                        for char_raw in chars_raw:
                            try:
                                split_tag = char_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            char = char_raw.text[:-len(char_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            self.characters.addItem(char)

                    tag_result = soup.find_all('ul', attrs={'class':'tags'})
                    if tag_result != []:
                        tag_res = tag_result[0]
                        tags_raw = tag_res.find_all('a', attrs={'class':'tag_btn'})
                        for tag_raw in tags_raw:
                            try:
                                split_tag = tag_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            tag = tag_raw.text[:-len(tag_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            self.tags.addItem(tag)

                    art_result = soup.find_all('ul', attrs={'class':'artists'})
                    if art_result != []:
                        art_res = art_result[0]
                        arts_raw = art_res.find_all('a', attrs={'class':'tag_btn'})
                        for art_raw in arts_raw:
                            try:
                                split_tag = art_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            art = art_raw.text[:-len(art_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            self.artistsandgroups.addItem(f"{art} (Artist)")

                    grp_result = soup.find_all('ul', attrs={'class':'groups'})
                    if grp_result != []:
                        grp_res = grp_result[0]
                        grps_raw = grp_res.find_all('a', attrs={'class':'tag_btn'})
                        for grp_raw in grps_raw:
                            try:
                                split_tag = grp_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            grp = grp_raw.text[:-len(grp_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            self.artistsandgroups.addItem(f"{grp} (Group)")

                    cat_result = soup.find_all('ul', attrs={'class':'categories'})
                    category_text = ""
                    if cat_result != []:
                        cat_res = cat_result[0]
                        cats_raw = cat_res.find_all('a', attrs={'class':'tag_btn'})
                        for cat_raw in cats_raw:
                            try:
                                split_tag = cat_raw.find("span", attrs={"class":"split_tag"}).text
                            except:
                                split_tag = ''
                            cat = cat_raw.text[:-len(cat_raw.find("span", attrs={"class":"t_badge"}).text)][:-1].replace(split_tag,'')
                            category_text = category_text + f"Category: [{cat}]"
                        self.category.setText(category_text)

                    image_raw = str(soup.find("div", attrs={'class':"cover"}))
                    image = image_raw[image_raw.find("src=")+5:image_raw.find('"/>')]
                    grab = requests.get(image, stream=True)
                    if grab.status_code == 200:
                        with open("Icons/cover.jpg", "wb") as f:
                            grab.raw.decode_content = True
                            shutil.copyfileobj(grab.raw, f)

                    width = self.cover.size().width()
                    height = self.cover.size().height()
                    if (width/height) > (350/496):
                        self.cover.setPixmap(QtGui.QPixmap("Icons/cover.jpg").scaled(QtCore.QSize(int((350/496)*height),int(height)),QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation))
                    elif (width/height) <= (350/496):
                        self.cover.setPixmap(QtGui.QPixmap("Icons/cover.jpg").scaled(QtCore.QSize(int(width),int(width/(350/496))),QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation))

        def opentaginbrowser2(self,type,abc):
            if type == "parodies":
                type = "parody"
            else:
                type = type[:-1]
            abc = abc.replace(" ", "-").replace(".","")
            if abc.endswith("-"):
                abc = abc[:-1]
            if self.check_internal2.isChecked() == True:
                qurl = QtCore.QUrl(f"https://hentaifox.com/{type}/{abc}/")
                self.tabWidget.setCurrentIndex(0)
                self.add_new_tab(qurl,label="loading...")
            elif self.check_external2.isChecked() == True:
                os.system(f"start https://hentaifox.com/{type}/{abc}/")

        def tags_opentaginbrowser(self):
            current_abc = self.tags.currentItem().text()
            current_type = "tags"
            self.opentaginbrowser2(abc=current_abc,type=current_type)

        def characters_opentaginbrowser(self):
            current_abc = self.characters.currentItem().text()
            current_type = "characters"
            self.opentaginbrowser2(abc=current_abc,type=current_type)

        def parodies_opentaginbrowser(self):
            current_abc = self.parodies.currentItem().text()
            current_type = "parodies"
            self.opentaginbrowser2(abc=current_abc,type=current_type)

        def artistsandgroups_opentaginbrowser(self):
            current_abc = self.artistsandgroups.currentItem().text()[:self.artistsandgroups.currentItem().text().find(" (")]
            current_type = self.artistsandgroups.currentItem().text()[self.artistsandgroups.currentItem().text().find("(")+1:self.artistsandgroups.currentItem().text().find(")")]
            if current_type == "Group":
                current_type = "groups"
            if current_type == "Artist":
                current_type = "artists"
            self.opentaginbrowser2(abc=current_abc,type=current_type)

        def opengalleryinternal(self):
            url = self.resultlist.currentItem().text()
            qurl = QtCore.QUrl(url)
            self.tabWidget.setCurrentIndex(0)
            self.add_new_tab(qurl,label="loading...")

        def opengalleryexternal(self):
            url = self.resultlist.currentItem().text()
            os.system(f"start {url}")

        def deletefile(self):
            if self.filebrowser.currentItem() != None:
                result_file = self.filebrowser.currentItem().text()
                os.remove(f"Results (JSON)/{result_file}")
                os.remove(f"Results (TXT)/{result_file[:-7]}.txt")
                self.load_result_filelist()

class WebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.tab = self.parent()

    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.tab)
        self.tab.create_new_tab(new_webview)
        return new_webview

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("HentaiFox Desktop")
    app.setOrganizationName("HentaiFox")
    app.setOrganizationDomain("hentaifox.com")
    app.setWindowIcon(QIcon("Icons/images.jpg"))
    HentaiFoxDesktop = QtWidgets.QMainWindow()
    ui = Ui_HentaiFoxDesktop()
    ui.setupUi(HentaiFoxDesktop)
    HentaiFoxDesktop.show()
    sys.exit(app.exec_())
