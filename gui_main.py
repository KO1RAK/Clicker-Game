import tkinter as tk
from logic import GameLogic
from shop import ShopWindow
from tutorial import TutorialBox
from menu_bar import MenuButton
from status_bar import StatusBar
from gui_components import BackgroundCanvas, ClickableEmoji, ScoreLabel, ShopButton
from rebirth import Rebirth

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

        self.bg_canvas = BackgroundCanvas(self.root, screen_width, screen_height)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.emoji = ClickableEmoji(self.bg_canvas, screen_width // 2, screen_height // 2, self.on_click)

        self.score_label = ScoreLabel(self.root, self.logic)
        self.score_label.pack(pady=(40, 5))

        if not self.logic.tutorial_completed:
            tutorial_steps = [
                "Click the Chicken in the egg",
                "Open the Shop",
                "Buy an Autoclicker",
                "Buy a Click Upgrade",
                "Buy a Rebirth", 
            ]
            self.tutorial_box = TutorialBox(self.root, tutorial_steps, on_complete=self.tutorial_finished)
            self.tutorial_box.place(x=10, y=40, width=350, height=280)
        else:
            self.tutorial_box = None

        self.shop_button = ShopButton(self.root, self.open_shop)

        self.flash_colors = ["#f4c2c2", "#f7d1d1", "#f4c2c2"]
        self.flash_index = 0

        self.shop_window = None

        self.menu_btn = MenuButton(self.root, self.on_reset, self.on_exit)
        self.menu_btn.place(relx=1.0, y=10, anchor="ne")

        self.status_bar = StatusBar(self.root, self.logic)
        self.status_bar.pack(side="bottom", fill="x")

        self.update_ui_loop()

    def tutorial_finished(self):
        self.logic.tutorial_completed = True
        self.logic.save()
        self.tutorial_box = None

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

    def on_exit(self):
        self.root.destroy()

    def on_click(self, event=None):
        self.logic.click()
        self.update_score()
        self.flash_emoji()
        if self.tutorial_box:
            self.tutorial_box.mark_step_done(0)

    def open_shop(self):
        if self.tutorial_box:
            self.tutorial_box.mark_step_done(1)
        if self.shop_window is not None and tk.Toplevel.winfo_exists(self.shop_window):
            self.shop_window.lift()
            return
        self.shop_window = ShopWindow(self.root, self.logic, self.tutorial_box.mark_step_done if self.tutorial_box else None)

    def update_score(self):
        eggs = self.logic.eggs
        self.score_label.config(text=f"Eggs: {eggs}")

    def flash_emoji(self):
        self.bg_canvas.itemconfig(self.emoji.text_id, fill="#f7d1d1")
        self.root.after(150, lambda: self.bg_canvas.itemconfig(self.emoji.text_id, fill="black"))

    def buy_rebirth(self):
        if self.logic.rebirth_purchase():
            if self.tutorial_box:
                self.tutorial_box.mark_step_done(4) 
            self.update_score()
        else:
            
            pass

    def on_reset(self):
        self.logic.eggs = 0
        self.logic.autoclickers = 0
        self.logic.autoclicker_cost = 10
        self.logic.click_power = 1
        self.logic.click_upgrade_cost = 15
        self.logic.rebirth = Rebirth()
        self.logic.tutorial_completed = False
        self.logic.save()
        self.update_score()

        if self.tutorial_box:
            self.tutorial_box.destroy()
        tutorial_steps = [
            "Click the big button",
            "Open the Shop",
            "Buy an Autoclicker",
            "Buy a Click Upgrade",
            "Buy a Rebirth",
        ]
        self.tutorial_box = TutorialBox(self.root, tutorial_steps, on_complete=self.tutorial_finished)
        self.tutorial_box.place(x=10, y=40, width=350, height=230)

    def update_ui_loop(self):
        self.update_score()
        self.status_bar.update_status()
        self.root.after(500, self.update_ui_loop)
