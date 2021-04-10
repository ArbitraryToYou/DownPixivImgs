import re
import os
from time import sleep
from random import randint
from libs.web import openImg

def purifyName(bf_name):
    name = re.sub(r'[:/*?|<>"\\]', '', bf_name)
    return name

def menu(titles, tot_page, page=1):
    if tot_page == 0:
        print('未查询到数据。')
    else:
        for i in range(0, 20):
            tmp = 20*page+i-20
            if tmp >= len(titles):
                break
            print(str(i+1) + '. ' + titles[tmp][0])
        print('=' * 24 + '第' + str(page) + '页  共' + str(tot_page) + '页' + '='*24)

def chtodir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

def getDirImgsNum(title):
    main_path = os.getcwd() + '\\Download\\' + title
    num = os.listdir(main_path)
    return len(num)

def getWinSize():
    width = os.get_terminal_size().columns
    return width

def myPrint(str, com, per):
    print(str + ' '*(getWinSize() - len(str)-4))
    print('\r[%s%s] %.2f%%\r' % ('='*com, ' '*(getWinSize()-12-com), per), end='')

def download(title, links, names, downnum, failnum, delta=1, done=1):
    if os.path.exists(title):
        return
    os.mkdir(title)
    os.chdir(title)
    imgs = links.split('|')
    img_names = names.split('|')#解析
    index = 0
    for img in imgs:
        stop = randint(800, 1200) / 1000
        per = (delta / len(imgs)*(index+1) + done)*100#百分比
        com = int((delta / len(imgs)*(index+1) + done) * (getWinSize()-12))
        parse = img.split('.')
        try:
            name = img_names[index] + '.' + parse[-1]
        except:
            name = img_names[index] + '.jpg'
        name = purifyName(name)
        try:
            html = openImg(img)
        except:
            strFail = '[Sorry: %s is die!]' % name
            myPrint(strFail, com, per)
            sleep(stop)
            failnum += 1
            index += 1
            continue
        text = html.content
        if len(text) < 88000:
            index += 1
            continue
        with open(name, 'wb') as file:
            file.write(text)
        strSuccess = 'Downloading %s ......' % name
        myPrint(strSuccess, com, per)
        sleep(stop)
        downnum += 1
        index += 1
    os.chdir('../')
    os.system('cls')
    return downnum, failnum

def readLastName():
    if os.path.exists('last.txt'):
        with open('last.txt', 'r') as f:
            lastName = f.read()
    else:
        lastName = ''
    return lastName

def rmFile(path):
    namelist = os.listdir(path)
    if not namelist:
        os.rmdir(path)
    else:
        for tmp in namelist:
            fileName = path + '\\' + tmp
            os.remove(fileName)
        os.rmdir(path)

if __name__ == '__main__':
    pass