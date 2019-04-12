#-*- endcoding:utf-8 -*-
from public.util.config_operation import configOperation
from public.read_config.config import readConfig

section = "requests"

class readRequest(configOperation):

    def __init__(self):
        self.readConfig = readConfig()
        super(readRequest, self).__init__(self.readConfig.get_requestsPath)

    @property
    def get_url(self):
        return self.get_value(section, "url")

    @property
    def get_secretKey(self):
        return self.get_value(section, "secretKey")

    @property
    def get_token(self):
        return self.get_value(section, "token")



if __name__ == "__main__":
    con = configOperation()
