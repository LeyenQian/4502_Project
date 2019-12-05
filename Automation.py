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
    ABC: int = 0x2
    DEFAULT: int = 0xff

class CategoryCode(Enum):
    US_CA: int = 0x0
    Business: int = 0x1
    Politics: int = 0x2


def removeFolder(path : str):
    for file_name in im_os.listdir(path):
        full_path = im_os.path.join(path, file_name)

        if im_os.path.isfile(full_path):
            im_os.remove(full_path)
        else:
            removeFolder(full_path)

    im_os.removedirs(path)
    return


def automation(sites_code: int = SitesCode.DEFAULT.value, category_code: int = CategoryCode.US_CA.value, result_path: str = '', site_url: str = ''):
    if sites_code == SitesCode.DEFAULT.value:
        return

    if result_path == '' or site_url == '':
        return

    # prepare config file environment
    full_name = im_os.path.basename(__file__)
    shor_name = im_os.path.splitext(full_name)[0] + '_' + str(im_os.getpid()) + str(int(round(im_time.time() * 1000)))
    dir_path = '.\\' + shor_name

    if not im_os.path.exists(dir_path): im_os.makedirs(dir_path)
    im_shutil.copy('.\\Tools\\DB_Ua.exe', dir_path + '\\DB_Ua.exe')
    im_shutil.copy('.\\Tools\\DB_Sock.ini', dir_path + '\\DB_Sock.ini')
    im_shutil.copytree('.\\Tools\\Ua', dir_path + '\\Ua')

    portal_page = im_pg_opr.PortalPage(target_path = '.\\' + shor_name, target_url = site_url)
    
    if sites_code == SitesCode.BBC.value:
        if category_code == CategoryCode.US_CA.value:
            # BBC US & Canada
            portal_page.setFeaturesBBC(title_class_name = 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor', title_url_feature = 'https://www.bbc.com/news/world-us-canada', title_text_tag = 'h3', link_article_tag = 'story-body__inner')
            portal_page.collectBBC(result_path)

        elif category_code == CategoryCode.Business.value:
            # BBC Business
            portal_page.setFeaturesBBC(title_class_name = 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor', title_url_feature = 'https://www.bbc.com/news/business', title_text_tag = 'h3', link_article_tag = 'story-body__inner')
            portal_page.collectBBC(result_path)

        elif category_code == CategoryCode.Politics.value:
            # BBC Politics
            portal_page.setFeaturesBBC(title_class_name = 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor', title_url_feature = 'https://www.bbc.com/news', title_text_tag = 'h3', link_article_tag = 'story-body__inner')
            portal_page.collectBBC(result_path)

    elif sites_code == SitesCode.CNN.value:
        if category_code == CategoryCode.US_CA.value:
            # CNN US
            portal_page.setFeaturesCNN(title_class_name = '', title_url_feature = '/us/', title_text_tag = 'span', link_article_tag = 'l-container')
            portal_page.collectCNN(result_path)

        elif category_code == CategoryCode.Business.value:
            # CNN Business
            portal_page.setFeaturesCNN(title_class_name = '', title_url_feature = '/business/', title_text_tag = 'span', link_article_tag = 'l-container')
            portal_page.collectCNN(result_path)

        elif category_code == CategoryCode.Politics.value:
            # CNN Politics
            portal_page.setFeaturesCNN(title_class_name = '', title_url_feature = '/politics/', title_text_tag = 'span', link_article_tag = 'l-container')
            portal_page.collectCNN(result_path)

    elif sites_code == SitesCode.ABC.value:
        if category_code == CategoryCode.US_CA.value:
            # ABC US
            portal_page.setFeaturesABC(title_class_name = 'black-ln', title_url_feature = 'https://abcnews.go.com/US', title_text_tag = '', link_article_tag = 'article-copy')
            portal_page.collectABC(result_path)

        elif category_code == CategoryCode.Business.value:
            # ABC Business
            portal_page.setFeaturesABC(title_class_name = 'black-ln', title_url_feature = 'https://abcnews.go.com/Business', title_text_tag = '', link_article_tag = 'article-copy')
            portal_page.collectABC(result_path)

        elif category_code == CategoryCode.Politics.value:
            # ABC Politics
            portal_page.setFeaturesABC(title_class_name = 'black-ln', title_url_feature = 'https://abcnews.go.com/Politics', title_text_tag = '', link_article_tag = 'article-copy')
            portal_page.collectABC(result_path)

    else:
        removeFolder(dir_path)

    portal_page.web_driver.quit()


if __name__ == '__main__':
    bbc_result_paths: List[str] = ['.\\result\\BBC\\US_and_canada\\', '.\\result\\BBC\\Business\\', '.\\result\\BBC\\Politics\\']
    bbc_target_links: List[str] = ['https://www.bbc.com/news/world/us_and_canada', 'https://www.bbc.com/news/business', 'https://www.bbc.com/news/politics']

    automation(SitesCode.BBC.value, CategoryCode.US_CA.value, bbc_result_paths[0], bbc_target_links[0])
    automation(SitesCode.BBC.value, CategoryCode.Business.value, bbc_result_paths[1], bbc_target_links[1])
    automation(SitesCode.BBC.value, CategoryCode.Politics.value, bbc_result_paths[2], bbc_target_links[2])



    cnn_result_paths: List[str] = ['.\\result\\CNN\\US\\', '.\\result\\CNN\\Business\\', '.\\result\\CNN\\Politics\\']
    cnn_target_links: List[str] = ['https://www.cnn.com/us', 'https://www.cnn.com/business', 'https://www.cnn.com/politics']

    automation(SitesCode.CNN.value, CategoryCode.US_CA.value, cnn_result_paths[0], cnn_target_links[0])
    automation(SitesCode.CNN.value, CategoryCode.Business.value, cnn_result_paths[1], cnn_target_links[1])
    automation(SitesCode.CNN.value, CategoryCode.Politics.value, cnn_result_paths[2], cnn_target_links[2])



    abc_result_paths: List[str] = ['.\\result\\ABC\\US\\', '.\\result\\ABC\\Business\\', '.\\result\\ABC\\Politics\\']
    abc_target_links: List[str] = ['https://abcnews.go.com/US', 'https://abcnews.go.com/Business', 'https://abcnews.go.com/Politics']

    automation(SitesCode.ABC.value, CategoryCode.US_CA.value, abc_result_paths[0], abc_target_links[0])
    automation(SitesCode.ABC.value, CategoryCode.Business.value, abc_result_paths[1], abc_target_links[1])
    automation(SitesCode.ABC.value, CategoryCode.Politics.value, abc_result_paths[2], abc_target_links[2])