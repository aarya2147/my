import os
import subprocess
import shutil
import threading
import time

CRD_SSH_Code = input("Google CRD SSH Code :")
username = "user" #@param {type:"string"}
password = "root" #@param {type:"string"}
os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

Pin = 123456 #@param {type: "integer"}
Autostart = True #@param {type: "boolean"}

# Timeout in seconds
TIMEOUT = 999999  # Change as needed

class CRDSetup:
    def __init__(self, user):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.finish(user)

    @staticmethod
    def run_command_with_timeout(command, timeout):
        try:
            subprocess.run(command, shell=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f"Command '{command}' timed out after {timeout} seconds.")

    @staticmethod
    def installCRD():
        if not os.path.exists('chrome-remote-desktop_current_amd64.deb'):
            CRDSetup.run_command_with_timeout('wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb', TIMEOUT)
        else:
            print("Chrome Remote Desktop file already downloaded.")
            
        CRDSetup.run_command_with_timeout('dpkg --install chrome-remote-desktop_current_amd64.deb', TIMEOUT)
        CRDSetup.run_command_with_timeout('apt install --assume-yes --fix-broken', TIMEOUT)
        print("Chrome Remote Desktop Installed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    @staticmethod
    def installDesktopEnvironment():
        os.system("export DEBIAN_FRONTEND=noninteractive")
        CRDSetup.run_command_with_timeout("apt install --assume-yes xfce4 desktop-base xfce4-terminal", TIMEOUT)
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("sudo service lightdm stop")
        os.system("sudo apt-get install dbus-x11 -y")
        os.system("service dbus start")
        print("Installed XFCE4 Desktop Environment !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    @staticmethod
    def finish(user):
        if Autostart:
            os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
            link = "whoer.net"
            colab_autostart = """[Desktop Entry]
            Type=Application
            Name=Colab
            Exec=sh -c "sensible-browser {}"
            Icon=
            Comment=Open a predefined notebook at session signin.
            X-GNOME-Autostart-enabled=true""".format(link)
            with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
                f.write(colab_autostart)
            os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop")
            os.system(f"chown {user}:{user} /home/{user}/.config")
            
        os.system(f"adduser {user} chrome-remote-desktop")
        command = f"{CRD_SSH_Code} --pin={Pin}"
        os.system(f"su - {user} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        
        print(" ..........................................................")
        print(" .....Brought By The Disala................................")
        print(" ..........................................................")
        print(" ......#####...######...####....####...##.......####.......")
        print(" ......##..##....##....##......##..##..##......##..##......")
        print(" ......##..##....##.....####...######..##......######......")
        print(" ......##..##....##........##..##..##..##......##..##......")
        print(" ......#####...######...####...##..##..######..##..##......")
        print(" ..........................................................")
        print(" ......... Telegram Channel - https://t.me/TheDisala4U ....")
        print(" ..........................................................")
        print(" ..Youtube Channel - https://www.youtube.com/@The_Disala ..")
        print(" ..........................................................")
        print("Log in PIN : 123456") 
        print("User Name : user") 
        print("User Pass : root") 

        # Run with timeout
        def infinite_loop():
            while True:
                pass

        thread = threading.Thread(target=infinite_loop)
        thread.start()
        thread.join(timeout=TIMEOUT)
        if thread.is_alive():
            print("Timeout reached, stopping execution.")
            thread.join()

try:
    if CRD_SSH_Code == "":
        print("Please enter authcode from the given link")
    elif len(str(Pin)) < 6:
        print("Enter a pin more or equal to 6 digits")
    else:
        CRDSetup(username)
except NameError as e:
    print("'username' variable not found, Create a user first")
