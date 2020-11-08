from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from service import HiddenChromeService, HiddenChromeWebDriver

like = 0
images_file_path = ''

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

def load_DM():  # Load the list of the persons previously DMed
    data = []
    global images_file_path
    try:
        os.chdir(images_file_path)
        with open('People_Dmed.txt', 'r') as f:
            data = f.read().splitlines()
    except:
        return data

    return data

def save_DM(data):  # Saves the list of the people DMed to avoid spamming the same person.
    global images_file_path
    if not os.path.exists(images_file_path):
        os.mkdir(images_file_path)
    os.chdir(images_file_path)
    with open('People_Dmed.txt', 'w+') as f:
        f.truncate(0)
        for item in data:
            f.write("%s\n" % item)

class InstagramBot:

    def __init__(self, username, password, var):
        self.username = username
        self.password = password
        if not var:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            self.driver = HiddenChromeWebDriver('chromedriver.exe', chrome_options=options)
        else:
            self.driver = HiddenChromeWebDriver('chromedriver.exe')


        self.driver.implicitly_wait(20)

    def login_verify(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        # time.sleep(5)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(8)
        if driver.current_url == "https://www.instagram.com/":
            driver.close()
            return 0
        else:
            driver.close()
            return 1

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        #time.sleep(5)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(8)
        if driver.current_url == "https://www.instagram.com/":
            return 0
        else:
            return 1

    def private_message(self, link, Messages): #Sends a DM to the profile corresponding to the link provided as a parameter
        global TURN_ON_NOTIFICATIONS
        driver = self.driver
        Message = random.choice(Messages)
        driver.get(link)
        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/div/button').click()
        text_box = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        text_box.send_keys(Message)
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Turn On']"))).click()
        driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()

    def like_photo_with_DM(self, hashtag, hashtags, follows, max_follow, Like_limit, Dms_List, Messages, path):
        global like
        global images_file_path
        images_file_path = path
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # get tags
            hrefs_in_view = driver.find_elements_by_tag_name('a')
            # finding relevant hrefs
            hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                             if '.com/p/' in elem.get_attribute('href')]
            # building list of unique photos
            [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]


        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            if like < Like_limit:
                driver.get(pic_href)
                time.sleep(random.randint(2, 4))
                try:
                    Element = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]')
                    Element.click()
                    like = like + 1
                    if follows < max_follow and int(driver.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span').text) < 150:
                        if driver.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                            driver.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button').click()
                            follows = follows + 1
                            time.sleep(2)
                        time.sleep(random.randint(2, 4))
                        try:
                            profile_link = driver.find_element_by_xpath(
                                '//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').get_attribute(
                                'href')
                            if profile_link not in Dms_List:
                                self.private_message(profile_link, Messages)
                                Dms_List.append(profile_link)
                                save_DM(Dms_List)

                        except Exception:
                            time.sleep(1)

                    for second in reversed(range(random.randint(18, 28))):
                        print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        time.sleep(1)
                except Exception:
                    time.sleep(2)

            else:
                save_DM(Dms_List)
                driver.close()
            unique_photos -= 1
        tag = random.choice(list(set(hashtags) - set(hashtag)))
        self.like_photo_with_DM(tag, hashtags, follows, max_follow, Like_limit, Dms_List, Messages)

    def like_photo(self, hashtag, hashtags, follows, max_follow, Like_limit):
        global like
        driver = self.driver
        driver.implicitly_wait(20)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            if like < Like_limit:
                driver.get(pic_href)
                time.sleep(random.randint(2, 4))
                try:
                    Element = driver.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]')
                    Element.click()
                    like = like + 1
                    if follows < max_follow and int(driver.find_element_by_xpath(
                            '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button/span').text) < 150:
                        if driver.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                            driver.find_element_by_xpath(
                                '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button').click()
                            follows = follows + 1
                            time.sleep(2)

                    for second in reversed(range(random.randint(18, 28))): #Wait for a randomly generated number of seconds
                        print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        time.sleep(1)
                except Exception:
                    time.sleep(2)
                unique_photos -= 1

            else:
                driver.close()
                exit("Done")
        hashtags.remove(hashtag)
        tag = random.choice(hashtags)
        self.like_photo(tag, hashtags, follows, max_follow, Like_limit)


#Test Unit If You Wish To Try The Bot
'''if __name__ == '__main__':

    username = ""
    password = ""
    follows = 0
    max_follow = 50
    Like_limit = 100
    Dms_List = load_DM()
    Messages = generate_messages()

    ig = InstagramBot(username, password, 1)
    hashtags = ['Food', 'FoodPorn', 'Foodie', 'foodstagram', 'foody', 'foodies', 'Delicious', 'FastFood', 'Miam']
    time.sleep(2)

    try:

        ig.login()
        tag = "likeforlike" #random.choice(hashtags) # Choose a random tag from the list of tags
        ig.like_photo(tag, hashtags, follows, max_follow, Like_limit) #Starts Liking And Following

    except Exception:

        ig.driver.close()
        time.sleep(60)
        ig = InstagramBot(username, password)
        ig.login()
        print('whoops')
        tag = "likeforlike" #TODO random.choice(hashtags)
        ig.like_photo(tag, hashtags, follows, max_follow, Like_limit)'''