import tkinter as tk
import customtkinter as ctk
import csv
import os
from CTkMenuBar import *
from PIL import Image
from tkinter import filedialog, Text
import datetime


# Global configurations
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()

runpath = os.getcwd()
csv_file_path = f'{runpath}/src/login.csv'
font_path = f'{runpath}/src/fonts/Quicksand-Light.ttf'


class LightweightNotesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("pt1 - Lightweight Notes")
        self.master.geometry('350x350')
        self.master.resizable(False, False)
        self.uid = None
        
        self.init_login_screen()

    def init_login_screen(self):
        """Initialize login screen components."""
        self.clear_window()

        title = ctk.CTkLabel(self.master, text="Login", font=('Bold Calibri', 25))
        title.place(relx=0.40625, rely=0.1)

        self.surname_entry = ctk.CTkEntry(self.master, placeholder_text="Surname", corner_radius=14)
        self.surname_entry.place(relx=0.1, rely=0.3, relwidth=0.8)

        self.password_entry = ctk.CTkEntry(self.master, placeholder_text="Password", corner_radius=14)
        self.password_entry.configure(show="*")
        self.password_entry.place(relx=0.1, rely=0.5, relwidth=0.8)

        login_button = ctk.CTkButton(self.master, text="Login", command=self.handle_login)
        login_button.place(relx=0.1, rely=0.7, relwidth=0.8)

        self.message_label = None

    def handle_login(self):
        """Handle login logic and authentication."""
        self.display_message("")
        surname = self.surname_entry.get()
        password = self.password_entry.get()
        
        if surname and password:
            self.check_credentials(surname, password)
        else:
            self.display_message("Please enter both surname and password.")

    def check_credentials(self, surname, password):
        """Check user credentials against CSV file."""
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row['first_name'] == surname and row['password'] == password:
                    self.uid = row['uid']
                    self.init_application()
                    return
        self.display_message("Invalid credentials.")

    def display_message(self, message):
        """Display a message in the login screen."""
        if self.message_label:
            self.message_label.destroy()
        
        self.message_label = ctk.CTkLabel(self.master, text=message, font=('Bold Calibri', 12), text_color="red")
        self.message_label.place(relx=0.1, rely=0.8, relwidth=0.8)

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def init_application(self):
        """Initialize main application window after successful login."""
        self.clear_window()

        self.master.geometry('800x600')
        self.master.minsize(width=850, height=510)
        self.master.resizable(True, True)

        self.init_menu_bar()
        self.init_dashboard()

    def init_menu_bar(self):
        """Initialize the menu bar for the application."""
        menu = CTkMenuBar(master=self.master)
        opt_file = menu.add_cascade("File")
        opt_edit = menu.add_cascade("Edit")
        opt_settings = menu.add_cascade("Settings")
        opt_about = menu.add_cascade("About")

        file_menu = CustomDropdownMenu(widget=opt_file)
        file_menu.add_option(option="Neu", command=self.create_document)
        file_menu.add_option(option="Open", command=self.open_document)
        file_menu.add_option(option="Save", command=lambda: print("Saved"))

        file_menu.add_separator()

        export_sub_menu = file_menu.add_submenu("Export As")
        export_sub_menu.add_option(option=".PDF")
        export_sub_menu.add_option(option=".docx")

        file_menu.add_option(option="Save as", command=lambda: print("Saved as"))
        file_menu.add_option(option="Rename", command=lambda: print("Renamed"))
        file_menu.add_option(option="Exit", command=self.master.destroy)

        edit_menu = CustomDropdownMenu(widget=opt_edit)
        edit_menu.add_option(option="Cut (CTRL + X)")
        edit_menu.add_option(option="Copy (CTRL + C)")
        edit_menu.add_option(option="Paste (CTRL + V)")

        settings_menu = CustomDropdownMenu(widget=opt_settings)
        settings_menu.add_option(option="Settings", command=self.open_settings)

        about_menu = CustomDropdownMenu(widget=opt_about)
        about_menu.add_option(option="About pt1 - Lightweight Notes")

    def init_dashboard(self):
        """Initialize the dashboard with available actions."""
        seg_backgr = ctk.CTkFrame(self.master, fg_color="#36454F")
        seg_backgr.pack(pady=10, padx=10, fill="both", expand=True)

        welcome = ctk.CTkLabel(self.master, text="Welcome to pt1 - Lightweight Notes", font=(f"{font_path}", 50))
        welcome.pack(pady=(10, 20))

        container = ctk.CTkFrame(seg_backgr, fg_color="#36454F")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure([0, 1, 2], weight=1)

        self.create_action_frame(container, "Create", self.create_document, 0)
        self.create_action_frame(container, "Open", self.open_document, 1)
        self.create_action_frame(container, "Settings", self.open_settings, 2)

    def create_action_frame(self, container, label_text, command, column_index):
        """Helper function to create action frames for dashboard."""
        action_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", width=250, height=256)
        action_frame.grid(row=0, column=column_index, padx=10, pady=10, sticky="nsew")

        button = ctk.CTkButton(action_frame, text=label_text, command=command)
        button.place(relx=0.25, rely=0.7, relwidth=0.5, relheight=0.2)

    def create_document(self):
        """Handle creating a new document."""
        file_path = filedialog.asksaveasfilename(defaultextension=".pt1", 
                                                 filetypes=[("pt1 Files", "*.pt1"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                date = datetime.datetime.now()
                file.write(f"uid:{self.uid}\n")
                file.write(f"title:test\n")
                file.write(f"date:{date}\n")
                file.write("\n")
            self.edit_document(file_path)

    def open_document(self):
        """Handle opening an existing document."""
        file_path = filedialog.askopenfilename(title="Open Document", 
                                               filetypes=[("pt1 Files", "*.pt1"), ("All Files", "*.*")])
        if file_path:
            self.edit_document(file_path)

    def edit_document(self, file_path):
        """Handle editing a document."""
        with open(file_path, 'w') as file:
            print(f"Editing file: {file_path}")

    def open_settings(self):
        """Open settings window."""
        settings_window = ctk.CTkToplevel(self.master)
        settings_window.title("pt1 Lightweight Notes - Settings")
        settings_window.geometry("400x200")
        settings_window.resizable(False, False)

        settings_change_theme_label = ctk.CTkLabel(settings_window, text="Change Theme")
        settings_change_theme_label.place(relx=0.03, rely=0.05)

        light_theme_button = ctk.CTkButton(settings_window, text="Light", command=lambda: print("Light Mode"))
        light_theme_button.place(relx=0.03, rely=0.2, relwidth=0.2, relheight=0.1)

        dark_theme_button = ctk.CTkButton(settings_window, text="Dark", command=lambda: print("Dark Mode"))
        dark_theme_button.place(relx=0.03, rely=0.325, relwidth=0.2, relheight=0.1)


# Initialize the application
if __name__ == "__main__":
    app = ctk.CTk()
    LightweightNotesApp(app)
    app.mainloop()
