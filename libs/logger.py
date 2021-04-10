import os
import logging

class Logger(object):
    def __init__(self, log_name, logger_name=None):#注意默认值顺序
        self.my_logger = logging.getLogger(logger_name)
        self.my_logger.setLevel(logging.DEBUG)#设置等级

        path = os.getcwd() + '/Logs/'
        if not os.path.exists(path):
            os.mkdir(path)
        file_path = path + log_name
        fh = logging.FileHandler(file_path, mode='w')
        fh.setLevel(logging.DEBUG)#输出到文件的log等级

        formatter = logging.Formatter('[%(asctime)s] %(filename)s - %(levelname)s: %(message)s', '%Y/%m/%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.my_logger.addHandler(fh)

    def get_logger(self):
        return self.my_logger