import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import csv  # Import CSV module
import os
from encryption import hash_password

from init import *
from csv_manager import read_credentials_rows, write_credentials_rows
from window_utils import place_child_window

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def init_creation(self):
    """
    Sets up the account creation window with input fields and a create button.
    """
    if self.create_account_window is None or not self.create_account_window.winfo_exists():
        self.create_account_window = ctk.CTkToplevel(self.master)
        self.create_account_window.title("pt1 Lightweight Notes - Create Account")
        place_child_window(self.master, self.create_account_window, 900, 600)
        if os.name == "nt":  # if Windows
            self.create_account_window.iconbitmap(icon_path)
        else:  # if Linux or macOS
            self.create_account_window.iconphoto(True, PhotoImage(file=png_icon_path))
        self.create_account_window.resizable(False, False)

        # Background image
        background_image = ctk.CTkImage(Image.open(resource("img/signup_background.jpg")), size=(900, 600))
        background_label = ctk.CTkLabel(self.create_account_window, image=background_image, text="")
        background_label.place(relwidth=1, relheight=1)

        # Segment background frame
        seg_backgr = ctk.CTkFrame(self.create_account_window, fg_color="#1a1a1a", width=900, height=550)
        seg_backgr.pack(padx=5, pady=5, expand=True)

        # Container for inputs
        container = ctk.CTkFrame(seg_backgr, fg_color="#293133", width=500, height=400)
        container.pack(padx=10, pady=10, fill="both", expand=True)

        # Configure grid for layout
        container.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=3)

        # Profile image
        image_path = resource("img/user.png")
        profile_image = ctk.CTkImage(Image.open(image_path), size=(150, 150))
        image_label = ctk.CTkLabel(container, image=profile_image, text="")
        image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=20, sticky="n")

        # Input fields and labels
        firstname_label = ctk.CTkLabel(container, text="Surname:", fg_color="transparent")
        firstname_label.grid(row=1, column=1, padx=10, pady=(5, 0), sticky="w")  

        firstname_entry = ctk.CTkEntry(container, placeholder_text="Enter your Surname...")
        firstname_entry.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="ew")  

        password_label = ctk.CTkLabel(container, text="Password:", fg_color="transparent")
        password_label.grid(row=3, column=1, padx=10, pady=(5, 0), sticky="w")  

        password_entry = ctk.CTkEntry(container, placeholder_text="Enter your Password...", show="*")
        password_entry.grid(row=4, column=1, padx=10, pady=(0, 5), sticky="ew")  

        confirm_password_label = ctk.CTkLabel(container, text="Confirm Password:", fg_color="transparent")
        confirm_password_label.grid(row=5, column=1, padx=10, pady=(2, 0), sticky="w")  

        confirm_password_entry = ctk.CTkEntry(container, placeholder_text="Enter your Password... again", show="*")
        confirm_password_entry.grid(row=6, column=1, padx=10, pady=(0, 5), sticky="ew")  

        # Create button
        create_button = ctk.CTkButton(container, text="Create", command=lambda: create_account(
            self,
            firstname_entry.get(),
            password_entry.get(),
            confirm_password_entry.get()
        ))
        create_button.grid(row=6, column=0, padx=20, pady=20, sticky="sw", columnspan=2)  # Aligned to bottom-left

        # Ensure the window stays on top
        self.create_account_window.after(100, self.create_account_window.lift)



import random

def create_account(self, get_firstname, get_password, get_confirmation):
    """
    Validates inputs and creates a new account if no duplicate exists.
    """
    
    # Check if any field is empty
    empty_field_message = check_if_empty(get_firstname, get_password, get_confirmation)

    if empty_field_message:
        display_message(self, empty_field_message, "red", 2000)
        return  # Stop account creation if fields are empty
    

    if not check_password_compliance(get_password, get_confirmation):
        display_message(self, "Passwords do not match or are not compliant.", "red", 2000)
        return

    try:
        existing_users = read_credentials_rows()
    except (FileNotFoundError, ValueError):
        existing_users = []

    if get_firstname in [row.get("first_name", "") for row in existing_users]:
        display_message(self, "An account with this name already exists.", "red", 2000)
        return

    # Generate a unique random UID
    existing_uids = set()
    for row in existing_users:
        uid_val = row.get("uid", "")
        try:
            existing_uids.add(int(uid_val))
        except (TypeError, ValueError):
            pass

    new_uid = random.randint(100000, 999999)  # Generate a random 6-digit UID
    while new_uid in existing_uids:  # Ensure the UID is unique
        new_uid = random.randint(100000, 999999)

    existing_users.append({
        "uid": str(new_uid),
        "first_name": get_firstname,
        "password": hash_password(get_password),
    })
    write_credentials_rows(existing_users)

    display_message(self, f"Account created successfully! UID: {new_uid}", "green", 2000)


def check_password_compliance(get_password, get_confirmation):
    """
    Checks if the password and confirmation match.
    """
    return get_password == get_confirmation

def check_if_empty(get_firstname, get_password, get_confirmation):
    """
    Checks if any input is empty and returns False.
    """
    if not get_firstname.strip():
        return "Please fill in your Surname."
    if not get_password.strip():
        return "Please enter your Password."
    if not get_confirmation.strip():
        return "Please confirm your Password."
    return None  # All fields are valid

def display_message(self, message, color, duration=None):
        """
        Override function from init.py - display_message.
        Displays a message on the create account window. 
        Why not use the function from init.py? Because the message will be displayed there,
        which is very hard to see, especially if create account window is initialised toplevel.
        """
        self.message_label = ctk.CTkLabel(self.create_account_window, text=message, font=('Bold Calibri', 12), text_color=color)
        self.message_label.place(relx=0.3, rely=0.75, relwidth=0.4)

        if duration:
            self.master.after(duration, self.message_label.destroy)
