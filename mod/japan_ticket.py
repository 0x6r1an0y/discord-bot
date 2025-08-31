import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import requests
from mod.addlog import serverlog, botlog#不要用print()，而是用botlog().debug()或severlog().info()等等

txt_path = '../project_discord\price_save\price.txt'#卡了一個小時 須注意相對路徑跟絕對路徑的問題
url = "https://www.jetstar.com/tw/zh/home?adults=1&children=0&destination=NRT&flexible=1&flight-type=1&infants=0&origin=TPE&selected-departure-date=06-02-2023&tab=1"
url2 = "https://booking.jetstar.com/tw/zh/booking/search-flights?Currency=TWD&adults=1&children=0&departuredate1=2023-02-06&destination1=NRT&dotcomFCOutboundMemberPriceShown=false&dotcomFCOutboundPriceShown=false&dotcomFCPricesHidden=false&infants=0&origin1=TPE"
url3 = "https://booking.jetstar.com/"
webhook_url = "https://discord.com/api/webhooks/1050476762691285002/3zkYNPnW52TLagD75IoNFvnDjfEimokWaUwPpPfoLjNMmu5HeKRVpGLHwa-cAyg03A1g"

japan_previous_price = ""

class japan:
    def create_uc_object(self):
        global wd
        wd = uc.Chrome(driver_executable_path="../project_discord\chromedriver.exe")

    def get_variable(self):
        try:
            global japan_previous_price
            with open(txt_path, 'r') as f:
                price = f.read()
            japan_previous_price = price
        except:
            bot().error("抓取價格數據失敗")

    def set_variable(self,value):
        try:
            with open(txt_path, 'w') as f:
                f.write(str(value))
            self.get_variable()
        except:
            bot().error("覆蓋價格數據失敗")

    def webhook(self,payload)->int:
        try:
            data = {"content": str(payload)}
            response = requests.post(webhook_url, json=data)
        except:
            bot().error("webhook傳出失敗")
        return response.status_code

    def check_airline_price(self):
        global japan_previous_price
        try:
            self.create_uc_object()
        except:
            bot().error("建立瀏覽器物件失敗")
            wd.quit()

        try:
            #wd.get(url)
            wd.execute_script('return navigator.webdriver')
            wd.get(url3)
            wd.find_element(by=By.TAG_NAME,value= "body").click()#除了傳統防爬蟲測試外，還有需要實際物理點擊或FOCUS的偵測
            time.sleep(1)
            wd.get(url2)
            time.sleep(3)
        except:
            bot().error("導覽網頁失敗")
            wd.quit()

        #try:
            #wd.find_element(by=By.XPATH, value= "/html/body/div[3]/div/div/main/div/div[1]/div[2]/div[2]/div/div/div/section/div/div[4]/button").click()
            #bot().debug("已點擊")
            #time.sleep(2)
        #except:
            #wd.get_screenshot_as_file("screenshot.png")
            #bot().error("查詢價格按鈕失敗")
            #wd.quit()
        try:
            self.get_variable()
            current_price = str(wd.find_element(by=By.XPATH,value= "/html/body/main/div[8]/form/div[3]/div[1]/div[3]/div/div/ul/li[4]/div[2]/div/span[2]").text).replace(",","")
            if japan_previous_price != current_price:
                self.webhook("2/6 TPE->NRT 捷星價格已變動 NT$" + current_price)
                self.set_variable(current_price)
            else:
                bot().debug("2/6 TPE->NRT 捷星價格無變動 NT$" + current_price)
        except:
            wd.get_screenshot_as_file("screenshot.png")
            bot().error("抓取或輸出價格失敗")
            wd.quit()
        wd.close()
        return
