import tkinter as tk
import customtkinter as ctk
import csv
import os
import platform
from CTkMenuBar import *
from PIL import Image
from tkinter import filedialog, Text
import datetime
from PIL import Image, ImageTk

# Import the CSV-Management module
from csv_manager import *
from editing_mode import *
from create_account import *

"""
ToDo:
 * Account creator
 * (Optional) Add Editor functionalities.
"""

# Global configurations
ctk.set_appearance_mode("white")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()

runpath = os.getcwd()
csv_file_path = get_csv_path() # Function is in csv_manager.py
font_path = f'{runpath}\\src\\fonts\\Quicksand-Light.ttf'



class LightweightNotesApp:
    """
    Main Application Window for pt1 - Lightweight Notes.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("pt1 - Lightweight Notes")
        self.master.geometry('350x350')
        self.master.resizable(False, False)
        self.uid = None
        self.settings_window = None
        self.about_window = None
        self.current_file_path = None  # To track the file being edited
        self.current_text_area = None  # To track the text area in editing mode
        self.init_login_screen()

    def init_login_screen(self):
        """
        Initializes and displays the login screen.
        """
        self.clear_window()

        title = ctk.CTkLabel(self.master, text="Login", font=('Bold Calibri', 25))
        title.place(relx=0.40625, rely=0.1)

        self.surname_entry = ctk.CTkEntry(self.master, placeholder_text="Surname", corner_radius=14)
        self.surname_entry.place(relx=0.1, rely=0.25, relwidth=0.8)

        self.password_entry = ctk.CTkEntry(self.master, placeholder_text="Password", corner_radius=14)
        self.password_entry.configure(show="*")
        self.password_entry.place(relx=0.1, rely=0.45, relwidth=0.8)

        login_button = ctk.CTkButton(self.master, text="Login", command=self.handle_login)
        login_button.place(relx=0.1, rely=0.65, relwidth=0.8)
        
        or_label = ctk.CTkLabel(self.master, text="or")
        or_label.place(relx=0.475, rely=0.75)

        create_account_button = ctk.CTkButton(self.master, text="Create Account", command=create_account)
        create_account_button.place(relx=0.25, rely=0.85, relwidth=0.5)

        self.message_label = None

    def handle_login(self):
        """
        Handles the login process.
        """
        self.display_message("")
        surname = self.surname_entry.get()
        password = self.password_entry.get()

        if surname and password:
            self.check_credentials(surname, password)
        else:
            self.display_message("Please enter both surname and password.")

    def check_credentials(self, surname, password):
        """
        Checks the entered credentials.
        """
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row['first_name'] == surname and row['password'] == password:
                    self.uid = row['uid']
                    self.init_application()
                    return
        self.display_message("Invalid credentials.")

    def display_message(self, message):
        """
        Displays a message on the login screen.
        """
        if self.message_label:
            self.message_label.destroy()

        self.message_label = ctk.CTkLabel(self.master, text=message, font=('Bold Calibri', 12), text_color="red")
        self.message_label.place(relx=0.1, rely=0.55, relwidth=0.8)

    def clear_window(self):
        """
        Clears all widgets from the current window.
        """
        for widget in self.master.winfo_children():
            widget.destroy()

    def init_application(self):
        """
        Initializes the main application interface.
        """
        self.clear_window()

        self.master.geometry('800x600')
        self.master.minsize(width=850, height=510)
        self.master.resizable(True, True)

        self.init_menu_bar()
        self.init_dashboard()

    def init_menu_bar(self):
        """
        Initializes the menu bar with various options.
        """
        menu = CTkMenuBar(master=self.master)
        opt_file = menu.add_cascade("File")
        opt_edit = menu.add_cascade("Edit")
        opt_settings = menu.add_cascade("Settings")
        opt_about = menu.add_cascade("About")

        file_menu = CustomDropdownMenu(widget=opt_file)
        file_menu.add_option(option="New", command=self.create_document)
        file_menu.add_option(option="Open", command=self.open_document)
        file_menu.add_option(option="Save", command=self.save_current_document)

        file_menu.add_separator()

        export_sub_menu = file_menu.add_submenu("Export As >>")
        export_sub_menu.add_option(option=".PDF", command=lambda: print("Exported as PDF"))
        export_sub_menu.add_option(option=".docx", command=lambda: print("Exported as docx"))

        file_menu.add_option(option="Save as", command=self.create_document)
        file_menu.add_option(option="Rename", command=lambda: print("Renamed"))
        file_menu.add_option(option="Exit", command=self.master.destroy)

        edit_menu = CustomDropdownMenu(widget=opt_edit)
        edit_menu.add_option(option="Cut (CTRL + X)")
        edit_menu.add_option(option="Copy (CTRL + C)")
        edit_menu.add_option(option="Paste (CTRL + V)")

        settings_menu = CustomDropdownMenu(widget=opt_settings)
        settings_menu.add_option(option="Settings", command=self.open_settings)

        about_menu = CustomDropdownMenu(widget=opt_about)
        about_menu.add_option(option="About pt1 - Lightweight Notes", command=self.open_about)

    def save_current_document(self):
        """
        Saves the currently open document.
        """
        if self.current_file_path and self.current_text_area:
            save_document(self, self.current_file_path, self.current_text_area)
        else:
            self.display_message("No document is currently open for saving.")

    def init_dashboard(self):
        """
        Sets up the main dashboard where users can access actions like creating 
        new documents, opening existing ones, or adjusting settings.
        """
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
        """
        Helper method to create a frame with a button on the dashboard for different 
        actions (e.g., Create, Open, Settings).
        """
        action_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", width=250, height=256)
        action_frame.grid(row=0, column=column_index, padx=10, pady=10, sticky="nsew")

        # Create Icon
        white_plus_path = f"{runpath}/src/img/PlusWhite.png"
        black_plus_path = f"{runpath}/src/img/PlusBlack.png"

        create_image = ctk.CTkImage(light_image=Image.open(white_plus_path),
                                           dark_image=Image.open(black_plus_path),
                                           size=(100,100))

        create_image_label = ctk.CTkLabel(container, text="", image=create_image)
        create_image_label.place(relx=0.1625, rely=0.3, anchor="center")

        # Open Icon
        white_open_path = f"{runpath}/src/img/FolderWhite.png"
        black_open_path = f"{runpath}/src/img/FolderBlack.png"

        create_image = ctk.CTkImage(light_image=Image.open(white_open_path),
                                           dark_image=Image.open(black_open_path),
                                           size=(100,100))

        open_image_label = ctk.CTkLabel(container, text="", image=create_image)
        open_image_label.place(relx=0.5, rely=0.3, anchor="center")

        # Settings Icon
        white_settings_path = f"{runpath}/src/img/SettingsWhite.png"
        black_settings_path = f"{runpath}/src/img/SettingsBlack.png"

        create_image = ctk.CTkImage(light_image=Image.open(white_settings_path),
                                           dark_image=Image.open(black_settings_path),
                                           size=(100,100))

        settings_image_label = ctk.CTkLabel(container, text="", image=create_image)
        settings_image_label.place(relx=0.83125, rely=0.3, anchor="center")

        button = ctk.CTkButton(action_frame, text=label_text, command=command)
        button.place(relx=0.25, rely=0.7, relwidth=0.5, relheight=0.2)

    def create_document(self):
        """
        Handles the creation of a new document, including opening a file dialog 
        and saving the document's metadata.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".pt1", 
                                                 filetypes=[("pt1 Files", "*.pt1"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w+') as file:
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"uid:{self.uid}\n")
                file.write(f"date:{date}\n")
                file.write("\n")  # Add an extra newline if desired for formatting
                file.flush()

            self.edit_document(file_path) 

    def open_document(self):
        """
        Opens an existing document by allowing the user to select a file from a file dialog.
        """
        file_path = filedialog.askopenfilename(title="Open Document", 
                                               filetypes=[("pt1 Files", "*.pt1"), ("All Files", "*.*")])
        if file_path:
            self.edit_document(file_path)

    def edit_document(self, file_path):
        """
        Manages the editing process of an opened document by providing the functionality 
        to write to the file.
        """
        with open(file_path, 'r') as file:
            first_line = file.readline()
            print(f"Checking UID in file: {first_line.strip()}") 

            if self.uid in first_line:
                print(f"Editing file: {file_path}")
                self.clear_window()
                editing_mode(self, file_path)
            else:
                print("You don't have permission to edit this file.")


    def open_settings(self):
        """
        Opens the settings window where users can adjust application settings, 
        such as changing themes. Prevents opening multiple instances of the settings window.
        """
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = ctk.CTkToplevel(self.master)
            self.settings_window.title("pt1 Lightweight Notes - Settings")
            self.settings_window.geometry("400x200")
            self.settings_window.resizable(False, False)
            self.settings_window.after(100, self.settings_window.lift)

            # Add close callback to set reference to None when the window is closed
            self.settings_window.protocol("WM_DELETE_WINDOW", self.on_settings_close)

            settings_change_theme_label = ctk.CTkLabel(self.settings_window, text="Change Theme")
            settings_change_theme_label.place(relx=0.03, rely=0.05)

            light_theme_button = ctk.CTkButton(self.settings_window, text="Light", command=lambda: print("Light Mode"))
            light_theme_button.place(relx=0.03, rely=0.2, relwidth=0.2, relheight=0.1)

            dark_theme_button = ctk.CTkButton(self.settings_window, text="Dark", command=lambda: print("Dark Mode"))
            dark_theme_button.place(relx=0.03, rely=0.325, relwidth=0.2, relheight=0.1)
    
    def on_settings_close(self):
        """
        Handles the event when the settings window is closed, ensuring the application
        knows the window is no longer open.
        """
        self.settings_window.destroy()
        self.settings_window = None

    def open_about(self):
        """
        Opens the 'About' window. Ensures only one instance is open at a time.
        """
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = ctk.CTkToplevel(self.master)
            self.about_window.title("pt1 Lightweight Notes - About")
            self.about_window.geometry("210x105")
            self.about_window.resizable(False, False)

            # Add content to the About window
            about_label = ctk.CTkLabel(
                self.about_window, 
                text="pt1 - Lightweight Notes\n-------------\nVersion 1.0\nCreated by Tizian Imseng", 
                justify="center", 
                font=('Bold Calibri', 14)
            )
            about_label.pack(pady=20, padx=20)

            # Intercept the window close event
            self.about_window.protocol("WM_DELETE_WINDOW", self.close_about)
            self.about_window.after(100, self.about_window.lift)

    def close_about(self):
        """
        Handles closing the 'About' window and resetting its reference.
        """
        if self.about_window is not None:
            self.about_window.destroy()
            self.about_window = None


# Initialize the application
if __name__ == "__main__":
    create_csv() # Function is in csv_manager.py
    app = ctk.CTk()
    LightweightNotesApp(app)
    app.mainloop()
    
