from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.uic import loadUiType
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
import urllib.request

form_class = loadUiType("google_image_downloader.ui")[0]

class downloader(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.c_num.activated.connect(self.num)
        self.b_save.clicked.connect(self.save)

    def num(self):
        try:
            self.cnt = int(self.c_num.currentText())
        except:
            pass

    def save(self):
        self.word = self.l_word.text()
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        # crawler
        driver = webdriver.Chrome()
        driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0&ogbl")
        elem = driver.find_element_by_name("q")
        elem.send_keys(self.word)
        elem.send_keys(Keys.RETURN)
        imgs = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        SCROLL_PAUSE_TIME = 1

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element_by_css_selector(".mye4qd").click()
                except:
                    break
            last_height = new_height

        i = 1
        for img in imgs[:self.cnt]:
            try:
                img.click()
                time.sleep(2)
                imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")
                s = directory + '/' + "{}.jpg".format(i)
                urllib.request.urlretrieve(imgUrl, s)
                i += 1
            except:
                pass
        driver.close()



app = QApplication(sys.argv)
my_window = downloader(None)
my_window.show()
app.exec()