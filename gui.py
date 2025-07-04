import tkinter as tk
import tkinter.font as tkfont
from logic import GameLogic
from shop import ShopWindow

class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()

        self.root.title("Egg Clicker Fun!")
        self.root.geometry("800x600")
        self.root.config(bg="#ffefd5")  # Warm pastel background

        self.playful_font = ("Comic Sans MS", 36, "bold")

        # Score label
        self.score_label = tk.Label(root, text=f"Eggs: {self.logic.eggs}",
                                    font=self.playful_font,
                                    fg="#ff4500", bg="#ffefd5")
        self.score_label.pack(pady=(20, 5))

        # Goal label
        self.goal_target = 500
        self.goal_label = tk.Label(root, text=f"Goal: {self.logic.eggs} / {self.goal_target} Eggs",
                                   font=("Comic Sans MS", 24),
                                   fg="#008000", bg="#ffefd5")
        self.goal_label.pack(pady=(0, 20))

        # --- Tutorial checklist setup ---
        self.tutorial_steps = [
            {"text": "1. Click the big button", "done": False},
            {"text": "2. Open the Shop", "done": False},
            {"text": "3. Buy an Autoclicker", "done": False},
            {"text": "4. Buy a Click Upgrade", "done": False},
        ]
        self.tutorial_frame = tk.Frame(root, bg="#fffacd", bd=2, relief="solid")
        self.tutorial_frame.place(x=10, y=10, width=300, height=160)

        self.tutorial_labels = []
        for step in self.tutorial_steps:
            lbl = tk.Label(self.tutorial_frame, text=step["text"],
                           font=("Arial", 12), anchor="w", bg="#fffacd")
            lbl.pack(fill="x", padx=5, pady=2)
            self.tutorial_labels.append(lbl)

        # Click button
        self.click_button = tk.Button(root, text="🐣 Click Me! 🐣",
                                      font=("Comic Sans MS", 28, "bold"),
                                      fg="#ffffff", bg="#ff69b4",
                                      activebackground="#ff1493",
                                      relief="raised", bd=8,
                                      command=self.on_click)
        self.click_button.pack(pady=30, ipadx=30, ipady=20)

        # Reset button
        self.reset_button = tk.Button(root, text="Reset Game",
                                      font=("Arial", 20),
                                      fg="#333", bg="#ffe4e1",
                                      command=self.on_reset)
        self.reset_button.pack(pady=10, ipadx=20, ipady=10)

        # Shop button
        self.shop_button = tk.Button(root, text="Open Shop 🛒",
                                     font=("Arial", 24),
                                     fg="#333", bg="#add8e6",
                                     command=self.open_shop)
        self.shop_button.pack(pady=20, ipadx=20, ipady=15)

        # Colors for flash effect on click button
        self.flash_colors = ["#ffb6c1", "#ff69b4", "#ff1493"]
        self.flash_index = 0

        self.shop_window = None

        self.update_ui_loop()

    def on_click(self):
        self.logic.click()
        self.update_score()
        self.flash_button()
        self.mark_step_done(0)  # Tutorial: clicked button

    def open_shop(self):
        self.mark_step_done(1)  # Tutorial: opened shop

        if self.shop_window is not None and tk.Toplevel.winfo_exists(self.shop_window):
            self.shop_window.lift()
            return

        self.shop_window = ShopWindow(self.root, self.logic, self.mark_step_done)

    def mark_step_done(self, index):
        if not self.tutorial_steps[index]["done"]:
            self.tutorial_steps[index]["done"] = True
            lbl = self.tutorial_labels[index]
            font = tkfont.Font(font=lbl.cget("font"))
            font.configure(overstrike=1)
            lbl.config(font=font, fg="gray")
            self.check_tutorial_complete()

    def check_tutorial_complete(self):
        if all(step["done"] for step in self.tutorial_steps):
            self.tutorial_frame.destroy()

    def update_score(self):
        eggs = self.logic.eggs
        self.score_label.config(text=f"Eggs: {eggs}")
        self.goal_label.config(text=f"Goal: {eggs} / {self.goal_target} Eggs")
        if eggs >= self.goal_target:
            self.goal_label.config(fg="#ffd700")

    def flash_button(self):
        color = self.flash_colors[self.flash_index]
        self.click_button.config(bg=color)
        self.flash_index = (self.flash_index + 1) % len(self.flash_colors)
        self.root.after(150, lambda: self.click_button.config(bg="#ff69b4"))

    def on_reset(self):
        self.logic.eggs = 0
        self.logic.autoclickers = 0
        self.logic.autoclicker_cost = 10
        self.logic.click_power = 1
        self.logic.click_upgrade_cost = 15
        self.logic.save()
        self.update_score()

        # Reset tutorial
        for i, step in enumerate(self.tutorial_steps):
            step["done"] = False
            lbl = self.tutorial_labels[i]
            font = tkfont.Font(font=lbl.cget("font"))
            font.configure(overstrike=0)
            lbl.config(font=font, fg="black")

        # Recreate tutorial box if missing
        if not self.tutorial_frame.winfo_exists():
            self.tutorial_frame = tk.Frame(self.root, bg="#fffacd", bd=2, relief="solid")
            self.tutorial_frame.place(x=10, y=10, width=300, height=160)
            self.tutorial_labels.clear()
            for step in self.tutorial_steps:
                lbl = tk.Label(self.tutorial_frame, text=step["text"],
                               font=("Arial", 12), anchor="w", bg="#fffacd")
                lbl.pack(fill="x", padx=5, pady=2)
                self.tutorial_labels.append(lbl)

    def update_ui_loop(self):
        self.update_score()
        self.root.after(500, self.update_ui_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGUI(root)
    root.mainloop()
