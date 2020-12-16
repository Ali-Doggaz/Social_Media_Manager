import tkinter
from Download_Trending_Photo_From_Reddit import download_reddit_PRAWN
import threading
import time
from BOT import InstagramBot
import csv
from PIL import ImageTk, Image
from os import listdir, chdir, sep
import os
from Upload import upload
import random
import praw
from prawcore import NotFound

USERNAME1 = ''
PASSWORD1 = ''
k = 1
i = 0
like = 0
follow = 0
ig = None
count_download_request = -1
IMAGES_FILE_PATH = '' #Path to the file Containing everything to store (Pictures, Captions, DMs, etc...)

def update_path(path_entry):
    global IMAGES_FILE_PATH
    IMAGES_FILE_PATH = path_entry.get()

def clear_trailing_newlines(str):
    '''
    :param str:
    deletes all trailing newlines in a string
    :return:
    The trailing newlines' free string
    I.e: 'test\n\n' -->'test'
    '''

    while(len(str)>0):
        if str[-1] == '\n':
            str = str[0:-1]
        else:
            break
    return str

def sub_exists(sub):
    '''
    :param sub (string, name of a potential subreddit):
    :return:
    1 if the subreddit exists
    0 if it doesn't
    '''
    reddit = praw.Reddit(client_id='TtC6ss4zB1F_2g',
                         client_secret='Pp5Im-Om1_AZgXochZqF7wqovsc',
                         user_agent='Downloader')
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

def destroy_widget(widget):
    '''
    :param widget:
    :return:
    destroys the widget from the frame
    '''
    widget.destroy

