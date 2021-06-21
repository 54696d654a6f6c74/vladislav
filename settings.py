from json import dumps, load
from os.path import isfile


# By default I should also exlcude the output_dir
# while walking and searching for .vlad files
class Settings:
    def __init__(self):
        self.data = {
            "file_ext": "vlad",
            "output_dir": "vlad_out",
            "output_ext": "html",
            "except_dir": [],
            "except_path": [],
            "except_filename": [],
            "cfg_filename": ".vlad_settings"
        }

        cfg_path = "vlad_settings.json"

        if not isfile(cfg_path):
            with open(cfg_path, "w+") as cfg_file:
                cfg_file.write(dumps(self.data, indent = True))
        else:
            with open(cfg_path, 'r') as cfg_file:
                read = load(cfg_file)
                self.data = read


settings = Settings()
