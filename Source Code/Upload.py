import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import autoit
import csv
from selenium.webdriver.common.keys import Keys

def load(data_path):
    data = dict()
    os.chdir(data_path)
    try: #If the file exists
        with open('Descriptions_File','r') as f:
            reader =csv.DictReader(f, delimiter=',')
            for row in reader:
                url = row['url']
                data[url] = row['description']
        f.close()
    except Exception: #if the file doesn't exit, return an empty dict
        return data

    return data

def save(Descriptions, path):  # Save the new added Descriptions
    '''
    :param dict(Descriptions), containing each picture's name and its corresponding caption :
    :return:
    stores the dict content in a .txt file
    '''

    os.chdir(path)
    with open('Descriptions_File.txt', 'w+') as f:
        f.write("url,description\n")
        mycsv = csv.writer(f)
        for url in Descriptions.keys():
            mycsv.writerow([url, Descriptions[url]])

def upload(username1,password1, data_path):
    Descriptions = load(data_path)
    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(chrome_options = chrome_options)

    #Login

    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    driver.find_element_by_name("username").send_keys(username1)
    driver.find_element_by_name("password").send_keys(password1)
    driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()

    time.sleep(3)

    driver.get('https://www.instagram.com/' + username1)

    #gets the image path
    images_path = data_path + os.sep + 'Images'
    for file in os.listdir(images_path):
        if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('png'):
            name = file

    #TODO ImagePath = r'C:\Users\AliDo\PycharmProjects\Clean_Insta_Bot\Images' + f'\{name}'
    ImagePath = images_path + f'\{name}'
    url = f'{name}'
    url = fr'Images\{url}'

    #upload
    ActionChains(driver).move_to_element( driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]""")).click().perform()
    handle = "[CLASS:#32770; TITLE:Open]"
    autoit.win_wait(handle, 3)
    time.sleep(1)
    autoit.control_set_text(handle, "Edit1", ImagePath)
    autoit.control_click(handle, "Button1")

    time.sleep(2)

    driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()

    time.sleep(2)

    txt = driver.find_element_by_class_name('_472V_')
    txt.send_keys('')
    txt = driver.find_element_by_class_name('_472V_')

    if url in Descriptions:
        description = Descriptions[url]
        Descriptions.pop(url, None)
        save(Descriptions, data_path)
    else:
        description = ''
        #TODO automatically generate a caption with ML/NLP

    txt.send_keys(description)
    txt.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="react-root"]/section/div[1]/header/div/div[2]/button""").click()
    time.sleep(5)
    #Remove the Uploaded picture
    os.remove(ImagePath)
    #Close Chrome
    driver.close()
