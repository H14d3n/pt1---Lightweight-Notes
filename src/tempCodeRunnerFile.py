def display_message(self, message, color, duration=None):
        """
        Displays a message on the login screen.
        """
        if self.message_label:
            self.message_label.destroy()

        self.message_label = ctk.CTkLabel(self.master, text=message, font=('Bold Calibri', 12), text_color=color)
        self.message_label.place(relx=0.1, rely=0.55, relwidth=0.8)

        if duration:
            self.master.after(duration, self.message_label.destroy)