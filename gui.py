import tkinter as tk
from logic import GameLogic

class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()

        self.root.title("Egg Clicker Deluxe")
        self.root.geometry("1920x1080")
        self.root.config(bg="#1e1e1e")

        self.root.rowconfigure([0,1,2,3], weight=1)
        self.root.columnconfigure(0, weight=1)

        self.score_label = tk.Label(root, text=f"Eggs: {self.logic.eggs}",
                                    font=("Comic Sans MS", 72, "bold"),
                                    fg="#FFD700", bg="#1e1e1e")
        self.score_label.grid(row=0, column=0, pady=(80, 20), sticky="n")

        self.click_button = tk.Button(root, text="Click", font=("Comic Sans MS", 96, "bold"),
                                      fg="#ffffff", bg="#ffb300", activebackground="#ffaa00",
                                      command=self.on_click, relief="raised", bd=8)
        self.click_button.grid(row=1, column=0, pady=40, ipadx=60, ipady=30)

        self.reset_button = tk.Button(root, text="Reset", font=("Arial", 28),
                                      fg="#1e1e1e", bg="#dddddd",
                                      command=self.on_reset)
        self.reset_button.grid(row=2, column=0, pady=20, ipadx=30, ipady=10)

        self.shop_button = tk.Button(root, text="Shop", font=("Arial", 28),
                                     fg="#1e1e1e", bg="#a0d8f0",
                                     command=self.open_shop)
        self.shop_button.grid(row=3, column=0, pady=(0, 80), ipadx=30, ipady=10)

        self.flash_colors = ["#ffd700", "#ffaa00", "#ff6f00"]
        self.flash_index = 0

        self.shop_window = None

        self.update_ui_loop()

    def on_click(self):
        self.logic.click()
        self.update_score()
        self.flash_button()

    def update_score(self):
        self.score_label.config(text=f"Eggs: {self.logic.eggs}")

    def on_reset(self):
        self.logic.eggs = 0
        self.logic.autoclickers = 0
        self.logic.autoclicker_cost = 10
        self.logic.click_power = 1
        self.logic.click_upgrade_cost = 15
        self.logic.save()
        self.update_score()

    def flash_button(self):
        color = self.flash_colors[self.flash_index]
        self.click_button.config(bg=color)
        self.flash_index = (self.flash_index + 1) % len(self.flash_colors)
        self.root.after(150, lambda: self.click_button.config(bg="#ffb300"))

    def open_shop(self):
        if self.shop_window is not None and tk.Toplevel.winfo_exists(self.shop_window):
            self.shop_window.lift()
            return

        self.shop_window = tk.Toplevel(self.root)
        self.shop_window.title("Shop")
        self.shop_window.geometry("800x600")
        self.shop_window.config(bg="#222")

        # Autoclicker section
        self.ac_label = tk.Label(self.shop_window, text=f"Autoclickers: {self.logic.autoclickers}",
                                 font=("Arial", 28), fg="#fff", bg="#222")
        self.ac_label.pack(pady=20)

        self.ac_cost_label = tk.Label(self.shop_window,
                                      text=f"Cost: {self.logic.autoclicker_cost} Eggs",
                                      font=("Arial", 24), fg="#ddd", bg="#222")
        self.ac_cost_label.pack(pady=10)

        self.buy_ac_button = tk.Button(self.shop_window, text="Buy Autoclicker",
                                       font=("Arial", 24), bg="#4CAF50", fg="#fff",
                                       command=self.buy_autoclicker)
        self.buy_ac_button.pack(pady=20)

        # Click upgrade section
        self.click_power_label = tk.Label(self.shop_window,
                                          text=f"Click Power: {self.logic.click_power}",
                                          font=("Arial", 28), fg="#fff", bg="#222")
        self.click_power_label.pack(pady=20)

        self.click_upgrade_cost_label = tk.Label(self.shop_window,
                                                 text=f"Upgrade Cost: {self.logic.click_upgrade_cost} Eggs",
                                                 font=("Arial", 24), fg="#ddd", bg="#222")
        self.click_upgrade_cost_label.pack(pady=10)

        self.buy_click_upgrade_button = tk.Button(self.shop_window, text="Buy Click Upgrade",
                                                  font=("Arial", 24), bg="#2196F3", fg="#fff",
                                                  command=self.buy_click_upgrade)
        self.buy_click_upgrade_button.pack(pady=20)

    def buy_autoclicker(self):
        success = self.logic.buy_autoclicker()
        if success:
            self.update_shop()
            self.update_score()
        else:
            self.buy_ac_button.config(bg="#f44336")
            self.shop_window.after(300, lambda: self.buy_ac_button.config(bg="#4CAF50"))

    def buy_click_upgrade(self):
        success = self.logic.buy_click_upgrade()
        if success:
            self.update_shop()
            self.update_score()
        else:
            self.buy_click_upgrade_button.config(bg="#f44336")
            self.shop_window.after(300, lambda: self.buy_click_upgrade_button.config(bg="#2196F3"))

    def update_shop(self):
        self.ac_label.config(text=f"Autoclickers: {self.logic.autoclickers}")
        self.ac_cost_label.config(text=f"Cost: {self.logic.autoclicker_cost} Eggs")
        self.click_power_label.config(text=f"Click Power: {self.logic.click_power}")
        self.click_upgrade_cost_label.config(text=f"Upgrade Cost: {self.logic.click_upgrade_cost} Eggs")

    def update_ui_loop(self):
        self.update_score()
        if self.shop_window and tk.Toplevel.winfo_exists(self.shop_window):
            self.update_shop()
        self.root.after(500, self.update_ui_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerGUI(root)
    root.mainloop()
