import os
import json
import appdirs


class Settings:
    def __init__(self, common):
        self.common = common
        self.settings_filename = os.path.join(self.common.appdata_path, "settings.json")

        if len(self.common.pdf_viewers) == 0:
            default_pdf_viewer = None
        else:
            default_pdf_viewer = list(self.common.pdf_viewers)[0]

        self.default_settings = {
            "save": True,
            "ocr": True,
            "ocr_language": "English",
            "open": True,
            "open_app": default_pdf_viewer,
            "update_container": True,
        }

        self.load()

    def get(self, key):
        return self.settings[key]

    def set(self, key, val):
        self.settings[key] = val

    def load(self):
        if os.path.isfile(self.settings_filename):
            # If the settings file exists, load it
            try:
                with open(self.settings_filename, "r") as settings_file:
                    self.settings = json.load(settings_file)

                # If it's missing any fields, add them from the default settings
                for key in self.default_settings:
                    if key not in self.settings:
                        self.settings[key] = self.default_settings[key]

            except:
                print("Error loading settings, falling back to default")
                self.settings = self.default_settings

        else:
            # Save with default settings
            print("Settings file doesn't exist, starting with default")
            self.settings = self.default_settings

        self.save()

    def save(self):
        os.makedirs(self.common.appdata_path, exist_ok=True)
        with open(self.settings_filename, "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)
