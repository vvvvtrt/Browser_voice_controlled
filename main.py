import sys
from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLineEdit, QMainWindow, QPushButton, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.Qt import Qt
import speech_recognition as sr
from threading import Thread
import requests
import pyttsx3
import keyboard
from bs4 import BeautifulSoup
import googlesearch
import json
import os
import openai

openai.api_key = 'token'


class MainWindow(QMainWindow):

    def __init__(self, url):
        super().__init__()

        self.setWindowTitle('Browser')

        self.toolBar = QToolBar()
        self.toolBar.setStyleSheet('background: rgb(51, 72, 83);')
        self.addToolBar(self.toolBar)
        self.backButton = QPushButton()
        self.backButton.setText("🠔 ")
        self.backButton.setFont(QFont("Bernard MT", 18))
        # self.backButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/left-32.png'))
        self.backButton.setStyleSheet('border-radius: 20px; background: rgb(51, 72, 83); color: rgb(255, 255, 255);')
        self.backButton.clicked.connect(self.back)
        self.toolBar.addWidget(self.backButton)
        self.forwardButton = QPushButton()
        self.forwardButton.setText(" 🠖 ")
        self.forwardButton.resize(50, 50)
        # self.forwardButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/right-32.png'))
        self.forwardButton.setStyleSheet('border-radius: 25px;background: rgb(51, 72, 83); color: rgb(255, 255, 255);')
        self.forwardButton.setFont(QFont("Bernard MT", 18))
        self.forwardButton.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forwardButton)

        self.reboot = QPushButton()
        self.reboot.setText("⭮ ")
        self.reboot.setFont(QFont("Bernard MT", 18))
        self.reboot.setStyleSheet('border-radius: 20px; background: rgb(51, 72, 83); color: rgb(255, 255, 255);')
        self.reboot.clicked.connect(self.load)
        self.toolBar.addWidget(self.reboot)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.setStyleSheet('border-radius: 20px; color: rgb(255, 255, 255);')
        self.addressLineEdit.setFont(QFont("Bernard MT", 10))
        self.addressLineEdit.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.addressLineEdit)

        self.webEngineView = QWebEngineView()
        self.setCentralWidget(self.webEngineView)

        initialUrl = url  # "http://google.com"

        self.addressLineEdit.setText(initialUrl)
        self.webEngineView.load(QUrl(initialUrl))
        # self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        self.webEngineView.page().urlChanged.connect(self.urlChanged)

        # self.hook = keyboard.on_press(self.keyboardEventReceived)

        self.c = recognition(self)
        self.c.start()

        # self.search("http://youtube.com")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.load()
        elif event.key() == Qt.Key_F3:
            self.back()
        elif event.key() == Qt.Key_F4:
            self.forward()

    def load(self):
        url = QUrl(self.addressLineEdit.text())

        self.webEngineView.load(url)

    def reboot1(self, url):
        self.webEngineView.load(QUrl(url))

    def back(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def urlChanged(self, url):
        c = url.toString()
        self.addressLineEdit.setText(c)

    def search(self, url):
        self.addressLineEdit.setText(url)
        print(url)
        self.load()


class recognition(Thread):
    def __init__(self, selff):
        Thread.__init__(self)
        self.selff = selff

    def search(self, text):
        URL = f"https://www.google.com/search?q={text}"

        self.selff.addressLineEdit.setText(URL)

        keyboard.press("F5")

    def url_open(self, num):
        global url_google
        if num < len(url_google):
            self.selff.addressLineEdit.setText(url_google[num])

            keyboard.press("F5")
            return True
        else:
            return False

    def run(self):
        global url_google

        mic = sr.Microphone(device_index=0)

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)

        command = {
            "загугли": 0,
            "загуляли": 0,
            "загуглить": 0,
            "google": 0,
            "за": 0,
            "найди": 0,
            "найти": 0,

            "прочитай": 1,
            "зачитай": 1,
            "почитай": 1,

            "хватит": 2,
            "остановись": 2,
            "остановить": 2,
            "стоп": 2,

            "пауза": 3,
            "приостанови": 3,
            "перерыв": 3,

            "продолжай": 4,
            "продолжи": 4,

            "открой": 5,

            "назад": 6,

            "вперёд": 7,

            "обнови": 8,
            "обновить": 8
        }

        while True:
            r = sr.Recognizer()

            with mic as source:
                print("Say something!")
                audio = r.listen(source, phrase_time_limit=10)

            try:
                text = r.recognize_google(audio, language="ru-RU").lower().split()

                print(text)

                if text[0] in command:
                    if command[text[0]] == 1:

                        dict_ = ReadFile("reading_url.json")

                        dict_["url"] = self.selff.addressLineEdit.text()
                        dict_["read"] = 0

                        if "https://www.google.com/search?q=" in dict_["url"]:
                            c = google_(dict_)

                            dict_["google"] = c

                        Write(dict_, "reading_url.json")
                    elif command[text[0]] == 2:
                        dict_ = ReadFile("reading_url.json")

                        dict_["read"] = 2

                        Write(dict_, "reading_url.json")

                    elif command[text[0]] == 3:
                        dict_ = ReadFile("reading_url.json")

                        dict_["read"] = 1

                        Write(dict_, "reading_url.json")
                    elif command[text[0]] == 4:
                        dict_ = ReadFile("reading_url.json")

                        dict_["read"] = 0

                        Write(dict_, "reading_url.json")

                    elif command[text[0]] == 5:
                        if text[2] in "0123456789":
                            c = self.url_open(int(text[2]) - 1)
                        else:
                            try:
                                arr = {"один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7}
                                c = self.url_open(arr[text[2]] - 1)
                            except:
                                c = False
                        if not c:
                            engine.say("Нет такой ссылки")

                    elif command[text[0]] == 6:
                        keyboard.press("F3")

                    elif command[text[0]] == 7:
                        keyboard.press("F4")

                    elif command[text[0]] == 8:
                        keyboard.press("F5")

                    elif command[text[0]] == 0:
                        new_text = ""

                        for i in text[1:]:
                            new_text += i + "+"

                        self.search(new_text)

                        engine.say(f"вот что удалось найти в интернете по запросу: {new_text.replace('+', ' ')}")
                else:
                    result = openai.Completion.create(
                        engine='text-davinci-003',
                        prompt=" ".join(text),
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.7,
                    )

                    engine.say(result.choices[0].text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

            engine.runAndWait()


def getText(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    try:
        title = root.find('title').string
        return title
    except:
        h1 = root.find('h1').string
        return h1


def google_(dict_):
    global url_google

    if "https://www.google.com/search?q=" in dict_["url"]:
        temp = dict_["url"][32:].split("&")
        query = temp[0].replace("+", " ")

        search = googlesearch.search(query, lang="ru")  # , num=5, stop=5, pause=0)

        arr = []
        url_google = []

        counter = 1

        for i in search:
            url_google.append(i)
            arr.append(f"ссылка {counter}" + getText(i))

            counter += 1

        return arr
    return []


def ReadFile(link):
    try:
        with open(link, "r") as ReadFile:
            data = json.load(ReadFile)
            return data
    except:
        return None


def Write(dict_, link):
    try:
        with open(link, "w") as WriteFile:
            json.dump(dict_, WriteFile)
        return True
    except:
        return False


url = "http://youtube.com"

url_google = []

if __name__ == '__main__':
    os.startfile("read_site.py")

    dict_ = {"url": "http://startpage.pythonanywhere.com/", "read": 0, "google": []}

    Write(dict_, "reading_url.json")

    app = QApplication(sys.argv)

    mainWin = MainWindow("http://startpage.pythonanywhere.com/")
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 2 / 3)
    mainWin.show()
    sys.exit(app.exec_())
