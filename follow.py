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


class InstaBot:
    def __init__(self):
        global popupCount
        global redo 
        global toaster
        popupCount = 0
        redo = False
        toaster = ToastNotifier()

        os.system("start cmd /k chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\TEGchrome")
        sleep(0.3)
        os.system("taskkill /f /im cmd.exe")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:9222")

        ser = Service("C:\\Users\\ciara\\OneDrive\Desktop\\coding\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=ser, options=options)

        # self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)


        self.driver.get("https://www.instagram.com/")

        # //button[@class="_acan _acap _acas"]
        self.enter()
    
    def sleep_for(self):
        limit = random.randint(0, 3) # between 0 and 3 seconds
        # print(limit)
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

        self.start(redo=True) 

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

    def enter(self):
        print(" ")
        print("E to exit")
        print("Or Ctrl + C to emergency exit")
        print(" ")
        run = input(colored("Go to an instagram account then press enter (make sure you're logged in) ", "green"))
        if run.lower() == "e":
            print(colored("EXITING","green"))
            quit()
        else:
            print(" ")
            print(colored("STARTING","green"))
            print(" ")
            self.start(redo)

    def start(self, redo):
        running = True
        while running:
            if redo: # if they want to re run it, it won't click the followers 
                None
            else: # clicking the "followers" button on account
                print(colored("Clicking followers...","green"))
                try:
                    self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div").click()
                except:
                    print(colored("Something went wrong clicking followers", "red"))
                    print("Where you already on the following popup? If so, run the program again without being on the popup.")
                    sleep(5)
                    quit()

            count = 0

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
                    list_of_people = self.driver.find_elements(By.XPATH, '//button[@class="_acan _acap _acas"]')
                    for person in list_of_people:
                        if person.text == "Follow":
                            person.click()
                            count += 1
                            print(colored(f"Followed: {count}","green"))
                            self.sleep_for()
                            self.checkpopup(popupCount) #checking if there are any popups    
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", list_of_people[-1])
                except Exception as e:
                    print(e)
                    print(colored("An error has occured","red"))


            print(" ") 
            print("Total followed:",count)
            print(" ")

            

            toaster.show_toast("Stopped following",
                            f"The program has stopped, see program. Total followed: {count}",
                            icon_path=None,
                            duration=5)


            again = input("Press Enter to run again on another account, A to run on the same account or E to exit: ")

            if again.lower() == "e":
                print(colored("EXITING", "green"))
                quit()
            elif again.lower() == "a":
                print(colored("STARTING AGAIN...", "green"))
                redo = True
                print(self.start(redo))
            else:
                redo = False
            print(self.enter(redo))

InstaBot()