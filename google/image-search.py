import os, sys, time, argparse, pandas as pd
import urllib.request as rq
from datetime import datetime
from pyvirtualdisplay import Display
from selenium.webdriver import Chrome, ChromeOptions


def start_chrome() -> (Display, Chrome):
    # # Chrom Dirver
    CHROME_ADDRESS = '/usr/local/bin/chromedriver'
    # # Chrome Options
    CHROME_OPTIONS = ChromeOptions()
    CHROME_OPTIONS.add_argument("start-maximized")
    CHROME_OPTIONS.add_argument("--disable-extensions")
    CHROME_OPTIONS.add_argument("--disable-gpu")
    CHROME_OPTIONS.add_argument("--no-sandbox")
    CHROME_OPTIONS.add_argument('disable_infobars')
    CHROME_OPTIONS.add_argument("--headless")

    try:
        driver = Chrome(CHROME_ADDRESS, options=CHROME_OPTIONS)
        display = Display(visible=0, size=(800, 800)); display.start()
    except:
        print("[ERROR] Can not start Chrome! Check your Xvbf and Chrome version.")
        sys.exit()
    
    return display, driver

def scroll_screen(driver:Chrome, stime:int=5, sleep:int=1, step:int=1000) -> None:
    value = 0
    for i in range(stime):
        script = "scrollBy("+ str(value) +",+%s);"%(step)
        driver.execute_script(script)
        value += step; time.sleep(sleep)

def crawl_ggimg(driver:Chrome, key:str, limit:int=100) -> None:
    ORIGIN_LINK = 'https://www.google.com/search?tbm=isch&q=' + key
    driver.get(ORIGIN_LINK); scroll_screen(driver)

    islmp = driver.find_element_by_id('islmp')
    imgs = islmp.find_elements_by_tag_name('img')

    for idx, img in enumerate(imgs):
        src = img.get_attribute('src')
        try:
            path = os.path.join('downloads', key + str(idx) + '.jpg')
            rq.urlretrieve(str(src), path)
            print('[INFO] Downloaded file!')

            if(idx >= limit): break
        except:
            print('[ERROR] Can not download file!')

if __name__ == "__main__":
    try:
        os.makedirs('downloads')
        ap = argparse.ArgumentParser()
        ap.add_argument("-k", "--key", type=str, required=True)
        key = vars(ap.parse_args())['key']
        display, driver = start_chrome()
        crawl_ggimg(driver, key)
    finally:
        driver.close()
        display.stop()
