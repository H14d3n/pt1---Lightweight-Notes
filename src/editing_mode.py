import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
import re
from encryption import decrypt_document_text, encrypt_document_text
from window_utils import place_child_window, show_child_window

EDITOR_FONT_SIZE = 13
CODE_BLOCK_BACKGROUND = "#EFEFEF"


def encrypt_text(self, text_area):
    """
    Encrypts the current text content with authenticated encryption.
    """
    plain_text = text_area.get("1.0", tk.END)
    if not getattr(self, "session_password", None):
        raise ValueError("No active session password available for encryption.")
    return encrypt_document_text(plain_text, self.session_password)

def decrypt_text(self, content, uid):
    """
    Decrypts the given content using the authenticated encryption payload.
    """
    if not getattr(self, "session_password", None):
        raise ValueError("No active session password available for decryption.")
    return decrypt_document_text(content, self.session_password, uid)

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

    # Scrolled text widget with horizontal scrolling
    text_area = ctk.CTkTextbox(frame, wrap=tk.NONE, undo=True, font=self.tk_font)
    try:
        text_area._textbox.configure(insertwidth=2)
    except AttributeError:
        pass
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
            apply_markdown_highlighting(text_area)
    except Exception as e:
        print(f"Error reading file: {e}")
        self.display_message("Failed to load document content.", "red")

    # Bind undo and redo to CTRL+Z and CTRL+Y
    text_area.bind("<Control-z>", lambda event: text_area.edit_undo())
    text_area.bind("<Control-y>", lambda event: text_area.edit_redo())
    text_area.bind("<KeyRelease>", lambda event: apply_markdown_highlighting(text_area))

    # Bind CTRL+S to the save function
    text_area.bind("<Control-s>", lambda event: save_document(self, file_path, text_area))
    text_area.bind("<Control-q>", lambda event: back_to_dashboard(self, file_path, text_area, uid))  

    # Bind CTRL+F to the find function
    text_area.bind("<Control-f>", lambda event: open_search_bar(text_area, self.master))

    # Save button
    save_button = ctk.CTkButton(self.master, text="Save (CTRL + S)", command=lambda: save_document(self, file_path, text_area))
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Markdown preview button
    preview_button = ctk.CTkButton(self.master, text="👁", width=44, command=lambda: open_markdown_preview(self.master, text_area))
    preview_button.pack(side=tk.LEFT, padx=(0, 10), pady=10)

    # Return to Dashboard button
    back_button = ctk.CTkButton(self.master, text="Back to Dashboard (CTRL + Q)", command=lambda: back_to_dashboard(self, file_path, text_area, uid))
    back_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Bind the window close (X) or Alt+F4 event to save and encrypt before closing.
    self.master.protocol("WM_DELETE_WINDOW", lambda: on_window_close(self, file_path, text_area, uid))

