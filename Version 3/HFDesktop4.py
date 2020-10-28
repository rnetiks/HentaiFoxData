# region-imports
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from bs4 import BeautifulSoup
from zipfile import ZipFile
import sys
import concurrent.futures
import threading
import requests
import urllib
import os
import shutil
import json
import time
import pyperclip
import sqlite3
import re
import subprocess
#endregion
# region---Global-Setup--------------
conn = sqlite3.connect("Data.db")
c = conn.cursor()

def db_con():
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
db_con()

localdb = sqlite3.connect("Local.db")
loc = localdb.cursor()

types = ["parodies", "characters", "tags", "artists", "groups", "categories"]
white_list = {}
black_list = {}
item_list = {}
result_view_list = []
tag_info_setting = 0
not_in_database = []
_version_ = "v.3.2"
#endregion
# region---Define-Converter----------
def type_converter(type):
    switcher = {
        "parodies":     "parody",
        "characters":   "character",
        "tags":         "tag",
        "artists":      "artist",
        "groups":       "group",
        "categories":   "category"
    }
    return switcher.get(type)
#endregion
# region---Define-Itemlist-----------
def create_itemlist(feature, up_down):
    for type in types:
        typex = type_converter(type)
        white_list[type] = []
        black_list[type] = []
        item_list[type] = []
        c.execute(f"SELECT DISTINCT tag FROM {typex}information WHERE true ORDER BY {feature} {up_down}")
        for tu in c.fetchall():
            item_list[type].append(tu[0])
#endregion
# region---get-latest-gallery--------
web = requests.get("https://hentaifox.com/")
html = web.text
soup = BeautifulSoup(html, "html.parser")
no1 = str(soup.find("div", attrs={"class": "inner_thumb"}))
latest_gallery = int(no1[no1.find("/gallery/") + 9:no1.find('/"><img')])
#endregion
# region fonts
font10 = QtGui.QFont()
font10.setFamily("Arial")
font10.setPointSize(10)
font11 = QtGui.QFont()
font11.setPointSize(11)
font12 = QtGui.QFont()
font12.setPointSize(12)
font13 = QtGui.QFont()
font13.setPointSize(13)
font14 = QtGui.QFont()
font14.setFamily("Arial")
font14.setPointSize(14)
font14.setWeight(50)
font15 = QtGui.QFont()
font15.setFamily("Arial")
font15.setPointSize(15)
font15.setWeight(50)
font30 = QtGui.QFont()
font30.setFamily("Arial")
font30.setPointSize(30)
font30.setWeight(80)
#endregion
# region credentials dialoge
class Credentials_dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Credentials_dialog, self).__init__(*args, **kwargs)
        self.setObjectName("Credentials_dialog")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.resize(500, 500)
        # p = QDesktopWidget().availableGeometry().center() - QPoint(250,250)
        # self.move(p)
        self.lineEdit_U = QLineEdit(self)
        self.lineEdit_U.setObjectName(u"lineEdit_U")
        self.lineEdit_U.setGeometry(QRect(20, 60, 461, 41))
        self.label_U = QLabel(self)
        self.label_U.setObjectName(u"label_U")
        self.label_U.setFont(font14)
        self.label_U.setGeometry(QRect(20, 20, 451, 31))
        self.label_U.setAlignment(Qt.AlignCenter)
        self.label_Pw = QLabel(self)
        self.label_Pw.setObjectName(u"label_Pw")
        self.label_Pw.setFont(font14)
        self.label_Pw.setGeometry(QRect(20, 110, 451, 31))
        self.label_Pw.setAlignment(Qt.AlignCenter)
        self.lineEdit_Pw = QLineEdit(self)
        self.lineEdit_Pw.setObjectName(u"lineEdit_Pw")
        self.lineEdit_Pw.setGeometry(QRect(20, 150, 461, 41))
        self.label_info = QLabel(self)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setFont(font11)
        self.label_info.setGeometry(QRect(30, 210, 461, 170))
        self.label_info.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label_info.setWordWrap(True)
        self.save_button = QPushButton(self)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setFont(font15)
        self.save_button.setGeometry(QRect(20, 390, 461, 91))

        self.label_U.setText("Username:")
        self.label_Pw.setText("Password:")
        self.label_info.setText("Warning:\nThe password will be saved as plaintext in the local database and can easily be read by other programs.\nUse on your own risk!\nBy leaving both fields empty you can delete your credentials.\nYou can disable this functions in the Menu")
        self.save_button.setText("Save")
        loc.execute("SELECT * FROM credentials WHERE TRUE")
        list_of_tuples = loc.fetchall()
        if list_of_tuples != [('', '')]:
            username = list_of_tuples[0][0]
            password = list_of_tuples[0][1]
            self.lineEdit_U.setPlaceholderText(username)
            self.lineEdit_Pw.setPlaceholderText(password)


        self.save_button.clicked.connect(self.update_credentials)

    def update_credentials(self):
        loc.execute(f"DELETE FROM credentials WHERE TRUE")              # for now remove everything so that only a single account exists
        localdb.commit()
        username = self.lineEdit_U.text().replace("'","''")
        password = self.lineEdit_Pw.text().replace("'","''")
        loc.execute(f"INSERT INTO credentials VALUES ('{username}','{password}')")
        localdb.commit()
        print(f"Saved Username:[{username}]\nSaved Password:[{password}]")
        self.done(0)

# endregion
# region database_download_dialog
class Ui_Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Ui_Dialog, self).__init__(*args, **kwargs)
        self.setObjectName(u"Dialog")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.resize(303, 123)
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 271, 61))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 90, 281, 23))
        self.progressBar.setValue(24)
        self.setWindowTitle("Database Download")
        self.label.setText("<html><head/><body><p><span style=\" font-size:12pt;\">Downloading database</span></p><p><span style=\" font-size:12pt;\">This may take a while...</span></p></body></html>")
#endregion
# region download class
class DownloadThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    message = pyqtSignal('PyQt_PyObject')
    close = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.data = []

    def run(self):
        print(self.data)

        data = self.data
        id = data[0]
        title = data[1].replace("|","\n")
        filename = data[1].replace("|", "_").replace(".", "").replace(":", "-").replace('"',"'").replace("<","[").replace(">","]").replace("?","").replace("/","_").replace("*","·")
        foldername =filename.replace(" ","_")
        pages = data[2]
        dir = data[3]
        eh_id = data[4]
        def download_(url2):
            resource = requests.get(url2)
            x = url2[[m.start() for m in re.finditer("/",url2)][4]+1:-4]
            if str(resource) == "<Response [200]>":
                output = open(f"{foldername}\{x}.jpg", "wb")
                output.write(resource.content)
                output.close()
            else:
                url2 = url2[:-3] + "png"
                resource2 = requests.get(url2)
                output = open(f"{foldername}\{x}.png", "wb")
                output.write(resource2.content)
                output.close()
            print(f"Page {x} done")

        try:
            os.mkdir(f"./{foldername}")
        except FileExistsError:
            print(f"FileExistsError: ./{foldername} already exsits")
            return

        url_list = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            self.message.emit(f"Downloading:\n{title}\nID: {id}\nPages: {pages}")
            for x in range(int(pages) + 1):
                if x > 0:
                    url2 = f"https://i.hentaifox.com/{dir}/{eh_id}/{x}.jpg"
                    url_list.append(url2)
            progress_value = 0
            progress_step = 100/int(pages)
            results = [executor.submit(download_, url2) for url2 in url_list]
            for thread in concurrent.futures.as_completed(results):
                progress_value += progress_step
                xx = int(progress_value)
                if xx <100:
                    self.signal.emit(xx)

        with ZipFile(f"Download/{filename}.zip", "w") as zip:
            for file in os.listdir(f"./{foldername}/"):
                zip.write(f"{foldername}/{file}")
            shutil.rmtree(f'./{foldername}/')
        self.signal.emit(100)
        print("finished")
        self.close.emit(filename)

class Ui_Download(QDialog):
    conn = sqlite3.connect("Data.db")
    c = conn.cursor()
    def __init__(self, *args, **kwargs):
        super(Ui_Download, self).__init__(*args, **kwargs)
        self.setObjectName(u"Dialog")
        self.setWindowTitle("Download Gallery")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.resize(250, 200)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setText("DOWNLOAD")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)

        self.pushButton.clicked.connect(self.start_download)

        self.dwn_thread = DownloadThread()
        self.dwn_thread.signal.connect(self.finished)
        self.dwn_thread.message.connect(self.message)
        self.dwn_thread.close.connect(self.close)

    def data_(self,data):
        self.data = data
        self.label.setText(f"Download:\n{data[1]}\nID: {data[0]}\nPages: {data[2]}")
        self.pushButton.setText("DOWNLOAD")


    def start_download(self):
        self.dwn_thread.data = self.data
        self.progressBar.show()
        self.dwn_thread.start()

    def finished(self,result):
        self.progressBar.setValue(int(result))

    def message(self,result):
        self.label.setText(f"{result}")

    def close(self,result):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Download Finished")
        msg.setText(f'You can find\n"{result}.zip"\nin the "Download" folder.')
        msg.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        msg.exec_()
        self.done(0)


