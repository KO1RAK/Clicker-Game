import tkinter as tk
from logic import GameLogic
from shop import ShopWindow
from tutorial import TutorialBox
from menu_bar import MenuButton
from status_bar import StatusBar

class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()

        self.root.title("Egg Clicker Fun!")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#ffefd5")
        self.root.bind("<Escape>", self.exit_fullscreen)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Background canvas with pastel pink stripes
        self.bg_canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        stripe_width = 40
        stripe_color_1 = "#f4c2c2"
        stripe_color_2 = "#f7d1d1"
        for x in range(0, screen_width, stripe_width * 2):
            self.bg_canvas.create_rectangle(x, 0, x + stripe_width, screen_height, fill=stripe_color_1, width=0)
            self.bg_canvas.create_rectangle(x + stripe_width, 0, x + 2 * stripe_width, screen_height, fill=stripe_color_2, width=0)

        # Draw clickable emoji centered horizontally and vertically
        emoji_x = screen_width // 2
        emoji_y = screen_height // 2
        self.emoji_text = self.bg_canvas.create_text(
            emoji_x, emoji_y,
            text="🐣",
            font=("Segoe UI Emoji", 200),
            fill="black",
            tags="clickable_emoji"
        )

        self.bg_canvas.tag_bind("clickable_emoji", "<Button-1>", self.on_click)
        self.bg_canvas.tag_bind("clickable_emoji", "<Enter>", lambda e: self.bg_canvas.config(cursor="hand2"))
        self.bg_canvas.tag_bind("clickable_emoji", "<Leave>", lambda e: self.bg_canvas.config(cursor=""))

        self.playful_font = ("Comic Sans MS", 36, "bold")

        # Score label
        self.score_label = tk.Label(root, text=f"Eggs: {self.logic.eggs}",
                                    font=self.playful_font,
                                    fg="#ff4500", bg="#ffefd5")
        self.score_label.pack(pady=(40, 5))

        # Goal label
        self.goal_target = 500
        self.goal_label = tk.Label(root, text=f"Goal: {self.logic.eggs} / {self.goal_target} Eggs",
                                   font=("Comic Sans MS", 24),
                                   fg="#008000", bg="#ffefd5")
        self.goal_label.pack(pady=(0, 20))

        # Tutorial box
        tutorial_steps = [
            "1. Click the big button",
            "2. Open the Shop",
            "3. Buy an Autoclicker",
            "4. Buy a Click Upgrade",
        ]
        self.tutorial_box = TutorialBox(root, tutorial_steps)
        self.tutorial_box.place(x=10, y=40, width=350, height=230)

        # Shop button
        self.shop_button = tk.Button(root, text="Open Shop 🛒",
                                     font=("Arial", 24),
                                     fg="#333", bg="#add8e6",
                                     command=self.open_shop)
        self.shop_button.pack(pady=20, ipadx=20, ipady=15)

        self.flash_colors = ["#f4c2c2", "#f7d1d1", "#f4c2c2"]
        self.flash_index = 0

        self.shop_window = None

        # Menu button (top-right)
        self.menu_btn = MenuButton(self.root, self.on_reset, self.on_exit)
        self.menu_btn.place(relx=1.0, y=10, anchor="ne")

        # Status bar
        self.status_bar = StatusBar(self.root, self.logic)
        self.status_bar.pack(side="bottom", fill="x")

        self.update_ui_loop()

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def on_exit(self):
        self.root.destroy()

    def on_click(self, event=None):
        self.logic.click()
        self.update_score()
        self.flash_emoji()
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

    def flash_emoji(self):
        self.bg_canvas.itemconfig(self.emoji_text, fill="#f7d1d1")
        self.root.after(150, lambda: self.bg_canvas.itemconfig(self.emoji_text, fill="black"))

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
        self.status_bar.update_status()
        self.root.after(500, self.update_ui_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGUI(root)
    root.mainloop()
