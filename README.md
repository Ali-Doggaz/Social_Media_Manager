# Social_Media_Manager
Python Bot that entirely automates an Instagram account.

## Introduction
The purpose of this project is to completely automatise an Instagram account, meaning that this script will take care of all the activity related to your account. 
The only thing the user has to do is to give the 'theme' of his account (I.e : your account could be about food, cars, modelling, sports/coaching, etc...)

## What will this bot do?
  * Scrape the web for the most trending pictures related to your account's theme.
  * Store a description for each downloaded photo. That description will be used as the picture's caption when we will upload the picture. (Right now, the user has to write down a description for each picture. In the future, I will implement a NLP algorithm to automatically generate a good caption).
  * Upload pictures on your account.
  * Like, follow, and (optionally) DM other users with personalized messages. This feature makes your account obtain a good visibility, and Instagram will recommend your profile to more users.
  
## Technologies
  * Python
  * Selenium (Web-Scraping)
  * PRAW (Reddit's API)
  * Multi-Threading
  * Pillow 
  * Tkinter for the UI

## Launch
  Run Main.py. This will display the UI and let you use the bot. (I will soon implement an entirely automatized way to run the script, without having to deal with any UI.)
 
 This project is still in development. Several new features will be added soon, and an executable file will be provided asap.