#endregion
# region---GUI-----------------------
class Ui_HentaiFoxDesktop(QMainWindow):
    def setupUi(self, HentaiFoxDesktop):
        # region Setup the GUI
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.homebutton.sizePolicy().hasHeightForWidth())
        self.homebutton.setSizePolicy(size_policy)
        self.homebutton.setFont(font14)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(".\\Icons/Home-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.homebutton.setIcon(icon3)
        self.homebutton.setIconSize(QtCore.QSize(25, 25))
        self.homebutton.setFlat(True)
        self.homebutton.setObjectName("homebutton")
        self.horizontalLayout.addWidget(self.homebutton)
        self.urlbar = QtWidgets.QLineEdit(self.browse)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.urlbar.sizePolicy().hasHeightForWidth())
        self.urlbar.setSizePolicy(size_policy)
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
        self.downloadbutton.setFont(font11)
        self.downloadbutton.setObjectName("downloadbutton")
        self.horizontalLayout.addWidget(self.downloadbutton)
        self.label_zoom = QtWidgets.QLabel(self.browse)
        self.label_zoom.setFont(font13)
        self.label_zoom.setObjectName("label_zoom")
        self.horizontalLayout.addWidget(self.label_zoom)
        self.zoomslider = QtWidgets.QSlider(self.browse)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.zoomslider.sizePolicy().hasHeightForWidth())
        self.zoomslider.setSizePolicy(size_policy)
        self.zoomslider.setMinimumSize(QtCore.QSize(100, 0))
        self.zoomslider.setMinimum(30)
        self.zoomslider.setMaximum(190)
        self.zoomslider.setProperty("value", 100)
        self.zoomslider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomslider.setObjectName("zoomslider")
        self.horizontalLayout.addWidget(self.zoomslider)
        self.menu_button = QToolButton(self.browse)
        self.menu_button.setIcon(QIcon("icons/menu.png"))
        self.menu_button.setIconSize(QSize(30, 30))
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

        # self.info_button = QPushButton(self.browse)
        # self.info_button.hide()

        self.hover_url = QLabel(self.browse)
        self.hover_url.setStyleSheet("background-color: white")
        self.hover_url.setFont(font11)
        self.hover_url.hide()

        self.tag_info_overlay = QLabel(self.browse)
        self.tag_info_overlay.setStyleSheet("background-color: white")
        self.tag_info_overlay.setFont(font13)
        self.tag_info_overlay.setAlignment(Qt.AlignCenter)
        self.tag_info_overlay.setFrameShape(QFrame.StyledPanel)
        self.tag_info_overlay.setLineWidth(2)
        self.tag_info_overlay.hide()

        self.gallery_info_overlay = QLabel(self.browse)
        self.gallery_info_overlay.setStyleSheet("background-color: white")
        self.gallery_info_overlay.setFont(font12)
        self.gallery_info_overlay.setAlignment(Qt.AlignCenter)
        self.gallery_info_overlay.setFrameShape(QFrame.StyledPanel)
        self.gallery_info_overlay.setLineWidth(2)
        self.gallery_info_overlay.hide()

        self.gallery_taginfo_overlay = QLabel(self.browse)
        self.gallery_taginfo_overlay.setStyleSheet("background-color: white")
        self.gallery_taginfo_overlay.setFont(font12)
        self.gallery_taginfo_overlay.setAlignment(Qt.AlignCenter)
        self.gallery_taginfo_overlay.setFrameShape(QFrame.StyledPanel)
        self.gallery_taginfo_overlay.setLineWidth(2)
        self.gallery_taginfo_overlay.hide()

        self.gallery_scraping_overlay = QLabel(self.browse)
        self.gallery_scraping_overlay.setStyleSheet("background-color: red")
        self.gallery_scraping_overlay.setFont(font30)
        self.gallery_scraping_overlay.setAlignment(Qt.AlignCenter)
        self.gallery_scraping_overlay.setFrameShape(QFrame.StyledPanel)
        self.gallery_scraping_overlay.setLineWidth(2)
        self.gallery_scraping_overlay.hide()

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
        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 100)
        self.verticalLayout_10.setStretch(2, 10)
        self.choosetype = QtWidgets.QComboBox(self.search)
        self.choosetype.setMinimumSize(QtCore.QSize(0, 40))
        self.choosetype.setFont(font11)
        self.choosetype.setObjectName("choosetype")
        self.verticalLayout_10.addWidget(self.choosetype)
        self.criterialist = QtWidgets.QListWidget(self.search)
        self.criterialist.setObjectName("criterialist")
        self.verticalLayout_10.addWidget(self.criterialist)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)

        self.horizontalLayout_sort = QHBoxLayout()
        self.horizontalLayout_sort.setObjectName("horizontalLayout_sort")
        self.horizontalLayout_sort.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_sortfeature = QVBoxLayout()
        self.verticalLayout_sortfeature.setObjectName("verticalLayout_sortfeature")
        self.verticalLayout_sortfeature.setSpacing(0)
        self.Sort_Name = QRadioButton(self.search)
        self.Sort_Name.setObjectName("Sort_Name")
        self.Sort_Name.setAutoExclusive(False)
        self.Sort_Name.setChecked(True)
        self.verticalLayout_sortfeature.addWidget(self.Sort_Name)
        self.Sort_Count = QRadioButton(self.search)
        self.Sort_Count.setObjectName("Sort_Count")
        self.Sort_Count.setAutoExclusive(False)
        self.verticalLayout_sortfeature.addWidget(self.Sort_Count)
        self.horizontalLayout_sort.addLayout(self.verticalLayout_sortfeature)
        self.verticalLayout_sorttype = QVBoxLayout()
        self.verticalLayout_sorttype.setObjectName(u"verticalLayout_sorttype")
        self.verticalLayout_sorttype.setSpacing(0)
        self.Sort_ASC = QRadioButton(self.search)
        self.Sort_ASC.setObjectName("Sort_ASC")
        self.Sort_ASC.setAutoExclusive(False)
        self.Sort_ASC.setChecked(True)
        self.verticalLayout_sorttype.addWidget(self.Sort_ASC)
        self.Sort_DESC = QRadioButton(self.search)
        self.Sort_DESC.setObjectName("Sort_DESC")
        self.Sort_DESC.setAutoExclusive(False)
        self.verticalLayout_sorttype.addWidget(self.Sort_DESC)
        self.horizontalLayout_sort.addLayout(self.verticalLayout_sorttype)
        self.Sort_ASC.setFont(font11)
        self.Sort_DESC.setFont(font11)
        self.Sort_Name.setFont(font11)
        self.Sort_Count.setFont(font11)
        self.verticalLayout_10.addLayout(self.horizontalLayout_sort)

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
        self.whitelist_addbutton = QtWidgets.QPushButton(self.search)
        self.whitelist_addbutton.setFont(font11)
        self.whitelist_addbutton.setObjectName("whitelist_addbutton")
        self.verticalLayout_2.addWidget(self.whitelist_addbutton)

        self.whitelist_clearbutton = QtWidgets.QPushButton(self.search)
        self.whitelist_clearbutton.setFont(font11)
        self.whitelist_clearbutton.setObjectName("whitelist_clearbutton")
        self.verticalLayout_2.addWidget(self.whitelist_clearbutton)

        self.whitelist_removebutton = QtWidgets.QPushButton(self.search)
        self.whitelist_removebutton.setFont(font11)
        self.whitelist_removebutton.setObjectName("whitelist_removebutton")
        self.verticalLayout_2.addWidget(self.whitelist_removebutton)
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
        self.blacklist_addbutton = QtWidgets.QPushButton(self.search)
        self.blacklist_addbutton.setFont(font11)
        self.blacklist_addbutton.setObjectName("blacklist_addbutton")
        self.verticalLayout_3.addWidget(self.blacklist_addbutton)

        self.blacklist_clearbutton = QtWidgets.QPushButton(self.search)
        self.blacklist_clearbutton.setFont(font11)
        self.blacklist_clearbutton.setObjectName("blacklist_clearbutton")
        self.verticalLayout_3.addWidget(self.blacklist_clearbutton)

        self.blacklist_removebutton = QtWidgets.QPushButton(self.search)
        self.blacklist_removebutton.setFont(font11)
        self.blacklist_removebutton.setObjectName("blacklist_removebutton")
        self.verticalLayout_3.addWidget(self.blacklist_removebutton)
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_choosedoubleclickfunc.sizePolicy().hasHeightForWidth())
        self.label_choosedoubleclickfunc.setSizePolicy(size_policy)
        self.label_choosedoubleclickfunc.setFont(font11)
        self.label_choosedoubleclickfunc.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_choosedoubleclickfunc.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_choosedoubleclickfunc.setObjectName("label_choosedoubleclickfunc")
        self.verticalLayout_5.addWidget(self.label_choosedoubleclickfunc)
        self.check_internal = QtWidgets.QRadioButton(self.search)
        self.check_internal.setFont(font11)
        self.check_internal.setChecked(True)
        self.check_internal.setAutoExclusive(False)
        self.check_internal.setObjectName("check_internal")
        self.verticalLayout_5.addWidget(self.check_internal)
        self.check_external = QtWidgets.QRadioButton(self.search)
        self.check_external.setFont(font11)
        self.check_external.setObjectName("check_external")
        self.check_external.setAutoExclusive(False)
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
        self.diagnostics.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
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
        self.describtion.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
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
        self.verticalLayout_20.setSpacing(2)
        self.choosedisplaytype = QtWidgets.QComboBox(self.search)
        self.choosedisplaytype.setMinimumSize(QtCore.QSize(0, 40))
        self.choosedisplaytype.setFont(font11)
        self.choosedisplaytype.setObjectName("choosedisplaytype")
        self.verticalLayout_20.addWidget(self.choosedisplaytype)
        self.resultlist = QtWidgets.QListWidget(self.results)
        self.resultlist.setMaximumSize(QtCore.QSize(700, 16777215))
        self.resultlist.setObjectName("resultlist")
        self.verticalLayout_20.addWidget(self.resultlist)

        self.horizontalLayout_sortresults = QHBoxLayout()
        self.horizontalLayout_sortresults.setObjectName("horizontalLayout_sortresults")
        self.horizontalLayout_sortresults.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_sortresults1 = QVBoxLayout()
        self.verticalLayout_sortresults1.setObjectName("verticalLayout_sortresults1")
        self.SortR_ID = QRadioButton(self.results)
        self.SortR_ID.setObjectName("SortR_ID")
        self.SortR_ID.setAutoExclusive(False)
        self.SortR_ID.setFont(font11)
        self.verticalLayout_sortresults1.addWidget(self.SortR_ID)
        self.SortR_TITLE = QRadioButton(self.results)
        self.SortR_TITLE.setObjectName("SortR_TITLE")
        self.SortR_TITLE.setAutoExclusive(False)
        self.SortR_TITLE.setFont(font11)
        self.SortR_TITLE.setChecked(True)
        self.verticalLayout_sortresults1.addWidget(self.SortR_TITLE)
        self.SortR_PAGES = QRadioButton(self.results)
        self.SortR_PAGES.setObjectName("SortR_PAGES")
        self.SortR_PAGES.setAutoExclusive(False)
        self.SortR_PAGES.setFont(font11)
        self.verticalLayout_sortresults1.addWidget(self.SortR_PAGES)
        self.horizontalLayout_sortresults.addLayout(self.verticalLayout_sortresults1)
        self.verticalLayout_sortresults2 = QVBoxLayout()
        self.verticalLayout_sortresults2.setObjectName("verticalLayout_sortresults2")
        self.SortR_ASC = QRadioButton(self.results)
        self.SortR_ASC.setObjectName("SortR_ASC")
        self.SortR_ASC.setChecked(True)
        self.SortR_ASC.setAutoExclusive(False)
        self.SortR_ASC.setFont(font11)
        self.verticalLayout_sortresults2.addWidget(self.SortR_ASC)
        self.SortR_DESC = QRadioButton(self.results)
        self.SortR_DESC.setObjectName("SortR_DESC")
        self.SortR_DESC.setAutoExclusive(False)
        self.SortR_DESC.setFont(font11)
        self.verticalLayout_sortresults2.addWidget(self.SortR_DESC)
        self.open_in_result_tab_button = QPushButton(self.results)
        self.open_in_result_tab_button.setDisabled(True)
        self.verticalLayout_sortresults2.addWidget(self.open_in_result_tab_button)

        self.verticalLayout_20.addLayout(self.horizontalLayout_sortresults)
        self.horizontalLayout_sortresults.addLayout(self.verticalLayout_sortresults2)
        self.check_preview = QtWidgets.QCheckBox(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.check_preview.sizePolicy().hasHeightForWidth())
        self.check_preview.setSizePolicy(size_policy)
        self.check_preview.setMinimumSize(QtCore.QSize(0, 30))
        self.check_preview.setObjectName("check_preview")

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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.loadfilebutton.sizePolicy().hasHeightForWidth())
        self.loadfilebutton.setSizePolicy(size_policy)
        self.loadfilebutton.setMinimumSize(QtCore.QSize(0, 40))
        self.loadfilebutton.setFont(font11)
        self.loadfilebutton.setObjectName("loadfilebutton")
        self.filebuttons_layout.addWidget(self.loadfilebutton)
        self.deletefilebutton = QtWidgets.QPushButton(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.deletefilebutton.sizePolicy().hasHeightForWidth())
        self.deletefilebutton.setSizePolicy(size_policy)
        self.deletefilebutton.setMinimumSize(QtCore.QSize(0, 40))
        self.deletefilebutton.setFont(font11)
        self.deletefilebutton.setObjectName("deletefilebutton")
        self.filebuttons_layout.addWidget(self.deletefilebutton)
        self.openjson_button = QtWidgets.QPushButton(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.openjson_button.sizePolicy().hasHeightForWidth())
        self.openjson_button.setSizePolicy(size_policy)
        self.openjson_button.setMinimumSize(QtCore.QSize(0, 40))
        self.openjson_button.setFont(font11)
        self.openjson_button.setObjectName("openjson_button")
        self.filebuttons_layout.addWidget(self.openjson_button)
        self.opentxt_button = QtWidgets.QPushButton(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.opentxt_button.sizePolicy().hasHeightForWidth())
        self.opentxt_button.setSizePolicy(size_policy)
        self.opentxt_button.setMinimumSize(QtCore.QSize(0, 40))
        self.opentxt_button.setFont(font11)
        self.opentxt_button.setObjectName("opentxt_button")
        self.filebuttons_layout.addWidget(self.opentxt_button)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_loadfile)
        self.line_3 = QtWidgets.QFrame(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(size_policy)
        self.line_3.setMinimumSize(QtCore.QSize(5, 0))
        self.line_3.setLineWidth(4)
        self.line_3.setMidLineWidth(0)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_9.addWidget(self.line_3)
        self.label_info = QtWidgets.QLabel(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_info.sizePolicy().hasHeightForWidth())
        self.label_info.setSizePolicy(size_policy)
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(size_policy)
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
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_choose_doubleclickfunc2 = QtWidgets.QLabel(self.results)
        self.label_choose_doubleclickfunc2.setFont(font)
        self.label_choose_doubleclickfunc2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_choose_doubleclickfunc2.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_choose_doubleclickfunc2.setObjectName("label_choose_doubleclickfunc2")
        self.verticalLayout_13.addWidget(self.label_choose_doubleclickfunc2)
        self.check_internal2 = QtWidgets.QRadioButton(self.results)
        self.check_internal2.setChecked(True)
        self.check_internal2.setObjectName("check_internal2")
        self.verticalLayout_13.addWidget(self.check_internal2)
        self.check_external2 = QtWidgets.QRadioButton(self.results)
        self.check_external2.setObjectName("check_external2")
        self.verticalLayout_13.addWidget(self.check_external2)
        self.verticalLayout_13.addWidget(self.check_preview)
        self.gridLayout_4.addLayout(self.verticalLayout_13, 3, 3, 1, 2)
        self.cover = QWebEngineView(self)
        self.cover.setMinimumSize(QtCore.QSize(175, 248))
        self.cover.setObjectName("cover")

        self.cover_id_overlay = QLabel(self.cover)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.cover_id_overlay.setPalette(palette)
        self.cover_id_overlay.setStyleSheet("background-color: rgba(10,10,10,0.6)")
        self.cover_id_overlay.setFont(font10)

        self.gridLayout_4.addWidget(self.cover, 0, 0, 3, 1)
        self.internalbrowserbutton = QtWidgets.QPushButton(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.internalbrowserbutton.sizePolicy().hasHeightForWidth())
        self.internalbrowserbutton.setSizePolicy(size_policy)
        self.internalbrowserbutton.setMinimumSize(QtCore.QSize(0, 50))
        self.internalbrowserbutton.setFont(font11)
        self.internalbrowserbutton.setObjectName("internalbrowserbutton")
        self.gridLayout_4.addWidget(self.internalbrowserbutton, 3, 1, 1, 1)
        self.externalbrowserbutton = QtWidgets.QPushButton(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.externalbrowserbutton.sizePolicy().hasHeightForWidth())
        self.externalbrowserbutton.setSizePolicy(size_policy)
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_pages.sizePolicy().hasHeightForWidth())
        self.label_pages.setSizePolicy(size_policy)
        font16 = QtGui.QFont()
        font16.setPointSize(16)
        self.label_pages.setFont(font16)
        self.label_pages.setObjectName("label_pages")
        self.horizontalLayout_8.addWidget(self.label_pages)
        self.pagescount2 = QtWidgets.QLCDNumber(self.results)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.pagescount2.sizePolicy().hasHeightForWidth())
        self.pagescount2.setSizePolicy(size_policy)
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
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_credits.sizePolicy().hasHeightForWidth())
        self.label_credits.setSizePolicy(size_policy)
        self.label_credits.setFont(font12)
        self.label_credits.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_credits.setWordWrap(True)
        self.label_credits.setObjectName("label_credits")
        self.gridLayout_6.addWidget(self.label_credits, 0, 2, 2, 1)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.updatebutton = QtWidgets.QPushButton(self.update)
        self.updatebutton.setMinimumSize(QtCore.QSize(0, 50))
        self.updatebutton.setFont(font16)
        self.updatebutton.setObjectName("updatebutton")
        self.verticalLayout_11.addWidget(self.updatebutton)
        self.gridLayout_6.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.update)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(size_policy)
        self.line_4.setMinimumSize(QtCore.QSize(6, 0))
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_6.addWidget(self.line_4, 0, 1, 2, 1)
        self.label_version = QtWidgets.QLabel(self.update)
        self.label_version.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
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
        # endregion
        # region---------browser-setup------------------------------------------
        self.tabWidget.setCurrentIndex(0)
        self.add_new_tab(QUrl('https://hentaifox.com/'), 'Homepage')
        self.urlbar.setText("https://hentaifox.com/")
        bookmarks = []
        self.bookmarkMenu = QMenu()
        loc.execute("SELECT * FROM bookmarks WHERE true")
        for tu in loc.fetchall():
            bookmarks.append(tu)
        self.bookmarkMenu.clear()
        self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"), "Add Bookmark", self.add_bookmark,
                                    QKeySequence("Ctrl+D"))
        self.bookmarkMenu.addSeparator()
        self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"), "Add Bookmark", self.add_bookmark,
                                    QKeySequence("Ctrl+D"))
        self.bookmarkMenu.addSeparator()
        for tu in bookmarks:
            self.bookmarkMenu.addAction(f"{tu[1]}", lambda bookmark_url=tu[0]: self.load_bookmark(bookmark_url))
        self.refresh_bookmarks()
        self.bookmark.setMenu(self.bookmarkMenu)
        self.browserMenu = QMenu()
        self.create_menu()
        # endregion
        # region---------multi-search-setup-------------------------------------
        create_itemlist("tag", "ASC")
        self.choosetype.addItem("-- Choose Type --")
        self.choosetype.addItem("tags")
        self.choosetype.addItem("parodies")
        self.choosetype.addItem("characters")
        self.choosetype.addItem("artists")
        self.choosetype.addItem("groups")
        self.choosetype.addItem("categories")
        self.describtion.setText("Select tag to view description")
        self.percentagecount.setValue(0)
        # endregion
        # region---------result-setup-------------------------------------------
        self.choosedisplaytype.addItem("TITLE")
        self.choosedisplaytype.addItem("ID")
        # endregion
        # region---------browser-signals----------------------------------------
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
        # self.info_button.clicked.connect(self.find_more_info)
        # endregion
        # region---------multi-search-signals-----------------------------------
        self.choosetype.activated.connect(self.update_taglist)
        self.whitelist_addbutton.clicked.connect(self.whitelist_add)
        self.whitelist_clearbutton.clicked.connect(self.whitelist_clear)
        self.whitelist_removebutton.clicked.connect(self.whitelist_remove)
        self.blacklist_addbutton.clicked.connect(self.blacklist_add)
        self.blacklist_clearbutton.clicked.connect(self.blacklist_clear)
        self.blacklist_removebutton.clicked.connect(self.blacklist_remove)
        self.criterialist.itemClicked.connect(self.criterialist_update_gallerycounter)
        self.whitelist.itemClicked.connect(self.whitelist_update_gallerycounter)
        self.blacklist.itemClicked.connect(self.blacklist_update_gallerycounter)
        self.criterialist.itemDoubleClicked.connect(self.criterialist_opentaginbrowser)
        self.whitelist.itemDoubleClicked.connect(self.whitelist_opentaginbrowser)
        self.blacklist.itemDoubleClicked.connect(self.blacklist_opentaginbrowser)
        self.search_button.clicked.connect(self.multi_search)
        self.check_internal.clicked.connect(self.internal_toggled)
        self.check_external.clicked.connect(self.external_toggled)
        self.Sort_ASC.clicked.connect(self.asc_toggled)
        self.Sort_DESC.clicked.connect(self.desc_toggled)
        self.Sort_Name.clicked.connect(self.name_toggled)
        self.Sort_Count.clicked.connect(self.count_toggled)
        # endregion
        # region---------update-signals-----------------------------------------
        self.updatebutton.clicked.connect(self.update_datamap)
        # endregion
        # region---------result-signals-----------------------------------------
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
        self.SortR_ID.clicked.connect(self.R_ID_toggled)
        self.SortR_TITLE.clicked.connect(self.R_TITLE_toggled)
        self.SortR_PAGES.clicked.connect(self.R_PAGES_toggled)
        self.SortR_ASC.clicked.connect(self.R_ASC_toggled)
        self.SortR_DESC.clicked.connect(self.R_DESC_toggled)
        self.choosedisplaytype.currentTextChanged.connect(self.display_results)
        self.resultlist.itemDoubleClicked.connect(self.copy_result_to_clipboard)
        self.opentxt_button.clicked.connect(self.open_txt_folder)
        self.openjson_button.clicked.connect(self.open_json_folder)
        self.open_in_result_tab_button.clicked.connect(self.open_in_result_tab)
    # endregion
    # region ---------set-text--------------------------------------------------
    def retranslateUi(self, HentaiFoxDesktop):
        _translate = QtCore.QCoreApplication.translate
        HentaiFoxDesktop.setWindowTitle(_translate("HentaiFoxDesktop", "HentaiFox Desktop"))
        self.label_version.setText(
            _translate("HentaiFoxDesktop", f"<html><head/><body><p>HF-Desktop {_version_}</p></body></html>"))
        self.downloadbutton.setText(_translate("HentaiFoxDesktop", "Download Gallery"))
        self.label_zoom.setText(_translate("HentaiFoxDesktop", "Zoom:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.browse), _translate("HentaiFoxDesktop", "Browse"))
        self.label.setText(_translate("HentaiFoxDesktop",
                                      "Press \"search\" to search for galleries featuring the whitelisted tags and not featuring the blacklisted tags."))
        self.whitelist_addbutton.setText(_translate("HentaiFoxDesktop", "Add to Whitelist"))
        self.whitelist_clearbutton.setText("Clear Whitelist")
        self.whitelist_removebutton.setText(_translate("HentaiFoxDesktop", "Remove from Whitelist"))
        self.blacklist_addbutton.setText(_translate("HentaiFoxDesktop", "Add to Blacklist"))
        self.blacklist_clearbutton.setText("Clear Blacklist")
        self.blacklist_removebutton.setText(_translate("HentaiFoxDesktop", "Remove from Blacklist"))
        self.label_choosedoubleclickfunc.setText(
            _translate("HentaiFoxDesktop", "<html><head/><body><p>Doubleclick Tag to:</p></body></html>"))
        self.check_internal.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.check_external.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.label_amount.setText(_translate("HentaiFoxDesktop",
                                             "<html><head/><body><p>Amount of Galleries containing the selected Tag:</p></body></html>"))
        self.label_percentage.setText(_translate("HentaiFoxDesktop",
                                                 "<html><head/><body><p>Percentage of Galleries containing the selected Tag:</p></body></html>"))
        self.check_loadfacts.setText(_translate("HentaiFoxDesktop", "Disable Gallerycounter"))
        self.search_button.setText(_translate("HentaiFoxDesktop", "Search"))
        self.diagnostics.setText(_translate("HentaiFoxDesktop", "Search Diagnostics..."))
        self.describtion.setText(_translate("HentaiFoxDesktop",
                                            "<html><head/><body><p>Chloroform, or trichloromethane, is an organic compound with formula CHCl<span style=\" vertical-align:sub;\">3.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search), _translate("HentaiFoxDesktop", "Multi-Search"))
        self.check_preview.setText(_translate("HentaiFoxDesktop", "Disable Cover (No sever interactions)"))
        self.loadfilebutton.setText(_translate("HentaiFoxDesktop", "Load selected .result file"))
        self.deletefilebutton.setText(_translate("HentaiFoxDesktop", "Delete selected .result file"))
        self.label_info.setText(_translate("HentaiFoxDesktop",
                                           "<html><head/><body><p>The Filename is constructed by the white- and blacklisted tags. First the whitelisted tags combined with a &quot;-&quot;, second the blacklisted tags added with a &quot;!&quot;.</p><p>The filetype &quot;.result&quot; is a custom json file containing the results of a Multi-search.</p><p>You can add external .result files by dropping them in the &quot;Results (JSON)&quot; folder. </p><p>You can also find a txt-file containing just the URLs in the &quot;Results (TXT)&quot; folder.</p><p>The delete button will delete both the .result file and the corresponding .txt file.</p></body></html>"))
        self.title.setText(_translate("HentaiFoxDesktop", "Title"))
        self.lable_tags.setText(_translate("HentaiFoxDesktop", "Tags:"))
        self.lable_artistandgroups.setText(_translate("HentaiFoxDesktop", "Artist and Groups:"))
        self.lable_parodies.setText(_translate("HentaiFoxDesktop", "Parodies:"))
        self.label_choose_doubleclickfunc2.setText(
            _translate("HentaiFoxDesktop", "<html><head/><body><p>Doubleclick Tag to:</p></body></html>"))
        self.check_internal2.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.check_external2.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.internalbrowserbutton.setText(_translate("HentaiFoxDesktop", "Open in internal Browser"))
        self.externalbrowserbutton.setText(_translate("HentaiFoxDesktop", "Open in external Browser"))
        self.lable_characters.setText(_translate("HentaiFoxDesktop", "Characters:"))
        self.label_pages.setText(_translate("HentaiFoxDesktop", "Pages:"))
        self.category.setText(_translate("HentaiFoxDesktop", "Category"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results), _translate("HentaiFoxDesktop", "Result-Viewer"))
        self.label_credits.setText(_translate("HentaiFoxDesktop",
                                              "<html><head/><body><p>Credits:</p><p><br/></p><p>Written in Python by "
                                              "Niggo Jächa.</p><p>GUI powerd by PyQt5. Database powerd by SQLite.</p><p><br/></p><p>This project "
                                              "aims to add aditional features to Hentaifox, mainly better search features.</p><p><br/></p><p>If you have questions join the "
                                              "Hentaifox Discord "
                                              "server:<br/>https://discord.gg/BdNqEWX</p><p><br/></p><p>Contact: "
                                              "</p><p>Discord: N. Jächa#1707</p><p>Email: "
                                              "andre.grabowich@gmail.com</p><p>Thanks to HentaiFox for this great "
                                              "Website!</p></body></html>"))
        self.updatebutton.setText(_translate("HentaiFoxDesktop", "Check for Updates (Database)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.update), _translate("HentaiFoxDesktop", "Update-Datamap"))
        self.Sort_ASC.setText("Ascending")
        self.Sort_DESC.setText("Descending")
        self.Sort_Name.setText("by Name")
        self.Sort_Count.setText("by Galleries")
        self.SortR_ID.setText("by ID")
        self.SortR_TITLE.setText("by Title")
        self.SortR_PAGES.setText("by Pages")
        self.SortR_ASC.setText("Ascending")
        self.SortR_DESC.setText("Descending")
        self.openjson_button.setText('Open "Results (JSON)"')
        self.opentxt_button.setText('Open "Results (TXT)"')
        self.open_in_result_tab_button.setText("Use Browser Viewer")
    # endregion
    # region ---------other-----------------------------------------------------
    def change_cursor(self):
        pixmap = QPixmap("Icons/HFCursor2.png")
        cursor = QCursor(pixmap)
        if app.overrideCursor() == None:
            app.setOverrideCursor(cursor)
        else:
            app.restoreOverrideCursor()

    def update_database(self):
        QtWidgets.qApp.processEvents()
        QtWidgets.qApp.processEvents()
        QtWidgets.qApp.processEvents()

        print("Checking for database update...")
        web = requests.get("https://doujindata.ddns.net/last.html")
        timestamp = web.text[:19]
        local_timestamp = open("timestamp.txt","r").read()
        if local_timestamp != timestamp:
            print("Downloading latest database\nDepending on your conection, this may take a while...")
            with open("Data.db","wb") as f:
                dlg = Ui_Dialog(self)
                new_data = requests.get("https://doujindata.ddns.net/Data.db",stream=True)
                total_length = new_data.headers.get('content-length')
                if total_length is None:
                    print("Error: length header missing")
                else:
                    dl = 0
                    dlg.open()
                    dlg.progressBar.setValue(0)
                    for data in new_data.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done= int(100*dl/int(total_length))
                        dlg.progressBar.setValue(done)
                        QtWidgets.qApp.processEvents()
                    dlg.done(0)

            open("timestamp.txt","w").write(timestamp)
            print("Database now up to date")
            return(1)
        else:
            print("Database already up to date.")
            return(0)
    #endregion
    # region ---------browser-functions-----------------------------------------
    def add_new_tab(self, qurl=None, label="Loading..."):
        if qurl is None:
            qurl = QUrl('https://hentaifox.com/')
        browser = WebEngineView(self)
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, browser=browser: self.on_load_finished(browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, str(str(browser.page().title())[:20]+"...")))
        browser.page().linkHovered.connect(lambda url=browser.page().linkHovered: self.link_hovered(url))

    def create_new_tab(self, page):
        browser = page
        i = self.tabs.addTab(browser, "loading...")
        loc.execute("SELECT value FROM settings WHERE setting='switch_tabs_setting'")
        switch_tabs_setting = int(loc.fetchone()[0])
        if switch_tabs_setting == 1:
            self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, browser=browser: self.on_load_finished(browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, str(str(browser.page().title())[:20]+"...")))
        browser.page().linkHovered.connect(lambda url=browser.page().linkHovered: self.link_hovered(url))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab(qurl=QUrl("https://hentaifox.com/"))

    def current_tab_changed(self, i):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            #region disable/enable
            self.zoomslider.show()
            self.label_zoom.show()
            self.downloadbutton.setEnabled(True)
            self.bookmark.setEnabled(True)
            self.backbutton.setEnabled(True)
            self.forwardbutton.setEnabled(True)
            self.reloadbutton.setEnabled(True)
            self.homebutton.setEnabled(True)
            self.browserMenu.back.setEnabled(True)
            self.browserMenu.forward.setEnabled(True)
            self.browserMenu.reload.setEnabled(True)
            self.browserMenu.home.setEnabled(True)
            self.browserMenu.zoom_in.setEnabled(True)
            self.browserMenu.zoom_out.setEnabled(True)
            self.browserMenu.zoom_reset.setEnabled(True)
            self.browserMenu.download.setEnabled(True)
            self.browserMenu.copypasta.setEnabled(True)
            self.browserMenu.result_file.setDisabled(True)
            #endregion
            qurl = self.tabs.currentWidget().url()
            self.update_urlbar(qurl, self.tabs.currentWidget())
            self.update_zoom()
            self.refresh_bookmarks()
            self.update_tab_count()
        elif isinstance(self.tabs.currentWidget(),QWidget) == True:
            #region disable/enable
            self.zoomslider.hide()
            self.label_zoom.hide()
            self.downloadbutton.setDisabled(True)
            self.bookmark.setDisabled(True)
            self.backbutton.setDisabled(True)
            self.forwardbutton.setDisabled(True)
            self.reloadbutton.setDisabled(True)
            self.homebutton.setDisabled(True)
            self.browserMenu.back.setDisabled(True)
            self.browserMenu.forward.setDisabled(True)
            self.browserMenu.reload.setDisabled(True)
            self.browserMenu.home.setDisabled(True)
            self.browserMenu.zoom_in.setDisabled(True)
            self.browserMenu.zoom_out.setDisabled(True)
            self.browserMenu.zoom_reset.setDisabled(True)
            self.browserMenu.download.setDisabled(True)
            self.browserMenu.copypasta.setDisabled(True)
            self.browserMenu.result_file.setEnabled(True)
            #endregion
            term = self.tabs.currentWidget().term
            self.urlbar.setText(term)
            self.urlbar.setCursorPosition(0)
            self.update_tab_count()
        else:
            pass

    def update_zoom(self):
        zoomvalue = int(self.tabs.currentWidget().zoomFactor() * 100)
        self.zoomslider.setValue(zoomvalue)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def navigate_home(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            self.tabs.currentWidget().setUrl(QUrl("https://hentaifox.com/"))

    def create_result_tab(self,tups,term):
        list_of_tuples = tups
        stack_page_count = int((len(list_of_tuples)+5)/6)

        if stack_page_count >= 1:
            overall_widget = QWidget(self.tabs)
            overall_widget.results = []
            for tu in list_of_tuples:
                overall_widget.results.append(tu[0])
            overall_widget.term = term
            layout_ = QVBoxLayout(overall_widget)
            stack = QStackedWidget()
            layout_.addWidget(stack)
            bottom_tools = QHBoxLayout()

            #region button functions
            def arrow_right_pressed():
                index = stack.currentIndex()
                total = stack.count()
                if index+1 < stack_page_count:
                    if index+1 >= total:
                            new_first_i = int((index+1)*6)
                            i = add_stack_page(new_first_i)
                            stack.setCurrentIndex(i)
                    else:
                        stack.setCurrentIndex(index+1)
                    current_page.setText(f"{index+2}/{stack_page_count}")
            def arrow_left_pressed():
                index = stack.currentIndex()
                if index > 0:
                    stack.setCurrentIndex(index-1)
                    current_page.setText(f"{index}/{stack_page_count}")
            #endregion

            arrow_right = QPushButton()
            arrow_right.setIcon(QIcon("Icons/arrow_right.png"))
            arrow_right.clicked.connect(arrow_right_pressed)
            arrow_left = QPushButton()
            arrow_left.setIcon(QIcon("Icons/arrow_left.png"))
            arrow_left.clicked.connect(arrow_left_pressed)
            current_page = QLabel()
            current_page.setAlignment(QtCore.Qt.AlignCenter)
            current_page.setFont(font11)
            current_page.setText(f"1/{stack_page_count}")
            bottom_tools.addWidget(arrow_left)
            bottom_tools.addWidget(current_page)
            bottom_tools.addWidget(arrow_right)
            layout_.addLayout(bottom_tools)

            #region def gal_view
            def gal_view(index):
                try:
                    tu = list_of_tuples[index]
                    id = tu[0]
                    title = tu[1].replace('|','\n')
                    pages = int(tu[2])
                    cover_url = tu[3]
                    content = QWidget()
                    layout = QHBoxLayout(content)
                    content.image = QWebEngineView(content)
                    content.image.setMinimumSize(175,242)
                    content.image.setUrl(QUrl(cover_url))
                    content.image.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

                    #region id overlay
                    id_overlay = QLabel(content.image)
                    palette = QPalette()
                    brush = QBrush(QColor(255, 255, 255, 255))
                    brush.setStyle(Qt.SolidPattern)
                    palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
                    palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
                    brush1 = QBrush(QColor(120, 120, 120, 255))
                    brush1.setStyle(Qt.SolidPattern)
                    palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
                    id_overlay.setPalette(palette)
                    id_overlay.setStyleSheet("background-color: rgba(10,10,10,0.6)")
                    id_overlay.setFont(font10)
                    id_overlay.setText(str(id))
                    id_overlay.adjustSize()
                    #endregion
                    match = str(re.search(term, title, re.IGNORECASE))
                    case_term = match[match.find("match")+7:-2]

                    title = "<html><head/><body><p>" + re.sub(f"{term}",f"<span style=\" font-weight:600;\">{case_term}</span>",title,flags=re.IGNORECASE) + "</p></body></html>"

                    layout2 = QVBoxLayout()
                    title_box = QLabel()
                    title_box.setAlignment(Qt.AlignCenter)
                    title_box.setWordWrap(True)
                    title_box.setText(title)
                    title_box.setFont(font12)
                    layout2.addWidget(title_box)
                    pages_box = QLabel()
                    pages_box.setAlignment(Qt.AlignCenter)
                    pages_box.setText(f"Pages: {pages}")
                    pages_box.setFont(font11)
                    layout2.addWidget(pages_box)
                    artist_box = QLabel()
                    artist_box.setAlignment(Qt.AlignCenter)
                    artist_box.setWordWrap(True)
                    artist_box.setFont(font11)
                    tags_box = QComboBox()
                    parodies_box = QLabel()
                    parodies_box.setAlignment(Qt.AlignCenter)
                    parodies_box.setWordWrap(True)
                    parodies_box.setFont(font11)
                    groups_box = QLabel()
                    groups_box.setAlignment(Qt.AlignCenter)
                    groups_box.setWordWrap(True)
                    groups_box.setFont(font11)
                    category_box = QLabel()
                    category_box.setAlignment(Qt.AlignCenter)
                    category_box.setWordWrap(True)
                    category_box.setFont(font12)

                    c.execute(f"SELECT tag FROM galleryartists WHERE gal={id}")
                    list_ = c.fetchall()
                    if len(list_) > 0:
                        art = "Artist:"
                        comb = " "
                        for tu in list_:
                            art = art + comb + tu[0]
                            comb = " | "
                        artist_box.setText(art)
                        layout2.addWidget(artist_box)
                    c.execute(f"SELECT tag FROM gallerygroups WHERE gal={id}")
                    list_ = c.fetchall()
                    if len(list_) > 0:
                        grp = "Groups:"
                        for tu in list_:
                            grp = grp + f"\n{tu[0]}"
                        groups_box.setText(grp)
                        layout2.addWidget(groups_box)
                    c.execute(f"SELECT tag FROM galleryparodies WHERE gal={id}")
                    list_ = c.fetchall()
                    if len(list_) > 0:
                        par = "Parodies:"
                        for tu in list_:
                            par = par + f"\n{tu[0]}"
                        parodies_box.setText(par)
                        layout2.addWidget(parodies_box)
                    c.execute(f"SELECT tag FROM gallerycategories WHERE gal={id}")
                    list_ = c.fetchall()
                    if len(list_) > 0:
                        cat = list_[0][0]
                        category_box.setText(cat)
                        layout2.addWidget(category_box)
                    #region def open tag
                    def open_tag(tag):
                        if tag != "View Tags":
                            tag = tag.replace(" ", "-")
                            qurl = QtCore.QUrl(f"https://hentaifox.com/tag/{tag}/")
                            self.add_new_tab(qurl, label="loading...")
                    #endregion
                    tags_box.addItem("View Tags")
                    c.execute(f"SELECT tag FROM gallerytags WHERE gal={id}")
                    list_ = c.fetchall()
                    for tu in list_:
                        tags_box.addItem(tu[0])
                    tags_box.activated.connect(lambda index=tags_box.activated: open_tag(tags_box.itemText(index)))
                    layout2.addWidget(tags_box)

                    #region open button Pressed
                    def open_button_pressed():
                        url = f"https://hentaifox.com/gallery/{id}/"
                        self.add_new_tab(QUrl(url))
                    #endregion
                    open_button = QPushButton()
                    open_button.setText("Open")
                    open_button.clicked.connect(open_button_pressed)
                    layout2.addWidget(open_button)

                    #region clipboard button Pressed
                    def clipboard_button_pressed():
                        url = f"https://hentaifox.com/gallery/{id}/"
                        pyperclip.copy(url)
                    #endregion
                    clipboard_button = QPushButton()
                    clipboard_button.setText("Copy URL")
                    clipboard_button.clicked.connect(clipboard_button_pressed)
                    layout2.addWidget(clipboard_button)

                    layout.addWidget(content.image)
                    layout.addLayout(layout2)
                except IndexError:
                    content = QWidget()
                    layout = QHBoxLayout(content)
                    content.image = QLabel(content)
                    content.image.setMinimumSize(175,242)
                    content.image.setText("")
                    text = QLabel(content)
                    text.setAlignment(Qt.AlignCenter)
                    text.setText("")
                    layout.addWidget(content.image)
                    layout.addWidget(text)
                return content
            #endregion
            #region def row
            def row(first_index):
                row_ = QHBoxLayout()
                row_.addWidget(gal_view(first_index))
                def line():
                    line_ = QFrame()
                    line_.setLineWidth(4)
                    line_.setFrameShape(QFrame.VLine)
                    line_.setFrameShadow(QFrame.Sunken)
                    return line_
                row_.addWidget(line())
                row_.addWidget(gal_view(first_index+1))
                row_.addWidget(line())
                row_.addWidget(gal_view(first_index+2))
                return row_
            #endregion
            #region def page
            def page(first_index):
                page_ = QWidget()
                layout = QVBoxLayout(page_)
                layout.addLayout(row(first_index))
                line = QFrame()
                line.setLineWidth(4)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                layout.addWidget(line)
                layout.addLayout(row(first_index+3))
                return page_
            #endregion
            #region fill stack
            def add_stack_page(first_index):
                return stack.addWidget(page(first_index))
            #endregion

            add_stack_page(0)
        else:
            overall_widget = QLabel(self.tabs)
            overall_widget.setAlignment(Qt.AlignCenter)
            overall_widget.setFont(font30)
            overall_widget.setText(f'Sorry no results for "{term}"')
        i = self.tabs.addTab(overall_widget, f'"{term}" - {len(list_of_tuples)} results')
        self.tabs.setCurrentIndex(i)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        url_raw = q.url()
        if str(url_raw).startswith("http"):
            if str(url_raw).startswith("http:"):
                url_raw = str(url_raw).replace("http:", "https:")
            if url_raw.startswith("https://hentaifox.com"):
                self.tabs.currentWidget().setUrl(QUrl(url_raw))
        else:
            if str(url_raw) == "rickroll":
                view = QWebEngineView(self.tabs)
                view.load(QUrl("https://youtu.be/dQw4w9WgXcQ"))
                i = self.tabs.addTab(view,"😏")
                self.tabs.setCurrentIndex(i)
            else:
                list = []
                term = str(self.urlbar.text())
                term_ = term.replace("'","''")
                c.execute(f"SELECT * FROM galleryinformation WHERE title LIKE '%{term_}%' ORDER BY gal DESC")
                list_of_tuples = c.fetchall()
                self.create_result_tab(list_of_tuples,term)

    def on_load_finished(self,browser):
        url = browser.url().url()
        if url.startswith("https://hentaifox.com/login"):
            self.fill_credentials()

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
            # elif q.toString().startswith("https://hentaifox.com/gallery/"):
            #     id = q.toString()[30:-1]
            #     self.more_information()
            # else:
            #     self.info_button.hide()
            self.tabs.setTabText(self.tabs.currentIndex(), str(str(browser.page().title())[:20]+"..."))

    #region hitomi.la wip
    # def more_information(self):
    #     p = self.browse.geometry().bottomLeft() + QPoint(20,-100)
    #     self.info_button.move(p)
    #     self.info_button.raise_()
    #     self.info_button.setText("Find More Information")
    #     self.info_button.adjustSize()
    #     self.info_button.show()
    #
    # def find_more_info(self):
    #     url = self.tabs.currentWidget().url().url()
    #     id = url[30:-1]
    #     c.execute(f"SELECT * FROM galleryinformation WHERE gal={id}")
    #     tu = c.fetchone()
    #     hitomi_title = tu[1].replace(" ","-").replace("'","-").lower()
    #     if hitomi_title.endswith("-"):
    #         hitomi_title = hitomi_title[:-1]
    #     im_url = tu[3]
    #     im_id = im_url[[m.start() for m in re.finditer("/",im_url)][3]+1:[m.start() for m in re.finditer("/",im_url)][4]]
    #     c.execute(f"SELECT tag FROM gallerycategories WHERE gal={id}")
    #     category = c.fetchone()[0]
    #     hitomi_url = f"https://hitomi.la/{category}/{hitomi_title}-english-{im_id}.html"
    #     print(hitomi_url)
    #     web = requests.get(hitomi_url)
    #     html = web.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     okay = soup.find('title')
    #     if str(okay) != "<title>404 Not Found</title>":
    #         test = soup.find("div",attrs={"class":"dj"})
    #         print(test)
    #endregion

    def fill_credentials(self):
        page = self.tabs.currentWidget().page()
        if page.url().url().startswith("https://hentaifox.com/login"):                          #doublecheck to prevent bugs
            loc.execute("SELECT value FROM settings WHERE setting='auto_fill_setting'")
            auto_fill_setting = int(loc.fetchone()[0])
            if auto_fill_setting == 1:
                loc.execute("SELECT * FROM credentials WHERE TRUE")
                list_of_tuples = loc.fetchall()
                if list_of_tuples == [('', '')]:
                    dwl = Credentials_dialog(self)
                    _ = dwl.show()
                else:
                    username = list_of_tuples[0][0]
                    password = list_of_tuples[0][1]
                    page.runJavaScript("""
                    document.getElementById('username').value="{0}"
                    document.getElementById('password').value="{1}"
                    """.format(username,password))

    def zoom_browser(self):
        webview = self.tabs.currentWidget()
        if isinstance(webview,QWebEngineView) == True:
            zoomfactor = int(self.zoomslider.value()) * 0.01
            webview.setZoomFactor(zoomfactor)

    def zoom_browser2(self, value):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            if self.tabs.currentWidget().zoomFactor() + 0.1 < 2 and value > 0:
                zoomfactor = self.tabs.currentWidget().zoomFactor() + value
                self.tabs.currentWidget().setZoomFactor(zoomfactor)
                self.update_zoom()
            if value < 0:
                zoomfactor = self.tabs.currentWidget().zoomFactor() + value
                self.tabs.currentWidget().setZoomFactor(zoomfactor)
                self.update_zoom()

    def reset_zoom(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            self.tabs.currentWidget().setZoomFactor(1)
            self.update_zoom()

    def download(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            url = self.tabs.currentWidget().url().url()
            if url.startswith("https://hentaifox.com/g/"):
                id = url[[m.start() for m in re.finditer("/",url)][3]+1:[m.start() for m in re.finditer("/",url)][4]]
            elif url.startswith("https://hentaifox.com/gallery/"):
                id = url[[m.start() for m in re.finditer("/",url)][3]+1:[m.start() for m in re.finditer("/",url)][4]]

            if url.startswith("https://hentaifox.com/g/") or url.startswith("https://hentaifox.com/gallery/"):
                c.execute(f"SELECT * FROM galleryinformation WHERE gal='{id}'")
                tu = c.fetchone()
                image_url = tu[3]
                pages = tu[2]
                title = tu[1]
                filename = title.replace("|", "_").replace(".", "").replace(":", "-")
                foldername = filename.replace(" ","_")
                dir = image_url[[m.start() for m in re.finditer("/",image_url)][2]+1:[m.start() for m in re.finditer("/",image_url)][3]]
                eh_id = image_url[[m.start() for m in re.finditer("/",image_url)][3]+1:[m.start() for m in re.finditer("/",image_url)][4]]
                data = [f"{id}",f"{title}",f"{pages}",f"{dir}",f"{eh_id}"]
                dwl = Ui_Download(self)
                dwl.data_(data)
                _ = dwl.show()

    def add_bookmark(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            url = self.tabs.currentWidget().url().url()
            loc.execute(f"SELECT * FROM bookmarks WHERE url='{url}'")
            if len(loc.fetchall()) < 1:
                loc.execute(
                    f"INSERT INTO bookmarks VALUES ('{url}','{self.tabs.currentWidget().page().title().replace('Free Hentai Manga, Doujinshi and Anime Porn','Home').replace(' - HentaiFox','').replace(' - Hentai Galleries','').replace('Free Hentai Manga and Doujinshi','Overview')}')")
                localdb.commit()
                self.refresh_bookmarks(mode="remove")

    def remove_bookmark(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            url = self.tabs.currentWidget().url().url()
            loc.execute(f"SELECT * FROM bookmarks WHERE url='{url}'")
            if len(loc.fetchall()) > 0:
                loc.execute(f"DELETE FROM bookmarks WHERE url='{url}'")
                localdb.commit()
                self.refresh_bookmarks(mode="add")

    def refresh_bookmarks(self, mode=None):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            url = self.tabs.currentWidget().url().url()

            bookmarks = []
            loc.execute("SELECT * FROM bookmarks WHERE true")
            for tu in loc.fetchall():
                bookmarks.append(tu)

            if mode == None:
                loc.execute(f"SELECT * FROM bookmarks WHERE url='{url}'")
                if len(loc.fetchall()) > 0:
                    mode = "remove"
                elif len(loc.fetchall()) < 1:
                    mode = "add"
            if mode == "remove":
                self.bookmark.setIcon(QIcon("icons/BookmarkSet.png"))
                self.bookmarkMenu.clear()
                self.bookmarkMenu.addAction(QIcon("icons/remove_Bookmark.png"), "Remove Bookmark", self.remove_bookmark,
                                            QKeySequence("Ctrl+D"))
                self.bookmarkMenu.addSeparator()
                for bookmark in bookmarks:
                    self.bookmarkMenu.addAction(f"{bookmark[1]}",
                                                lambda bookmark_url=bookmark[0]: self.load_bookmark(bookmark_url))
            elif mode == "add":
                self.bookmark.setIcon(QIcon("icons/Bookmark.png"))
                self.bookmarkMenu.clear()
                self.bookmarkMenu.addAction(QIcon("icons/add_Bookmark.png"), "Add Bookmark", self.add_bookmark,
                                            QKeySequence("Ctrl+D"))
                self.bookmarkMenu.addSeparator()
                for bookmark in bookmarks:
                    self.bookmarkMenu.addAction(f"{bookmark[1]}",
                                                lambda bookmark_url=bookmark[0]: self.load_bookmark(bookmark_url))

    def load_bookmark(self, bookmark_url):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            self.tabs.currentWidget().load(QUrl(bookmark_url))

    def update_tab_count(self):
        lenght = self.tabs.count()
        self.tabsMenu.clear()
        for x in range(lenght):
            if x <= 8:
                i = x + 1
                self.tabsMenu.addAction(f"Switch to Tab {i}", lambda x=x: self.tabs.setCurrentIndex(x),
                                        QKeySequence(f"Ctrl+{i}"))

    def copy_url(self):
        if isinstance(self.tabs.currentWidget(),QWebEngineView) == True:
            url = self.tabs.currentWidget().url().url()
            pyperclip.copy(url)

    def link_hovered(self,url):
        if len(url) > 150:
            url = url[:100]+"..."
        if url != "":
            p = self.browse.geometry().bottomLeft() + QPoint(12,-33)
            self.hover_url.move(p)
            self.hover_url.raise_()
            self.hover_url.setText(url)
            self.hover_url.adjustSize()
            self.hover_url.show()
        else:
            self.hover_url.hide()
            self.tag_info_overlay.hide()
            self.gallery_info_overlay.hide()
            self.gallery_taginfo_overlay.hide()

        loc.execute("SELECT value FROM settings WHERE setting='tag_info_setting'")
        tag_info_setting = loc.fetchone()[0]
        if tag_info_setting == 1:
            if url.startswith("https://hentaifox.com/tag/"):
                c.execute(f"SELECT * FROM taginformation WHERE url='{url}'")
                tu = c.fetchone()
                if tu != None:
                    tag = tu[0]
                    galleries = tu[1]
                    wiki_description = tu[2]
                    if len(wiki_description) > 180:
                        positions = ( [pos for pos, char in enumerate(wiki_description) if char == " "])
                        postition = min(positions, key=lambda x:abs(x-170))
                        wiki_description = f"{wiki_description[:postition]}\n{wiki_description[postition:]}"


                    info = f"{tag}:\n{wiki_description}\nReal amount of Galleries: {galleries}"
                else:
                    info = "Currently Unavalible"

                self.tag_info_overlay.raise_()
                self.tag_info_overlay.setText(info)
                self.tag_info_overlay.adjustSize()
                p = self.tabs.geometry().bottomRight() - QPoint(int(self.tabs.geometry().width()/2+(self.tag_info_overlay.geometry().width()/2)),int(self.tag_info_overlay.geometry().height()+30))
                self.tag_info_overlay.move(p)
                self.tag_info_overlay.show()

        loc.execute("SELECT value FROM settings WHERE setting='gallery_info_setting'")
        gallery_info_setting = int(loc.fetchone()[0])
        if gallery_info_setting == 1:
            if url.startswith("https://hentaifox.com/gallery/"):
                id = url[30:-1]
                c.execute(f"SELECT * FROM galleryinformation WHERE gal={id}")
                test = c.fetchall()
                if test != []:
                    pages = test[0][2]
                    text = ""
                    for type in types:
                        typex = type_converter(type)
                        c.execute(f"SELECT tag FROM gallery{type} WHERE gal={id}")
                        list_ = c.fetchall()
                        if type != "tags":
                            if list_ == []:
                                pass
                            else:
                                text = text + f"\n\n{type}:\n"
                                comb = ""
                                for tu in list_:
                                    text = text +comb+ f"{tu[0]}"
                                    comb = ", "
                        else:
                            text2 = "Tags:"
                            if list_ == []:
                                text2 = "No tags in database"
                                pass
                            else:
                                for tu in list_:
                                    text2 = text2 + f"\n{tu[0]}"
                    text = text+ f"\n\nPages:\n{pages}"

                    self.gallery_info_overlay.raise_()
                    self.gallery_info_overlay.setText(text[2:])
                    self.gallery_info_overlay.adjustSize()
                    p = self.tabs.geometry().topRight() + QPoint(-(int(self.gallery_info_overlay.geometry().width())+40),100)
                    self.gallery_info_overlay.move(p)
                    self.gallery_info_overlay.show()

                    self.gallery_taginfo_overlay.raise_()
                    self.gallery_taginfo_overlay.setText(text2)
                    self.gallery_taginfo_overlay.adjustSize()
                    p = self.tabs.geometry().topLeft() + QPoint(20,100)
                    self.gallery_taginfo_overlay.move(p)
                    self.gallery_taginfo_overlay.show()
                else:
                    self.gallery_scraping_overlay.raise_()
                    self.gallery_scraping_overlay.setText(f"Database Update\nDepending on your connection this may take a while...")
                    self.gallery_scraping_overlay.adjustSize()
                    p = self.tabs.geometry().bottomRight() - QPoint(int(self.tabs.geometry().width()/2+self.gallery_scraping_overlay.geometry().width()/2) ,int(self.tabs.geometry().height()/2+self.gallery_scraping_overlay.geometry().height()/2))
                    self.gallery_scraping_overlay.move(p)
                    self.gallery_scraping_overlay.show()
                    self.gallery_info_overlay.hide()
                    self.gallery_taginfo_overlay.hide()
                    QtWidgets.qApp.processEvents()

                    if id not in not_in_database:
                        print(f"Gallery with ID [{id}] not in Database, updating Database...")
                        try_update = self.update_database()
                        if try_update == 0:
                            msg = QtWidgets.QMessageBox(self.tabs)
                            msg.setWindowTitle("Gallery Missing")
                            msg.setText(f'Gallery is not in database yet, please update again in a few minutes.')
                            msg.exec_()
                            not_in_database.append(id)
                    self.gallery_scraping_overlay.hide()

    def create_result_file(self):
        if isinstance(self.tabs.currentWidget(),QWidget):
            results = self.tabs.currentWidget().results
            term = str(self.tabs.currentWidget().term).replace(":","_").replace("/","_").replace("*","·").replace('"',"'").replace("|","_").replace("<","[").replace(">","]").replace("?","")
            filename = f"[term]_{term}"
            if len(results) > 0:
                with open(f"Results (TXT)/{filename}.txt", "w+") as t:
                    for gallery in results:
                        t.write(f"https://hentaifox.com/gallery/{gallery}/\n")
                with open(f"Results (JSON)/{filename}.result", "w") as j:
                    data = []
                    for gallery in results:
                        data.append(gallery)
                    json.dump(data, j, indent=4)
                self.tabWidget.setCurrentIndex(2)

    def deactivate_taginformation(self):
        loc.execute("UPDATE settings SET value = '0' WHERE setting ='tag_info_setting'")
        localdb.commit()
        self.create_menu()

    def activate_taginformation(self):
        loc.execute("UPDATE settings SET value = '1' WHERE setting = 'tag_info_setting'")
        localdb.commit()
        self.create_menu()

    def deactivate_tabswitching(self):
        loc.execute("UPDATE settings SET value = '0' WHERE setting ='switch_tabs_setting'")
        localdb.commit()
        self.create_menu()

    def activate_tabswitching(self):
        loc.execute("UPDATE settings SET value = '1' WHERE setting = 'switch_tabs_setting'")
        localdb.commit()
        self.create_menu()

    def deactivate_galleryinformation(self):
        loc.execute("UPDATE settings SET value = '0' WHERE setting ='gallery_info_setting'")
        localdb.commit()
        self.create_menu()

    def activate_galleryinformation(self):
        loc.execute("UPDATE settings SET value = '1' WHERE setting = 'gallery_info_setting'")
        localdb.commit()
        self.create_menu()

    def deactivate_auto_fill(self):
        loc.execute("UPDATE settings SET value = '0' WHERE setting = 'auto_fill_setting'")
        localdb.commit()
        self.create_menu()

    def activate_auto_fill(self):
        loc.execute("UPDATE settings SET value = '1' WHERE setting = 'auto_fill_setting'")
        localdb.commit()
        self.create_menu()

    def create_menu(self):
        loc.execute("SELECT value FROM settings WHERE setting='tag_info_setting'")
        tag_info_setting = int(loc.fetchone()[0])
        loc.execute("SELECT value FROM settings WHERE setting='switch_tabs_setting'")
        switch_tabs_setting = int(loc.fetchone()[0])
        loc.execute("SELECT value FROM settings WHERE setting='gallery_info_setting'")
        gallery_info_setting = int(loc.fetchone()[0])
        loc.execute("SELECT value FROM settings WHERE setting='auto_fill_setting'")
        auto_fill_setting = int(loc.fetchone()[0])

        self.browserMenu.clear()
        self.browserMenu.back = self.browserMenu.addAction(QIcon("icons/Back_Arrow.png"),"Back",lambda: self.tabs.currentWidget().back(),QKeySequence("Ctrl+Left"))
        self.browserMenu.forward = self.browserMenu.addAction(QIcon("icons/Forward_Arrow.png"),"Forward",lambda: self.tabs.currentWidget().forward(),QKeySequence("Ctrl+Right"))
        self.browserMenu.reload = self.browserMenu.addAction(QIcon("icons/Reload_Arrow.png"),"Reload",lambda: self.tabs.currentWidget().reload(),QKeySequence("Ctrl+R"))
        self.browserMenu.home = self.browserMenu.addAction(QIcon("icons/Home-icon.png"),"Home",self.navigate_home,QKeySequence("Ctrl+H"))
        self.browserMenu.addSeparator()
        self.browserMenu.addAction(QIcon("icons/add_tab.png"),"New Tab",self.add_new_tab,QKeySequence("Ctrl+T"))
        self.browserMenu.addAction(QIcon("icons/remove_tab.png"),"Close Tab",lambda i=self.tabs.currentIndex(): self.close_current_tab(i),QKeySequence("Ctrl+W"))
        self.tabsMenu = self.browserMenu.addMenu(QIcon("icons/tab.png"),"Navigate Tabs")
        self.tabsMenu.addAction("Switch to Tab 1",lambda: self.tabs.setCurrentIndex(0),QKeySequence("Ctrl+1"))
        self.browserMenu.addSeparator()
        self.browserMenu.zoom_in = self.browserMenu.addAction(QIcon("icons/zoom_in.png"),"Zoom in by 10%",lambda value=0.1:self.zoom_browser2(value=value),QKeySequence("Ctrl++"))
        self.browserMenu.zoom_out = self.browserMenu.addAction(QIcon("icons/zoom_out.png"),"Zoom out by 10%",lambda value=-0.1:self.zoom_browser2(value=value),QKeySequence("Ctrl+-"))
        self.browserMenu.zoom_reset = self.browserMenu.addAction(QIcon("icons/zoom.png"),"Reset Zoom to 100%",self.reset_zoom,QKeySequence("Ctrl+0"))
        self.browserMenu.addSeparator()
        self.browserMenu.download = self.browserMenu.addAction(QIcon("icons/download.png"),"Download current Gallery",self.download,QKeySequence("Ctrl+S"))
        self.browserMenu.copypasta = self.browserMenu.addAction(QIcon("icons/copy.png"),"Copy page URL to clipboard",self.copy_url,QKeySequence("Ctrl+Shift+C"))
        self.browserMenu.result_file = self.browserMenu.addAction(QIcon("icons/wirte_file.png"),"Create .result of this search",self.create_result_file,QKeySequence("Ctrl+B"))
        self.browserMenu.result_file.setDisabled(True)
        self.browserMenu.addAction("Change saved Credentials",lambda: Credentials_dialog(self).show())
        self.browserMenu.addSeparator()
        self.settingsMenu = self.browserMenu.addMenu(QIcon("icons/setting_icon.png"),"Settings")
        self.browserMenu.addSeparator()
        self.browserMenu.addAction("Special Cursor",self.change_cursor,QKeySequence("Alt+H"))

        if tag_info_setting == 0:
            self.settingsMenu.addAction(QIcon("icons/checkbox_empty.png"),"Display Taginformation on hover", self.activate_taginformation)
        elif tag_info_setting == 1:
            self.settingsMenu.addAction(QIcon("icons/checkbox_checked.png"),"Display Taginformation on hover", self.deactivate_taginformation)

        if gallery_info_setting == 0:
            self.settingsMenu.addAction(QIcon("icons/checkbox_empty.png"),"Display Galleryinformation on hover", self.activate_galleryinformation)
        elif gallery_info_setting == 1:
            self.settingsMenu.addAction(QIcon("icons/checkbox_checked.png"),"Display Galleryinformation on hover", self.deactivate_galleryinformation)

        if switch_tabs_setting == 0:
            self.settingsMenu.addAction(QIcon("icons/checkbox_empty.png"),"Autoswitch to new Tab when opening", self.activate_tabswitching)
        elif switch_tabs_setting == 1:
            self.settingsMenu.addAction(QIcon("icons/checkbox_checked.png"),"Autoswitch to new Tab when opening", self.deactivate_tabswitching)

        if auto_fill_setting == 0:
            self.settingsMenu.addAction(QIcon("icons/checkbox_empty.png"),"Autofill login credentials", self.activate_auto_fill)
        elif auto_fill_setting == 1:
            self.settingsMenu.addAction(QIcon("icons/checkbox_checked.png"),"Autofill login credentials", self.deactivate_auto_fill)

        self.menu_button.setMenu(self.browserMenu)
    # endregion
    # region ---------multi-search-functions------------------------------------
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

    def whitelist_clear(self):
        for _ in range(self.whitelist.count()):
            item_raw = self.whitelist.takeItem(0)
            item_name = item_raw.text()[:item_raw.text().find(" (")]
            item_type = item_raw.text()[item_raw.text().find("(") + 1:item_raw.text().find(")")]
            white_list[item_type].remove(item_name)
            item_list[item_type].append(item_name)
            item_list[item_type].sort()
        self.update_taglist()

    def whitelist_remove(self):
        current = self.whitelist.currentItem()
        if current != None:
            item_raw = self.whitelist.takeItem(self.whitelist.row(self.whitelist.currentItem()))
            item_name = item_raw.text()[:item_raw.text().find(" (")]
            item_type = item_raw.text()[item_raw.text().find("(") + 1:item_raw.text().find(")")]
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

    def blacklist_clear(self):
        for _ in range(self.blacklist.count()):
            item_raw = self.blacklist.takeItem(0)
            item_name = item_raw.text()[:item_raw.text().find(" (")]
            item_type = item_raw.text()[item_raw.text().find("(") + 1:item_raw.text().find(")")]
            black_list[item_type].remove(item_name)
            item_list[item_type].append(item_name)
            item_list[item_type].sort()
        self.update_taglist()

    def blacklist_remove(self):
        current = self.blacklist.currentItem()
        if current != None:
            item_raw = self.blacklist.takeItem(self.blacklist.row(self.blacklist.currentItem()))
            item_name = item_raw.text()[:item_raw.text().find(" (")]
            item_type = item_raw.text()[item_raw.text().find("(") + 1:item_raw.text().find(")")]
            black_list[item_type].remove(item_name)
            item_list[item_type].append(item_name)
            item_list[item_type].sort()
            self.update_taglist()

    def update_gallerycounter(self, abc, type):
        if self.check_loadfacts.isChecked() == False:
            typex = type_converter(type)
            try:
                c.execute(f"SELECT * FROM {typex}information WHERE tag='{abc}'")
                tu = c.fetchone()
                count = int(tu[1])
                self.pagecount.display(count)
                percentage = int(count) / int(latest_gallery)
                self.percentagecount.setValue(int(percentage * 100))
                text = ""
                if tu[2] != 'None':
                    text = text + f"{tu[2]}\nby EHwiki"
                if tu[3] != 'None':
                    text = text + f"\n\n{tu[3]}"
                if text == "":
                    text = "No description written yet.\nIf you want to add a description for this tag, please contact me on Discord:\nN. J\u00e4cha#1707"

                self.describtion.setText(text)

            except:
                print("Error while loading the description or gallery-counter")

    def criterialist_update_gallerycounter(self):
        current_abc = self.criterialist.currentItem().text()
        current_type = self.choosetype.currentText()
        self.update_gallerycounter(abc=current_abc, type=current_type)

    def whitelist_update_gallerycounter(self):
        current_abc = self.whitelist.currentItem().text()[:self.whitelist.currentItem().text().find(" (")]
        current_type = self.whitelist.currentItem().text()[
                       self.whitelist.currentItem().text().find("(") + 1:self.whitelist.currentItem().text().find(
                           ")")]
        self.update_gallerycounter(abc=current_abc, type=current_type)

    def blacklist_update_gallerycounter(self):
        current_abc = self.blacklist.currentItem().text()[:self.blacklist.currentItem().text().find(" (")]
        current_type = self.blacklist.currentItem().text()[
                       self.blacklist.currentItem().text().find("(") + 1:self.blacklist.currentItem().text().find(
                           ")")]
        self.update_gallerycounter(abc=current_abc, type=current_type)

    def opentaginbrowser(self, type, abc):
        type = type_converter(type)
        abc = abc.replace(" ", "-")  # .replace(".","")
        if abc.endswith("-"):
            abc = abc[:-1]
        if self.check_internal.isChecked() == True:
            qurl = QtCore.QUrl(f"https://hentaifox.com/{type}/{abc}/")
            self.tabWidget.setCurrentIndex(0)
            self.add_new_tab(qurl, label="loading...")
        elif self.check_external.isChecked() == True:
            os.system(f"start https://hentaifox.com/{type}/{abc}/")

    def criterialist_opentaginbrowser(self):
        current_abc = self.criterialist.currentItem().text()
        current_type = self.choosetype.currentText()
        self.opentaginbrowser(abc=current_abc, type=current_type)

    def whitelist_opentaginbrowser(self):
        current_abc = self.whitelist.currentItem().text()[:self.whitelist.currentItem().text().find(" (")]
        current_type = self.whitelist.currentItem().text()[
                       self.whitelist.currentItem().text().find("(") + 1:self.whitelist.currentItem().text().find(
                           ")")]
        self.opentaginbrowser(abc=current_abc, type=current_type)

    def blacklist_opentaginbrowser(self):
        current_abc = self.blacklist.currentItem().text()[:self.blacklist.currentItem().text().find(" (")]
        current_type = self.blacklist.currentItem().text()[
                       self.blacklist.currentItem().text().find("(") + 1:self.blacklist.currentItem().text().find(
                           ")")]
        self.opentaginbrowser(abc=current_abc, type=current_type)

    def multi_search(self):
        if self.whitelist.count() > 0:
            start_time = time.time()
            filename = ""
            connection = ""
            for list_ in white_list.values():
                for tag in list_:
                    filename = filename + connection + f"{tag}"
                    connection = "-"
            connection = "!"
            for list_ in black_list.values():
                for tag in list_:
                    filename = filename + connection + f"{tag}"
            filename = filename.replace(" ", "_")
            whitelist = []
            blacklist = []

            string = f"SELECT DISTINCT gal FROM galleryinformation WHERE true "
            for type, list_ in white_list.items():
                if len(list_) > 0:
                    for tag in white_list[type]:
                        string = string + f"AND gal IN (SELECT gal FROM gallery{type} WHERE tag='{tag}') "
            c.execute(f"{string}")
            result = c.fetchall()
            for tu in result:
                whitelist.append(tu[0])

            for type, list_ in black_list.items():
                if len(list_) > 0:
                    string = f"SELECT DISTINCT gal FROM galleryinformation WHERE true"
                    for type, list_ in black_list.items():
                        if len(list_) > 0:
                            connection = " AND "
                            for tag in black_list[type]:
                                string = string + connection + f"gal IN (SELECT gal FROM gallery{type} WHERE tag='{tag}')"
                                connection = " OR "
                    print(string)
                    c.execute(f"{string}")
                    result = c.fetchall()
                    for tu in result:
                        blacklist.append(tu[0])
                    break

            whitelist.sort()
            blacklist.sort()
            if len(blacklist) > 0:
                results = list(set(whitelist) - set(blacklist))
            else:
                results = list(whitelist)
            results.sort()

            if len(results) > 0:
                with open(f"Results (TXT)/{filename}.txt", "w+") as t:
                    for gallery in results:
                        t.write(f"https://hentaifox.com/gallery/{gallery}/\n")
                with open(f"Results (JSON)/{filename}.result", "w") as j:
                    data = []
                    for gallery in results:
                        data.append(gallery)
                    json.dump(data, j, indent=4)
                self.label.setText(
                    f'Found {len(results)} galleries. You can find "{filename}.txt" in the "Results (TXT)" folder and "{filename}.result" in the "Results (JSON)" folder.')
            else:
                self.label.setText(f'Sorry no results for the combination {filename}.')
            duration = time.time() - start_time
            self.diagnostics.setText(
                f"Search Diagnostics:\n\nGalleries found: {len(results)}\nDuration: {duration} seconds")
            print(f"Multisearch finished | File: {filename}.txt/result")

    def internal_toggled(self):
        self.check_external.setChecked(False)

    def external_toggled(self):
        self.check_internal.setChecked(False)

    def reorder_itemlist(self, feature, up_down):
        for type in types:
            typex = type_converter(type)
            item_list[type] = []
            c.execute(f"SELECT DISTINCT tag FROM {typex}information WHERE true ORDER BY {feature} {up_down}")
            for tu in c.fetchall():
                item_list[type].append(tu[0])

            for item in white_list[type]:
                item_list[type].remove(item)
            for item in black_list[type]:
                item_list[type].remove(item)
            self.update_taglist()

    def name_toggled(self):
        self.Sort_Name.setChecked(True)
        self.Sort_Count.setChecked(False)
        self.reorder_taglist()

    def count_toggled(self):
        self.Sort_Count.setChecked(True)
        self.Sort_Name.setChecked(False)
        self.reorder_taglist()

    def asc_toggled(self):
        self.Sort_ASC.setChecked(True)
        self.Sort_DESC.setChecked(False)
        self.reorder_taglist()

    def desc_toggled(self):
        self.Sort_DESC.setChecked(True)
        self.Sort_ASC.setChecked(False)
        self.reorder_taglist()

    def reorder_taglist(self):
        if self.Sort_ASC.isChecked() == True:
            up_down = "ASC"
        elif self.Sort_DESC.isChecked() == True:
            up_down = "DESC"
        if self.Sort_Name.isChecked() == True:
            feature = "tag"
        elif self.Sort_Count.isChecked() == True:
            feature = "galleries"
        self.reorder_itemlist(feature, up_down)
    # endregion
    # region ---------update-functions------------------------------------------
    def update_start(self):
        self.start.setText(f"Start searching for gaps and updates at: {self.startslider.value()}")

    def update_stop(self):
        self.stop.setText(f"Stop searching for gaps and updates at: {self.stopslider.value()}")

    def update_datamap(self):
        try_update = self.update_database()
        if try_update == 0:
            msg = QtWidgets.QMessageBox(self.tabs)
            msg.setWindowTitle("Up to Date")
            msg.setText(f'Already using the latest version of the database.')
            msg.exec_()
    #endregion
    # region ---------result-functions------------------------------------------
    def load_result_filelist(self):
        self.filebrowser.clear()
        if self.tabWidget.currentIndex() == 2:
            for file in os.listdir("./Results (JSON)/"):
                if file.endswith(".result"):
                    self.filebrowser.addItem(file)

    def load_results(self):
        result_view_list.clear()
        self.resultlist.clear()
        if self.filebrowser.currentItem() != None:
            result_file = self.filebrowser.currentItem().text()
            with open(f"Results (JSON)/{result_file}", "r") as f:
                data = json.load(f)
                for gallery in data:
                    result_view_list.append(gallery)
        self.result_file_name = result_file
        self.open_in_result_tab_button.setEnabled(True)
        self.display_results()

    def display_results(self):
        self.resultlist.clear()
        if self.SortR_TITLE.isChecked() == True:
            feature = "title"
        elif self.SortR_PAGES.isChecked() == True:
            feature = "pages"
        else:
            feature = "gal"
        if self.SortR_DESC.isChecked() == True:
            up_down = "DESC"
        else:
            up_down = "ASC"
        if len(result_view_list) > 0:
            c.execute(
                f"SELECT * FROM galleryinformation WHERE gal IN {tuple(result_view_list)} ORDER BY {feature} {up_down}")
            self.list_of_tuples = c.fetchall()
            if self.choosedisplaytype.currentText() == "ID":
                for tu in self.list_of_tuples:
                    item = QtWidgets.QListWidgetItem()
                    item.setText(str(tu[0]))
                    item.setToolTip(tu[1])
                    self.resultlist.addItem(item)
            elif self.choosedisplaytype.currentText() == "TITLE":
                for tu in self.list_of_tuples:
                    item = QtWidgets.QListWidgetItem()
                    item.setText(tu[1])
                    item.setToolTip(str(tu[0]))
                    self.resultlist.addItem(item)

    def open_in_result_tab(self):
        tups = self.list_of_tuples
        term = self.result_file_name
        self.create_result_tab(tups,term)
        self.tabWidget.setCurrentIndex(0)

    def preview(self):
        if self.resultlist.currentItem() != None:
            self.tags.clear()
            self.characters.clear()
            self.artistsandgroups.clear()
            self.parodies.clear()
            if self.choosedisplaytype.currentText() == "ID":
                id = self.resultlist.currentItem().text()
            if self.choosedisplaytype.currentText() == "TITLE":
                id = self.resultlist.currentItem().toolTip()
            c.execute(f"SELECT * FROM galleryinformation WHERE gal='{id}'")
            tu = c.fetchone()
            title = tu[1]
            pages = int(tu[2])
            cover_url = tu[3]

            self.title.setText(title.replace("|", "\n"))
            self.pagescount2.display(pages)

            if self.check_preview.isChecked() == False:
                try:
                    self.cover.setUrl(QUrl(cover_url))
                    self.cover_id_overlay.setText(id)
                    self.cover_id_overlay.adjustSize()
                    self.cover_id_overlay.raise_()
                except:
                    print("Error while loading Cover")

            for type in types:
                if type != "categories":
                    try:
                        c.execute(f"SELECT tag FROM gallery{type} WHERE gal='{id}'")
                        for tu in c.fetchall():
                            if type == "parodies":
                                self.parodies.addItem(tu[0])
                            if type == "characters":
                                self.characters.addItem(tu[0])
                            if type == "tags":
                                self.tags.addItem(tu[0])
                            if type == "artists":
                                self.artistsandgroups.addItem(f"{tu[0]} (artist)")
                            if type == "groups":
                                self.artistsandgroups.addItem(f"{tu[0]} (group)")
                    except:
                        print(f"Error: {type}")

    def R_ID_toggled(self):
        self.SortR_ID.setChecked(True)
        self.SortR_TITLE.setChecked(False)
        self.SortR_PAGES.setChecked(False)
        self.display_results()

    def R_PAGES_toggled(self):
        self.SortR_PAGES.setChecked(True)
        self.SortR_TITLE.setChecked(False)
        self.SortR_ID.setChecked(False)
        self.display_results()

    def R_TITLE_toggled(self):
        self.SortR_TITLE.setChecked(True)
        self.SortR_ID.setChecked(False)
        self.SortR_PAGES.setChecked(False)
        self.display_results()

    def R_ASC_toggled(self):
        self.SortR_ASC.setChecked(True)
        self.SortR_DESC.setChecked(False)
        self.display_results()

    def R_DESC_toggled(self):
        self.SortR_DESC.setChecked(True)
        self.SortR_ASC.setChecked(False)
        self.display_results()

    def opentaginbrowser2(self, type, abc):
        type = type_converter(type)
        abc = abc.replace(" ", "-")  # .replace(".","")
        if abc.endswith("-"):
            abc = abc[:-1]
        if self.check_internal2.isChecked() == True:
            qurl = QtCore.QUrl(f"https://hentaifox.com/{type}/{abc}/")
            self.tabWidget.setCurrentIndex(0)
            self.add_new_tab(qurl, label="loading...")
        elif self.check_external2.isChecked() == True:
            os.system(f"start https://hentaifox.com/{type}/{abc}/")

    def tags_opentaginbrowser(self):
        current_abc = self.tags.currentItem().text()
        current_type = "tags"
        self.opentaginbrowser2(abc=current_abc, type=current_type)

    def characters_opentaginbrowser(self):
        current_abc = self.characters.currentItem().text()
        current_type = "characters"
        self.opentaginbrowser2(abc=current_abc, type=current_type)

    def parodies_opentaginbrowser(self):
        current_abc = self.parodies.currentItem().text()
        current_type = "parodies"
        self.opentaginbrowser2(abc=current_abc, type=current_type)

    def artistsandgroups_opentaginbrowser(self):
        current_abc = self.artistsandgroups.currentItem().text()[
                      :self.artistsandgroups.currentItem().text().find(" (")]
        current_type = self.artistsandgroups.currentItem().text()[self.artistsandgroups.currentItem().text().find(
            "(") + 1:self.artistsandgroups.currentItem().text().find(")")]
        current_type = current_type + "s"
        self.opentaginbrowser2(abc=current_abc, type=current_type)

    def opengalleryinternal(self):
        if self.choosedisplaytype.currentText() == "ID":
            id = self.resultlist.currentItem().text()
        if self.choosedisplaytype.currentText() == "TITLE":
            id = self.resultlist.currentItem().toolTip()
        url = f"https://hentaifox.com/gallery/{id}"
        qurl = QtCore.QUrl(url)
        self.tabWidget.setCurrentIndex(0)
        self.add_new_tab(qurl, label="loading...")

    def opengalleryexternal(self):
        if self.choosedisplaytype.currentText() == "ID":
            id = self.resultlist.currentItem().text()
        if self.choosedisplaytype.currentText() == "TITLE":
            id = self.resultlist.currentItem().toolTip()
        url = f"https://hentaifox.com/gallery/{id}"
        os.system(f"start {url}")

    def deletefile(self):
        if self.filebrowser.currentItem() != None:
            result_file = self.filebrowser.currentItem().text()
            os.remove(f"Results (JSON)/{result_file}")
            os.remove(f"Results (TXT)/{result_file[:-7]}.txt")
            self.load_result_filelist()

    def copy_result_to_clipboard(self):
        if self.choosedisplaytype.currentText() == "ID":
            id = self.resultlist.currentItem().text()
        if self.choosedisplaytype.currentText() == "TITLE":
            id = self.resultlist.currentItem().toolTip()
        pyperclip.copy(f"https://hentaifox.com/gallery/{id}")

    def open_json_folder(self):
        path = os.path.abspath("./Results (JSON)/")
        os.system(f'explorer {path}')

    def open_txt_folder(self):
        path = os.path.abspath("./Results (TXT)/")
        os.system(f'explorer {path}')
    #endregion
#endregion
# region-web-engine
class WebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.tab = self.parent()

    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.tab)
        self.tab.create_new_tab(new_webview)
        return new_webview
#endregion
# region app.exec_
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
#endregion
