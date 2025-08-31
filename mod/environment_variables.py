import json
def init()->tuple:
    with open('mod/config/setting.json',mode='r',encoding='utf-8') as jfile: #母路徑是最外層
        jdata = json.load(jfile)
    TOKEN = jdata['TOKEN']
    ID = jdata['ID']
    SEVERWEBHOOK = jdata['SeverWebhookUrl'] 
    BOTWEBHOOK = jdata['BotWebhookUrl']
    MORNING = jdata['Morning_pic']
    return ID,TOKEN,SEVERWEBHOOK,BOTWEBHOOK,MORNING