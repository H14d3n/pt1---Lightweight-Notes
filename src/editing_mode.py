from tkinter import scrolledtext
from init import *

def editing_mode(self, file_path):
    """
    Manages the editing process of an opened document by providing the functionality
    to write to the file.
    """
    self.clear_window()
    self.init_menu_bar()

    # Set up a title and text area for editing
    title_label = ctk.CTkLabel(self.master, text="Editing Document", font=('Bold Calibri', 20))
    title_label.pack(pady=(10, 5))

    # Scrolled text widget for the document's content
    text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=100, height=25)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Load and display the content of the file in the text area
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text_area.insert(tk.END, content)
    except Exception as e:
        print(f"Error reading file: {e}")
        self.display_message("Failed to load document content.")

    # Save button
    save_button = ctk.CTkButton(self.master, text="Save", command=lambda: save_document(self, file_path, text_area))
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Return to Dashboard button
    back_button = ctk.CTkButton(self.master, text="Back to Dashboard", command=self.init_application)
    back_button.pack(side=tk.RIGHT, padx=10, pady=10)

def save_document(self, file_path, text_area):
    """
    Saves the current content of the text area back to the specified file.
    """
    content = text_area.get("1.0", tk.END)  # Get all text from the text area
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        self.display_message("Document saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")
        self.display_message("Failed to save document.")