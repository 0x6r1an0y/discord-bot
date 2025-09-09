#!/bin/bash
# Linux/macOS 初始化腳本

# run at terminal
# cd ~/discord-bot
# sudo bash _init.sh





# 建立虛擬環境
python3 -m venv discord-bot
# 啟動虛擬環境
source discord-bot/bin/activate
sudo apt update
sudo apt install -y python3-pip git ffmpeg chromium-browser
pip install -r requirements.txt