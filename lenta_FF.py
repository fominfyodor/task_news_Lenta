import requests
import pandas as pd

from bs4 import BeautifulSoup
from collections import Counter

#Создаём список с категориями новостей из Ленты
category = [
    "russia", "world", "ussr", 
    "economics", "forces", "science", 
    "culture", "sport", "media", 
    "style", "travel", "life", "realty"]

site_lenta_rubrics = "https://lenta.ru/rubrics/"
site_lenta = "https://lenta.ru"

for i in category:
    d = []
    r = requests.get(site_lenta_rubrics+i, timeout=5)
    soup = BeautifulSoup(r.text)
    for j in soup.find_all("h3"): #Ссылки на статьи на странице рубрики хранятся между тегами "h3"
        for k in j.find_all("a", href=True): #и тегами "a"
            r = requests.get(site_lenta+k["href"], timeout=5)
            soup = BeautifulSoup(r.text)
            for l in soup.find_all("p"): # Текст статьи хранится между тегами "p"
                l = l.getText()
                words = l.lower() #Переводим символы строки в строчный формат
                words = words.replace(".","") #Избавляемся от лишних символов перед и после слова
                words = words.replace(",","")
                words = words.replace('"','')
                words = words.replace('«','')
                words = words.replace('»','')
                words = words.replace('—','')
                words = words.replace('(','')
                words = words.replace(')','')
                words = words.replace(':','')
                words = words.replace(';','')
                words = words.split()
                d.extend(words)
        wordCount = Counter(d)
    df = pd.DataFrame.from_dict(wordCount, orient='index').reset_index()
    df = df.sort_values([0], ascending=False)
    df = df.reset_index(drop=True)
    df[0:20].to_csv(i+'.csv', index=False, header=False)