def apply_markdown_highlighting(text_area):
    """
    Lightweight Markdown syntax highlighting for common note-taking patterns.
    """
    content = text_area.get("1.0", "end-1c")
    tag_options = {
        "md_heading1": {"foreground": "#4EA8DE"},
        "md_heading2": {"foreground": "#5E60CE"},
        "md_heading3": {"foreground": "#7B61FF"},
        "md_heading4": {"foreground": "#8A63D2"},
        "md_heading5": {"foreground": "#9B72CF"},
        "md_heading6": {"foreground": "#A78BFA"},
        "md_bold": {"foreground": "#005CC5"},
        "md_italic": {"foreground": "#6F42C1"},
        "md_code": {"foreground": "#F77F00"},
        "md_quote": {"foreground": "#52B788"},
        "md_list": {"foreground": "#E9C46A"},
    }
    for tag, options in tag_options.items():
        text_area.tag_remove(tag, "1.0", tk.END)
        text_area.tag_config(tag, **options)

    for line_number, line in enumerate(content.splitlines(), start=1):
        line_start = f"{line_number}.0"
        heading_match = re.match(r"^(#{1,6})\s*.+$", line)
        if heading_match:
            heading_level = len(heading_match.group(1))
            text_area.tag_add(f"md_heading{heading_level}", line_start, f"{line_number}.end")
        if line.startswith("> "):
            text_area.tag_add("md_quote", line_start, f"{line_number}.end")
        if re.match(r"^\s*(-|\*|\d+\.)\s+", line):
            text_area.tag_add("md_list", line_start, f"{line_number}.end")

        for match in re.finditer(r"\*\*(.+?)\*\*", line):
            text_area.tag_add("md_bold", f"{line_number}.{match.start(1)}", f"{line_number}.{match.end(1)}")
        for match in re.finditer(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", line):
            text_area.tag_add("md_italic", f"{line_number}.{match.start(1)}", f"{line_number}.{match.end(1)}")
        for match in re.finditer(r"`([^`]+)`", line):
            text_area.tag_add("md_code", f"{line_number}.{match.start(1)}", f"{line_number}.{match.end(1)}")

def open_markdown_preview(parent, text_area):
    existing_window = getattr(parent, "_markdown_preview_window", None)
    existing_text = getattr(parent, "_markdown_preview_text", None)
    existing_window_open = False
    if existing_window is not None:
        try:
            existing_window_open = existing_window.winfo_exists()
        except tk.TclError:
            existing_window_open = False

    if existing_window_open and existing_text is not None:
        update_markdown_preview(existing_window, existing_text, text_area)
        bring_preview_to_front(parent, existing_window)
        return

    preview_window = ctk.CTkToplevel(parent)
    preview_window.title("Markdown Preview")
    place_child_window(parent, preview_window, 520, 420, 48, 48, transient=False)
    preview_window.resizable(True, True)
    try:
        preview_window.attributes("-toolwindow", False)
    except tk.TclError:
        pass

    container = ctk.CTkFrame(preview_window)
    container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    font_family, font_size = get_textbox_font_settings(preview_window, text_area)
    preview_family = get_scalable_preview_family(preview_window, font_family)
    preview = tk.Text(
        container,
        wrap=tk.WORD,
        font=(preview_family, font_size),
        relief="flat",
        padx=12,
        pady=10,
        borderwidth=0,
    )
    scrollbar = tk.Scrollbar(container, command=preview.yview)
    preview.configure(yscrollcommand=scrollbar.set)
    preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    configure_preview_tags(preview, preview_family, font_size)
    update_markdown_preview(preview_window, preview, text_area)
    preview.configure(cursor="arrow")
    parent._markdown_preview_window = preview_window
    parent._markdown_preview_text = preview
    preview_window.protocol("WM_DELETE_WINDOW", lambda: close_markdown_preview(parent, preview_window))
    preview_window.after(100, lambda: bring_preview_to_front(parent, preview_window))

def bring_preview_to_front(parent, preview_window):
    show_child_window(parent, preview_window)
    try:
        preview_window.attributes("-topmost", True)
        preview_window.after(200, lambda: preview_window.attributes("-topmost", False))
    except tk.TclError:
        pass

def update_markdown_preview(preview_window, preview, text_area):
    font_family, font_size = get_textbox_font_settings(preview_window, text_area)
    preview_family = get_scalable_preview_family(preview_window, font_family)
    preview.configure(state="normal", font=(preview_family, font_size))
    configure_preview_tags(preview, preview_family, font_size)
    render_markdown_into_preview(preview, text_area.get("1.0", "end-1c"))
    preview.configure(state="disabled")

def close_markdown_preview(parent, preview_window):
    preview_window.destroy()
    parent._markdown_preview_window = None
    parent._markdown_preview_text = None

def get_textbox_font_settings(root, text_area):
    """
    Reuse the editor's font family and size for the rendered preview.
    """
    editor_font = text_area.cget("font")
    try:
        family = editor_font.cget("family")
        size = editor_font.cget("size")
    except AttributeError:
        try:
            actual_font = tkfont.Font(root=root, font=editor_font)
            family = actual_font.actual("family")
            size = actual_font.actual("size")
        except tk.TclError:
            family = "Calibri"
            size = 14

    return family or "Calibri", int(size or 14)

def configure_preview_tags(preview, family, size):
    heading_family = get_available_font_family(preview, "Arial Black", "Arial")
    heading_sizes = {
        "h1": 40,
        "h2": 20,
        "h3": 15,
        "h4": 12,
        "h5": 10,
        "h6": 8,
    }
    preview.tag_config("h1", font=(heading_family, heading_sizes["h1"], "bold"), spacing1=10, spacing3=5)
    preview.tag_config("h2", font=(heading_family, heading_sizes["h2"], "bold"), spacing1=7, spacing3=3)
    preview.tag_config("h3", font=(heading_family, heading_sizes["h3"], "bold"), spacing1=5, spacing3=2)
    preview.tag_config("h4", font=(heading_family, heading_sizes["h4"], "bold"), spacing1=3, spacing3=1)
    preview.tag_config("h5", font=(heading_family, heading_sizes["h5"], "bold"), spacing1=1, spacing3=1)
    preview.tag_config("h6", font=(heading_family, heading_sizes["h6"], "bold"), spacing1=1, spacing3=1)
    preview.tag_config("bold", font=(family, size, "bold"))
    preview.tag_config("italic", font=(family, size, "italic"))
    preview.tag_config("code", font=("Courier New", size), background=CODE_BLOCK_BACKGROUND)
    preview.tag_config("code_block", font=("Courier New", size), background=CODE_BLOCK_BACKGROUND, lmargin1=16, lmargin2=16, spacing1=4, spacing3=4)
    preview.tag_config("code_language", font=("Courier New", max(size - 1, 8), "bold"), foreground="#57606A", background=CODE_BLOCK_BACKGROUND, lmargin1=16, lmargin2=16, spacing1=8)
    preview.tag_config("code_comment", foreground="#6A737D")
    preview.tag_config("code_keyword", foreground="#D73A49")
    preview.tag_config("code_string", foreground="#032F62")
    preview.tag_config("code_number", foreground="#005CC5")
    preview.tag_config("code_function", foreground="#6F42C1")
    preview.tag_config("code_tag", foreground="#22863A")
    preview.tag_config("code_attr", foreground="#E36209")
    preview.tag_config("quote", foreground="#4D7C59", lmargin1=16, lmargin2=16)
    preview.tag_config("list", lmargin1=18, lmargin2=34)
    preview.tag_config("meta", foreground="#666666", font=(family, max(size - 1, 8)))
    preview._preview_font_size = size

def get_available_font_family(root, preferred, fallback):
    available_fonts = {font.lower(): font for font in tkfont.families(root=root)}
    return available_fonts.get(preferred.lower(), fallback)

def get_scalable_preview_family(root, family):
    """
    Some bitmap fonts ignore requested sizes. Use one consistent preview font.
    """
    try:
        h1_linespace = tkfont.Font(root=root, family=family, size=24, weight="bold").metrics("linespace")
        h3_linespace = tkfont.Font(root=root, family=family, size=17, weight="bold").metrics("linespace")
        if h1_linespace > h3_linespace:
            return family
    except tk.TclError:
        pass

    return "Segoe UI"

def render_markdown_into_preview(preview, markdown_text):
    preview.configure(state="normal")
    destroy_code_block_frames(preview)
    preview.delete("1.0", tk.END)
    in_code_block = False
    code_language = ""
    code_lines = []

    for line in markdown_text.splitlines():
        fence_match = re.match(r"^\s*```\s*([A-Za-z0-9_+-]*)", line)
        if fence_match:
            if in_code_block:
                render_code_block(preview, code_lines, code_language)
                code_lines = []
                code_language = ""
                in_code_block = False
            else:
                in_code_block = True
                code_language = normalize_code_language(fence_match.group(1))
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        heading_match = re.match(r"^(#{1,6})\s*(.*)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            insert_inline_markdown(preview, heading_match.group(2), (f"h{level}",))
            preview.insert(tk.END, "\n")
            continue

        bullet_match = re.match(r"^(\s*)([-*+])\s+(.*)$", line)
        if bullet_match:
            indent = "  " * (len(bullet_match.group(1)) // 2)
            preview.insert(tk.END, f"{indent}{chr(8226)} ", ("list",))
            insert_inline_markdown(preview, bullet_match.group(3), ("list",))
            preview.insert(tk.END, "\n")
            continue

        arrow_match = re.match(r"^(\s*)->\s+(.*)$", line)
        if arrow_match:
            indent = "  " * (len(arrow_match.group(1)) // 2)
            preview.insert(tk.END, f"{indent}{chr(8226)} ", ("list",))
            insert_inline_markdown(preview, arrow_match.group(2), ("list",))
            preview.insert(tk.END, "\n")
            continue

        numbered_match = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if numbered_match:
            indent = "  " * (len(numbered_match.group(1)) // 2)
            preview.insert(tk.END, f"{indent}{numbered_match.group(2)}. ", ("list",))
            insert_inline_markdown(preview, numbered_match.group(3), ("list",))
            preview.insert(tk.END, "\n")
            continue

        quote_match = re.match(r"^>\s?(.*)$", line)
        if quote_match:
            insert_inline_markdown(preview, quote_match.group(1), ("quote",))
            preview.insert(tk.END, "\n")
            continue

        meta_tags = ("meta",) if re.match(r"^(uid|date):", line) else ()
        insert_inline_markdown(preview, line, meta_tags)
        preview.insert(tk.END, "\n")

    if in_code_block:
        render_code_block(preview, code_lines, code_language)

def insert_inline_markdown(preview, text, base_tags=()):
    token_pattern = re.compile(r"(`[^`]+`|\*\*[^*]+?\*\*|(?<!\*)\*[^*\n]+?\*(?!\*))")
    position = 0
    for match in token_pattern.finditer(text):
        if match.start() > position:
            preview.insert(tk.END, text[position:match.start()], base_tags)

        token = match.group(0)
        if token.startswith("`") and token.endswith("`"):
            preview.insert(tk.END, token[1:-1], base_tags + ("code",))
        elif token.startswith("**") and token.endswith("**"):
            preview.insert(tk.END, token[2:-2], base_tags + ("bold",))
        elif token.startswith("*") and token.endswith("*"):
            preview.insert(tk.END, token[1:-1], base_tags + ("italic",))

        position = match.end()

    if position < len(text):
        preview.insert(tk.END, text[position:], base_tags)

def normalize_code_language(language):
    language = language.lower().strip()
    aliases = {
        "py": "python",
        "python3": "python",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "javascript",
        "tsx": "javascript",
        "htm": "html",
        "xml": "html",
        "sh": "bash",
        "shell": "bash",
        "zsh": "bash",
        "ps1": "powershell",
        "c++": "cpp",
        "cc": "cpp",
        "h": "c",
        "hpp": "cpp",
    }
    return aliases.get(language, language)

def destroy_code_block_frames(preview):
    for frame in getattr(preview, "_code_block_frames", []):
        try:
            frame.destroy()
        except tk.TclError:
            pass
    preview._code_block_frames = []

def render_code_block(preview, lines, language):
    if not lines and not language:
        return

    font_size = getattr(preview, "_preview_font_size", EDITOR_FONT_SIZE)
    line_count = max(len(lines) + (1 if language else 0), 1)
    frame = tk.Frame(preview, bg=CODE_BLOCK_BACKGROUND)
    code_text = tk.Text(
        frame,
        height=line_count,
        wrap=tk.NONE,
        font=("Courier New", font_size),
        bg=CODE_BLOCK_BACKGROUND,
        relief="flat",
        borderwidth=0,
        padx=12,
        pady=8,
        highlightthickness=0,
    )
    code_text._font_size = font_size
    code_text.pack(fill=tk.BOTH, expand=True)
    configure_code_text_tags(code_text)

    if language:
        code_text.insert(tk.END, language + "\n", ("code_language",))

    for line in lines:
        insert_code_line(code_text, line, language)
        code_text.insert(tk.END, "\n")

    code_text.configure(state="disabled", cursor="arrow")
    frame.update_idletasks()
    frame.configure(height=code_text.winfo_reqheight())
    frame.pack_propagate(False)
    preview.window_create(tk.END, window=frame, stretch=True)
    preview.insert(tk.END, "\n")
    preview._code_block_frames.append(frame)
    update_code_block_width(preview, frame)
    if not getattr(preview, "_code_block_resize_bound", False):
        preview.bind("<Configure>", lambda event, text_widget=preview: update_code_block_widths(text_widget), add="+")
        preview._code_block_resize_bound = True

def update_code_block_widths(preview):
    for frame in getattr(preview, "_code_block_frames", []):
        update_code_block_width(preview, frame)

def update_code_block_width(preview, frame):
    width = max(preview.winfo_width() - 36, 120)
    frame.configure(width=width)

def configure_code_text_tags(code_text):
    code_text.tag_config("code_language", font=("Courier New", max(getattr(code_text, "_font_size", EDITOR_FONT_SIZE) - 1, 8), "bold"), foreground="#57606A")
    code_text.tag_config("code_comment", foreground="#6A737D")
    code_text.tag_config("code_keyword", foreground="#D73A49")
    code_text.tag_config("code_string", foreground="#032F62")
    code_text.tag_config("code_number", foreground="#005CC5")
    code_text.tag_config("code_function", foreground="#6F42C1")
    code_text.tag_config("code_tag", foreground="#22863A")
    code_text.tag_config("code_attr", foreground="#E36209")

def insert_code_line(preview, line, language):
    spans = get_code_spans(line, language)
    position = 0
    for start, end, tag in spans:
        if start > position:
            preview.insert(tk.END, line[position:start], ("code_block",))
        preview.insert(tk.END, line[start:end], ("code_block", tag))
        position = end

    if position < len(line):
        preview.insert(tk.END, line[position:], ("code_block",))

def get_code_spans(line, language):
    if language == "html":
        return get_html_spans(line)
    if language == "css":
        return get_css_spans(line)
    if language in {"bash", "powershell"}:
        return get_shell_spans(line, language)

    keywords = get_language_keywords(language)
    spans = []
    protected = []

    comment_pattern = get_comment_pattern(language)
    if comment_pattern:
        comment_match = re.search(comment_pattern, line)
        if comment_match:
            add_span(spans, protected, comment_match.start(), len(line), "code_comment")

    for match in re.finditer(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")", line):
        add_span(spans, protected, match.start(), match.end(), "code_string")

    for match in re.finditer(r"\b\d+(?:\.\d+)?\b", line):
        add_span(spans, protected, match.start(), match.end(), "code_number")

    if keywords:
        keyword_pattern = r"\b(" + "|".join(re.escape(word) for word in sorted(keywords, key=len, reverse=True)) + r")\b"
        for match in re.finditer(keyword_pattern, line):
            add_span(spans, protected, match.start(), match.end(), "code_keyword")

    for match in re.finditer(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*(?=\()", line):
        if match.group(1) not in keywords:
            add_span(spans, protected, match.start(1), match.end(1), "code_function")

    return sorted(spans, key=lambda item: item[0])

def add_span(spans, protected, start, end, tag):
    if start >= end:
        return
    if any(start < protected_end and end > protected_start for protected_start, protected_end in protected):
        return
    spans.append((start, end, tag))
    if tag in {"code_comment", "code_string"}:
        protected.append((start, end))

def get_language_keywords(language):
    keyword_sets = {
        "python": {
            "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del",
            "elif", "else", "except", "False", "finally", "for", "from", "global", "if", "import",
            "in", "is", "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield",
        },
        "javascript": {
            "async", "await", "break", "case", "catch", "class", "const", "continue", "default",
            "delete", "do", "else", "export", "extends", "false", "finally", "for", "from",
            "function", "if", "import", "in", "instanceof", "let", "new", "null", "return",
            "switch", "this", "throw", "true", "try", "typeof", "undefined", "var", "while",
        },
        "java": {
            "abstract", "boolean", "break", "case", "catch", "class", "const", "continue",
            "default", "do", "else", "extends", "false", "final", "finally", "for", "if",
            "implements", "import", "instanceof", "interface", "new", "null", "private",
            "protected", "public", "return", "static", "super", "switch", "this", "throw",
            "true", "try", "void", "while",
        },
        "c": {
            "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
            "else", "enum", "extern", "float", "for", "if", "int", "long", "return", "short",
            "signed", "sizeof", "static", "struct", "switch", "typedef", "unsigned", "void",
            "while",
        },
        "cpp": {
            "auto", "bool", "break", "case", "catch", "char", "class", "const", "continue",
            "default", "delete", "do", "double", "else", "enum", "false", "float", "for",
            "if", "int", "long", "namespace", "new", "private", "protected", "public",
            "return", "short", "static", "struct", "switch", "template", "this", "throw",
            "true", "try", "typedef", "using", "void", "while",
        },
        "json": {"true", "false", "null"},
    }
    return keyword_sets.get(language, set())

def get_comment_pattern(language):
    if language == "python":
        return r"#.*$"
    if language in {"javascript", "java", "c", "cpp", "css", "json"}:
        return r"//.*$|/\*.*?\*/"
    if not language:
        return r"#.*$|//.*$|/\*.*?\*/"
    return None

def get_html_spans(line):
    spans = []
    protected = []
    for match in re.finditer(r"<!--.*?-->", line):
        add_span(spans, protected, match.start(), match.end(), "code_comment")
    for match in re.finditer(r"</?[A-Za-z][A-Za-z0-9-]*|/?>", line):
        add_span(spans, protected, match.start(), match.end(), "code_tag")
    for match in re.finditer(r"\b[A-Za-z_:][-A-Za-z0-9_:.]*(?=\=)", line):
        add_span(spans, protected, match.start(), match.end(), "code_attr")
    for match in re.finditer(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")", line):
        add_span(spans, protected, match.start(), match.end(), "code_string")
    return sorted(spans, key=lambda item: item[0])

def get_css_spans(line):
    spans = []
    protected = []
    for match in re.finditer(r"/\*.*?\*/", line):
        add_span(spans, protected, match.start(), match.end(), "code_comment")
    for match in re.finditer(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")", line):
        add_span(spans, protected, match.start(), match.end(), "code_string")
    for match in re.finditer(r"(?<![.#-])\b[-A-Za-z]+\b(?=\s*:)", line):
        add_span(spans, protected, match.start(), match.end(), "code_attr")
    for match in re.finditer(r"[.#]?[A-Za-z_][A-Za-z0-9_-]*(?=\s*\{)", line):
        add_span(spans, protected, match.start(), match.end(), "code_tag")
    for match in re.finditer(r"\b\d+(?:\.\d+)?(?:px|rem|em|%|vh|vw)?\b", line):
        add_span(spans, protected, match.start(), match.end(), "code_number")
    return sorted(spans, key=lambda item: item[0])

def get_shell_spans(line, language):
    spans = []
    protected = []
    comment_pattern = r"#.*$" if language == "bash" else r"#.*$"
    comment_match = re.search(comment_pattern, line)
    if comment_match:
        add_span(spans, protected, comment_match.start(), len(line), "code_comment")
    for match in re.finditer(r"('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")", line):
        add_span(spans, protected, match.start(), match.end(), "code_string")
    for match in re.finditer(r"(?<!\S)-{1,2}[A-Za-z0-9-]+", line):
        add_span(spans, protected, match.start(), match.end(), "code_attr")
    for match in re.finditer(r"\b(if|then|else|fi|for|while|do|done|function|return|echo|cd|mkdir|rm|git|python|pip|npm)\b", line):
        add_span(spans, protected, match.start(), match.end(), "code_keyword")
    return sorted(spans, key=lambda item: item[0])

def on_window_close(self, file_path, text_area, uid):
    """
    This method is triggered when the window is closed (either via Alt+F4 or the close button).
    It ensures the content is encrypted and saved before closing the window.
    """
    print("Window close event triggered")
    
    try:
        # Save encrypted content to disk before exiting.
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
    print("Saving encrypted text before navigating to the dashboard...")
    save_document(self, file_path, text_area)

    # Unset the editing mode
    self.editing = False
    
    # Now navigate to the dashboard or do whatever you need
    self.init_application()

def save_document(self, file_path, text_area):
    """
    Saves the current content of the text area back to the specified file.
    """
    # Use self.current_file_path instead of file_path
    file_path = self.current_file_path
    try:
        if text_area is None:
            raise ValueError("No active text area available for saving.")
        encrypted_content = encrypt_text(self, text_area)
        with open(file_path, 'w') as file:
            file.write(encrypted_content)
        self.display_message("Document saved successfully.", "green", duration=2000)
    except Exception as e:
        print(f"Error saving file: {e}")
        self.display_message("Failed to save document.", "red", duration=2000)

def open_search_bar(text_area, parent=None):
    """
    Opens a search bar for finding words in the text area.
    Removes highlights when the search window is closed.
    """
    def close_search_window():
        # Remove all highlights when the search window is closed
        text_area.tag_remove("highlight", "1.0", tk.END)
        search_window.destroy()

    # Create a Toplevel window for the search bar
    search_window = tk.Toplevel(parent)
    search_window.title("Search")
    if parent is not None:
        place_child_window(parent, search_window, 300, 100, 48, 48)
    else:
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
    Searches for the next occurrence of a word in the text area, highlights it, and scrolls to it.
    If no previous search, starts from the beginning. If at the end, wraps to the first occurrence.
    """
    # Remove previous highlights
    text_area.tag_remove("highlight", "1.0", tk.END)

    if not word:
        return

    # Get current cursor position
    current_pos = text_area.index(tk.INSERT)

    # Search for the next occurrence after the current position
    start_pos = text_area.search(word, current_pos, stopindex=tk.END, nocase=True)

    # If not found, wrap around and search from the beginning
    if not start_pos or start_pos == current_pos:
        start_pos = text_area.search(word, "1.0", stopindex=tk.END, nocase=True)

    if start_pos:
        end_pos = f"{start_pos}+{len(word)}c"
        text_area.tag_add("highlight", start_pos, end_pos)
        text_area.tag_config("highlight", background="yellow", foreground="black")
        text_area.see(start_pos)
        text_area.mark_set(tk.INSERT, end_pos)
        text_area.focus()
    else:
        text_area.bell()
