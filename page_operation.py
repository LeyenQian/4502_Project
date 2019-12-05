
import json
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
from hashlib import sha256



class PortalPage(BasePage):
    """index page of the target web site"""

    def __init__(self, target_path : str, target_url : str = '', remote_hub_addr = None, remote_hub_enable = False):
        self.profile_socks_vers : str = ''
        self.profile_socks_addr : str = ''
        self.profile_socks_port : str = ''

        # load profile
        self.target_path = target_path
        self.loadProfile(self.target_path + '\\DB_Ua.ini', self.target_path + '\\DB_Sock.ini')
        self.target_url = target_url

        self.open_explore(target_url, 
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


    def retrieveInboundLinks(self, title_class_name: str = '', title_id_name: str = '', title_url_feature: str = '', title_text_tag: str = ''):

        # retrieve all <a> web elements
        links = self.web_driver.find_elements_by_tag_name('a')
        self.inbound_links.clear()

        # only keep web elements with inbound link & text content
        for link in links:

            try:
                key : str = ''
                href : str = link.get_attribute('href')

                if title_text_tag != '':
                    titles = link.find_elements_by_tag_name(title_text_tag)
                    for title in titles:
                        key = title.get_attribute('textContent')
                        break
                else:
                    key = link.get_attribute('textContent')

                # only keep content with desired class name or id
                if title_class_name != '' and link.get_attribute('class') != title_class_name:
                    continue
                elif title_id_name != '' and link.get_attribute('id') != title_id_name:
                    continue

                location = link.location
            except im_selexc.StaleElementReferenceException:
                continue
            
            if key == None or href == None: continue
            if len(key) == 0 or len(href) == 0: continue
            if key.isspace() or href.isspace(): continue

            # if title_url_feature == '' and href.startswith(self.target_url) == False:
            #     continue

            # elif title_url_feature != '' and href.startswith(title_url_feature) == False:
            #     continue
            
            if title_url_feature == '' and not (self.target_url in href):
                continue

            elif title_url_feature != '' and not (title_url_feature in href):
                continue

            key = key.strip()
            key = _re.sub('[\r\n\t\xa0]', '', key)
            self.inbound_links[key] = [href, link, location]

        return (len(self.inbound_links) != 0)


    def loadProfile(self, ua_from_path : str, socks_from_path : str):
        # call outside function
        handle = im_win32process.CreateProcess(self.target_path + '\\DB_Ua.exe', '', None, None, 0, im_win32process.CREATE_NO_WINDOW, None, None, im_win32process.STARTUPINFO())
        im_win32event.WaitForSingleObject(handle[0], -1)
        
        with open(ua_from_path, 'r', encoding = 'utf-8') as ifs:
            content : List[str] = ifs.readline().split('|', 7)
            self.profile_ua = content[6]
            self.profile_dpi : List[str] = content[1].split('*')

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

            # switch back to the new tab
            self.web_driver.switch_to.window(new_tab)


    def setFeaturesBBC(self, title_class_name: str, title_url_feature: str, title_text_tag: str, link_article_tag: str):
        self.BBC_title_class_name: str = title_class_name
        self.BBC_title_url_feature: str = title_url_feature
        self.BBC_title_text_tag: str = title_text_tag
        self.BBC_link_article_tag: str = link_article_tag


    def retrieveBBCArticle(self, link: str) -> str:

        self.web_driver.get(link)
        
        try:
            article_ele = self.web_driver.find_element_by_class_name(self.BBC_link_article_tag)
        except im_selexc.NoSuchElementException:
            return ''
        
        para_eles = article_ele.find_elements_by_tag_name('p')
        article: str = ''
        for item in para_eles:
            try:
                article += item.get_attribute('textContent')
            except im_selexc.StaleElementReferenceException:
                continue


        return article
        

    def collectBBC(self, result_path: str):

        # create result path, if the path doesn't exist
        if not im_os.path.exists(result_path):
            im_os.makedirs(result_path)

        self.retrieveInboundLinks(title_class_name = self.BBC_title_class_name, title_url_feature = self.BBC_title_url_feature, title_text_tag = self.BBC_title_text_tag)

        for key, value in self.inbound_links.items():
            link_info: bytes = (key + value[0]).rstrip().encode()
            link_hash: str = sha256(link_info).hexdigest()
            file_path: str = result_path + '\\' + link_hash + '.json'
            
            # skip duplicated content
            if im_os.path.isfile(file_path): continue

            # open link for article retrieving
            article: str = self.retrieveBBCArticle(value[0])
            if article == '': continue

            with open(file_path, 'w') as ifs:
                data: dict = {'Title': key, 'Link': value[0], 'Article': article}
                json.dump(data, ifs)


    def setFeaturesCNN(self, title_class_name: str, title_url_feature: str, title_text_tag: str, link_article_tag: str):
        self.CNN_title_class_name: str = title_class_name
        self.CNN_title_url_feature: str = title_url_feature
        self.CNN_title_text_tag: str = title_text_tag
        self.CNN_link_article_tag: str = link_article_tag

 
    def retrieveCNNArticle(self, link: str) -> str:

        self.web_driver.get(link)
        
        try:
            article_ele = self.web_driver.find_element_by_class_name(self.CNN_link_article_tag)
        except im_selexc.NoSuchElementException:
            return ''
        
        para_eles = article_ele.find_elements_by_class_name('zn-body__paragraph')
        if(len(para_eles) == 0):
            para_eles = article_ele.find_elements_by_xpath("//div[contains(@class, 'zn-body__paragraph')]")

        article: str = ''
        for item in para_eles:
            try:
                article += item.get_attribute('textContent')
            except im_selexc.StaleElementReferenceException:
                continue

        return article


    def collectCNN(self, result_path: str):

        # create result path, if the path doesn't exist
        if not im_os.path.exists(result_path):
            im_os.makedirs(result_path)

        self.retrieveInboundLinks(title_class_name = self.CNN_title_class_name, title_url_feature = self.CNN_title_url_feature, title_text_tag = self.CNN_title_text_tag)

        for key, value in self.inbound_links.items():
            link_info: bytes = (key + value[0]).rstrip().encode()
            link_hash: str = sha256(link_info).hexdigest()
            file_path: str = result_path + '\\' + link_hash + '.json'
            
            # skip duplicated content
            if im_os.path.isfile(file_path): continue

            # open link for article retrieving
            article: str = self.retrieveCNNArticle(value[0])
            if article == '': continue

            with open(file_path, 'w') as ifs:
                data: dict = {'Title': key, 'Link': value[0], 'Article': article}
                json.dump(data, ifs)


    def setFeaturesABC(self, title_class_name: str, title_url_feature: str, title_text_tag: str, link_article_tag: str):
        self.ABC_title_class_name: str = title_class_name
        self.ABC_title_url_feature: str = title_url_feature
        self.ABC_title_text_tag: str = title_text_tag
        self.ABC_link_article_tag: str = link_article_tag


    def retrieveABCArticle(self, link: str) -> str:
        # self.web_driver.execute_script('window.open('');')
        # self.web_driver.switch_to.window(self.web_driver.window_handles[1])
        self.web_driver.get(link)
        
        try:
            article_ele = self.web_driver.find_element_by_class_name(self.ABC_link_article_tag)
        except im_selexc.NoSuchElementException:
            try:
                article_ele = self.web_driver.find_element_by_tag_name('article')
            except im_selexc.NoSuchElementException:
                return ''
        
        para_eles = article_ele.find_elements_by_tag_name('p')
        article: str = ''
        for item in para_eles:
            try:
                article += item.get_attribute('textContent')
            except im_selexc.StaleElementReferenceException:
                continue

        # self.web_driver.close()
        # self.web_driver.switch_to.window(self.web_driver.window_handles[0])

        return article


    def collectABC(self, result_path: str):

        # create result path, if the path doesn't exist
        if not im_os.path.exists(result_path):
            im_os.makedirs(result_path)

        self.retrieveInboundLinks(title_class_name = self.ABC_title_class_name, title_url_feature = self.ABC_title_url_feature, title_text_tag = self.ABC_title_text_tag)

        for key, value in self.inbound_links.items():
            link_info: bytes = (key + value[0]).rstrip().encode()
            link_hash: str = sha256(link_info).hexdigest()
            file_path: str = result_path + '\\' + link_hash + '.json'

            # skip duplicated content
            if im_os.path.isfile(file_path): continue

            # open link for article retrieving
            article: str = self.retrieveABCArticle(value[0])
            if article == '': continue

            with open(file_path, 'w') as ifs:
                data: dict = {'Title': key, 'Link': value[0], 'Article': article}
                json.dump(data, ifs)