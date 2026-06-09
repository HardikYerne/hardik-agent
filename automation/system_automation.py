import psutil
import os
import subprocess
import sys
import datetime
import socket

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = 'charging' if battery.power_plugged else 'not charging'
            return f'Battery is at {percent}% and {plugged}'
        return 'Battery information not available'
    except Exception as e:
        return f'Could not get battery: {e}'

def get_cpu_usage():
    try:
        cpu = psutil.cpu_percent(interval=1)
        return f'CPU usage is {cpu}%'
    except Exception as e:
        return f'Could not get CPU: {e}'

def get_ram_usage():
    try:
        ram = psutil.virtual_memory()
        used = round(ram.used / (1024**3), 2)
        total = round(ram.total / (1024**3), 2)
        percent = ram.percent
        return f'RAM usage is {used}GB of {total}GB at {percent}%'
    except Exception as e:
        return f'Could not get RAM: {e}'

def get_disk_usage():
    try:
        disk = psutil.disk_usage('C:/')
        used = round(disk.used / (1024**3), 2)
        total = round(disk.total / (1024**3), 2)
        percent = disk.percent
        return f'Disk usage is {used}GB of {total}GB at {percent}%'
    except Exception as e:
        return f'Could not get disk: {e}'

def list_running_apps():
    try:
        apps = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name and name.endswith('.exe'):
                    apps.append(name.replace('.exe', ''))
            except:
                pass
        apps = list(set(apps))[:10]
        return f'Running apps: {", ".join(apps)}'
    except Exception as e:
        return f'Could not list apps: {e}'

def get_ip_address():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return f'Your IP address is {ip}'
    except Exception as e:
        return f'Could not get IP: {e}'

def empty_recycle_bin():
    try:
        if sys.platform == 'win32':
            subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], check=True)
            return 'Recycle bin emptied'
    except Exception as e:
        return f'Could not empty recycle bin: {e}'

def get_current_time():
    now = datetime.datetime.now()
    return f'Current time is {now.strftime("%I:%M %p")} on {now.strftime("%A, %B %d %Y")}'

def get_weather(city='your city'):
    try:
        subprocess.Popen(['start', f'https://www.google.com/search?q=weather+{city}'], shell=True)
        return f'Opening weather for {city}'
    except Exception as e:
        return f'Could not get weather: {e}'
