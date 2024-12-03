from tkinter import scrolledtext
import tkinter as tk
import customtkinter as ctk


def editing_mode(self, file_path):
    """
    Manages the editing process of an opened document.
    """
    self.init_menu_bar()

    # Set up a title and text area for editing
    title_label = ctk.CTkLabel(self.master, text="Editing Document", font=('Bold Calibri', 20))
    title_label.pack(pady=(10, 5))

    # Scrolled text widget for the document's content
    text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=100, height=25, undo=True)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Store the current file path and text area for Save functionality
    self.current_file_path = file_path
    self.current_text_area = text_area

    # Load and display the content of the file in the text area
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text_area.insert(tk.END, content)
    except Exception as e:
        print(f"Error reading file: {e}")
        self.display_message("Failed to load document content.", "red")

    # Bind undo and redo to CTRL+Z and CTRL+Y
    text_area.bind("<Control-z>", lambda event: text_area.edit_undo())
    text_area.bind("<Control-y>", lambda event: text_area.edit_redo())

    # Bind CTRL+S to the save function
    text_area.bind("<Control-s>", lambda event: save_document(self, file_path, text_area))
    text_area.bind("<Control-q>", lambda event: self.init_application())

    # Save button
    save_button = ctk.CTkButton(self.master, text="Save (CTRL + S)", command=lambda: save_document(self, file_path, text_area))
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Return to Dashboard button
    back_button = ctk.CTkButton(self.master, text="Back to Dashboard (CTRL + Q)", command=self.init_application)
    back_button.pack(side=tk.RIGHT, padx=10, pady=10)
  

def save_document(self, file_path, text_area):
    """
    Saves the current content of the text area back to the specified file.
    """
    content = text_area.get("1.0", tk.END)  # Get all text from the text area
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        self.display_message("Document saved successfully.", "green", duration=2000)
    except Exception as e:
        print(f"Error saving file: {e}")
        self.display_message("Failed to save document.", "red", duration=2000)