from api.utils.log import myLogger
from api.utils.helper import Singleton


# This class is add/modify/list/delete item to item=value(键值对) model settings file

class SettingsFile(object):

    __metaclass__ = Singleton

    def __init__(self, path):
        self._config = {}
        self.config_file = path
        
    def build_config(self):
        try:
            with open(self.config_file, 'r') as f:
                data = f.readlines()
        except Exception as e:
            data = []
        for i in data:
            if i.startswith('#'):
                continue
            i = i.replace('\n', '').replace('\r\n', '')
            if not i:
                continue
            tmp = i.split('=')
            if len(tmp) != 2:
                myLogger.error_logger(f'invalid format {i}')
                continue
            
            key, value = i.split('=')
            if self._config.get(key) != value:
                self._config[key] = value
        return self._config

    def init_config_from_file(self, config_file: str=None):
        if config_file:
            self.config_file = config_file
        self.build_config()

    def update_setting(self, key: str, value: str):
        self._config[key] = value
        self.flush_config()

    def get_setting(self, key: str, default=None):
        return self._config.get(key, default)

    def list_all_settings(self) -> dict:
        self.build_config()
        return self._config

    def delete_setting(self, key: str, value: str):
        if self._config.get(key) == value:
            del self._config[key]
            self.flush_config()

    def flush_config(self):
        try:
            with open(self.config_file, 'w') as f:
                for key, value in self._config.items():
                    f.write(f'{key}={value}\n')
        except Exception as e:
            myLogger.error_logger(e)
            

# This class is add/modify/cat/delete content from file
# src: path | URL