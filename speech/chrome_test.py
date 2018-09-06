from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome = '/media/anurag/Other Stuff/assistants/chatbot_new/speech/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--enable-speech-dispatcher[18]")
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--incognito")
chrome_options.add_argument('--user-data-dir=/home/anurag/.config/google-chrome/')
Browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome)

input('? ')

Browser.get('file:///home/anurag/Downloads/webspeak-master/test/index.html')


Browser.find_element_by_xpath("//option[@value='ko-KR)']").click()

time.sleep(1)

Browser.find_element_by_id('play').click()

time.sleep(1)

print ('quitting!')

Browser.quit()
