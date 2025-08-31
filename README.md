# discord-bot
記錄我的discord-bot
## 步驟
### Python
#### 1.架設python環境
https://www.python.org/downloads/
#### 2.確認pip在新版本

```python.exe -m pip install --upgrade pip```

#### 3.下載discord包

```pip install discord.py```

### Discord
#### 1.進入discord developers
https://discord.com/developers/applications
#### 2.建立新機器人
右上角New Application->輸入想要的名字->同意條款
#### 3.填入基本資料
NAME、DESCRIPTION、TAGS 簡單填一下
#### 4.建立機器人
左邊設定項bot->右上角add bot
#### 5.設定機器人邀請網址
左邊設定項OAuth2->URL Generator->SCOPES中選擇bot->BOT PERMISSIONS就是你希望機器人能擁有的權限

這邊不多做解釋，如果是自己測試用的機器人並且自己也有在該伺服器對應的權限就直接大膽的選擇Administator吧

#### 6.邀請機器人進去伺服器
將會生成網址：
```https://discord.com/api/oauth2/authorize?client_id=1XXXXXXXXXXXXXXXXX&permissions=8&scope=bot```

複製後邀請機器人到想要的伺服器

#### 7.記下ID及TOKEN
左邊設定項OAuth2->General->中間Client information->CLIENT ID複製```1XXXXXXXXXXXXXXXXX```

左邊設定項Bot->token 如果沒看到就reset token->token複製
```XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX```

### 開始
#### 複製repo
```git clone https://github.com/brianoy/discord_bot.git```
#### 填入token

discord_bot/setting.json中填入自己的TOKEN及ID

#### 部屬

部屬到自己的伺服器上
也可以參考https://www.kocpc.com.tw/archives/335244
