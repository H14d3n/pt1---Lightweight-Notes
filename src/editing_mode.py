import tkinter as tk
import customtkinter as ctk
from encryption import generate_key, encrypt_message


def encrypt_text(self, uid):
    """
    Encrypts the text in the text area using a fixed seed, but leaves the first two lines unencrypted.
    """
    plain_text = self.current_text_area.get("1.0", tk.END)
    
    # Split the content into lines
    lines = plain_text.splitlines()
    
    # Keep the first two lines unchanged
    lines_to_encrypt = lines[2:] 
    content_to_encrypt = "\n".join(lines_to_encrypt)
    
    # Encryption
    seed = 5901 * uid  # You can choose any seed you prefer
    chars, key = generate_key(seed)  # Generate the key using the seed
    cipher_text = encrypt_message(content_to_encrypt, chars, key)
    
    # Combine the unchanged first two lines with the encrypted content
    encrypted_text = "\n".join(lines[:2]) + "\n" + cipher_text

    # Replace the text in the text area with the encrypted message
    self.current_text_area.delete("1.0", tk.END)
    self.current_text_area.insert(tk.END, encrypted_text)

def decrypt_text(self, content, uid):
    """
    Decrypts the given content using the same key and seed, but leaves the first two lines unencrypted.
    """
    # Split the content into lines
    lines = content.splitlines()
    
    # Keep the first two lines unchanged
    lines_to_decrypt = lines[2:]
    content_to_decrypt = "\n".join(lines_to_decrypt)
    
    # Decrypting is simply encrypting again with the same key
    seed = 5901 * uid
    chars, key = generate_key(seed)  
    decrypted_text = encrypt_message(content_to_decrypt, key, chars)  

    # Combine the unchanged first two lines with the decrypted content
    decrypted_message = "\n".join(lines[:2]) + "\n" + decrypted_text
    
    return decrypted_message

def editing_mode(self, file_path, uid):
    """
    Manages the editing process of an opened document, decrypting the file content upon opening.
    """
    self.init_menu_bar()
    self.editing = True

    # Set up a title and text area for editing
    title_label = ctk.CTkLabel(self.master, text="Editing Document", font=('Bold Calibri', 20))
    title_label.pack(pady=(10, 5))

    # Frame to hold the text area and scrollbars
    frame = ctk.CTkFrame(self.master)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # I REMOVED THE SCROLLBARS BECAUSE WHEN THE TEXT DOESN'T FIT, THEY APPEAR THEMSELVES.

    # Scrolled text widget with horizontal scrolling
    text_area = ctk.CTkTextbox(frame, wrap=tk.NONE, undo=True, font=self.tk_font)
    text_area.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.BOTH, expand=True)

    # Store the current file path and text area for Save functionality
    self.current_file_path = file_path
    self.current_text_area = text_area
    self.uid = uid

    # Load and display the content of the file in the text area
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Decrypt the content as the file is loaded
            decrypted_content = decrypt_text(self, content, uid)
            text_area.insert(tk.END, decrypted_content)
    except Exception as e:
        print(f"Error reading file: {e}")
        self.display_message("Failed to load document content.", "red")

    # Bind undo and redo to CTRL+Z and CTRL+Y
    text_area.bind("<Control-z>", lambda event: text_area.edit_undo())
    text_area.bind("<Control-y>", lambda event: text_area.edit_redo())

    # Bind CTRL+S to the save function
    text_area.bind("<Control-s>", lambda event: save_document(self, file_path, text_area))
    text_area.bind("<Control-q>", lambda event: back_to_dashboard(self, file_path, text_area, uid))  

    # Bind CTRL+F to the find function
    text_area.bind("<Control-f>", lambda event: open_search_bar(text_area))

    # Save button
    save_button = ctk.CTkButton(self.master, text="Save (CTRL + S)", command=lambda: save_document(self, file_path, text_area))
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Return to Dashboard button
    back_button = ctk.CTkButton(self.master, text="Back to Dashboard (CTRL + Q)", command=lambda: back_to_dashboard(self, file_path, text_area, uid))
    back_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Bind the window close (X) or Alt+F4 event to save and encrypt before closing.
    self.master.protocol("WM_DELETE_WINDOW", lambda: on_window_close(self, file_path, text_area, uid))

def on_window_close(self, file_path, text_area, uid):
    """
    This method is triggered when the window is closed (either via Alt+F4 or the close button).
    It ensures the content is encrypted and saved before closing the window.
    """
    print("Window close event triggered")
    
    try:
        # Encrypt the text content before closing
        encrypt_text(self, uid)

        # Save the encrypted content to the file
        save_document(self, file_path, text_area)

        # Close the window
        self.master.destroy()  
    except:
        self.master.destroy()


def back_to_dashboard(self, file_path, text_area, uid):
    """
    Handles the action when the user clicks 'Back to Dashboard' button.
    Encrypts the text content before navigating back to the dashboard.
    """
    # Encrypt the text content before going back to the dashboard
    print("Encrypting text before navigating to the dashboard...")
    encrypt_text(self, uid)  
    
    # Save the encrypted content to the file
    save_document(self, file_path, text_area)

    # Unset the editing mode
    self.editing = False
    
    # Now navigate to the dashboard or do whatever you need
    self.init_application()

def save_document(self, file_path, text_area):
    """
    Saves the current content of the text area back to the specified file.
    """
    content = text_area.get("1.0", tk.END)
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
        return 
    start_pos = "1.0"
    while True:
        # Search for the word
        start_pos = text_area.search(word, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break  
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
        return

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
