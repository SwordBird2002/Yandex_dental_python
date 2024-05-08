#Yandex dental clinic scrapper
#pip install selenium, webdriver-manager

import sys
import unittest, time
import re
import random
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.core.utils import ChromeType 
from selenium.webdriver.chrome.service import Service as ChromeService
from Checkdriver import *
from User_agents import *
from Driver_init import *
from Test_Unit import *


yandex_url = 'https://yandex.ru'
main_url = 'https://yandex.ru/maps'
scroll_width = 70
timeout = 120
write_sleep = 1
scroller_sleep = 2
tel_instance_sleep = 3
short_sleep = 5
long_sleep = 10
city = "CITY_GOES_HERE"
newline = '\n'

#Getting a unique, updating cell ID for entering a city. 

def YM_entry(by_city):
     YM_browser = web_driver()    
     YM_browser.minimize_window()
     YM_browser.request_interceptor = interceptor
     YM_browser.get(main_url)
     YM_source = YM_browser.page_source
     YM_html_parse = BeautifulSoup(YM_source, 'html.parser')
     input_element_class = YM_html_parse.find('span', class_ = 'input__context').input
     input_element_id = input_element_class.get('id')
     print('Input id: {}'.format(input_element_id))
    
     try:
         # Direct search by city from the city value
         time.sleep(long_sleep)
         search_by_city = WebDriverWait(YM_browser, timeout).until(EC.presence_of_element_located((By.ID, input_element_id)))
         search_by_city.send_keys(by_city)
         search_by_city.send_keys(Keys.ENTER)
         time.sleep(long_sleep)
         YM_citysource = YM_browser.page_source
         page_handle = YM_browser.current_window_handle
         child_handle = YM_browser.window_handles
         # Switch to a new open tab
         for window in child_handle:
             if(window!=page_handle):
                 YM_browser.switch_to.window(window)
         # Checking the correctness of the link to the city in the search query   
         global city_url
         city_url = YM_browser.current_url 
         print(city_url)
        
     finally:  
         YM_browser.quit()
 
 

# Self-loading window caret swipe function
def scroll(browser):
    
    element = browser.find_element(By.CSS_SELECTOR, "div.scroll__scrollbar-thumb")
    stylepx_last = "transform: translate3d(0px, 0px, 0px)"
    
    while True:
        
        try:
            action = AC(browser)
            action.drag_and_drop_by_offset(element, 0, scroll_width).perform()
            time.sleep(scroller_sleep)
            stylepx_new_unsplit = element.get_attribute('style')
            stylepx_new =  stylepx_new_unsplit.split(";", 1)[0]
            time.sleep(short_sleep)
           
            if stylepx_new == stylepx_last:
                break 
         
            stylepx_last = stylepx_new       
        
        except Exception:
            break
         
   
   
# Parsing the list of organizations by city and searching for dental clinics
def YM_dental():
     YM_browser_inst_2 = web_driver()    
     YM_browser_inst_2.minimize_window()
     YM_browser_inst_2.request_interceptor = interceptor
     YM_browser_inst_2.get(city_url)
     time.sleep(long_sleep)
     global city_page_source
     city_page_source = YM_browser_inst_2.page_source
     time.sleep(long_sleep)    
     all_items_soup = BeautifulSoup(city_page_source, 'html.parser')
     all_items_holder = all_items_soup.find('a', class_="catalog-entry-point")
     all_items_href = all_items_holder.get('href')
     selector = YM_browser_inst_2.get(yandex_url + all_items_href)
     time.sleep(short_sleep)
     selector_page_source = YM_browser_inst_2.page_source
     selector_class_pagesource = BeautifulSoup(selector_page_source, 'html.parser')
     selector_href = selector_class_pagesource.find('a', title="Медицина").get('href')
     dental_selector_page = YM_browser_inst_2.get(yandex_url + selector_href)
     time.sleep(short_sleep)
     dental_selector_page_source = YM_browser_inst_2.page_source
     dental_selector_soup = BeautifulSoup(dental_selector_page_source, 'html.parser')
     global  private_dental_href
     private_dental_href = dental_selector_soup.find('a', title = 'Стоматологическая клиника').get('href')
     #global public_dental_href
     #public_dental_href = dental_selector_soup.find('a', title = 'Стоматологическая поликлиника').get('href') # FOR PUBLIC CLINICS
     YM_browser_inst_2.quit()

# Browse and collect clinics
def YM_scroller():
     global YM_browser_inst_3
     YM_browser_inst_3 = web_driver()   
     #YM_browser_inst_3.minimize_window()     
     YM_browser_inst_3.request_interceptor = interceptor
     YM_browser_inst_3.get(yandex_url + private_dental_href) # REPLACE WITH public_dental_href FOR PRIVATE CLINICS
     time.sleep(short_sleep)
     scroll(YM_browser_inst_3)
     time.sleep(long_sleep)
     global dental_scrolled
     dental_scrolled = YM_browser_inst_3.page_source
     page_private_dental = BeautifulSoup(dental_scrolled, 'html.parser')
     global all_private_dental_list 
     all_private_dental_list = page_private_dental.find_all('li', class_="search-snippet-view")
     print('Collected items: {}'.format(len(all_private_dental_list)))
     YM_browser_inst_3.quit()

# Collecting phone numbers
def tel_browser_instance(link):
    global tel_instance
    tel_instance = web_driver()
    tel_instance.minimize_window()  
    tel_instance.request_interceptor = interceptor
    
    try:
        tel_instance.get(link)
        
    except Exception: 
        pass
    
# Collect title, title, and number
def dental_source_processor():
    citystr = str('{}.txt').format(city)
    with open(citystr, 'w') as file:
        for elem in all_private_dental_list:
           
            try:
                dental_href_id = elem.find('div', class_ = "search-snippet-view__body _type_business").get('data-id')
                dental_href_fixed = str('https://yandex.ru/maps/org/{}/').format(dental_href_id)
                   
                
                customer_page_driver = tel_browser_instance(dental_href_fixed)
                customer_page = tel_instance.page_source
                time.sleep(tel_instance_sleep)
                    
            except Exception:
                continue
                    
            try:   
                customer_page_soup = BeautifulSoup(customer_page, 'html.parser')
                dental_title = customer_page_soup.find('h1', class_ = "orgpage-header-view__header").text
                dental_adress = customer_page_soup.find('a', class_ = "business-contacts-view__address-link").text
            
            except Exception:
                continue
                
            try:
                phone_number = customer_page_soup.find('span', itemprop='telephone').text
  
# Write to file
                if phone_number is not None:
                
                    file.write(dental_title)
                    file.write(newline)
                    file.write(dental_adress)
                    file.write(newline)
                    file.write(phone_number)
                    file.write(newline)
                    file.write(newline)
                    print('Value recorded with phone number: {}'.format(dental_title))
                    time.sleep(write_sleep)
                    
            except Exception:
                
                file.write(dental_title)
                file.write(newline)
                file.write(dental_adress)
                file.write(newline)
                file.write(newline)
                print('Value recorded without phone number: {}'.format(dental_title))
                time.sleep(write_sleep)
                
    file.close()
    tel_instance.quit()
        
        



if __name__ == "__main__":  
    Check_driver() 
    # INSTALLS THE CHROME BROWSER DRIVER ON YOUR COMPUTER IF IT IS NOT FOUND IN THE WDM FOLDER AND CHECKS FOR ITS PRESENCE
    web_driver() 
    # Initialization
    #Test_unit()
    YM_entry(city) 
    YM_dental()
    YM_scroller()
    dental_source_processor()
