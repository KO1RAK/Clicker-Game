import tkinter as tk
from logic import GameLogic

class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()

        self.root.title("Egg Clicker Deluxe")
        self.root.geometry("1920x1080")
        self.root.config(bg="#1e1e1e")  # Dark background for modern look

        # Configure grid layout with 3 rows and 1 column, stretch vertically
        self.root.rowconfigure([0,1,2], weight=1)
        self.root.columnconfigure(0, weight=1)

        # Score Label
        self.score_label = tk.Label(root, text=f"Eggs: {self.logic.eggs}",
                                    font=("Comic Sans MS", 72, "bold"),
                                    fg="#FFD700", bg="#1e1e1e")
        self.score_label.grid(row=0, column=0, pady=(80, 20), sticky="n")

        # Click Button
        self.click_button = tk.Button(root, text="Click", font=("Comic Sans MS", 96, "bold"),
                                      fg="#ffffff", bg="#ffb300", activebackground="#ffaa00",
                                      command=self.on_click, relief="raised", bd=8)
        self.click_button.grid(row=1, column=0, pady=40, ipadx=60, ipady=30)

        # Reset Button
        self.reset_button = tk.Button(root, text="Reset", font=("Arial", 28),
                                      fg="#1e1e1e", bg="#dddddd",
                                      command=self.on_reset)
        self.reset_button.grid(row=2, column=0, pady=(20, 80), ipadx=30, ipady=10)

        # Button flash colors
        self.flash_colors = ["#ffd700", "#ffaa00", "#ff6f00"]
        self.flash_index = 0

    def on_click(self):
        self.logic.click()
        self.update_score()
        self.flash_button()

    def update_score(self):
        self.score_label.config(text=f"Eggs: {self.logic.eggs}")

    def on_reset(self):
        self.logic.eggs = 0
        self.logic.save()
        self.update_score()

    def flash_button(self):
        color = self.flash_colors[self.flash_index]
        self.click_button.config(bg=color)
        self.flash_index = (self.flash_index + 1) % len(self.flash_colors)
        self.root.after(150, lambda: self.click_button.config(bg="#ffb300"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGUI(root)
    root.mainloop()
