import tkinter as tk
import customtkinter as ctk

# Theme of Application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("yellow")
ctk.deactivate_automatic_dpi_awareness()

app = ctk.CTk()

def login_screen():
    root = ctk.CTk()
    
    # Create Windows for GUI
    root.title("pt1 - Lightweight Notes")
    root.geometry('350x350')
    root.resizable(False, False)
    
    title = ctk.CTkLabel(root, text="Login", font=('Bold Calibri', 25))
    title.place(relx=0.3, rely=0.1)
    
    surname = ctk.CTkEntry(root, placeholder_text="Surname")
    surname.place(relx=0.1, rely=0.3, relwidth=0.8)
    
    name = ctk.CTkEntry(root, placeholder_text="Name")
    surname.place(relx=0.1, rely=0.5, relwidth=0.8)
    
    login_button = ctk.CTkButton(root, text="Login", command=lambda: login(surname))
    login_button.place(relx=0.1, rely=0.7, relwidth=0.8)
    
    root.mainloop()

def login(surname):
    if not len(surname.get())  == 0:
        application()
        
def application():
    app = ctk.CTk()
    app.title("pt1 - Lightweight Notes - Application")
    app.geometry('500x500')
    app.resizable(False, False)
    
    label = ctk.CTkLabel(app, text="Welcome to the Application", font=('Bold Calibri', 25))
    label.place(relx=0.1, rely=0.1)
    
    app.mainloop()

# Start the login screen
login_screen()
