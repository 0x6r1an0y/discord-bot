#!/bin/bash
# Linux/macOS 初始化腳本

echo "正在安裝 Python 套件..."
pip3 install -r requirements.txt

echo "檢查 FFmpeg 是否已安裝..."
if ! command -v ffmpeg &> /dev/null; then
    echo "警告: FFmpeg 未安裝，請手動安裝："
    echo "Ubuntu/Debian: sudo apt install ffmpeg"
    echo "CentOS/RHEL: sudo yum install ffmpeg"
    echo "macOS: brew install ffmpeg"
else
    echo "FFmpeg 已安裝"
fi

echo "檢查 Chrome/Chromium 是否已安裝..."
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "警告: Chrome/Chromium 未安裝，請手動安裝："
    echo "Ubuntu/Debian: sudo apt install chromium-browser"
    echo "CentOS/RHEL: sudo yum install chromium"
    echo "macOS: brew install --cask google-chrome"
else
    echo "Chrome/Chromium 已安裝"
fi

echo "初始化完成！"
