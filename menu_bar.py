import tkinter as tk

class MenuButton(tk.Menubutton):
    def __init__(self, parent, on_new_game, on_exit, **kwargs):
        super().__init__(parent, **kwargs)

        # Style the menu button
        self.config(
            text="☰ Menu",
            font=("Comic Sans MS", 18, "bold"),
            bg="#ff69b4",
            fg="white",
            activebackground="#ff1493",
            activeforeground="white",
            relief="raised",
            bd=5,
            cursor="hand2",
        )

        # Create dropdown menu
        self.menu = tk.Menu(self, tearoff=0,
                            font=("Comic Sans MS", 14, "bold"),
                            bg="#fff0f5",
                            fg="#ff1493",
                            activebackground="#ff69b4",
                            activeforeground="white",
                            bd=3, relief="ridge")
        self.menu.add_command(label="New Game", command=on_new_game)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=on_exit)

        self.config(menu=self.menu)
