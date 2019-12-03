import os as im_os
import time as im_time
import unittest as im_unittest
import shutil as im_shutil
import random as im_rand
import page_operation as im_pg_opr

from enum import Enum
from config_manager import ConfigManager
from selenium.common import exceptions as im_selexc
from typing import List

class SitesCode(Enum):
    BBC: int = 0x0
    CNN: int = 0x1
    RT: int = 0x2
    DEFAULT: int = 0xff


def removeFolder(path : str):
    for file_name in im_os.listdir(path):
        full_path = im_os.path.join(path, file_name)

        if im_os.path.isfile(full_path):
            im_os.remove(full_path)
        else:
            removeFolder(full_path)

    im_os.removedirs(path)
    return


def automation(sites_code: int = SitesCode.DEFAULT.value, result_path: str = ""):
    if sites_code == SitesCode.DEFAULT.value:
        return

    if result_path == "":
        return

    # prepare config file environment
    full_name = im_os.path.basename(__file__)
    shor_name = im_os.path.splitext(full_name)[0]
    shor_name += '_'
    shor_name += str(im_os.getpid())

    #time stamp
    shor_name += '_'
    shor_name += str(int(round(im_time.time() * 1000)))

    dir_path = '.\\' + shor_name
    if not im_os.path.exists(dir_path): im_os.makedirs(dir_path)

    im_shutil.copy('.\\Tools\\DB_Ua.exe', dir_path + '\\DB_Ua.exe')
    im_shutil.copy('.\\Tools\\DB_Sock.ini', dir_path + '\\DB_Sock.ini')
    im_shutil.copy('.\\Tools\\DB_Target_URL.ini', dir_path + '\\DB_Target_URL.ini')
    im_shutil.copytree('.\\Tools\\Ua', dir_path + '\\Ua')

    portal_page = im_pg_opr.PortalPage(target_path = '.\\' + shor_name)
    

    if sites_code == SitesCode.BBC.value:
        portal_page.collectBBC(result_path)
    elif sites_code == SitesCode.CNN.value:
        portal_page.collectCNN(result_path)
    elif sites_code == SitesCode.RT.value:
        portal_page.collectRT(result_path)
    else:
        removeFolder(dir_path)

    portal_page.web_driver.quit()


if __name__ == '__main__':
        automation(SitesCode.BBC.value)
