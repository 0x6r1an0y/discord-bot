"""
平台相關配置模組
根據不同作業系統提供對應的配置
"""
import platform
import os

class PlatformConfig:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_linux = self.system == "linux"
        self.is_macos = self.system == "darwin"
        
    def get_ffmpeg_executable(self):
        """獲取 FFmpeg 執行檔名稱"""
        if self.is_windows:
            return "ffmpeg.exe"
        else:
            return "ffmpeg"
    
    def get_chrome_options(self):
        """獲取 Chrome 瀏覽器選項（針對不同平台優化）"""
        from selenium import webdriver
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('user-agent=Mozilla/5.0')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-infobars")
        
        # Raspberry Pi 特定優化
        if self.is_linux and self._is_raspberry_pi():
            chrome_options.add_argument('--memory-pressure-off')
            chrome_options.add_argument('--max_old_space_size=4096')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
        
        return chrome_options
    
    def _is_raspberry_pi(self):
        """檢測是否為 Raspberry Pi"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                return 'raspberry pi' in cpuinfo.lower() or 'bcm' in cpuinfo.lower()
        except FileNotFoundError:
            return False
    
    def get_startup_scripts(self):
        """獲取啟動腳本名稱"""
        if self.is_windows:
            return {
                'init': '_init.cmd',
                'start': '_start.cmd'
            }
        else:
            return {
                'init': '_init.sh',
                'start': '_start.sh'
            }
    
    def get_platform_info(self):
        """獲取平台資訊"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'node': platform.node()
        }

# 建立全域配置實例
config = PlatformConfig()
