import tkinter as tk
import customtkinter as ctk
import csv
import os
from CTkMenuBar import *
from PIL import Image

# Theme of Application
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()


runpath = os.getcwd()
csv_file_path = f'{runpath}/src/login.csv'
font_path = f'{runpath}/src/fonts/Quicksand-Light.ttf'

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

def exit_sidewindow():
    for widget in app.winfo_children(): 
        widget.destroy()    
     
def application(): 
    exit_sidewindow()
        
    appwidth = 800
    appheight = 600
    startup = True
    app.minsize(width=850, height=510)
     
    app.title("pt1 - Lightweight Notes") 
    app.geometry(f'{appwidth}x{appheight}') 
    app.resizable(True, True)
    
    menu = CTkMenuBar(master=app)
    opt_file = menu.add_cascade("File")
    opt_edit = menu.add_cascade("Edit")
    opt_settings = menu.add_cascade("Settings")
    opt_about = menu.add_cascade("About")
    
    dropdown1 = CustomDropdownMenu(widget=opt_file)
    dropdown1.add_option(option="Neu", command=lambda: print("Created"))
    dropdown1.add_option(option="Open", command=lambda: print("Opened"))
    dropdown1.add_option(option="Save", command=lambda: print("Saved"))
    
    dropdown1.add_separator()
    
    sub_menu1 = dropdown1.add_submenu("Export As")
    sub_menu1.add_option(option=".PDF")
    sub_menu1.add_option(option=".docx")
    
    dropdown1.add_option(option="Save as", command=lambda: print("Saved as"))
    dropdown1.add_option(option="Rename", command=lambda: print("Renamed"))
    dropdown1.add_option(option="Exit", command=lambda:app.destroy())
    
    dropdown2 = CustomDropdownMenu(widget=opt_edit)
    dropdown2.add_option(option="Cut (CTRL + X)")
    dropdown2.add_option(option="Copy (CTRL + C)")
    dropdown2.add_option(option="Paste (CTRL + V)")
    
    dropdown3 = CustomDropdownMenu(widget=opt_settings)
    dropdown3.add_option(option="Settings")
    
    dropdown4 = CustomDropdownMenu(widget=opt_about)
    dropdown4.add_option(option="About pt1 - Lightweight Notes")
    
    if startup:
    
        seg_backgr = ctk.CTkFrame(
             app,
            fg_color="#36454F"
        )
        seg_backgr.pack(pady=10, padx=10, fill="both", expand=True)
    
        welcome = ctk.CTkLabel(app, text="Welcome to pt1 - Lightweight Notes", font=(f"{font_path}", 50))
        welcome.pack(pady=(10, 20))  
    
        container = ctk.CTkFrame(seg_backgr, fg_color="#36454F")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure([0, 1, 2], weight=1)

        seg_create = ctk.CTkFrame(
            container,
            fg_color="#FFFFFF",
            width=250,
            height=256
        )
        seg_create.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
        seg_open = ctk.CTkFrame(
            container,
            fg_color="#FFFFFF",
            width=250,
            height=256
        )
        seg_open.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") 
         
        seg_settings = ctk.CTkFrame( 
            container, 
            fg_color="#FFFFFF", 
            width=250, 
            height=256 
        ) 
        seg_settings.grid(row=0, column=2, padx=10, pady=10, sticky="nsew") 

        img_create = ctk.CTkImage(light_image=Image.open('img/PlusBlack.png'), 
                                  dark_image=Image.open('img/PlusWhite.png'),
                                  size=(64,64)) # Width x Height

# Start the login screen; everything else is initialized from there on 
login_screen() 
app.mainloop()