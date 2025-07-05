import tkinter as tk

class BackgroundCanvas(tk.Canvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        stripe_width = 40
        stripe_color_1 = "#f4c2c2"
        stripe_color_2 = "#f7d1d1"
        for x in range(0, width, stripe_width * 2):
            self.create_rectangle(x, 0, x + stripe_width, height, fill=stripe_color_1, width=0)
            self.create_rectangle(x + stripe_width, 0, x + 2 * stripe_width, height, fill=stripe_color_2, width=0)

class ClickableEmoji:
    def __init__(self, canvas, x, y, click_callback):
        self.canvas = canvas
        self.text_id = self.canvas.create_text(
            x, y,
            text="🐣",
            font=("Segoe UI Emoji", 200),
            fill="black",
            tags="clickable_emoji"
        )
        self.canvas.tag_bind("clickable_emoji", "<Button-1>", click_callback)
        self.canvas.tag_bind("clickable_emoji", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("clickable_emoji", "<Leave>", lambda e: self.canvas.config(cursor=""))

class ScoreLabel(tk.Label):
    def __init__(self, parent, logic):
        super().__init__(parent, text=f"Eggs: {logic.eggs}",
                         font=("Comic Sans MS", 36, "bold"),
                         fg="#ff4500", bg="#ffefd5")

class GoalLabel(tk.Label):
    def __init__(self, parent, eggs, goal_target):
        super().__init__(parent, text=f"Goal: {eggs} / {goal_target} Eggs",
                         font=("Comic Sans MS", 24),
                         fg="#008000", bg="#ffefd5")

class ShopButton(tk.Button):
    def __init__(self, parent, command):
        super().__init__(parent, text="Open Shop 🛒",
                         font=("Arial", 24),
                         fg="#333", bg="#add8e6",
                         command=command)
        self.pack(pady=20, ipadx=20, ipady=15)
