from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import youtube_dl
import argparse
from os import listdir, mkdir
import time

# Add the arguments to the parser
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--key", type=str, nargs=2, required=True)
ap.add_argument("-s", "--scroll", type=int, nargs=2, default=[30, 1])
ap.add_argument("-t", "--time", type=int, nargs=2, default=[120, 600])


args = vars(ap.parse_args())
TYPE, KEY = args['key']
SCROLL, TIME = args['scroll']
MIN, MAX = args['time']

# Setup Chrome Webdriver
CHROME_ADDRESS = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('disable_infobars')
driver = webdriver.Chrome(
    CHROME_ADDRESS,
    options=options)
waiter = WebDriverWait(driver, 10)

# Access web by webdriver (YOUTUBE trending)
ORIGIN_LINK = 'https://www.youtube.com/'
if TYPE == 'search':
    ORIGIN_LINK += 'results?search_query=%s'
elif TYPE == 'channel':
    ORIGIN_LINK += 'channel/%s/videos'
driver.get(ORIGIN_LINK % (KEY))

for _ in range(SCROLL):
    time.sleep(TIME)
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight)")

# Extract link list of trending videos
video_list = []
if TYPE == 'search':
    video_list = driver.find_elements_by_xpath('//a[@id="video-title"]')
elif TYPE == 'channel':
    video_list = driver.find_elements_by_xpath('//a[@id="thumbnail"]')

video_links = [x.get_attribute('href') for x in video_list]
video_links = [x[32:] for x in video_links if x != None]

exist_links = []
try:
    exist_links = [f[:-4] for f in listdir("../data")]
except FileNotFoundError:
    print("[WARNING] Creat data directory")
    mkdir('../data')

video_links = [x for x in video_links if x not in exist_links]

# Close web driver
driver.close()

# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'data/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# download audio from youtube
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for link in video_links:
        link = 'https://www.youtube.com/watch?v=' + link

        try:
            info = ydl.extract_info(link, download=False)
        except:
            print("[WARNING] Sign in to confirm your age.")
            continue

        duration = info['duration']
        if duration < MAX and duration > MIN:
            ydl.download([link])
        else:
            print('[WARNING] Duration is out of limit: %i', duration)
