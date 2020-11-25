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
        parses the identifer and returns the EFI partition identifer

        1) Check to see if disk is APFS
        2) If it is APFS partition get the phsyical disk number (APFS phsyical store)
        3) Use diskutil info diskn to get the partitions of the disk
        4) return diskiddentifier of EFI
    '''
    def __parse_identifier(self,raw:str)->str:
        id_list = raw.splitlines()
        disk_of_vol = None
        #goes through all the lines and grabs relevent information
        for s in id_list:
            if 'Part of Whole:' in s:
                disk_of_vol = s.split(' ')
                disk_of_vol = set(disk_of_vol) #removes repeating char
            if 'APFS Physical Store:' in s: #if it's an APFS partition rewrite
                disk_of_vol = s.split(' ')
                disk_of_vol = set(disk_of_vol)

        if disk_of_vol is None:
            return None
        
        disk_num = None
        for s in disk_of_vol: #gets disk number
            if 'disk' in s:
                disk_num = s
                break
        
        if disk_num is None:
            return None
        try: #drops the sector number if it exists
            split = disk_num.split('s') 
            disk_num = split[0] + 's' + split[1]
        except:
            pass

        raw_disk_info = os.popen('diskutil list ' + disk_num).read() #gets the disk info
        disk_info = raw_disk_info.splitlines()

        efi_data = None
        for s in disk_info:
            if 'EFI' in s:
                efi_data = set(s.split(' ')) #gets identifier for the EFI partition
                break
        if efi_data is None:
            return None
        for s in efi_data:
            if 'disk' in s:
                return s #returns disk number of the EFI partition



        return None
            


    '''
        Lists available disks, and asks user which EFI partition they'd like to mount

        If an OpenCore enviroment exists in the EFI partition that enviroment will be set as the working partition.

        A special thanks to corpnewt's MountEFI for some inspiration, corpnewt's project can be found here:
        https://github.com/corpnewt/MountEFI
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

            #insures user inputed an integer, and that integer is in the list
            try:
                sel = int(sel)
                mnt_pnt = dsk_lst[sel]
            except:
                print('Unable to find selected')
                return False

            raw_id = os.popen('diskutil info ' + mnt_pnt).read()
            parsed_id = self.__parse_identifier(raw_id)

            os.system('sudo diskutil mount '+parsed_id)


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

