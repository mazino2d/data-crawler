from datetime import datetime
import pandas as pd
from selenium import webdriver
from pyvirtualdisplay import Display
import schedule
import time
import os


def start_chrome():
    # # Chrom Dirver
    CHROME_ADDRESS = '/usr/local/bin/chromedriver'
    # # Chrome Options
    CHROME_OPTIONS = webdriver.ChromeOptions()
    CHROME_OPTIONS.add_argument("start-maximized")
    CHROME_OPTIONS.add_argument("--disable-extensions")
    CHROME_OPTIONS.add_argument("--disable-gpu")
    CHROME_OPTIONS.add_argument("--no-sandbox")
    CHROME_OPTIONS.add_argument('disable_infobars')
    CHROME_OPTIONS.add_argument("--headless")
    # # Virtual Display
    display = Display(visible=0, size=(800, 800))

    try:
        driver = webdriver.Chrome(CHROME_ADDRESS, options=CHROME_OPTIONS)
        display = Display(visible=0, size=(800, 800))
        display.start()
    except:
        print("[BUG][CHROME] Can not start Chrome! Check your Xvbf and Chrome version.")

    return display, driver


def crawl_youtube(driver):
    # Access web by webdriver (YOUTUBE trending)
    ORIGIN_LINK = 'https://www.youtube.com/feed/trending'
    driver.get(ORIGIN_LINK)

    # Find music trending link
    xpath = '//*[@id="contents"]/ytd-channel-list-sub-menu-avatar-renderer[1]/a'
    trending_links = driver.find_elements_by_xpath(xpath)[0]
    driver.get(trending_links.get_attribute('href'))

    # Scroll to load all video
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight)")

    # Get artist links
    xpath = '//div[@id="meta"]/ytd-video-meta-block/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a'
    artist_list = driver.find_elements_by_xpath(xpath)

    artist_infos = list()
    for x in artist_list[:-1]:
        artist_infos.append(
            {'name': x.text, "link": x.get_attribute("href")[24:]})

    timestamp = datetime.now().strftime("%d-%b-%Y-%H")
    df = pd.DataFrame(data=artist_infos)
    df = df.drop_duplicates(ignore_index=True)
    df.to_csv('data/artist/artist-%s.csv' % (timestamp))

    # Get video links
    xpath = '//a[@id="video-title"]'
    video_list = driver.find_elements_by_xpath(xpath)

    video_infos = list()
    for x in video_list[:-1]:
        video_infos.append({'title': x.get_attribute("title"),
                            "link": x.get_attribute("href")[32:]})

    timestamp = datetime.now().strftime("%d-%b-%Y-%H")
    df = pd.DataFrame(data=video_infos)
    df = df.drop_duplicates(ignore_index=True)
    df.to_csv('data/video/video-%s.csv' % (timestamp))


def job():
    try:
        display, driver = start_chrome()
        crawl_youtube(driver)
        print('Downloaded at ' + datetime.now().strftime("%d-%b-%Y-%H"))
    finally:
        driver.close()
        display.stop()


if __name__ == "__main__":
    job()
    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
