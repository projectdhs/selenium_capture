import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, cv2
from datetime import timezone, timedelta, datetime

height_setting=8000 #전체 화면 캡쳐시 높이가 이 이상이면 분할 캡쳐됨

def do_screen_capturing(url, screen_path, width, height):
    print("Capturing screen..")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--hide-scrollbars")
    options.add_argument("disable-gpu") 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=ko_KR") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)

    driver.set_window_size(width, height)

    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    driver.set_script_timeout(30)

    driver.get(url)


    WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, 'div')))
    time.sleep(2)
    driver.save_screenshot(screen_path+'.png')
    driver.quit()

def do_full_screen_capturing(url, screen_path):
    print("Capturing screen..")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu") 
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,8000")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--lang=ko_KR")
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    

    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    driver.set_script_timeout(30)

    driver.get(url)
    WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located(
        (By.TAG_NAME, 'div')))
    time.sleep(2)
    height = driver.execute_script("return document.body.scrollHeight")
    
    if(height<=height_setting):
        
        print("작은 사이트")
        driver.set_window_size(1920, height+100)
        driver.save_screenshot(screen_path+'.png')
        driver.quit()

    else:
        print("큰 사이트")
        os.makedirs(screen_path)

        driver.set_window_size(1920, height_setting)

        temp_height=0
        rectangles = []

        t1=[]
        while temp_height < height:
            if(temp_height==0):
                plus=0
            else:
                plus=50
            if(temp_height+height_setting>height):
                set_height=height
                t1=[set_height,temp_height-plus]
            else:
                set_height=temp_height+height_setting
            print("Appending rectangle ({0},{1},{2},{3})".format(0, temp_height-plus, 1920, set_height))
            rectangles.append((0, temp_height-plus, 1920, set_height))
            
            temp_height+=height_setting

        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))
            part+=1
            previous = rectangle

            driver.get_screenshot_as_file(screen_path+'/'+file_name)

        driver.quit()

        img = cv2.imread(screen_path+'/'+file_name) 
        cropped_img = img[8000-(t1[0]-t1[1])-50:9000, 0:1920]
        cv2.imwrite('%s/%s'%(screen_path,file_name),cropped_img)

def get_screenshot(**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 1024)) 
    height = int(kwargs.get('height', 768))
    filename = kwargs.get('filename', 'screen.png')
    do_screen_capturing(url, filename, width, height)

def get_full_screenshot(**kwargs):
    url = kwargs['url']
    filename = kwargs.get('filename', 'screen.png')
    do_full_screen_capturing(url, filename)

if __name__ == '__main__':
    timestamp=time.time()
    tz = timezone(timedelta(hours=9))
    dt_9 = datetime.fromtimestamp(timestamp, tz)

    year=dt_9.year
    month="{:%m}".format(dt_9)
    day="{:%d}".format(dt_9)
    hour="{:%H}".format(dt_9)
    min="{:%M}".format(dt_9)
    sec="{:%S}".format(dt_9)

#캡쳐할 웹 url
    url = 'https://daum.net'

    try:
#지정 사이즈 캡쳐시
        # get_screenshot(
        # url=url, filename='capture_%s-%s-%s-%s_%s_%s'%(year,month,day,hour,min,sec),
        # width=1920, height=1080
        # )

#전체 페이지 캡쳐시
        get_full_screenshot(
            url=url, filename='capture_%s-%s-%s_%s_%s_%s'%(year,month,day,hour,min,sec),
        )

        print("캡쳐성공")
        os.system('killall chromedriver')
        os.system('pkill chromium')
        os.system('pkill chrome')
    except KeyboardInterrupt:
        print('중지')
        os.system('killall chromedriver')
        os.system('pkill chromium')
        os.system('pkill chrome')