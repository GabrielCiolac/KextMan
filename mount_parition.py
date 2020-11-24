import os
import platform
import time
'''
 Mounts EFI partition, and set Mounter path to the OpenCore enviroment on that EFI partition

 if the system is not Darwin, it allows the user to set a custom OpenCore enviroment
'''
class Mounter():
    def __init__(self):
        self.__path = None
        self.__controller()
        
    
    '''
        Checks the system to insure Darwin
    '''
    def __check_os(self)->bool:
        return platform.system() == 'Darwin'

    '''
        Lists available disks, and asks user which EFI partition they'd like to mount

        If an OpenCore enviroment exists in the EFI partition that enviroment will be set as the working partition.
    '''
    def __mount_efi(self)->bool:
        while self.__path is None:
            raw_disks = os.popen('ls /Volumes').read() #gets a list of mounted volumes
            dsk_lst = raw_disks.splitlines() #splits this list along the line breaks

            if dsk_lst is None: #if the list is empty, notify user and return
                print('No Disks Mounted')
                time.sleep(2)
                os.system('clear')
                return False
            
            for i in range(len(dsk_lst)): #print available volumes
                print(str(i) +'. '+ dsk_lst[i])
            sel = input('Enter Selection (enter nothing to return): ')

            if sel is None:
                return False
            
            

            return True

    '''
        Lists OpenCore Enviroments from KextMan/Enviroments/

        Allows user select one as the working enviroment, if none are found returns False
    '''
    def __set_OC_env(self):
        pass

    '''
        simply checks OS version and desides if you'll be using a custom enviroment or
        an enviroment in the EFI partition
    '''
    def __controller(self):
        if self.__check_os() and self.__mount_efi():
            return
        self.__set_OC_env()

    def get_path(self):
        return self.__path

