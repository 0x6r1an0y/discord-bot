from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager 
import time

def upgrade_chromedriver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver.get("https://www.google.com")