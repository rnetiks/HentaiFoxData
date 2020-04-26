import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import requests
import json
import os
import os.path
import concurrent.futures
from bs4 import BeautifulSoup
import datetime
import time

web = requests.get("https://hentaifox.com/")
html = web.text
soup = BeautifulSoup(html, "html.parser")
no1 = str(soup.find("div", attrs={"class":"inner_thumb"}))
latest = int(no1[no1.find("/gallery/")+9:no1.find('/"><img')])

values={}
values["start"] = latest-500
values["stop"] = latest

class Ui_Updater(object):
    def setupUi(self, Updater):
        Updater.setObjectName("Updater")
        Updater.resize(576, 221)
        self.centralwidget = QtWidgets.QWidget(Updater)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(10, 150, 551, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.StartSlider = QtWidgets.QSlider(self.centralwidget)
        self.StartSlider.setGeometry(QtCore.QRect(20, 40, 291, 31))
        self.StartSlider.setMinimum(1)
        self.StartSlider.setMaximum(int(latest))
        self.StartSlider.setValue(int(latest)-1000)
        self.StartSlider.setOrientation(QtCore.Qt.Horizontal)
        self.StartSlider.setObjectName("StartSlider")
        self.StopSlider = QtWidgets.QSlider(self.centralwidget)
        self.StopSlider.setGeometry(QtCore.QRect(20, 110, 291, 31))
        self.StopSlider.setMinimum(1)
        self.StopSlider.setMaximum(int(latest))
        self.StopSlider.setValue(int(latest))
        self.StopSlider.setOrientation(QtCore.Qt.Horizontal)
        self.StopSlider.setObjectName("StopSlider")
        self.UpdateButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateButton.setGeometry(QtCore.QRect(360, 30, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.UpdateButton.setFont(font)
        self.UpdateButton.setObjectName("UpdateButton")
        self.StartLable = QtWidgets.QLabel(self.centralwidget)
        self.StartLable.setGeometry(QtCore.QRect(20, 10, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.StartLable.setFont(font)
        self.StartLable.setObjectName("StartLable")
        self.StopLable = QtWidgets.QLabel(self.centralwidget)
        self.StopLable.setGeometry(QtCore.QRect(20, 80, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.StopLable.setFont(font)
        self.StopLable.setObjectName("StopLable")
        self.StatusLable = QtWidgets.QLabel(self.centralwidget)
        self.StatusLable.setGeometry(QtCore.QRect(360, 90, 200, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.StatusLable.setFont(font)
        self.StatusLable.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.StatusLable.setObjectName("StatusLable")
        Updater.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Updater)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 22))
        self.menubar.setObjectName("menubar")
        Updater.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Updater)
        self.statusbar.setObjectName("statusbar")
        Updater.setStatusBar(self.statusbar)

        self.retranslateUi(Updater)
        QtCore.QMetaObject.connectSlotsByName(Updater)

        self.StartSlider.valueChanged.connect(self.start_moved)
        self.StopSlider.valueChanged.connect(self.stop_moved)
        self.UpdateButton.clicked.connect(self.update)

    def retranslateUi(self, Updater):
        _translate = QtCore.QCoreApplication.translate
        Updater.setWindowTitle(_translate("Updater", "Updater"))
        self.UpdateButton.setText(_translate("Updater", "Update"))
        self.StartLable.setText(_translate("Updater", f"Start searching for gaps and updates at: {latest-500}"))
        self.StopLable.setText(_translate("Updater", f"Stop searching for gaps and updates at: {latest}"))
        self.StatusLable.setText(_translate("Updater", "Current status:"))

    def start_moved(self):
        self.StartLable.setText(f"Start searching for gaps and updates at: {self.StartSlider.value()}")
        values["start"] = self.StartSlider.value()

    def stop_moved(self):
        self.StopLable.setText(f"Stop searching for gaps and updates at: {self.StopSlider.value()}")
        values["stop"] = self.StopSlider.value()

    def update(self):
        parodies = {}
        characters = {}
        tags = {}
        artists = {}
        groups = {}
        categories = {}
        gals = {}
        found= {}
        not_found= []


        types = ["parodies","characters","tags","artists","groups","categories"]
        for type in types:
            self.StatusLable.setText(f"Current status: Loading {type}")
            for file in os.listdir(f"./{type}/"):
                abc = str(file)[:-5]
                with open(f"{type}/{abc}.json","r") as g:
                    gals_per_tag = json.load(g)
                    gals[abc] = gals_per_tag["galleries"]
            val = self.progressBar.value() + 5
            self.progressBar.setValue(int(val))

        start_id = values["start"]
        y = values["stop"]

        for x in range(start_id,int(y+1)):
            print(f"searching for {x}")
            found[x]= "not found"
            for abc in gals:
                if x in gals[abc]:
                    found[x]= "found"
                    break
        self.progressBar.setValue(60)

        time.sleep(0.1)

        for gal in found:
            if found[gal] == "found":
                pass
            else:
                not_found.append(gal)

        with open("not_found.json","w") as f:
            data = not_found
            json.dump(data,f,indent=4)

        gaps = []

        def fetch(x):
            web = requests.get(f"https://hentaifox.com/gallery/{x}/")
            html = web.text
            soup = BeautifulSoup(html, 'html.parser')
            okay = soup.find('title')
            if str(okay) == "<title>404 Not Found - HentaiFox</title>":
                gaps.append(x)
                return f"404 not found ({x})"
            par_result = soup.find_all('ul', attrs={'class':'parodies'})
            if par_result != []:
                par_res = par_result[0]
                pars_raw = par_res.find_all('a', attrs={'class':'tag_btn'})
                for par_raw in pars_raw:
                    par = (par_raw.text.replace(str(par_raw.find("span").text),''))[:-1]
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
                    char = (char_raw.text.replace(str(char_raw.find("span").text),''))[:-1]
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
                    tag = (tag_raw.text.replace(str(tag_raw.find("span").text),''))[:-1]
                    if int(tag_raw.find("span",attrs={'class':'t_badge'}).text) > 100:
                        if str(tag) in tags:
                            pass
                        else:
                            tags[tag] = []
                        tags[tag].append(x)

            art_result = soup.find_all('ul', attrs={'class':'artitst'})
            if art_result != []:
                art_res = art_result[0]
                arts_raw = art_res.find_all('a', attrs={'class':'tag_btn'})
                for art_raw in arts_raw:
                    art = (art_raw.text.replace(str(art_raw.find("span").text),''))[:-1]
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
                    grp = (grp_raw.text.replace(str(grp_raw.find("span").text),''))[:-1]
                    if int(grp_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                        if str(grp) in groups:
                            pass
                        else:
                            groups[grp] = []
                        groups[grp].append(x)

            cat_result = soup.find_all('ul', attrs={'class':'groups'})
            if cat_result != []:
                cat_res = cat_result[0]
                cats_raw = cat_res.find_all('a', attrs={'class':'tag_btn'})
                for cat_raw in cats_raw:
                    cat = (cat_raw.text.replace(str(cat_raw.find("span").text),''))[:-1]
                    if int(cat_raw.find("span",attrs={'class':'t_badge'}).text) > 1:
                        if str(cat) in groups:
                            pass
                        else:
                            groups[cat] = []
                        groups[cat].append(x)
            return f"Done ({x})"

        def save():
            print("saving all")
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
                        print(f"{tag} saved")
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
                        print(f"{par} saved")
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
                        print(f"{char} saved")
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
                        print(f"{art} saved")
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
                        print(f"{grp} saved")
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
                        print(f"{cat} saved")
                categories[cat] = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(fetch, x) for x in not_found]
            le = 40/int(len(not_found))
            for f in concurrent.futures.as_completed(results):
                print(f.result())
                val = self.progressBar.value() + le
                self.progressBar.setValue(int(val))

        save()
        with open("404.txt","w+") as f:
            for gal in gaps:
                content = f.read()
                f.write(f"{content}\n{gal}")
        self.progressBar.setValue(100)
        msg = QMessageBox()
        msg.setWindowTitle("Finished")
        msg.setText(f"Datamap up to date.\nWrote URL(s) of gaps into 404.txt\n")
        x=msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Updater = QtWidgets.QMainWindow()
    ui = Ui_Updater()
    ui.setupUi(Updater)
    Updater.show()
    sys.exit(app.exec_())
