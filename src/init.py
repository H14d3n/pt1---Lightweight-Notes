import tkinter as tk
import customtkinter
import subprocess
import os

# Theme of Application
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("yellow")
customtkinter.deactiviate_automatic_dpi_awareness()

app = customtkinter.Ctk()

def login_screen():
    root = customtkinter.CTk()
    
    # Create Windows for GUI
    root.title("pt1 - Lightweight Notes")
    root.geometry('350x350')
    root.resizable(False, False)
    
    title = customtkinter.CTkLabel(root, font=('Bold Calibri, 25'))
    title.place(relx=0.3, rely=0.3)
    
    surname = customtkinter.CtkEntry(root, placeholder_text="Surname")
    surname.place(relx=1, rely=1)
    
    login = customtkinter.CTkButton(root, placeholder_text="Login", command=login )
    login.place(relx=1.3, rely=1.3)
    
    
    def login():
        if not len(surname.get()) == 0:
            application()
            
        
        
def application():
            
    app.mainloop()
    
    