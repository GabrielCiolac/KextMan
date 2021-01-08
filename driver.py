from mount_parition import Mounter
from plist_parser import Plist


plist = Plist('config.plist')

print(plist.get_kext_list())