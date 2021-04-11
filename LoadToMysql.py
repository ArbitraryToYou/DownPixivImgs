from libs.web import *
from libs.util import *
from time import sleep
from lxml import etree
from random import randint
from libs.logger import Logger
from libs.my_sql import global_mysql

if __name__ == '__main__':
    final_page = int(input('最终页数：'))
    i = int(input('开始页数：'))
    last_page = 0
    first_page = i
    UPDATE_NUM = REPEAT_NUM = 0
    START_DATE = END_DATE = START_TITLE = END_TITLE = ERR = ''
    try:
        while i <= final_page and i > 0:
            url = 'http://acg17.com/tag/pixiv' + '/page/' + str(i) + '/'
            base_response = openImg(url)
            if str(type(base_response)) == '<class \'str\'>':
                ERR = ERR + base_response + ', '
                continue
            base_html = etree.HTML(base_response.text)
            if last_page == 0:
                last_page = getLastPage(base_html)
            links = base_html.xpath('//div[contains(@class, "post-listing")]//h2//a//@href')#每页标题链接
            titles = base_html.xpath('//div[contains(@class, "post-listing")]//h2//a/text()')#标题
            be_types = base_html.xpath('//div[contains(@class, "post-listing")]//span[@class="post-cats"]//text()')#类型
            types = handleType(be_types)
            be_dates = base_html.xpath('//div[contains(@class, "post-listing")]//span[@class="tie-date"]//text()')#日期
            dates = handleDate(be_dates)
            if i == first_page:
                END_DATE = dates[0]
                END_TITLE = titles[0]
            START_DATE = dates[-1]
            START_TITLE = titles[-1]
            if len(links) != len(titles) or len(links) != len(types):
                raise Exception('ParseError:标题/类型和链接个数不匹配！')
                break
            index = 0
            for link in links:
                if index >= len(links):
                    break
                print('Downloading Title: %s ...' % titles[index])
                stop = randint(1000, 1500) / 1000
                if global_mysql.isRepeat(titles[index], dates[index]):
                    index += 1
                    REPEAT_NUM += 1
                    sleep(0.2)
                    continue
                main_response = openImg(link)
                sleep(stop)
                main_html = etree.HTML(main_response.text)
                imgs = main_html.xpath('//div[@class="entry"]//p//img//@src')#图片链接
                be_names = catchTitles(main_response.text, imgs)#每个图片标题
                names = []
                for name in be_names:
                    tmp = purifyName(name)
                    names.append(tmp)
                global_mysql.insert(titles[index], types[index], dates[index], imgs, names)
                UPDATE_NUM += 1
                index += 1
            i += 1
            sleep(0.5)
            if i > last_page or i > final_page:
                print('Tip: already the last page.')
                break
            print('>>>>>Go to Next Page!<<<<<')
    except (BaseException, Exception) as e:
        global_mysql.myRollback()
        err_log = Logger(log_name='LoadToMysqlError.log', logger_name='ltmerr').get_logger()
        err_log.error(ERR)
        err_log.error(str(e))
    finally:
        output_log = Logger(log_name='LoadToMysqlOutput.log', logger_name='ltmotp').get_logger()
        output_log.info('更新数据%d条' % UPDATE_NUM)
        output_log.info('重复数据%d条' % REPEAT_NUM)
        output_log.info('起始日期%s' % START_DATE)
        output_log.info('起始标题%s' % START_TITLE)
        output_log.info('终止日期%s' % END_DATE)
        output_log.info('终止标题%s' % END_TITLE)
    print('\n\nDone!')