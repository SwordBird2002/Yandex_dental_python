import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from User_agents import *
from ProxyRand import *

driver_path = os.path.expanduser('~/.wdm/drivers/chromedriver/win32/114.0.5735.90/chromedriver.exe')
#userAgent = return_agent()
#proxy_rand = return_proxy()


def interceptor(request):
    request.headers['Accept'] = 'text/html, application/xhtml+xml'
    request.headers['accept-encoding'] = 'gzip, deflate, br'
    request.headers['content-type'] = 'text/html'

def web_driver():
    driver_service = Service(driver_path)
    driver_options = webdriver.ChromeOptions()
    #driver_options.add_argument(f'--user-agent={userAgent}')
    #driver_options.add_argument(f'--proxy-server={proxy_rand}')
    driver_options.add_argument("--verbose")
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--disable-gpu')
    driver_options.add_argument("--window-size=1920, 1200")
    driver_options.add_argument('--disable-dev-shm-usage')
    driver_options.add_argument('disable-infobars')
    driver_options.add_argument("--disable-extensions")
    driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service = driver_service, options = driver_options)
    return driver