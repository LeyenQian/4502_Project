

import re as _re
import os as im_os
import time as _time
import random as _random
import win32api as im_win32
import win32process as im_win32process
import win32event as im_win32event
from base_page import BasePage
from base_page import im_selexc
from config_manager import ConfigManager
import shutil as im_shutil
from typing import List



class PortalPage(BasePage):
    """index page of the target web site"""

    def __init__(self, target_path : str, target_url : str = '', remote_hub_addr = None, remote_hub_enable = False):
        self.profile_socks_vers : str = ''
        self.profile_socks_addr : str = ''
        self.profile_socks_port : str = ''

        # load profile
        self.target_path = target_path
        self.loadProfile(self.target_path + '\\DB_Ua.ini', self.target_path + '\\DB_Target_URL.ini', self.target_path + '\\DB_Sock.ini')
        self.target_url : str = self.profile_url

        self.open_explore(self.profile_url, 
                         remote_hub_addr, 
                         remote_hub_enable,
                         self.profile_socks_vers,
                         self.profile_socks_addr,
                         self.profile_socks_port,
                         user_agent = self.profile_ua,
                         win_width = int(self.profile_dpi[1]),
                         win_height = int(self.profile_dpi[0]))

        self.inbound_links : dict = {}
        return


    def retrieveInboundLinks(self):
        
        # switch to default iframe
        #self.web_driver.execute_script('document.createElement=0')
        #self.web_driver.switch_to.parent_frame()

        #ads = self.web_driver.find_elements_by_tag_name('svb')
        #self.web_driver.execute_script('arguments[0].remove()', ads)
        
        # retrieve all <a> web elements
        #self.web_driver.execute_script('window.stop();')
        links = self.web_driver.find_elements_by_tag_name('a')
        
        #links = im_WebDriverWait(self.web_driver, 10).until(im_expected_conditions.visibility_of_any_elements_located((im_By.TAG_NAME, 'a')))

        # clear current dictionary
        self.inbound_links.clear()

        # only keep web elements with inbound link & text content
        for link in links:

            try:
                key : str = link.get_attribute('textContent')
                href : str = link.get_attribute('href')
                location = link.location
            except im_selexc.StaleElementReferenceException:
                #print('StaleElementReferenceException !!!')
                continue
            
            if key == None or href == None: continue
            if len(key) == 0 or len(href) == 0: continue
            if key.isspace() or href.isspace(): continue
            if href.startswith(self.target_url) == False: continue
            
            key = key.strip()
            key = _re.sub('[\r\n\t\xa0]', '', key)
            self.inbound_links[key] = [href, link, location]

        return (len(self.inbound_links) != 0)


    def loadProfile(self, ua_from_path : str, url_from_path : str, socks_from_path : str):
        # call outside function
        handle = im_win32process.CreateProcess(self.target_path + '\\DB_Ua.exe', '', None, None, 0, im_win32process.CREATE_NO_WINDOW, None, None, im_win32process.STARTUPINFO())
        im_win32event.WaitForSingleObject(handle[0], -1)
        
        with open(ua_from_path, 'r', encoding = 'utf-8') as ifs:
            content : List[str] = ifs.readline().split('|', 7)
            self.profile_ua = content[6]
            self.profile_dpi : List[str] = content[1].split('*')

        with open(url_from_path, 'r', encoding = 'utf-8') as ifs:
            self.profile_url = ifs.readline()

        if not im_os.path.exists(socks_from_path): return
        with open(socks_from_path, 'r', encoding = 'utf-8') as ifs:
            content = ifs.readline()
            if content == '': return

            socksInfo : List[str] = content.split(':', 3)
            self.profile_socks_vers = socksInfo[0]
            self.profile_socks_addr = socksInfo[1]
            self.profile_socks_port = socksInfo[2]


    def switchNewTab(self):
        tab_handles : list = self.web_driver.window_handles
        if len(tab_handles) > 1:
            self.web_driver.switch_to.window[-1]


    def closeOutdatedTabs(self):
        '''only keep the new tab'''

        tab_handles : list = self.web_driver.window_handles
        if len(tab_handles) > 1:
            # save the handle of the new tab
            new_tab = tab_handles[-1]
            for tab in tab_handles:
                # switch to the tab and close it
                self.web_driver.switch_to.window(tab)
                if tab != new_tab: 
                    self.web_driver.close()
                    #print('old tab closed')
            # switch back to the new tab
            self.web_driver.switch_to.window(new_tab)


    def collectBBC(self, result_path: str):
        pass


    def collectCNN(self, result_path: str):
        pass


    def collectRT(self, result_path: str):
        pass