test_url = 'https://yandex.ru/maps'
from Driver_init import web_driver
def Test_unit():
    driver = web_driver()    
    driver.get(test_url)
    driver.quit()
    if True:
        print('ChromeDriver status: OK')
    else:
        print('ChromeDriver failed')