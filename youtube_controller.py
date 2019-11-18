from logging import getLogger
from threading import Lock
from time import sleep

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

DEFAULT_URL = "https://www.youtube.com/watch?v=ESx_hy1n7HA"
PAUSE_BTN = "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button"
AD_PLAYER_OVRELAY = 'ytp-ad-player-overlay-instream-info'
log = getLogger(__name__)

op = Options()
op.add_argument('--disable-extensions')
op.add_argument('--proxy-server="direct://"')
op.add_argument('--proxy-bypass-list=*')
op.add_argument('--autoplay-policy=no-user-required')


class YouTubeController():
    def __init__(self, url=DEFAULT_URL):
        self.url = url

        self.driver = webdriver.Chrome('E:\Program Files\chromedriver\chromedriver.exe',options=op)
        self.lock = Lock()
        self.player = None

        self.open_page()

    def open_page(self):
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.player = self.driver.find_element_by_xpath("/*")
        if not self.player:
            log.error("Failed to get player element.")
            raise Exception("Fuck!")

        # self.skip_ad()

        if self.driver.find_element_by_css_selector(PAUSE_BTN).get_attribute("aria-label").startswith("Play"):
            self.resume()

    def resume(self):
        with self.lock:
            self.player.send_keys('k')

    def skip(self):
        if self.lock.locked():
            return
        with self.lock:
            self.player.send_keys(Keys.SHIFT, 'n')
            sleep(15)

        # self.skip_ad()

    def skip_ad(self):
        try:
            self.driver.find_element_by_class_name(AD_PLAYER_OVRELAY)
            print('ad skip')
            self.skip()
        except exceptions.NoSuchElementException:
            pass
        except Exception as e:
            log.error(exc_info=True)
            raise Exception()

    def close(self):
        self.driver.close()

# for module debugging
def cli():
    conn = YouTubeController()
    while True:
        input("Enter to skip: ")
        conn.skip()

if __name__ == "__main__":
    cli()