def load():
    '''
    Load all the stored captions
    :return:
    a dictionary containing each picture's name and corresponding caption
    '''
    data = dict()
    global IMAGES_FILE_PATH
    chdir(IMAGES_FILE_PATH)
    try:
        with open('Descriptions_File.txt', 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                url = row['url']
                data[url] = row['description']
        f.close()
    except Exception: #If no Descriptions found
        return data
    return data

def save(Descriptions):  # Save the new added Descriptions
    '''
    :param dict(Descriptions), containing each picture's name and its corresponding caption :
    :return:
    stores the dict content in a .txt file
    '''

    global IMAGES_FILE_PATH
    chdir(IMAGES_FILE_PATH)
    with open('Descriptions_File.txt', 'w+') as f:
        f.write("url,description\n")
        mycsv = csv.writer(f)
        for url in Descriptions.keys():
            mycsv.writerow([url, Descriptions[url]])

def load_DM():
    '''
    :return:
    Load the list of the persons previously DMed
    Utility : avoid messaging the same person twice, even after several uses of the app.
    '''
    global IMAGES_FILE_PATH
    chdir(IMAGES_FILE_PATH)
    data = []
    try:
        with open('People_Dmed.txt', 'r') as f:
            data = f.read().splitlines()
    except Exception:
        return data
    return data

def login_verify():
    '''
    Verify the (username,password) combination
    :return:
    1 if valid
    0 if invalid
    '''
    global USERNAME1
    global PASSWORD1
    USERNAME1 = username.get()
    PASSWORD1 = password.get()
    def call():
        win2_Login()
        username.set(USERNAME1)
        password.set(PASSWORD1)
        wait = tkinter.Label(mframe, text="Please Wait While We're Logging You", bg='pink', width=200, font=("Courier", 13), pady=50)
        wait.pack()
        global ig
        ig = InstagramBot(USERNAME1, PASSWORD1, 0)
        bool = ig.login_verify()
        if bool:
            win6_Account()
        else:
            wait.pack_forget()
            Invalid_Message = tkinter.Label(mframe, text="Invalid Details", bg='pink', width=200, font=("Courier", 20), pady=50)
            Invalid_Message.pack()
            time.sleep(1)
            Invalid_Message.pack_forget()


    t = threading.Thread(target=call)
    t.start()

def clearwin(event=None):
    '''Clear the main windows frame of all widgets'''
    
    global mframe
    mframe.destroy()
    mframe = tkinter.Frame(main, width=800, height=600, background='pink')
    mframe.pack(fill="both", expand=True, padx=20, pady=20)

def download():
    '''
    Downloads the number of pictures needed by the user
    Displays any error if encountered
    '''
    def call():
        global count_download_request
        count_download_request += 1
        subreddit_name = subreddit.get()
        s = number.get()
        if s == '' or s == '0' or not s.isnumeric():
            def invalid_msg_1():
                Waiting_Label_1 = tkinter.Label(mframe, text="Please indicate a valid number", bg='pink', width=200,
                                              font=("Courier", 10))
                Waiting_Label_2 = tkinter.Label(mframe, text="of pictures to download", bg='pink', width=200,
                                              font=("Courier", 10))
                Waiting_Label_1.pack()
                Waiting_Label_2.pack()
                time.sleep(1.5)
                Waiting_Label_1.pack_forget()
                Waiting_Label_2.pack_forget()

            t = threading.Thread(target=invalid_msg_1)
            t.start()

        elif subreddit_name == '' or not sub_exists(subreddit_name):
            def invalid_message_2():
                Waiting_Label_3 = tkinter.Label(mframe, text="Please provide a valid Subreddit name", bg='pink', width=200,
                                              font=("Courier", 10))
                Waiting_Label_3.pack()
                time.sleep(1.5)
                Waiting_Label_3.pack_forget()

            t = threading.Thread(target=invalid_message_2)
            t.start()

        else: #If everything is good to go, start downloading 
            n = int(s) + 1

            def call():
                global count_download_request
                global IMAGES_FILE_PATH
                if len(IMAGES_FILE_PATH)<=0:
                    def invalid_path_error():
                        Error_Label = tkinter.Label(mframe, text="Invalid Download Path, please go back to", bg='pink', width=200,
                                                      font=("Courier", 14), pady=50)
                        Error_Label.pack()
                        Error_Label2 = tkinter.Label(mframe, text="Main Menu And Provide A Valid Path", bg='pink',
                                                    width=200, font=("Courier", 14), pady=50)
                        Error_Label2.pack()
                        time.sleep(1.5)
                        Error_Label.pack_forget()
                        Error_Label2.pack_forget()
                        win1()


                    t = threading.Thread(target=invalid_path_error())
                    t.start()
                else:
                    if count_download_request == 0:
                        Waiting_Label = tkinter.Label(mframe, text="Downloading... Please Wait", bg='pink', width=200,
                                                    font=("Courier", 20), pady=50)
                        Waiting_Label.pack()
                    else:
                        Waiting_Label = tkinter.Label(mframe, text=f"Please Wait...(request{count_download_request})", bg='pink', width=200,
                                                          font=("Courier", 20), pady=50)

                    Waiting_Label.pack()
                    if not os.path.exists(IMAGES_FILE_PATH+os.sep+'Images'):
                        os.mkdir(IMAGES_FILE_PATH+os.sep+'Images')
                    pictures_downloaded_bool = download_reddit_PRAWN(n, subreddit_name, IMAGES_FILE_PATH)
                    if pictures_downloaded_bool:
                        count_download_request-=1
                        Waiting_Label.pack_forget()
                        Done_Label = tkinter.Label(mframe, text="Pictures Downloaded!", bg='pink', width=200,
                                                      font=("Courier", 20), pady=50)
                        Done_Label.pack()
                        time.sleep(1)
                        Done_Label.pack_forget()
                    else:
                        count_download_request -= 1
                        Waiting_Label.pack_forget()
                        Done_Label = tkinter.Label(mframe, text="Not enough trending pictures in subreddit!", bg='pink', width=200,
                                                   font=("Courier", 20), pady=50)
                        Done_Label.pack()
                        time.sleep(1.5)
                        Done_Label.pack_forget()



            t2 = threading.Thread(target=call)
            t2.start()

    t1 = threading.Thread(target=call)
    t1.start()

def win1(event=None):
    '''
    Generates the main menu
    '''
    clearwin()
    mframe.pack_propagate(0)
    b1 = tkinter.Button(mframe, command=win2_Login, text='Manage Account', bg='violet', padx=25)
    b1.pack(side='top', expand='YES')
    b1.place(relx=0.5, rely=0.3, anchor='center')
    b2 = tkinter.Button(mframe, command=win3_ManagePictures, text='Manage Pictures', bg='violet', padx=25)
    b2.pack(side='top', expand='YES')
    b2.place(relx=0.5, rely=0.4, anchor='center')

    global IMAGES_FILE_PATH
    global images_path
    images_path = tkinter.StringVar()

    text1 = tkinter.Label(mframe, text="(Required) Please Provide The Path Of The File ", bg='pink')
    text1.pack()
    text1.place(relx=0.5, rely=0.5, anchor='center')

    text2 = tkinter.Label(mframe, text="Where You Wish To Store Your Files (Pictures, Captions, DMs Logs)", bg='pink')
    text2.pack()
    text2.place(relx=0.5, rely=0.54, anchor='center')

    path_entry = tkinter.Entry(mframe, textvariable=images_path, bg='pink', width=33,
                               font=("Courier", 13))
    path_entry.pack()
    path_entry.place(relx=0.5, rely=0.59, anchor='center')
    images_path.set(IMAGES_FILE_PATH)

    back = tkinter.Button(mframe, command= lambda : update_path(images_path), text='Validate Path', bg='violet', padx=40)
    back.pack()
    back.place(relx=0.5, rely=0.63, anchor='center')


#All win{i}_{name} below generate the iTH page of the app. In total, there are
# 8 pages. Each one deals with a certain feature (Uploading content, Downloading pictures, Liking/DMing people, logging
# in, etc...)

def win2_Login(event=None):
    """
    Generates the login screen.
    The username/password combination provided by the user will be verified.
    If the combination is correct, generates the next menu (def win6_Account(event=None), see line 490).
    """
    global IMAGES_FILE_PATH

    clearwin()
    login_screen = mframe

    tkinter.Label(login_screen, text="Please enter your instagram details", bg='pink', width=200, font=("Courier", 20), pady=50).pack()
    login_screen.place(relx=0.5, rely=0.3, anchor='center')
    tkinter.Label(login_screen, text="", bg='pink').pack()

    global username
    global password
    username = tkinter.StringVar()
    password = tkinter.StringVar()

    global username_login_entry
    global password_login_entry

    tkinter.Label(login_screen, text="Username ", bg='pink').pack()
    username_login_entry = tkinter.Entry(login_screen, textvariable=username, bg='pink', width=33, font=("Courier", 13))
    username_login_entry.pack()
    tkinter.Label(login_screen, text="", bg='pink').pack()
    tkinter.Label(login_screen, text="Password ", bg='pink').pack()
    password_login_entry = tkinter.Entry(login_screen, textvariable=password, show='*', bg='pink', width=33,
                                 font=("Courier", 13))
    password_login_entry.pack()
    tkinter.Label(login_screen, text="", bg='pink').pack()

    tkinter.Button(login_screen, text="Login", width=10, height=1, command=login_verify, bg='pink').pack()
    tkinter.Button(mframe, text='Back', width=10, height=1, command=win1, bg='pink').pack()

def win3_ManagePictures(event=None):
    """
    Generates a simple menu containing 3 buttons:
    button 1: 'Download Pictures', will take the user to the picture downloader menu.
    button 2: 'Manage Database/Add Captions', will prompt all the user's downloaded pictures and their captions.
    The user will be able to modify any caption.
    button 3: 'Back', takes the user back to the previous menu.
    """
    
    global IMAGES_FILE_PATH
    clearwin()
    mframe.pack_propagate(0)
    b1 = tkinter.Button(mframe, command=win4_DownloadPictures, text='Download Pictures', bg='violet', padx=25)
    b1.pack(side='top', expand='YES')
    b1.place(relx=0.5, rely=0.3, anchor='center')
    b2 = tkinter.Button(mframe, command=win5_ManageData_Caption, text='Manage Database/Add Captions', bg='violet', padx=25)
    b2.pack(side='top', expand='YES')
    b2.place(relx=0.5, rely=0.5, anchor='center')
    b3 = tkinter.Button(mframe, text='Back', width=10, height=1, command=win1, bg='violet', padx=25)
    b3.pack(side='top', expand='YES')
    b3.place(relx=0.5, rely=0.7, anchor='center')

def win4_DownloadPictures(event=None):
    """
    Generates the download screen. The user will be asked to write a certain theme's name (ie: food, cars, models, etc...), the 
    number of pictures he wishes to download, and a few other details.
    The app will then download the most trending pictures related to that theme.
    """
    
    clearwin()

    global count_download_request
    count_download_request = -1

    tkinter.Label(mframe, text="Please enter a subreddit's name or a theme's name (I.e: food, cars, models, etc...)", bg='pink', width=100, font=("Courier", 12)).pack()
    tkinter.Label(mframe, text="(We will soon add the possibility to download from pixabay and other such website)", bg='pink', width=200, font=("Courier", 10)).pack()
    mframe.place(relx=0.5, rely=0.3, anchor='center')

    global subreddit
    global number
    number = tkinter.StringVar()
    subreddit = tkinter.StringVar()

    global subreddit_entry
    global number_entry

    subreddit_entry = tkinter.Entry(mframe, textvariable=subreddit, bg='pink', width=33, font=("Courier", 13)).pack()

    tkinter.Label(mframe, text="Number Of Pictures To download:",bg='pink', width=200, font=("Courier", 13)).pack()
    number_entry = tkinter.Entry(mframe, textvariable=number, bg='pink', width=33, font=("Courier", 13))
    number_entry.pack()

    tkinter.Button(mframe, text="Download", width=10, height=1, command=download, bg='pink').pack()
    back = tkinter.Button(mframe, text='Back', width=10, height=1, command=win3_ManagePictures, bg='pink')
    back.pack()

def win5_ManageData_Caption(event=None):
    """
    Each picture downloaded (or manually added to the images' folder) will be prompted. 
    If a caption of the picture is stored, it will also be displayed.
    The user will have a text box below each image, and will be able to edit the caption 
    as much as he wants.
    To go the next picture, the user will either click on the 'Add description' button, or
    press the right arrow key of his keyboard.
    """
    
    clearwin()
    global IMAGES_FILE_PATH
    global i
    i=0

    Descriptions = load()
    imgs = []
    if os.path.exists(IMAGES_FILE_PATH+sep+'Images'):
        for picture in sorted(listdir(IMAGES_FILE_PATH+sep+'Images')):  # Store all the Images' Path in imgs []
            path = fr'Images\{picture}'
            imgs.append(path)

        # Opens the first Image with an adequate format (size)
        Images = Image.open(imgs[0])
        basewidth = 700
        wpercent = (basewidth / float(Images.size[0]))
        hsize = int((float(Images.size[1]) * float(wpercent)))
        Image_copy = Images.resize((basewidth, hsize), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(Image_copy)
        img_label = tkinter.Label(mframe, image=photo)
        img_label.pack(padx=10, pady=10)

        def myClick(event=None):
            global i

            i = i + 1
            # get the description of image n*i
            save(Descriptions)
            if i > len(imgs):
                save(Descriptions)
                win1()
                return
            Descriptions[imgs[i - 1]] = T.get("1.0", 'end')
            Descriptions[imgs[i - 1]] = clear_trailing_newlines(Descriptions[imgs[i - 1]])
            if i >= len(imgs):  # If we reached the last image
                save(Descriptions)
                win1()
                return

            T.delete("1.0", 'end')
            Images = Image.open(imgs[i])
            basewidth = 350
            wpercent = (basewidth / float(Images.size[0]))
            hsize = int((float(Images.size[1]) * float(wpercent)))
            Image_copy = Images.resize((basewidth, hsize), Image.ANTIALIAS)
            img_label.img = ImageTk.PhotoImage(Image_copy)
            img_label.config(image=img_label.img)
            img_label.image = img_label.img
            if imgs[i] in Descriptions:
                T.insert("1.0", Descriptions[imgs[i]])

        def Back(event=None):
            global i
            i = i - 2
            myClick()

        # Adding the entry box
        T = tkinter.Text(mframe, height=10, width=40)
        if imgs[0] in Descriptions:
            T.insert("1.0", Descriptions[imgs[0]])
            T.insert("1.0", '')

        T.pack()
        # add_button
        my_button = tkinter.Button(mframe, text="Add Description", command=lambda: myClick())
        my_button.pack(padx=10)
        T.bind('<Right>', func=myClick)
        T.bind('<Left>', func=Back)

        mframe.mainloop()

        back = tkinter.Button(mframe, command=win3_ManagePictures, text='Back')
        back.pack()
    else:
        def no_pictures_error():
            mframe.pack_propagate(0)

            b1 = tkinter.Label(mframe, text='Please Download Pictures (Or', font=("Courier", 18), bg='pink')
            b1.pack(side='top', expand='YES')
            b1.place(relx=0.5, rely=0.4, anchor='center')
            b1 = tkinter.Label(mframe, text='Add Them Manually) Before Adding Captions', font=("Courier", 18), bg='pink')
            b1.pack(side='top', expand='YES')
            b1.place(relx=0.5, rely=0.5, anchor='center')
            time.sleep(1.5)
            win3_ManagePictures()


        t = threading.Thread(target=no_pictures_error)
        t.start()

def win6_Account(event=None):
    """
    This menu will give the user access to 2 main features:
        *Activating the bot (following, dming, liking pictures, etc...)
        *Uploading a downloaded picture
    """
    
    clearwin()
    mframe.pack_propagate(0)

    global IMAGES_FILE_PATH

    b1 = tkinter.Button(mframe, command=win7_Like_Follow, text='Like, Follow, and DM Automatically, to make your account better placed in Instagram Algorithm', bg='violet', padx=25)
    b1.pack(side='top', expand='YES')
    b1.place(relx=0.5, rely=0.3, anchor='center')

    b2 = tkinter.Button(mframe, command=win8_Upload, text="Upload A Picture From The Database With Its caption",
                        bg='violet', padx=25)
    b2.pack(side='top', expand='YES')
    b2.place(relx=0.5, rely=0.4, anchor='center')

    text2 = tkinter.Label(mframe, text="You Can Modify The Download Path Here", bg='pink')
    text2.pack()
    text2.place(relx=0.5, rely=0.5, anchor='center')

    global images_path
    images_path = tkinter.StringVar()
    path_entry = tkinter.Entry(mframe, textvariable=images_path, bg='pink', width=33,
                               font=("Courier", 13))
    path_entry.pack()
    path_entry.place(relx=0.5, rely=0.55, anchor='center')
    images_path.set(IMAGES_FILE_PATH)

    back = tkinter.Button(mframe, command= lambda : update_path(images_path), text='Validate Path ', bg='violet', padx=40)
    back.pack()
    back.place(relx=0.5, rely=0.6, anchor='center')

    back = tkinter.Button(mframe, command=win1, text='      Back      ', bg='violet', padx=40)
    back.pack(padx=23)
    back.place(relx=0.5, rely=0.67, anchor='center')

def win7_Like_Follow(event=None):
    """
    This is where the Bot kicks in. 
    In this menu, the user will be asked several informations to
    determine how the bot will work. Once all the necessary information is
    entered by the user (Number of pictures to like, nbr of person to follow, 
    whether or not to show the web scraping while it is occuring (make a chrome
    window appear and shows all the bot's action), etc...), the bot will start working.
    """
    
    clearwin()
    mframe.pack_propagate(0)

    def Run():
        global USERNAME1
        global PASSWORD1
        global IMAGES_FILE_PATH

        tags = tags_string.get()
        max_likes = number_likes.get()
        max_follows = number_follows.get()
        messages_to_send = messages.get()
        var = var1.get()  # Determines if we will DM people or not
        var_2 = var2.get()  # Determines whether to show the browser or not

        if len(tags) == 0:
            tags_entry = tkinter.Label(mframe, text="Please Indicates The Tags To Explore", bg='pink')
            tags_entry.pack()
            time.sleep(1)
            tags_entry.pack_forget()

        elif max_likes == '' or max_likes.isalpha() or max_likes == 0:
            invalid_likes_entry = tkinter.Label(mframe, text="Please Indicate A Valid Number Of Likes", bg='pink')
            invalid_likes_entry.pack()
            time.sleep(1)
            invalid_likes_entry.pack_forget()

        elif max_follows == '' or max_follows.isalpha():
            invalid_follows_entry = tkinter.Label(mframe, text="Please Indicate A Valid Number Of Likes",
                                                  bg='pink').pack()
            invalid_follows_entry.pack()
            time.sleep(1)
            invalid_follows_entry.pack_forget()

        else:  # If everything is good to go
            tags = tags.split(',')
            tag = random.choice(tags)
            ig = InstagramBot(USERNAME1, PASSWORD1, var_2)
            follow = 0
            if var:  # If we will DM people:
                def send_with_DM():
                    msg = messages_to_send.split(',')
                    Dms_List = load_DM()
                    ig.login()
                    ig.like_photo_with_DM(tag, tags, follow, int(max_follows), int(max_likes), Dms_List, msg, IMAGES_FILE_PATH)
                t = threading.Thread(target=send_with_DM)
                t.start()
            else:  # If we won't DM anyone:
                def send_without_DM():
                    ig.login()
                    ig.like_photo(tag, tags, follow, int(max_follows), int(max_likes))

                t = threading.Thread(target=send_without_DM)
                t.start()


    tags_string = tkinter.StringVar()
    number_likes = tkinter.StringVar()
    number_follows = tkinter.StringVar()
    messages = tkinter.StringVar()

    tkinter.Label(mframe, text="Tags you wish to explore, separated by a ',' ", bg='pink').pack()
    tags_entry = tkinter.Entry(mframe, textvariable=tags_string, bg='pink', width=33,
                               font=("Courier", 13))
    tags_entry.pack()

    tkinter.Label(mframe, text="Number Of Likes (must be superior to 0)", bg='pink').pack()
    number_likes_entry = tkinter.Entry(mframe, textvariable=number_likes, bg='pink', width=33,
                                       font=("Courier", 13))
    number_likes_entry.pack()

    tkinter.Label(mframe, text="Maximum Number Of Follows (Will only follow people that have", bg='pink').pack()
    tkinter.Label(mframe, text="high chances of following you back)", bg='pink').pack()
    number_follows_entry = tkinter.Entry(mframe, textvariable=number_follows, bg='pink', width=33,
                                         font=("Courier", 13))
    number_follows_entry.pack()

    tkinter.Label(mframe, text="Messages you wish to send to people, separated by a ',' (Optional)", bg='pink').pack()
    messages_entry = tkinter.Entry(mframe, textvariable=messages, bg='pink', width=33,
                                   font=("Courier", 13))
    messages_entry.pack()

    var1 = tkinter.IntVar()
    tkinter.Checkbutton(mframe,
                        text="DM People (Won't DM the same person twice) (Will only DM people with high chances of following you)",
                        variable=var1, bg='pink').pack()

    var2 = tkinter.IntVar()
    tkinter.Checkbutton(mframe, text="Show What Is Going On During The Process", variable=var2, bg='pink').pack()

    tkinter.Label(mframe, text="(Between each like/Follow, the app wil pause for a bit", bg='pink').pack()
    tkinter.Label(mframe, text="to avoid being detected as a Bot by Instagram.)", bg='pink').pack()

    tkinter.Button(mframe, text="Run", width=10, height=1, command=Run, bg='pink').pack(pady=5)
    tkinter.Button(mframe, text='Back', width=10, height=1, command=win6_Account, bg='pink').pack(pady=5)

def win8_Upload(event=None):
    '''
    Uploads the last downloaded picture with its caption.
    RK : If you are uploading a picture with no description, you'll need to provide one!
    '''

    def call_upload():

        global IMAGES_FILE_PATH
        if len(IMAGES_FILE_PATH)>0:
            if os.path.exists(IMAGES_FILE_PATH) and os.path.exists(IMAGES_FILE_PATH+os.sep+'Images'):
                chdir(IMAGES_FILE_PATH)
                test=0 #Boolean to check if there are pictures in database
                try:
                    for file in listdir('Images'):
                        if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('png'):
                            test=1
                            break
                except Exception:
                    test=0

            if test==0: #If No Pictures in Database
                Error_Message = tkinter.Label(mframe, text="No Picture in database! Please download a picture and add a caption.", bg='pink', width=200,
                                             font=("Courier", 10))
                Error_Message.pack()
                Error_Message.place(relx=0.5, rely=0.7, anchor='center')
                time.sleep(1.5)
                Error_Message.pack_forget()

            else: #If everything is good to go
                Wait_Message = tkinter.Label(mframe, text="Uploading, please wait...", bg='pink', width=200,
                                             font=("Courier", 18))
                Wait_Message.pack()
                Wait_Message.place(relx=0.5, rely=0.8, anchor='center')
                global USERNAME1
                global PASSWORD1
                upload(USERNAME1,PASSWORD1,IMAGES_FILE_PATH)
                Wait_Message.pack_forget()

        else:
            Invalid_Path = tkinter.Label(mframe, text="Invalid Path!", bg='pink', width=200,
                                         font=("Courier", 18))
            Invalid_Path.pack()
            time.sleep(1)
            Invalid_Path.pack_forget()

    def Uploading():
        t = threading.Thread(target=call_upload)
        t.start()

    clearwin()
    mframe.pack_propagate(0)

    info1_Message = tkinter.Label(mframe, text="This will upload the most recent picture in",
                                  bg='pink', width=200,
                                  font=("Courier", 12))
    info1_Message.pack()
    info1_Message.place(relx=0.5, rely=0.24, anchor='center')

    info2_Message = tkinter.Label(mframe,
                                  text="your database (downloaded/added manually).",
                                  bg='pink', width=200,
                                  font=("Courier", 12))
    info2_Message.pack()
    info2_Message.place(relx=0.5, rely=0.3, anchor='center')


    Upload_Button = tkinter.Button(mframe, text="Upload!", width=10, height=1, command=Uploading, bg='pink')
    Upload_Button.pack()
    Upload_Button.place(relx=0.5, rely=0.4, anchor='center')

    back = tkinter.Button(mframe, text='Back', width=10, height=1, command=win6_Account, bg='pink')
    back.pack()
    back.place(relx=0.5, rely=0.5, anchor='center')



if __name__ == '__main__':
    """
    Generates the main window
    """
    main = tkinter.Tk()
    main.config(width=800, height=600, background='pink')
    main.title('Instagram Manager')
    main.wm_iconbitmap('logo.ico')
    mframe = tkinter.Frame(main, width=800, height=600, background='pink')
    mframe.grid_propagate(0)
    mframe.pack(fill="both", expand=True, padx=20, pady=20)
    win1() #Generate Welcome Menu
    main.mainloop()
