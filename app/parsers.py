import configparser


class config:
    def getData(self, section, key):
        Config = configparser.ConfigParser()
        Config.read('./app/config.ini')
        return Config.get(section, key)
        

    def throwData(self, section, key, data):
        Config = configparser.ConfigParser()
        Config.read('./app/config.ini')
        Config.set(section, key, data)
        with open('./app/config.ini', 'w') as configfile:
            Config.write(configfile)