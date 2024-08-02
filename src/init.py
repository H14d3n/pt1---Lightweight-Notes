import tkinter as tk
import customtkinter as ctk
import csv
import pandas

# Theme of Application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
ctk.deactivate_automatic_dpi_awareness()

app = ctk.CTk()

def login_screen():
    # Create Windows for GUI
    app.title("pt1 - Lightweight Notes")
    app.geometry('350x350')
    app.resizable(False, False)
    
    title = ctk.CTkLabel(app, text="Login", font=('Bold Calibri', 25))
    title.place(relx=0.40625, rely=0.1)
    
    surname = ctk.CTkEntry(app, placeholder_text="Surname")
    surname.place(relx=0.1, rely=0.3, relwidth=0.8)
    
    password = ctk.CTkEntry(app, placeholder_text="Password")
    password.configure(show="*")
    password.place(relx=0.1, rely=0.5, relwidth=0.8)
    
    login_button = ctk.CTkButton(app, text="Login", command=lambda: login(surname, password))
    login_button.place(relx=0.1, rely=0.7, relwidth=0.8)
    

def login(surname, password):
    # Check if user put in information, after that check which user and authentificate
    if not (len(surname.get()) and len(password.get())) == 0:
        with open('login.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for user in reader:
                user = print(row['first_name'])
                user_password = print(row['password'])
            if (surname.get() and password.get() == user, user_password):
                application()

def application():
    for widget in app.winfo_children():
        widget.destroy()
    
    app.title("pt1 - Lightweight Notes - ")
    app.geometry('500x500')
    
    label = ctk.CTkLabel(app, text="Welcome to the Application", font=('Bold Calibri', 25))
    label.place(relx=0.1, rely=0.1)
    

# Start the login screen everything else is initialised from there on
login_screen()
app.mainloop()
