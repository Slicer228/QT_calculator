from bs4 import BeautifulSoup as Bs


class ConfigEngine(Bs):
    def __init__(self, file):
        super().__init__(open(file, 'r').read(), 'xml')


app_config = ConfigEngine('config/app_configuration.xml')
ui_declaration = ConfigEngine('config/ui_declaration.xml')
