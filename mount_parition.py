import os
import platform
class Mounter():
    def __init__(self):
        pass
    
    def __check_os(self)->bool:
        return platform.system() == 'Darwin'

    def __mount_efi(self):
        pass

    def __set_OC_env(self):
        pass

    def __controller(self):
        if self.__check_os:
            self.__mount_efi()
        else:
            self.__set_OC_env()
        self.path = ''

    def get_path(self):
        return self.path

