import os
import pyperclip
import shutil
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from pyrobot import Robot,Keys

def dgcUpload(file):

    print('Inside function')
    print(file)
    #Set browser (Firefox) to be opened
    browser = webdriver.Firefox()

    #Open DGC instance on local machine
    dgcWebLink = 'http://localhost:4400/'
    browser.get(dgcWebLink)

    #User credentials
    user_acc="Admin"
    user_pas="admin"

    #Pass in credentials
    user = browser.find_element_by_css_selector('div.row:nth-child(2) > div:nth-child(1) > span:nth-child(1)')
    user.send_keys(user_acc)

    pass_key = browser.find_element_by_css_selector('div.row:nth-child(3) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)')
    pass_key.send_keys(user_pas)

    #Click 'Signin' button to login into DGC
    login = browser.find_element_by_css_selector('.uf-normal-button').click()

    #Wait for 20 seconds for the page to load
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.item:nth-child(6)')))
    except TimeoutException:
        print("Browser didn't load properly")
        browser.quit()

    #Click 'Settings' on DGC
    settings = browser.find_element_by_css_selector('a.item:nth-child(6)').click()

    # Wait for 20 seconds for the page to load
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.maintab:nth-child(6)')))
    except TimeoutException:
        print("Browser didn't load properly")
        browser.quit()

    #Click 'Workflows' on the left hand side
    workflows = browser.find_element_by_css_selector('li.maintab:nth-child(6)').click()

    # Wait for 20 seconds for the page to load
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.fileupload-button')))
    except TimeoutException:
        print("Browser didn't load properly")
        browser.quit()

    #Click 'Deploy' to upload the workflow
    deploy = browser.find_element_by_css_selector('.fileupload-button').click()

    pyperclip.copy(file)

    # Wait for 10 seconds for the page to load
    for i in range(1, 25):
        print('')

    robot = Robot()
    robot.paste()

    # Wait for 10 seconds for the page to load
    for i in range(1, 25):
        print('')

    robot.key_press('enter')
    print('pressed enter')

   # browser.find_element_by_xpath("//button[contains(text(), 'Open')]").click()

    robot.key_release('enter')
    print('released enter')

print('Inside the script')
SRC_DIR = "K:/Git Code/Collibra/New-process--Code-Value-approval"
print('SRC_DIR has been declared')
SRC_FILES = os.listdir(SRC_DIR)
print('SRC_FILES list has been declared')
TGT_DIR = 'C:/Users/User/Desktop'

for file in SRC_FILES:
    file_path = SRC_DIR+ "/ "
    file_path = file_path.strip() + file + " "

    if file_path.strip().endswith(".bpmn"):
        print(file_path)
        shutil.copy(file_path.strip(), TGT_DIR)

        dgcUpload(file)


