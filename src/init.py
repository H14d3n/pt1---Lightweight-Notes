import tkinter as tk
import customtkinter as ctk
import csv
import os
from CTkMenuBar import *

# Theme of Application
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")


runpath = os.getcwd()
csv_file_path = f'{runpath}/src/login.csv'

app = ctk.CTk()

def login_screen():
    # Create Windows for GUI
    app.title("pt1 - Lightweight Notes")
    app.geometry('350x350')
    app.resizable(False, False)
    
    title = ctk.CTkLabel(app, text="Login", font=('Bold Calibri', 25))
    title.place(relx=0.40625, rely=0.1)
    
    surname = ctk.CTkEntry(app, placeholder_text="Surname", corner_radius=14)
    surname.place(relx=0.1, rely=0.3, relwidth=0.8,)
    
    password = ctk.CTkEntry(app, placeholder_text="Password", corner_radius=14)
    password.configure(show="*")
    password.place(relx=0.1, rely=0.5, relwidth=0.8)
    
    login_button = ctk.CTkButton(app, text="Login", command=lambda: login(surname, password, csv_file_path))
    login_button.place(relx=0.1, rely=0.7, relwidth=0.8)
    

def login(surname, password, csv_file_path):
    display_message("")
    # Check if user put in information, after that check which user and authenticate
    if len(surname.get()) > 0 and len(password.get()) > 0:
        check_credentials(csv_file_path, surname, password)
    else:
        display_message("Please enter both surname and password.")  
        
                
def check_credentials(csv_file_path, surname, password):
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['first_name'] == surname.get() and row['password'] == password.get():
                application()
                return
        display_message("Invalid credentials.")  
         
         
def display_message(message): 
    message_label = ctk.CTkLabel(app, text=message, font=('Bold Calibri', 12), text_color="red") 
    message_label.place(relx=0.1, rely=0.8, relwidth=0.8) 
     
 
def application(): 
    for widget in app.winfo_children(): 
        widget.destroy() 
     
    app.title("pt1 - Lightweight Notes") 
    app.geometry('500x500') 
    app.resizable(True, True)
    
    menu = CTkMenuBar(master=app)
    menu.add_cascade("Menu")
    menu.add_cascade("Edit")
    menu.add_cascade("Settings")
    menu.add_cascade("About")
    
    
# Start the login screen; everything else is initialized from there on 
login_screen() 
app.mainloop() 
