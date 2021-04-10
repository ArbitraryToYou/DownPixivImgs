import os
import configparser

class Config(object):
    def __init__(self, config_file = 'config.ini'):
        abs_path = os.path.abspath(__file__)
        self._path = os.path.join(os.path.dirname(abs_path), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError('No such file: "config.ini" in %s' % os.path.dirname(abs_path))
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)

    def items(self, section):
        return self._config.items(section)

    def itemsRaw(self, section):
        return self._configRaw.items(section)

global_config = Config()