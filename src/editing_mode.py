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

    # Frame to hold the text area and scrollbars
    frame = tk.Frame(self.master)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Horizontal scrollbar
    h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Vertical scrollbar
    v_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Scrolled text widget with horizontal scrolling
    text_area = tk.Text(frame, wrap=tk.NONE, xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set, undo=True, borderwidth=0, highlightthickness=0)
    text_area.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH, expand=True)

    # Configure scrollbars
    h_scroll.config(command=text_area.xview)
    v_scroll.config(command=text_area.yview)

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

    # Bind CTRL+F to the find function
    text_area.bind("<Control-f>", lambda event: open_search_bar(text_area))

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


def open_search_bar(text_area):
    """
    Opens a search bar for finding words in the text area.
    Removes highlights when the search window is closed.
    """
    def close_search_window():
        # Remove all highlights when the search window is closed
        text_area.tag_remove("highlight", "1.0", tk.END)
        search_window.destroy()

    # Create a Toplevel window for the search bar
    search_window = tk.Toplevel()
    search_window.title("Search")
    search_window.geometry("300x100")

    # Make the window non-resizable
    search_window.resizable(False, False)

    # Bind the close action to remove highlights
    search_window.protocol("WM_DELETE_WINDOW", close_search_window)

    search_label = tk.Label(search_window, text="Search for:")
    search_label.pack(pady=5)

    search_entry = tk.Entry(search_window, width=30)
    search_entry.pack(pady=5)

    search_button = tk.Button(search_window, text="Search", command=lambda: search_and_jump(text_area, search_entry.get()))
    search_button.pack(pady=5)

    # Focus on the search entry when the window opens
    search_entry.focus()

    # Bind Enter key to the search functionality
    search_window.bind("<Return>", lambda event: search_and_jump(text_area, search_entry.get()))


def search_word(text_area, word):
    """
    Searches for all occurrences of a word in the text area and highlights them.
    """
    # Remove previous highlights
    text_area.tag_remove("highlight", "1.0", tk.END)
    if not word:
        return  # Do nothing if the search word is empty
    start_pos = "1.0"
    while True:
        # Search for the word
        start_pos = text_area.search(word, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break  # Exit loop if word is not found
        # Calculate the end position of the found word
        end_pos = f"{start_pos}+{len(word)}c"
        # Highlight the found word
        text_area.tag_add("highlight", start_pos, end_pos)
        text_area.tag_config("highlight", background="yellow", foreground="black")
        # Move to the next position after the current word
        start_pos = end_pos


def search_and_jump(text_area, word):
    """
    Searches for the first occurrence of a word in the text area, highlights it, and scrolls to it.
    """
    # Remove previous highlights
    text_area.tag_remove("highlight", "1.0", tk.END)

    if not word:
        return  # Do nothing if the search word is empty

    # Search for the word
    start_pos = text_area.search(word, "1.0", stopindex=tk.END, nocase=True)

    if start_pos:
        # Calculate the end position of the found word
        end_pos = f"{start_pos}+{len(word)}c"

        # Highlight the found word
        text_area.tag_add("highlight", start_pos, end_pos)
        text_area.tag_config("highlight", background="yellow", foreground="black")

        # Scroll to the word
        text_area.see(start_pos)

        # Set the cursor to the start of the word
        text_area.mark_set(tk.INSERT, start_pos)
        text_area.focus()
    else:
        # Word not found - Optionally, show a message to the user
        self.display_message("Word not found.", "red", duration=2000)
