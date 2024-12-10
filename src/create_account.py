import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import csv  # Import CSV module

from init import *
from csv_manager import csv_file_path

def init_creation(self):
    """
    Sets up the account creation window with input fields and a create button.
    """
    if self.create_account_window is None or not self.create_account_window.winfo_exists():
        self.create_account_window = ctk.CTkToplevel(self.master)
        self.create_account_window.title("pt1 Lightweight Notes - Create Account")
        self.create_account_window.geometry("900x600")
        self.create_account_window.resizable(False, False)

        background_image = ctk.CTkImage(Image.open(f"{runpath}\\src\\img\\signup_background.jpg"), size=(900, 600))
        background_label = ctk.CTkLabel(self.create_account_window, image=background_image, text="")
        background_label.place(relwidth=1, relheight=1)

        seg_backgr = ctk.CTkFrame(self.create_account_window, fg_color="#1a1a1a", width=800, height=500)
        seg_backgr.pack(padx=5, pady=5, expand=True)

        container = ctk.CTkFrame(seg_backgr, fg_color="#293133", width=500, height=400)
        container.pack(padx=5, pady=5, fill="both", expand=True)

        container.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=3)

        image_path = f"{runpath}\\src\\img\\user.png"
        profile_image = ctk.CTkImage(Image.open(image_path), size=(150, 150))
        image_label = ctk.CTkLabel(container, image=profile_image, text="")
        image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=20, sticky="n")

        firstname_label = ctk.CTkLabel(container, text="Surname:", fg_color="transparent")
        firstname_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        firstname_entry = ctk.CTkEntry(container, placeholder_text="Enter your Surname...")
        firstname_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        password_label = ctk.CTkLabel(container, text="Password:", fg_color="transparent")
        password_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        password_entry = ctk.CTkEntry(container, placeholder_text="Enter your Password...", show="*")
        password_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        confirm_password_label = ctk.CTkLabel(container, text="Confirm Password:", fg_color="transparent")
        confirm_password_label.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        confirm_password_entry = ctk.CTkEntry(container, placeholder_text="Enter your Password... again", show="*")
        confirm_password_entry.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        create_button = ctk.CTkButton(container, text="Create", command=lambda: create_account(
            self,
            firstname_entry.get(),
            password_entry.get(),
            confirm_password_entry.get()
        ))
        create_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.create_account_window.after(100, self.create_account_window.lift)


def create_account(self, get_firstname, get_password, get_confirmation):
    """
    Validates inputs and creates a new account if no duplicate exists.
    """
    if not check_password_compliance(get_password, get_confirmation):
        self.display_message("Passwords do not match or are not compliant.", "red", 2000)
        return

    try:
        # Open the CSV file in read mode to check for duplicates and count rows
        existing_users = []
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=";")  # Ensure delimiter matches write operation
            for row in reader:
                existing_users.append(row)

        # Check if the file has a header and extract content accordingly
        if existing_users and get_firstname in [row[1] for row in existing_users[1:]]:
            self.display_message("An account with this name already exists.", "red", 2000)
            return

        # Calculate UID based on the number of entries (excluding header)
        new_uid = len(existing_users)  # Header is excluded automatically since it isn't a user entry

    except FileNotFoundError:
        # If the file doesn't exist, start with UID 1
        new_uid = 1

    # Write the new account information to the CSV
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=";")  # Use `;` as the delimiter
        writer.writerow([new_uid, get_firstname, get_password])  # Pass data as a list

    self.display_message(f"Account created successfully! UID: {new_uid}", "green", 2000)


def check_password_compliance(get_password, get_confirmation):
    """
    Checks if the password and confirmation match.
    """
    return get_password == get_confirmation


