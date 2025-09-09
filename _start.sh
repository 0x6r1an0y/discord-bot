#!/bin/bash
# Linux/macOS 啟動腳本
# inner script

exec 2>error.log
set -x
cd "/home/brian"
git clone https://github.com/0x6r1an0y/discord-bot.git
. "/home/brian/discord-bot/discord-bot/bin/activate"
python3 "/home/brian/discord-bot/bot.py"

