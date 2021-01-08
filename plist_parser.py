import plistlib

class Plist():
    def __init__(self,path):
        self.__import_plist(path)


    def __import_plist(self,path):
        with open(path,'rb') as file:
            self.__plist = plistlib.load(file)
    
    def __export_plist(self,path):
        with open(path,'wb') as file:
            plistlib.dump(self.__plist,file)

    '''
        adds a kext
    '''
    def add_kext(self,kext_name):
        pass
    '''
        removes a kext
    '''
    def remove_kext(self,kext_num):
        del self.__plist['Kernal']['Add'][kext_num]

    '''
        gets a list of kexts
    '''
    def get_kext_list(self):
        li = []
        for i in self.__plist['Kernel']['Add']:
            li.append(i['BundlePath'])
        return li


        
