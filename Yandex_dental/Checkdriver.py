import os
from Driver_init import *
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.core.utils import ChromeType 

check_path = '~/.wdm/drivers/chromedriver/win32/'
chromedriver_version = '114.0.5735.90'



def Check_driver():
    
    boolpath = os.path.expanduser(check_path)
    isExist = os.path.exists(boolpath)
    
    if isExist == True:
        pass
        
    else:
        print('Installing ChromeDriver...')
        chromeinstaller_service = ChromeDriverManager(version = chromedriver_version).install()
        webdriver.Chrome(chromeinstaller_service)
        print('ChromeDriver successfully installed.')
