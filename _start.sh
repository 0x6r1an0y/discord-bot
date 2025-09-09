#!/bin/bash
# Linux/macOS 啟動腳本
# inner script

exec 2>error.log
set -x
. "/home/brian/discord-bot/discord-bot/bin/activate"
python3 "/home/brian/discord-bot/bot.py"

