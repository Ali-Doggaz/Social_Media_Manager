from tkinter import *
from PIL import ImageTk, Image
from os import listdir
import csv
i = 0

def load(): #Load all the stored captions
    data = dict()
    with open('Descriptions_File','r') as f:
        reader =csv.DictReader(f, delimiter=',')
        for row in reader:
            url = row['url']
            data[url] = row['description']
    f.close()
    return data

def save(Descriptions): #Save the new added Descriptions
    with open('Descriptions_File','w') as f:
        f.write("url,description\n")
        mycsv = csv.writer(f)
        for url in Descriptions.keys():
            mycsv.writerow([url, Descriptions[url]])

def add_description(): #Displays each image and ask the user to input a corresponding caption.
    Descriptions = load()
    window = Tk() #This will be the only window used.
    window.title('Instagram Captions')
    window.geometry("1080x720")
    window.config(background='#41B77F')
    imgs=[]

    def myClick(event=None): #Display Next picture
        global i
        i = i + 1

        #get the description of image n*i
        save(Descriptions)
        if i>len(imgs):
            save(Descriptions)
            window.destroy()
            exit("Done")
        Descriptions[imgs[i-1]] = T.get("1.0",'end')

        if i >= len(imgs): #If we reached the last image
            save(Descriptions)
            window.destroy()
            exit("Done")

        T.delete("1.0",'end')
        Images = Image.open(imgs[i])
        basewidth = 350
        wpercent = (basewidth / float(Images.size[0]))
        hsize = int((float(Images.size[1]) * float(wpercent)))
        Image_copy = Images.resize((basewidth, hsize), Image.ANTIALIAS)
        img_label.img = ImageTk.PhotoImage(Image_copy)
        img_label.config(image=img_label.img)
        img_label.image = img_label.img
        if imgs[i] in Descriptions: #If the picture already has a description, diplay it in the text area
            T.insert("1.0", Descriptions[imgs[i]])
        else: #If the picture doesn't has any desc, put these generic tags in the text area
            T.insert("1.0",'\n.\n.\n.\n.\n#Food #Cake #Beauty #Desserts #Delicious #Yummy #FoodPorn #FoodPhotography #Foodie #Baking #foodstagram')

    def Back(event=None): #Go back to previous picture
        global i
        i = i-2
        myClick()

    for picture in sorted(listdir('Images')): #Store all the Images' Path in imgs []
        path = fr'Images\{picture}'
        imgs.append(path)

    #Opens the first Image with an adequate format (size)

    Images = Image.open(imgs[0])
    basewidth = 350
    wpercent = (basewidth / float(Images.size[0]))
    hsize = int((float(Images.size[1]) * float(wpercent)))
    Image_copy = Images.resize((basewidth, hsize), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(Image_copy)
    img_label = Label(window, image=photo)
    img_label.pack(padx=10,pady=10)

    #Adding the entry box

    T = Text(window, height=10, width=40)
    if imgs[0] in Descriptions:
        T.insert("1.0", Descriptions[imgs[0]])
    else:
        T.insert("1.0", '\n.\n.\n.\n.\n#Food #Cake #Beauty #Desserts #Delicious #Yummy #FoodPorn #FoodPhotography #Foodie #Baking #foodstagram')

    T.pack()

    #add_button
    my_button = Button(window, text="Add Description", command = lambda : myClick()) #Add 'Next_Picture' Button to go to the next picture
    my_button.pack(padx=10)
    T.bind('<Right>', func=myClick)
    T.bind('<Left>', func=Back)

    window.mainloop()
