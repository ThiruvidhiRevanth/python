import winreg
import psutil
import time
from collections import defaultdict

def get_installed_apps():
    # Initialize an empty list to store application names
    app_list = []

    # Function to retrieve installed apps from a specified registry key
    def get_apps_from_key(reg_key):
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key)
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name)
            try:
                app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                app_list.append(app_name)
            except FileNotFoundError:
                pass
            finally:
                winreg.CloseKey(subkey)
        winreg.CloseKey(key)

    # Retrieve apps from both 32-bit and 64-bit registry keys
    reg_keys = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]
    for reg_key in reg_keys:
        get_apps_from_key(reg_key)

    return app_list

def track_app_usage(interval=1):
    # Dictionary to store start time for each application
    app_start_times = defaultdict(int)
    
    # Dictionary to store usage intervals for each application
    app_usage_intervals = defaultdict(list)

    while True:
        # Iterate over all running processes
        for proc in psutil.process_iter(['pid', 'name']):
            pid = proc.info['pid']
            name = proc.info['name']
            
            # Check if the process corresponds to an installed application
            if name in installed_apps:
                # Check if the process is not in start times dictionary and add it
                if pid not in app_start_times:
                    app_start_times[pid] = time.time()
                    app_usage_intervals[name].append((app_start_times[pid], None))  # Record start time
                    
                # Update usage intervals for the application
                else:
                    if app_usage_intervals[name][-1][1] is None:  # Check if last interval end time is not set
                        app_usage_intervals[name][-1] = (app_usage_intervals[name][-1][0], time.time())  # Set end time for last interval
                    app_start_times[pid] = time.time()
                    app_usage_intervals[name].append((app_start_times[pid], None))  # Record start time
        
        # Wait for the specified interval
        time.sleep(interval)

if __name__ == "__main__":
    installed_apps = get_installed_apps()
    track_app_usage()
