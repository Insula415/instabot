import os
import sys
import keyboard
import random

from time import sleep
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from win10toast import ToastNotifier

class unfollowBot:
    def __init__(self):
        global popupCount
        popupCount = 0
        global toaster
        toaster = ToastNotifier()

        os.system("start cmd /k chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\TEGchrome")
        sleep(0.3)
        os.system("taskkill /f /im cmd.exe")

        global options
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        global ser
        ser = Service("C:\\Users\\ciara\\OneDrive\Desktop\\coding\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=ser, options=options)

        # self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)


        self.driver.get("https://www.instagram.com/la.bulls/following/")
        self.unfollow() 
    
    def sleep_for(self):
        limit = random.randint(0, 3) # between 0 and 3 seconds
        print(limit)
        sleep(limit)

    def scroll(self): # scrolling through following list
        print(colored("SCROLLING","green"))
        pop_up_window = WebDriverWait(
            self.driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")))
        newCount = 0
        while newCount <= 30:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', 
            pop_up_window)
            newCount+=1

    def checkpopup(self, popupCount): #checking if instagram blocks actions
        if "Try again later" in self.driver.page_source:
            popupCount += 1
            print(" ")
            print(colored("POPUP DETECTED","red"))
            if popupCount >= 3:
                print(colored("3 popups have occured, closing program","red"))
                
                toaster.show_toast("Program stopping",
                                "3 popups have occured, closing program",
                                icon_path=None,
                                duration=5)
                sleep(5)
                quit()
            else: 
                print("Waiting 60 seconds then starting again (Press E to exit)")
                count = 0
                while count <= 60:
                    if keyboard.is_pressed('e'):
                        print(colored("EXITING","green"))
                        quit()
                    else:
                        None
                    sleep(1)
                    count+=1
                print(" ")
                print(colored("Refreshing...", "green")) # refreshing the browser then starting script again
                self.driver.get(self.driver.current_url)
                sleep(1)
                self.scroll() # scrolling
                               
        else:
            return None
            
    def checkPrivate(self): #check if account is private
        if "x1swf91x" in self.driver.page_source: #if popup class name is in page source
            print("Account private")
            try:
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]").click()
            except:
                print("Couldn't unfollow")
            # _a9-- _a9-_
        else:
            return None

    def unfollow(self):
        count = 0
        running = True
        while running:
            try: # checking keypress to exit
                if keyboard.is_pressed('e'): 
                    print("EXITING")
                    print(" ") 
                    print(colored("Total followed: ",count))
                    print(" ")
                    running = False
                    quit()
            except:
                None

            try: # try following 
                list_of_people = self.driver.find_elements(By.XPATH, '//button[@class="_acan _acap _acat"]')
                for person in list_of_people:
                    if person.text == "Following":
                        try:
                            person.click()
                            sleep(1)
                            self.checkPrivate()
                            count += 1
                            print(colored(f"Unfollowed: {count}","green"))
                        except:
                            print("something went wrong unfollowing this user")
                        
                        self.sleep_for() # sleep for certain period of time
                        self.checkpopup(popupCount) # checking if there are any popups    
                self.driver.execute_script("arguments[0].scrollIntoView(true);", list_of_people[-1])
            except Exception as e:
                print(e)
                print(colored("An error has occured","red"))


        

unfollowBot()