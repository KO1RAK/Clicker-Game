import tkinter as tk
from logic import GameLogic
from shop import ShopWindow
from tutorial import TutorialBox
from menu_bar import MenuButton  # Import the separate menu script

class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()

        self.root.title("Egg Clicker Fun!")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#ffefd5")
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Menu button top-right using the separate MenuButton class
        self.menu_btn = MenuButton(self.root, self.on_reset, self.on_exit)
        self.menu_btn.place(relx=1.0, y=10, anchor="ne")

        self.playful_font = ("Comic Sans MS", 36, "bold")

        self.score_label = tk.Label(root, text=f"Eggs: {self.logic.eggs}",
                                    font=self.playful_font,
                                    fg="#ff4500", bg="#ffefd5")
        self.score_label.pack(pady=(40, 5))

        self.goal_target = 500
        self.goal_label = tk.Label(root, text=f"Goal: {self.logic.eggs} / {self.goal_target} Eggs",
                                   font=("Comic Sans MS", 24),
                                   fg="#008000", bg="#ffefd5")
        self.goal_label.pack(pady=(0, 20))

        tutorial_steps = [
            "1. Click the big button",
            "2. Open the Shop",
            "3. Buy an Autoclicker",
            "4. Buy a Click Upgrade",
        ]
        self.tutorial_box = TutorialBox(root, tutorial_steps)
        self.tutorial_box.place(x=10, y=40, width=350, height=230)

        self.click_button = tk.Button(root, text="🐣 Click Me! 🐣",
                                      font=("Comic Sans MS", 28, "bold"),
                                      fg="#ffffff", bg="#ff69b4",
                                      activebackground="#ff1493",
                                      relief="raised", bd=8,
                                      command=self.on_click)
        self.click_button.pack(pady=30, ipadx=30, ipady=20)

        self.reset_button = tk.Button(root, text="Reset Game",
                                      font=("Arial", 20),
                                      fg="#333", bg="#ffe4e1",
                                      command=self.on_reset)
        self.reset_button.pack(pady=10, ipadx=20, ipady=10)

        self.shop_button = tk.Button(root, text="Open Shop 🛒",
                                     font=("Arial", 24),
                                     fg="#333", bg="#add8e6",
                                     command=self.open_shop)
        self.shop_button.pack(pady=20, ipadx=20, ipady=15)

        self.flash_colors = ["#ffb6c1", "#ff69b4", "#ff1493"]
        self.flash_index = 0

        self.shop_window = None

        self.update_ui_loop()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def on_exit(self):
        self.root.destroy()

    def on_click(self):
        self.logic.click()
        self.update_score()
        self.flash_button()
        self.tutorial_box.mark_step_done(0)

    def open_shop(self):
        self.tutorial_box.mark_step_done(1)
        if self.shop_window is not None and tk.Toplevel.winfo_exists(self.shop_window):
            self.shop_window.lift()
            return
        self.shop_window = ShopWindow(self.root, self.logic, self.tutorial_box.mark_step_done)

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

        self.tutorial_box.destroy()
        tutorial_steps = [
            "1. Click the big button",
            "2. Open the Shop",
            "3. Buy an Autoclicker",
            "4. Buy a Click Upgrade",
        ]
        self.tutorial_box = TutorialBox(self.root, tutorial_steps)
        self.tutorial_box.place(x=10, y=40, width=350, height=230)

    def update_ui_loop(self):
        self.update_score()
        self.root.after(500, self.update_ui_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGUI(root)
    root.mainloop()
