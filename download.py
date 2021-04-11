import win32api
from libs.util import *
from libs.web import *
from libs.my_sql import global_mysql
from libs.logger import Logger

global MAIN_PATH, ENDNAME, DOWNNUM, FAILNUM

def onClose(sig):
    global MAIN_PATH, END_NAME, DOWN_NUM, FAIL_NUM
    os.chdir(MAIN_PATH)
    lastTitle = MAIN_PATH + '\\Download\\' + purifyName(END_NAME)
    try:
        rmFile(lastTitle)
    except Exception as e:
        err_log = Logger(log_name='CloseErr.log', logger_name='clerr').get_logger()
        err_log.error(str(e))
    with open('last.txt', 'w') as f:
        f.write(END_NAME)
    output_log = Logger(log_name='CloseOutput.log', logger_name='clopt').get_logger()
    output_log.info('下载完成%d张' % DOWN_NUM)
    output_log.info('下载失败%d张' % FAIL_NUM)
    return False

if __name__ == '__main__':
    global MAIN_PATH, END_NAME, DOWN_NUM, FAIL_NUM
    DOWN_NUM = 0
    FAIL_NUM = 0
    END_NAME = ''
    MAIN_PATH = os.getcwd()
    lastName = readLastName()
    if lastName == '':
        titles, links, names = global_mysql.takeall()
    else:
        id = global_mysql.search('SELECT id from tb_imgs WHERE title="%s"' % lastName)
        titles, links, names = global_mysql.takeall(tail='WHERE id>=%d' % id[0])
    global_mysql.close()
    if len(titles) % 20 == 0:
        tot_page = int(len(titles) / 20)
    else:
        tot_page = int(len(titles) / 20) + 1
    menu(titles=titles, tot_page=tot_page)
    chtodir('Download')
    index = 0
    input('\n\nThis program will download all items!\nPress any key to continue.')
    os.system('cls')
    win32api.SetConsoleCtrlHandler(onClose, True)
    try:
        for tit in titles:
            downnum = failnum = 0
            END_NAME = tit[0]
            done = index / len(titles)
            delta = (index+1) / len(titles) - done
            img_title = purifyName(tit[0])
            if not os.path.exists(img_title):
                os.mkdir(img_title)
                os.chdir(img_title)
                downnum, failnum = download(title=img_title, links=links[index][0], names=names[index][0], delta=delta, done=done)
                os.chdir('../')
                os.system('cls')
            index += 1
            DOWN_NUM += downnum
            FAIL_NUM += failnum
    except Exception as e:
        os.chdir(MAIN_PATH)
        lastTitle = MAIN_PATH + '\\Download\\' + purifyName(END_NAME)
        err_log = Logger(log_name='Error.log', logger_name='err').get_logger()
        try:
            rmFile(lastTitle)
        except Exception as fe:
            err_log.error(str(fe))
        with open('last.txt', 'w') as f:
            f.write(END_NAME)
        err_log.error(str(e))
    finally:
        if os.getcwd() != MAIN_PATH:
            os.chdir(MAIN_PATH)
        output_log = Logger(log_name='Output.log', logger_name='output').get_logger()
        output_log.info('下载完成%d张' % DOWN_NUM)
        output_log.info('下载失败%d张' % FAIL_NUM)
        print('>>>The log file in %s.<<<' % MAIN_PATH)
    print('Done!')
    input('\n\nPress any key to quit.')
    