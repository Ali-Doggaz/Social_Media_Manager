from selenium import webdriver
import wget
import os
from PIL import ImageChops,Image
import shutil
import time
import praw
import urllib.request
import re

def get_trailing_number(s):
    str = re.findall('\d+', s)
    if len(str)>0:
        return (int(str[-1]))
    else:
        return 0

def same_picture(pic1,pic2):
    '''
    :param pic1:
    :param pic2:
    :return:
    1 if picture 1 == picture 2
    0 if Picture1 != Picture 2
    '''
    im1 = Image.open(pic1)
    im2 = Image.open(pic2)
    if ImageChops.difference(im2, im1).getbbox() is None:
        return 1
    return 0

def download_reddit(n): #DOWNLOAD USING SELENIUM
    driver = webdriver.Chrome('chromedriver.exe')
    for i in range(n):
        driver.get('https://www.reddit.com/r/food/hot/')
        i = 0
        k=1
        p = 1
        while(k==1):
            i = i +1
            if i==2:
                i=4
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if (p-i == 2):
                p = i
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:                                        #/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[4]/div[6]/div/div/div[2]/div[3]/div/div[2]/a/div/div/img
                Picture = driver.find_element_by_xpath(f"/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[4]/div[{i}]/div/div/div[2]/div[3]/div/div[2]/a/div/div/img")
                image_url = Picture.get_attribute('src')
                wget.download(image_url,'New_Image')
                for picture in os.listdir('New_Image'):
                    url_new = 'New_Image/' + picture
                    im1 = Image.open(url_new)
                k = 0
                for picture in os.listdir('Used_Images'):
                    url = 'Used_Images/' + picture
                    im2 = Image.open(url)
                    if ImageChops.difference(im2, im1).getbbox() is None:
                        print("image already posted")
                        os.remove(url_new)
                        k=1
                    else:
                        continue
                for picture in os.listdir('Images'):
                    url = 'Images/' + picture
                    im2 = Image.open(url)
                    if ImageChops.difference(im2, im1).getbbox() is None:
                        print("image already posted")
                        os.remove(url_new)
                        k=1
                    else:
                        continue
                if k==0:
                    for picture in os.listdir('New_Image'):
                        url = 'New_Image/' + picture
                        shutil.move(url, 'Images')
            except:
                time.sleep(2)
    driver.close()

def download_reddit_PRAWN(n,subreddit_name, data_path): #DOWNLOAD USING PRAWN (WAY QUICKER)
    reddit = praw.Reddit(client_id='TtC6ss4zB1F_2g',
                         client_secret='Pp5Im-Om1_AZgXochZqF7wqovsc',
                         user_agent='Downloader')
    subreddit = reddit.subreddit(subreddit_name).top("week", limit=None)
    images_path = data_path + os.sep + 'Images'
    os.chdir(images_path)
    L= os.listdir()
    begin_count = 0
    if len(L)>0:
        for file in L:
            if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('png'):
                number = get_trailing_number(file)
                begin_count = max(begin_count, number)

    i=begin_count+1
    for submission in subreddit:
        url = str(submission.url)
        if url.endswith("jpg") or url.endswith('jpeg') or url.endswith("png"): #If the post is an image
            if url[-2] == 'p':
                ext = 'jpg'
            elif url[-2] == 'e':
                ext = 'jpeg'
            else:
                ext = 'png'
            urllib.request.urlretrieve(url,f"image{i}.{ext}")
            for pict2 in os.listdir(): #Check if we already downloaded the same picture, if we did, then skip it and decrement the counter (i)
                if same_picture(pict2, f"image{i}.{ext}") and pict2 != f"image{i}.{ext}":
                    os.remove(f"image{i}.{ext}")
                    i -= 1
                    break

            i+=1

        if i>=(begin_count+n):
            return 1
            break

    return 0


