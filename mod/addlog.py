import logging
import requests
import time
import platform

from mod.environment_variables import init
file_path = "./bot.log"#若為相對路徑時，有可能會讓在其他資料夾的module無法執行(會寫undefined)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(filename)s %(levelname)s %(message)s",
                    datefmt="%a %d %b %Y %H:%M:%S",
                    filename=file_path,
                    filemode="a",
                    encoding="utf-8")

ID,TOKEN,SERVERWEBHOOK,BOTWEBHOOK,MORNING = init()

class addlog:
    def __init__(self):
        struct_time = time.localtime(time.time()) # 轉成時間元組
        self.time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        self.user_name = f"{platform.node()}@{platform.system()}"

    def _webhook_(self,url,payload)->int:
        data = {"content": str(payload)}
        response = requests.post(url, json=data)
        return response.status_code

    def _debug_(self,url,msg):
        msg = str(msg)
        msg = self.time_stamp +  " : " + self.user_name + " / 🟢[DEBUG]" + msg + "\n"
        print(msg)
        logging.debug(msg)
        self._webhook_(url,msg)

    def _info_(self,url,msg):
        msg = str(msg)
        msg = self.time_stamp +  " : " + self.user_name + " / 🟡[INFO]" + msg + "\n"
        print(msg)
        logging.info(msg)
        self._webhook_(url,msg)

    def _warning_(self,url,msg):
        msg = str(msg)
        msg = self.time_stamp +  " : " + self.user_name + " / 🟠[WARNING]" + msg + "\n"
        print(msg)
        logging.warning(msg)
        self._webhook_(url,msg)

    def _error_(self,url,msg):
        msg = str(msg)
        msg = self.time_stamp +  " : " + self.user_name + " / 🔴[ERROR]" + msg + "\n"
        print(msg)
        logging.error(msg)
        self._webhook_(url,msg)

class serverlog(addlog):
    def debug(self, msg:str,url=SERVERWEBHOOK):
        addlog()._debug_(url=url,msg=msg)
    def info(self, msg:str,url=SERVERWEBHOOK):
        addlog()._info_(url=url,msg=msg)
    def warning(self, msg:str,url=SERVERWEBHOOK):
        addlog()._warning_(url=url,msg=msg)
    def error(self, msg:str,url=SERVERWEBHOOK):
        addlog()._error_(url=url,msg=msg)

class botlog(addlog):
    def debug(self, msg:str,url=BOTWEBHOOK):
        addlog()._debug_(url=url,msg=msg)
    def info(self, msg:str,url=BOTWEBHOOK):
        addlog()._info_(url=url,msg=msg)
    def warning(self, msg:str,url=BOTWEBHOOK):
        addlog()._warning_(url=url,msg=msg)
    def error(self, msg:str,url=BOTWEBHOOK):
        addlog()._error_(url=url,msg=msg)

