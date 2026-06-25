def place_child_window(parent, child, width, height, offset_x=24, offset_y=24, transient=True):
    """
    Position a child window relative to the root window's top-left corner
    and keep it visually associated with the parent window.
    """
    parent.update_idletasks()
    x = parent.winfo_rootx() + offset_x
    y = parent.winfo_rooty() + offset_y
    child.geometry(f"{width}x{height}+{x}+{y}")

    if transient:
        try:
            child.transient(parent)
        except Exception:
            pass

    child.after(50, lambda: show_child_window(parent, child))

def show_child_window(parent, child):
    """
    Restore and focus an existing child window.
    """
    try:
        if not child.winfo_exists():
            return
        child.deiconify()
        child.lift()
        child.focus_force()
        parent.after(50, child.lift)
    except Exception:
        pass
