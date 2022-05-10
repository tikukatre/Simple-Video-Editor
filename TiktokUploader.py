import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
#Original code from https://github.com/redianmarku/tiktok-autouploader

print('=====================================================================================================')
print(
    'Hey, you have to login manually on tiktok, so the bot will wait you 30 seconds for logging in and completing reCAPTCHA manually!')
print('=====================================================================================================')
time.sleep(8)
print('Running bot now, get ready and login manually...')
time.sleep(4)

options = webdriver.ChromeOptions()
#If you can't log into TikTok on the gerenrated Chrome instance, try the following code and
#options.add_argument("user-data-dir= Add here path to your user data)
#bot = webdriver.Chrome(options=options, executable_path=CM(version="100.0.4896.60").install())
bot = webdriver.Chrome(options=options,  executable_path=CM().install())
bot.set_window_size(1680, 900)

bot.get('https://www.tiktok.com/login')
ActionChains(bot).key_down(Keys.CONTROL).send_keys(
    '-').key_up(Keys.CONTROL).perform()
ActionChains(bot).key_down(Keys.CONTROL).send_keys(
    '-').key_up(Keys.CONTROL).perform()
print('Waiting 10s for manual login...')
time.sleep(10)
bot.get('https://www.tiktok.com/upload/?lang=en')
time.sleep(3)
# bot.switch_to_frame('//*[@id="main"]/div[2]/div/iframe')
bot.switch_to.frame(0);





def upload(video_path):
    while True:
        file_uploader = bot.find_element_by_xpath(
            "//button[normalize-space()='Select file']")

        file_uploader.send_keys(video_path)

        caption = bot.find_element_by_xpath(
            "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")

        bot.implicitly_wait(10)
        ActionChains(bot).move_to_element(caption).click(
            caption).perform()
        # ActionChains(bot).key_down(Keys.CONTROL).send_keys(
        #     'v').key_up(Keys.CONTROL).perform()

        with open("caption.txt", "r") as f:
            tags = [line.strip() for line in f]

        for tag in tags:
            ActionChains(bot).send_keys(tag).perform()
            time.sleep(2)
            ActionChains(bot).send_keys(Keys.RETURN).perform()
            time.sleep(1)

        time.sleep(5)
        bot.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        post = WebDriverWait(bot, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Post']")))

        post.click()
        time.sleep(30)

        time.sleep(1)
        return 


# ================================================================
# Here is the path of the video that you want to upload in tiktok.
# Plese edit the path because this is different to everyone.
upload(r"C:\Users\Katre\Desktop\tiktok-autouploader\mining tip 2.mp4")
# ================================================================
