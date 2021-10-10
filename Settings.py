import json, os
class AppConfig():

    IS_DEBUG_KEY = 'is_debug'
    OUT_PATH_KEY = 'out_path'
    FONT_MARGIN_KEY = 'font_margin'
    DELETE_LOG_INTERVAL_KEY = 'delete_log_interval'

    def __init__(self, debug = False):
        self.debug = debug
        self.json_filename = '.\\App_config\\setting.json'
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.default_out_path = os.path.join(ROOT_DIR, 'out')
        self.default_font_margin = 3
        self.default_log_delete_interval = 15 #in days

    def is_debug(self):
        try:
            file = open(self.json_filename, encoding='utf-8-sig')
            data = json.loads(file.read())
            file.close()
            if AppConfig.IS_DEBUG_KEY in data.keys():
                return data[AppConfig.IS_DEBUG_KEY]
            else:
                data[AppConfig.IS_DEBUG_KEY] = self.debug
                with open(self.json_filename, "w") as jsonFile:
                    json.dump(data, jsonFile)
                self.is_debug()
        except FileNotFoundError:
            empty_data = {}
            with open(self.json_filename, "w") as jsonFile:
                json.dump(empty_data, jsonFile)
            self.is_debug()
        except Exception as e:
            raise e


    def get_setting_json(self):
        try:
            f = open(self.json_filename, encoding='utf-8-sig')
            self.setting_json = json.loads(f.read())
            f.close()
            return self.setting_json
        except Exception as e:
            raise e

    def get_out_path(self):
        try:
            file = open(self.json_filename, encoding='utf-8-sig')
            data = json.loads(file.read())
            file.close()
            if AppConfig.OUT_PATH_KEY in data.keys():
                return data[AppConfig.OUT_PATH_KEY]
            else:
                data[AppConfig.OUT_PATH_KEY] = self.default_out_path
                with open(self.json_filename, "w") as jsonFile:
                    json.dump(data, jsonFile)
                self.get_out_path()
        except FileNotFoundError:
            empty_data = {}
            with open(self.json_filename, "w") as jsonFile:
                json.dump(empty_data, jsonFile)
            self.get_out_path()
        except Exception as e:
            raise e

    def update_out_path(self, out_path):
        try:
            data = self.get_setting_json()
            data[AppConfig.OUT_PATH_KEY] = out_path
            with open(self.json_filename, "w") as jsonFile:
                json.dump(data, jsonFile)
        except Exception as e:
            raise e

    def get_font_margin(self):
        try:
            data = self.get_setting_json()
            if AppConfig.FONT_MARGIN_KEY in data.keys():
                return data[AppConfig.FONT_MARGIN_KEY]
            else:
                data[AppConfig.FONT_MARGIN_KEY] = self.default_font_margin
                with open(self.json_filename, "w") as jsonFile:
                    json.dump(data, jsonFile)
                self.get_font_margin()
        except Exception as e:
            raise e

    def get_log_delete_interval(self): #in days
        try:
            data = self.get_setting_json()
            if AppConfig.DELETE_LOG_INTERVAL_KEY in data.keys():
                return data[AppConfig.DELETE_LOG_INTERVAL_KEY]
            else:
                data[AppConfig.DELETE_LOG_INTERVAL_KEY] = self.default_log_delete_interval
                with open(self.json_filename, "w") as jsonFile:
                    json.dump(data, jsonFile)
                self.get_log_delete_interval()
        except FileNotFoundError:
            default_data = {}
            default_data[AppConfig.DELETE_LOG_INTERVAL_KEY] = self.default_log_delete_interval
            with open(self.json_filename, "w") as jsonFile:
                json.dump(default_data, jsonFile)
            self.get_log_delete_interval()

        except Exception as e:
            raise e
