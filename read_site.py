import requests
from bs4 import BeautifulSoup
import pyttsx3
import json
from time import sleep
import googlesearch

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def getText(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.get_text()#.select_one('p')

    return article

def getGoogle(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.find('title').string

    return article

def google_(url):
    search = googlesearch.search("", lang="ru", num=10, stop=10, pause=2)

    for i in search:
        print(getText(i), i)




#https://ru.hexlet.io/courses/introduction_to_programming
#'https://habr.com/ru/post/416889/'
 #"https://www.ilibrary.ru/text/4325/p.1/index.html" #"https://habr.com/ru/post/519454/"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

url =  ""
text = []


i = 0
n = 0

while True:
    with open("reading_url.json", "r", errors='ignore') as ReadFile:
        data = json.load(ReadFile)

    print(data)

    if data["url"] != url:
        engine.say("Сейчас прочитаю")

        url = data["url"]

        if "https://www.google.com/search?q=" in url:
            text = data["google"]
        else:
            text = getText(url).split(".")

        n = len(text)
        i = 0

    if data["read"] == 0:
        print(i, n)
        if i < n:
            engine.say(str(text[i]))
            i += 1
    elif data["read"] == 2:
        while data["read"] == 2:
            with open("reading_url.json", "r", errors='ignore') as ReadFile:
                data = json.load(ReadFile)
            sleep(1)

        engine.say("Сейчас прочитаю")

        url = data["url"]

        if "https://www.google.com/search?q=" in url:
            text = data["google"]
        else:
            text = getText(url).split(".")

        n = len(text)
        i = 0

    engine.runAndWait()