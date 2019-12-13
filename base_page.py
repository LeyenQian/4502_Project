import traceback
import time as _time
import os as _os

from selenium import webdriver as im_webdriver
from selenium.webdriver import ActionChains as im_ActionChains
from selenium.webdriver.common.touch_actions import TouchActions as im_TouchAction
from selenium.webdriver.common.keys import Keys as im_Keys
from selenium.webdriver.common.by import By as im_By
from selenium.webdriver.support import expected_conditions as im_expected_conditions
from selenium.webdriver.support.ui import WebDriverWait as im_WebDriverWait
from selenium.common import exceptions as im_selexc
from typing import List


class BasePage:
    """Fundamental functions for all page object"""

    def open_explore(self, search_engine_url, remote_hub_addr = None, remote_hub_enable = False, sock_vers : str = '', sock_addr : str = '', sock_port : str = '', user_agent : str = '', win_width : int = 0, win_height : int = 0):
        """
	    fundemantal function to open the explorer locally or remotely and used to initial web driver in other page classes

        :args:
         - remote_hub_addr: the IP address of selenium hub server
         - search_engine_url: the url of search engine
         - remote_hub_enable: flag of whether use remote hub server
         - explorer_type: flag that decide to run which type of explorer, firefox is the default explorer

        :return:
         - Home page object
        """

        # value must be assigned in subclass
        self.target_path = ""

        self.search_engine_url = search_engine_url
        desired_caps = im_webdriver.DesiredCapabilities.CHROME.copy()

        # initial the user agent header of the select explorer
        my_chrome_option = im_webdriver.ChromeOptions()
        if user_agent != '': my_chrome_option.add_argument('user-agent=' + user_agent)
        my_chrome_option.add_argument('--incognito')
        my_chrome_option.add_argument('--disable-infobars')
        my_chrome_option.add_argument('--disable-plugins')
        my_chrome_option.add_argument('--hide-scrollbars')
        my_chrome_option.add_argument('--ignore-certificate-errors')

        fullPath = _os.path.abspath(self.target_path)
        my_chrome_option.add_argument('--disk-cache-dir=' + fullPath)
        my_chrome_option.binary_location = 'C:\\chrome\\chrome.exe'
        my_chrome_option.add_experimental_option('prefs', {"profile.managed_default_content_settings.images":2})

        if sock_vers != '' and sock_addr != '' and sock_port != '':
            my_chrome_option.add_argument('--proxy-server=socks' + sock_vers + '://' + sock_addr + ':' + sock_port)
        
        # set user agent information
        if user_agent == '': 
            user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'

        # set mobile emulation profile for Chrome
        if win_width != 0 and win_height != 0:

            pixelRatio : float = 1
            pixelRatio = win_width / 320.0

            win_height = (int)(win_height / pixelRatio)
            win_width = (int)(win_width / pixelRatio)

            mobileEmulation = {"deviceMetrics": {"width": win_width, "height": win_height, "pixelRatio": pixelRatio}, "userAgent": user_agent}
            my_chrome_option.add_experimental_option('mobileEmulation', mobileEmulation)
        else:
            my_chrome_option.add_experimental_option('mobileEmulation', {'deviceName' : 'Nexus 5'})

        self.web_driver = im_webdriver.Chrome(\
            executable_path = '.\\Tools\\Chrome_Driver\\chromedriver.exe', \
            desired_capabilities = desired_caps, \
            options = my_chrome_option)

        self.web_driver.set_window_size(win_width, win_height + 124)
        self.web_driver.get(search_engine_url)
        self.wait_dom(self.web_driver)
        
        return


    def close_explore(self):
        self.web_driver.quit()


    def move_mouse(self, web_driver, to_element = None, to_location = None, is_clickable = False):
        """
        Move mouse to an element or a specific location

        :args:
         - to_element: move mouse to an element
         - to_location: a screen coordinate based on the current mouse location
           a set with x and y value
         - is_clickable: click the element if it's True
        """
        try:
            if to_element != None:
                #location = to_element.location
                #im_ActionChains(web_driver).move_by_offset(location[0], location[1]).perform()
                im_ActionChains(web_driver).move_to_element(to_element).perform()
                
            elif to_location != None:
                im_ActionChains(web_driver).move_by_offset(to_location[0], to_location[1]).perform()

            if is_clickable == True:
                touchAction = im_TouchAction(web_driver)
                touchAction.tap(to_element)
                touchAction.perform()

        except im_selexc.ElementClickInterceptedException:
            self.web_driver.execute_script('arguments[0].click();', to_element)

        except im_selexc.WebDriverException:
            self.web_driver.execute_script('window.location.href="' + to_element.get_attribute('href') + '";')

        except Exception:
            return False

        return True


    def scroll_page_new(self, mode):
        page = self.web_driver.find_element_by_tag_name('html')
        if mode:
            page.send_keys(im_Keys.END)
        else:
            page.send_keys(im_Keys.HOME)


    def scroll_page_touch_offset(self, offX, offY) -> bool:

        actionTouch = im_TouchAction(self.web_driver)

        actionTouch.scroll(offX, offY)
        actionTouch.perform()
        
        return True


    def scroll_page_touch_track(self, stX : int, stY : int, enX : int, enY : int, duration : int = 0) -> bool:

        actionTouch = im_TouchAction(self.web_driver)

        actionTouch.tap_and_hold(stX, stY)
        actionTouch.move(enX, enY)
        actionTouch.release(enX, enY)

        try:
            actionTouch.perform()
        except im_selexc.WebDriverException:
            ifsObj = open(self.target_path + '\\touchError.log', 'a+')
            ifsObj.write('Move from: [ ' + str(stX) + ' : ' + str(stY) + ' ] --> [ ' + str(enX) + ' : ' + str(enY) + ' ]')
            ifsObj.flush()
            ifsObj.close()
            return False

        return True


    def locate_element(self, web_driver, by_id = None, by_xpath = None, check_visibility = False, check_clickable = False):
        """
        retrieve element objects by given id or xpath

        :args:
         - web_driver: selenium page object
         - by_id: the HTML id tag
         - by_xpath: the path expression used to represent the position of element(s)

        :return:
         - element object
        """

        element_object = None

        if by_id != None:
            if check_visibility == True:
                element_object = im_WebDriverWait(web_driver, 10).until(im_expected_conditions.visibility_of_element_located((im_By.ID, by_id)))

            if check_clickable == True:
                element_object = im_WebDriverWait(web_driver, 10).until(im_expected_conditions.element_to_be_clickable((im_By.ID, by_id)))

            if check_visibility == False and check_clickable == False:
                element_object = web_driver.find_element_by_id(by_id)

        elif by_xpath != None:
            if check_visibility == True:
                element_object = im_WebDriverWait(web_driver, 10).until(im_expected_conditions.visibility_of_element_located((im_By.XPATH, by_xpath)))

            if check_clickable == True:
                element_object = im_WebDriverWait(web_driver, 10).until(im_expected_conditions.element_to_be_clickable((im_By.XPATH, by_xpath)))

            if check_visibility == False and check_clickable == False:
                element_object = web_driver.find_element_by_xpath(by_xpath)

        return element_object


    def retrieve_child_elements(self, web_driver, parent_element : im_webdriver, target_identity : str, identity_type : int):
        """
        find child elements
        
        :args:
         - parent_element: parent element used to find child elements
         - target_identity: partial url of child elements
         - identity_type: type of identity
           0: href link
           1: class name

        :return:
         - child elements list
        """

        if identity_type == 0:
            child_elements = parent_element.find_elements_by_css_selector('div[class="div_t"]>a')
        return child_elements


    def page_navigate(self, web_driver, navigate_mode, by_id = None, by_xpath = None):
        """
        navigate to the next page
        the default action is using brower's record

        :args:
         - navigate_mode: 0 or 1
           0: forward action
           1: back action
         - by_id: the HTML id tag
         - by_xpath: the path expression used to represent the position of element(s)
        """

        if by_id == None and by_xpath == None:
            if navigate_mode == 0: web_driver.forward()
            if navigate_mode == 1: web_driver.back()
        
        navi_element_obj = self.locate_element(web_driver, by_id, by_xpath)
        self.move_mouse(web_driver, to_element = navi_element_obj)

        return


    def wait_dom(self, web_driver) -> None:
        while(True):
            if (web_driver.execute_script('return document.readyState') != 'loading') and\
               (web_driver.execute_script('return document.body != null;')):
               break

            _time.sleep(1)