import winreg

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

if __name__ == "__main__":
    installed_apps = get_installed_apps()
    for app in installed_apps:
        print(app)
