import os
import platform
class Mounter():
    def __init__(self):
        pass
    
    def check_os(self)->bool:
        return platform.system() == 'Darwin'

