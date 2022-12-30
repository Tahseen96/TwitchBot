from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver import ActionChains
import undetected_chromedriver as uc
import random
import re
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from configs import username, pswd
import os
import random
from DBHandler import DBHandler

def get_message(n_messages):
    message_files = [int(i.replace('.txt', '')) for i in os.listdir('messages')]
    message_files.sort()
    n_files = message_files[-1]

    message_file = n_messages if n_messages < n_files else n_files

    with open(f"messages/{message_file}.txt") as file:
        messages = file.readlines()
    message = random.choice(messages)
    return message

def get_cooldown(string):
    matches = re.findall('\d+ \w+', string)
    return matches[0]

def random_wait(lower_limit, uper_limit):
    time_wait = random.randint(lower_limit, uper_limit)
    sleep(time_wait)

def human_clicker_click(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
    
def get_element(driver_arg,xpath):
    element = WebDriverWait(driver_arg, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    return element

def wait_for_elements(driver_arg, xpath):
    WebDriverWait(driver_arg, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
        
def wait_for_element(driver_arg, xpath):
    WebDriverWait(driver_arg, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

def waiting_messages(chat_link, message,  cookies, eel):
    print("Starting Scheduler")
    new_driver = webdriver.Chrome(executable_path="./chromedriver")
    new_driver.implicitly_wait(5)
    new_driver.get('https://www.twitch.tv/directory/all/tags/Germany')
    for cookie in cookies:
        new_driver.add_cookie(cookie)


    new_driver.get(chat_link)
    follow = new_driver.find_element('xpath', '//*[contains (text(), "Followers-Only Chat")]')
    human_clicker_click(new_driver,'//button[@data-a-target="follow-button"]')
    human_clicker_click(new_driver,'//textarea')
    # send_message = new_driver.find_element('xpath', '//textarea')
    # send_message.click()
    try:
        human_clicker_click(new_driver,'//button[@data-test-selector="chat-rules-ok-button"]')
        # chat_button = new_driver.find_element('xpath', '//button[@data-test-selector="chat-rules-ok-button"]')
        # chat_button.click()
    except:
        pass
    
    human_typer(new_driver,'//textarea',message)
    # send_message = get_element(driver,'//textarea')
    # send_message.send_keys(message)
    human_clicker_click(new_driver,'//button[@data-a-target="chat-send-button"]')
    
    # msg_button = new_driver.find_element('xpath', '//button[@data-a-target="chat-send-button"]')
    # msg_button.click()
    new_driver.get_screenshot_as_file("screenshots/{}.png".format(chat_link.split("/")[-1]))
    random_wait(3,5)
    human_clicker_click(new_driver,"(//button[@data-a-target='unfollow-button'])[1]")
    eel.remove_from_cooldown()
    new_driver.quit()
    

    



def human_typer(driver, xpath, text: str):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    for s in text:
        element.send_keys(s)
        sleep(random.uniform(0.08, 0.12))






def main(eel):
    db = DBHandler()
    chrome_options  = uc.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = uc.Chrome()
    driver.implicitly_wait(2)
    driver.get('https://www.twitch.tv/login')
    
    human_typer(driver, '//input[@id="login-username"]', username)
    human_typer(driver, '//input[@id="password-input"]', pswd)
    human_clicker_click(driver,'//button[contains(@data-a-target,"login")]')
    # login_button = driver.find_element('xpath', '//button[contains(@data-a-target,"login")]')
    # login_button.click()
    input('Login and press enter')
    cookies = driver.get_cookies()
    driver.get('https://www.twitch.tv/directory/all/tags/Germany')
    human_clicker_click(driver,'//button[@data-a-target="browse-sort-menu"]')
    # viewer_button = driver.find_element('xpath', '//button[@data-a-target="browse-sort-menu"]')
    # viewer_button.click()
    human_clicker_click(driver,'//*[contains (text(), "Viewers (High to Low)" )]')
    # viewer_high = driver.find_element('xpath', '//*[contains (text(), "Viewers (High to Low)" )]')
    # viewer_high.click()
    human_clicker_click(driver,'//main')
    # driver.find_element('xpath', '//main').click()
    while True:
        wait_for_elements(driver,'//a[@data-a-target = "preview-card-image-link"]')
        streamers_links = driver.find_elements('xpath', '//a[@data-a-target = "preview-card-image-link"]')
        n_urls = len(streamers_links)  
        wait_for_element(driver,'//*') 
        driver.find_element('xpath', '//*').send_keys(Keys.END)
        try:
            WebDriverWait(driver, 5).until(lambda x: len(driver.find_elements('xpath', '//img[@class = "tw-image"]')) > n_urls)
        except:
            break
    streamers_links = [element.get_attribute('href') for element in streamers_links]

    # streamers_links =  ['https://www.twitch.tv/twitter_schwurbel', 'https://www.twitch.tv/clubhouseradiotechno'] + streamers_links[:2]
    cooldown_links = []
    # streamers_links = ["https://www.twitch.tv/otplol_"]
    for link in streamers_links:
        driver.get(link)
        streamer = link.split('/')[-1]
        record = db.get_record(streamer)
        n_messages = 1 if record == None else record[1] + 1
        if not record:
            db.add_record(streamer, n_messages)
        else:
            db.update_record(streamer, n_messages)
        message = get_message(n_messages)
        print(message)
        try:
            follow = driver.find_element('xpath', '//*[contains (text(), "Followers-Only Chat")]')
            human_clicker_click(driver,'//button[@data-a-target="follow-button"]')
            # driver.find_element('xpath', '//button[@data-a-target="follow-button"]').click()
            human_clicker_click(driver,'//div[@data-slate-node="element"]')
            # send_message = driver.find_element('xpath', '//div[@data-slate-node="element"]')
            # send_message.click()
            try:
                human_clicker_click(driver,'//button[@data-test-selector="chat-rules-ok-button"]')
                # chat_button = driver.find_element('xpath', '//button[@data-test-selector="chat-rules-ok-button"]')
                # chat_button.click()
            except:
                pass
            human_typer(driver,'//div[@data-slate-node="element"]',message)
            # send_message.send_keys(message)
            human_clicker_click(driver,'//button[@data-a-target="chat-send-button"]')
            driver.get_screenshot_as_file("screenshots/{}.png".format(link.split("/")[-1]))
            random_wait(3,5)
            human_clicker_click(driver,"(//button[@data-a-target='unfollow-button'])[1]")
            human_clicker_click(driver,"//div[text()='Yes, unfollow']")
            # msg_button = driver.find_element('xpath', '//button[@data-a-target="chat-send-button"]')
            # msg_button.click()
            try:
                cooldown_msg = driver.find_element('xpath', '//p[contains (text(), "You need to be a follower")]').text
                cooldown_time = get_cooldown(cooldown_msg)
                cooldown_time = cooldown_time.split(" ")
                cooldown_time_format = cooldown_time[-1]
                cooldown_time = int(cooldown_time[0])
                if(cooldown_time_format == 'minutes'):
                    cooldown_time = datetime.datetime.now() + datetime.timedelta(minutes=cooldown_time+1)
                elif(cooldown_time_format == 'hour' or cooldown_time_format == 'hours'):
                    cooldown_time = datetime.datetime.now() + datetime.timedelta(hours=cooldown_time,minutes=1)
                elif(cooldown_time_format == 'day' or cooldown_time_format == 'days'):
                    cooldown_time = datetime.datetime.now() + datetime.timedelta(day=cooldown_time, minutes=1)
                
                if cooldown_time_format == 'week':
                    pass
                else:
                    scheduler = BackgroundScheduler()
                    scheduler.add_job(waiting_messages,'date', run_date=cooldown_time, args=[link, message, cookies, eel])
                    scheduler.start()
                    cooldown_links.append([cooldown_time, link, scheduler])
                    eel.add_new_to_cooldown()
                    print('*** cooldown ***')
            except Exception as e: print(e)
                
        except: 
            try:
                human_clicker_click(driver,'//div[@data-slate-node="element"]')
                # send_message = driver.find_element('xpath', '//div[@data-slate-node="element"]')
                # send_message.click()
                human_clicker_click(driver,'//button[@data-test-selector="chat-rules-ok-button"]')
                # chat_button = driver.find_element('xpath', '//button[@data-test-selector="chat-rules-ok-button"]')
                # chat_button.click()
            except:
                pass
            try:
                human_typer(driver,'//div[@data-slate-node="element"]',message)
                # send_message.send_keys(message)
                human_clicker_click(driver,'//button[@data-a-target="chat-send-button"]')
                driver.get_screenshot_as_file("screenshots/{}.png".format(link.split("/")[-1]))
                random_wait(3,5)
                human_clicker_click(driver,"(//button[@data-a-target='unfollow-button'])[1]")
                human_clicker_click(driver,"//div[text()='Yes, unfollow']")
                # msg_button = driver.find_element('xpath', '//button[@data-a-target="chat-send-button"]')
                # msg_button.click()
            except:
                pass
    print(streamers_links)
    if cooldown_links:
        cooldown_links.sort(key=lambda x: x[0])
        last_cooldown = cooldown_links[-1][0] + datetime.timedelta(minutes=2)
        last_cooldown = (last_cooldown - datetime.datetime.now()).seconds
        sleep(last_cooldown)
    driver.quit()