import os
from time import sleep

os.system("start cmd /k pip install -r requirements.txt")
sleep(2)
os.system("taskkill /f /im cmd.exe")