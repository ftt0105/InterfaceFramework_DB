from configparser import ConfigParser

class ConfigParse(object):
    def __init__(self):
        pass

    @classmethod
    #cls表示类方法
    def get_db_config(cls, configPath):
        cls.cf = ConfigParser()
        cls.cf.read(configPath)
        host = cls.cf.get("mysqlconf","host")
        port = cls.cf.get("mysqlconf","port")
        user = cls.cf.get("mysqlconf","user")
        password = cls.cf.get("mysqlconf","password")
        db = cls.cf.get("mysqlconf","db_name")
        return {"host":host, "port":port, "user":user, "password":password, "db":db}

if __name__ == "__main__":
    from config.public_data import config_path
    res = ConfigParse.get_db_config(config_path)
    print(res)