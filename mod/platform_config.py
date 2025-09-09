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
    
    def get_cpu_usage(self):
        """獲取 CPU 占用率（跨平台）"""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"{cpu_percent:.1f}%"
        except ImportError:
            return "需要安裝 psutil"
        except Exception as e:
            return f"無法取得: {str(e)}"
    
    def get_cpu_temperature(self):
        """獲取 CPU 溫度（跨平台）"""
        try:
            if self.is_linux:
                return self._get_linux_cpu_temp()
            elif self.is_windows:
                return self._get_windows_cpu_temp()
            else:
                return "不支援的平台"
        except Exception as e:
            return f"無法取得: {str(e)}"
    
    def _get_linux_cpu_temp(self):
        """獲取 Linux/Raspberry Pi CPU 溫度"""
        try:
            import psutil
            # 嘗試使用 psutil 獲取溫度感測器
            sensors = psutil.sensors_temperatures()
            
            # Raspberry Pi 特定路徑
            if self._is_raspberry_pi():
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp = float(f.read()) / 1000.0
                        return f"{temp:.1f}°C"
                except FileNotFoundError:
                    pass
            
            # 一般 Linux 系統
            if 'coretemp' in sensors:
                temps = sensors['coretemp']
                if temps:
                    return f"{temps[0].current:.1f}°C"
            
            # 其他可能的溫度感測器
            for sensor_name, temps in sensors.items():
                if temps and 'cpu' in sensor_name.lower():
                    return f"{temps[0].current:.1f}°C"
            
            return "無可用溫度感測器"
            
        except ImportError:
            # 如果 psutil 不支援溫度感測器，嘗試直接讀取系統檔案
            if self._is_raspberry_pi():
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp = float(f.read()) / 1000.0
                        return f"{temp:.1f}°C"
                except FileNotFoundError:
                    return "無法讀取溫度檔案"
            return "需要 psutil 支援"
        except Exception as e:
            return f"讀取失敗: {str(e)}"
    
    def _get_windows_cpu_temp(self):
        """獲取 Windows CPU 溫度"""
        # 方法1: 嘗試使用 psutil（如果支援溫度感測器）
        try:
            import psutil
            if hasattr(psutil, 'sensors_temperatures'):
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        for entry in entries:
                            if 'cpu' in name.lower() or 'core' in name.lower():
                                return f"{entry.current:.1f}°C"
        except:
            pass
        
        # 方法2: 嘗試 WMI 的多個命名空間
        try:
            import wmi
            
            # 嘗試 OpenHardwareMonitor 命名空間
            try:
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                temperature_infos = w.Sensor()
                for sensor in temperature_infos:
                    if sensor.SensorType == 'Temperature' and 'cpu' in sensor.Name.lower():
                        return f"{sensor.Value:.1f}°C"
            except:
                pass
            
            # 嘗試 LibreHardwareMonitor 命名空間
            try:
                w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
                temperature_infos = w.Sensor()
                for sensor in temperature_infos:
                    if sensor.SensorType == 'Temperature' and 'cpu' in sensor.Name.lower():
                        return f"{sensor.Value:.1f}°C"
            except:
                pass
            
            # 嘗試 WMI 熱區命名空間
            try:
                w = wmi.WMI(namespace="root\\wmi")
                temp_info = w.MSAcpi_ThermalZoneTemperature()
                if temp_info:
                    # 轉換開爾文溫度到攝氏溫度
                    temp_celsius = (temp_info[0].CurrentTemperature / 10.0) - 273.15
                    return f"{temp_celsius:.1f}°C"
            except:
                pass
                
            # 嘗試 CIMV2 命名空間的溫度感測器
            try:
                w = wmi.WMI(namespace="root\\cimv2")
                temp_probes = w.Win32_TemperatureProbe()
                if temp_probes:
                    for probe in temp_probes:
                        if probe.CurrentReading:
                            # Win32_TemperatureProbe 的溫度單位是十分之一開爾文
                            temp_celsius = (probe.CurrentReading / 10.0) - 273.15
                            return f"{temp_celsius:.1f}°C"
            except:
                pass
                
        except ImportError:
            return "需要安裝 wmi 套件"
        except Exception as e:
            pass
        
        # 方法3: 嘗試讀取系統註冊表或其他方法
        try:
            import subprocess
            import re
            
            # 使用 wmic 命令列工具
            result = subprocess.run(['wmic', '/namespace:\\\\root\\wmi', 'path', 'MSAcpi_ThermalZoneTemperature', 'get', 'CurrentTemperature'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # 跳過標題行
                    if line.strip() and line.strip().isdigit():
                        temp_kelvin = int(line.strip()) / 10.0
                        temp_celsius = temp_kelvin - 273.15
                        return f"{temp_celsius:.1f}°C"
        except:
            pass
        
        # 如果所有方法都失敗
        return "不存在"

# 建立全域配置實例
config = PlatformConfig()
