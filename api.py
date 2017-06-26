import json
import matplotlib.pyplot as plt
import urllib.request
import sys
import os
import re


#выкачиваем посты с Лентача, записываем в файл
def lentach(target_date, non_bmp_map):
    lentach = open('lentach.txt', 'w', encoding='utf-8')

    check_date=False
    w = 0
    while check_date == False: #выкачиваем посты по 100, пока не "наткнемся" на пограничную дату
        req_lentach = urllib.request.Request('https://api.vk.com/method/wall.get?domain=oldlentach&count=100&offset='+str(w*100))
        response_lentach = urllib.request.urlopen(req_lentach)
        result_lentach = response_lentach.read().decode('utf-8')
        data1 = json.loads(result_lentach)
        for i in range(1, 101):
            if data1['response'][i]['date'] < target_date:
                check_date = True
                break
            else:
                text_lentach = data1['response'][i]['text'].translate(non_bmp_map) #разбираемся со смайликами
                lentach.write(text_lentach)
                print (text_lentach)
        w+=1
    lentach.close()


#выкачиваем посты с рбк, записываем в файл
def rbc(target_date, non_bmp_map):
    rbc = open('rbc.txt', 'w', encoding='utf-8')

    check_date=False
    w = 0
    while check_date == False:
        req_rbc = urllib.request.Request('https://api.vk.com/method/wall.get?domain=rbc&count=100') #каждый раз по 100, до нужной даты
        response_rbc = urllib.request.urlopen(req_rbc)
        result_rbc = response_rbc.read().decode('utf-8')
        data2 = json.loads(result_rbc)
        for i in range(1, 101):
            if data1['response'][i]['date'] < target_date:
                check_date = True
                break
            else:
                text_rbc = data2['response'][i]['text'].translate(non_bmp_map)
                rbc.write(text_rbc)
        w+=1
    rbc.close()


#выкачиваем посты с ленты.ру, записываем их в файл
def lentaru(target_date, non_bmp_map):
    lentaru = open('lentaru.txt', 'w', encoding='utf-8')

    check_date=False
    w = 0
    while check_date == False:
        req_lentaru = urllib.request.Request('https://api.vk.com/method/wall.get?domain=lentaru&count=100')
        response_lentaru = urllib.request.urlopen(req_lentaru)
        result_lentaru = response_lentaru.read().decode('utf-8')
        data3 = json.loads(result_lentaru)
        for i in range(1, 101):
            if data1['response'][i]['date'] < target_date:
                check_date = True
                break
            else:
                text_lentaru = data['response'][i]['text'].translate(non_bmp_map)
                lentaru.write(text_lentaru)
        w+=1
    lentaru.close()


def my_stem(filename):
    os.system('C:/Users/Note/Desktop/python/mystem.exe ' + filename +  ' new_' + filename + ' -n')


#находим нужные слова + их частотность (кол-во искомых слов делим на общее кол-во слов)
def get_word(filename, data, words):
    local_data = []
    f = open(filename, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    dlina = len(text.split())

    for n,word in enumerate (words):
        wrd = len (re.findall(word, text))
        local_data.append (wrd/dlina)
    data.append(local_data)

    return data


#строим график частотности (три больших столбца,  в каждом из которых по 5 столбцов, обозначающих искомые слова)
def graph(data):
    X = [1, 2, 3, 4, 5]

    plt.plot(X, data[0], 'g', label='Лентач')
    plt.plot(X, data[1], 'c', label='РБК')
    plt.plot(X, data[2], 'r', label='Лента.ру')
    plt.xticks(X, words, rotation='vertical')

    plt.title('График частотности некоторых слов в сообществах с политической тематикой')
    plt.ylabel('Частотность')
    plt.xlabel('Слова')
    plt.legend()
    plt.savefig('graph.png')


def main():
    target_date = 1497268800  # unixtime 12\06\2017 12:00:00
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    words = ['президент', 'правительство', 'политолог', 'закон', 'депутат']
    data = []

    lentach(target_date, non_bmp_map)
    rbc(target_date, non_bmp_map)
    lentaru(target_date, non_bmp_map)

    my_stem('lentach.txt')
    my_stem('rbc.txt')
    my_stem('lentaru.txt')

    data = get_word('new_lentach.txt', data, words)
    data = get_word('new_rbc.txt', data, words)
    data = get_word('new_lentaru.txt', data, words)

    graph(data)


if __name__ == '__main__':
    main()
