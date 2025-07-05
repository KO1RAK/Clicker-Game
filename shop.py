import tkinter as tk

class ShopWindow(tk.Toplevel):
    def __init__(self, parent, logic, tutorial_mark_done_callback):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic
        self.tutorial_mark_done = tutorial_mark_done_callback

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Position on right side docked to parent window
        parent.update_idletasks()
        px, py = parent.winfo_x(), parent.winfo_y()
        pw, ph = parent.winfo_width(), parent.winfo_height()

        width = 420
        height = ph
        x = px + pw - width
        y = py

        self.geometry(f"{width}x{height}+{x}+{y}")

        # Outer frame acting as the border
        border_color = "#d6336c"  # deep pink/red border
        border_width = 8

        self.border_frame = tk.Frame(self, bg=border_color)
        self.border_frame.pack(fill="both", expand=True)

        # Inner frame for content, with padding and lighter bg
        self.main_frame = tk.Frame(self.border_frame, bg="#fff0f6", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True, padx=border_width, pady=border_width)

        # Close button styled with hover effect
        self.close_btn = tk.Button(self.main_frame, text="✕", font=("Arial", 14, "bold"),
                                   bg="#ff4d6d", fg="white", bd=0, relief="flat",
                                   activebackground="#ff1a3c", activeforeground="white",
                                   command=self.on_close)
        self.close_btn.place(relx=1, x=-10, y=10, anchor="ne")
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(bg="#ff1a3c"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(bg="#ff4d6d"))

        self.create_widgets()

        self.resizable(False, False)

    def create_widgets(self):
        title = tk.Label(self.main_frame, text="Shop", font=("Comic Sans MS", 28, "bold"),
                         bg="#fff0f6", fg="#d6336c")
        title.pack(pady=(30, 20))

        self.autoclicker_label = tk.Label(self.main_frame, text=f"Autoclickers: {self.logic.autoclickers}",
                                          font=("Comic Sans MS", 18), bg="#fff0f6", fg="#b3003b")
        self.autoclicker_label.pack(pady=(10, 5))

        self.autoclicker_cost_label = tk.Label(self.main_frame, text=f"Cost: {self.logic.autoclicker_cost} eggs",
                                               font=("Comic Sans MS", 16), bg="#fff0f6", fg="#80002b")
        self.autoclicker_cost_label.pack(pady=(0, 10))

        self.buy_autoclicker_btn = tk.Button(self.main_frame, text="Buy Autoclicker",
                                             font=("Comic Sans MS", 18, "bold"),
                                             bg="#ff4d6d", fg="white",
                                             activebackground="#ff1a3c",
                                             activeforeground="white",
                                             relief="flat", bd=0,
                                             command=self.buy_autoclicker)
        self.buy_autoclicker_btn.pack(pady=10, ipadx=10, ipady=8)

        self.click_power_label = tk.Label(self.main_frame, text=f"Click Power: {self.logic.click_power}",
                                          font=("Comic Sans MS", 18), bg="#fff0f6", fg="#b3003b")
        self.click_power_label.pack(pady=(40, 5))

        self.click_upgrade_cost_label = tk.Label(self.main_frame, text=f"Cost: {self.logic.click_upgrade_cost} eggs",
                                                 font=("Comic Sans MS", 16), bg="#fff0f6", fg="#80002b")
        self.click_upgrade_cost_label.pack(pady=(0, 10))

        self.buy_click_upgrade_btn = tk.Button(self.main_frame, text="Buy Click Upgrade",
                                               font=("Comic Sans MS", 18, "bold"),
                                               bg="#ff4d6d", fg="white",
                                               activebackground="#ff1a3c",
                                               activeforeground="white",
                                               relief="flat", bd=0,
                                               command=self.buy_click_upgrade)
        self.buy_click_upgrade_btn.pack(pady=10, ipadx=10, ipady=8)

        # --- ADD REBIRTH WIDGETS BELOW ---

        self.rebirth_cost = 500 * (2 ** self.logic.rebirth.count)  # Initial 500, doubles each rebirth

        self.rebirth_label = tk.Label(self.main_frame, 
                                      text=f"Rebirths: {self.logic.rebirth.count} (Multiplier: x{self.logic.rebirth.get_multiplier()})",
                                      font=("Comic Sans MS", 18), bg="#fff0f6", fg="#b3003b")
        self.rebirth_label.pack(pady=(40, 5))

        self.rebirth_cost_label = tk.Label(self.main_frame, 
                                           text=f"Cost: {self.rebirth_cost} eggs",
                                           font=("Comic Sans MS", 16), bg="#fff0f6", fg="#80002b")
        self.rebirth_cost_label.pack(pady=(0, 10))

        self.buy_rebirth_btn = tk.Button(self.main_frame, text="Buy Rebirth",
                                         font=("Comic Sans MS", 18, "bold"),
                                         bg="#ff4d6d", fg="white",
                                         activebackground="#ff1a3c",
                                         activeforeground="white",
                                         relief="flat", bd=0,
                                         command=self.buy_rebirth)
        self.buy_rebirth_btn.pack(pady=10, ipadx=10, ipady=8)

    def buy_autoclicker(self):
        if self.logic.eggs >= self.logic.autoclicker_cost:
            self.logic.eggs -= self.logic.autoclicker_cost
            self.logic.autoclickers += 1
            self.logic.autoclicker_cost = int(round(self.logic.autoclicker_cost * 1.25))
            self.logic.save()
            self.update_shop_ui()
            self.tutorial_mark_done(2)

    def buy_click_upgrade(self):
        if self.logic.eggs >= self.logic.click_upgrade_cost:
            self.logic.eggs -= self.logic.click_upgrade_cost
            self.logic.click_power += 1
            self.logic.click_upgrade_cost = int(round(self.logic.click_upgrade_cost * 1.25))
            self.logic.save()
            self.update_shop_ui()
            self.tutorial_mark_done(3)

    # --- ADD REBIRTH BUY METHOD ---

    def buy_rebirth(self):
        cost = 500 * (2 ** self.logic.rebirth.count)
        if self.logic.eggs >= cost:
            if self.logic.rebirth_purchase():
                self.logic.save()
                self.update_shop_ui()
                self.tutorial_mark_done(4)  # optional: mark rebirth tutorial step if you want
                # Update rebirth cost for next time
                self.rebirth_cost = 500 * (2 ** self.logic.rebirth.count)
                self.rebirth_cost_label.config(text=f"Cost: {self.rebirth_cost} eggs")
                self.rebirth_label.config(text=f"Rebirths: {self.logic.rebirth.count} (Multiplier: x{self.logic.rebirth.get_multiplier()})")

    def update_shop_ui(self):
        self.autoclicker_label.config(text=f"Autoclickers: {self.logic.autoclickers}")
        self.autoclicker_cost_label.config(text=f"Cost: {self.logic.autoclicker_cost} eggs")
        self.click_power_label.config(text=f"Click Power: {self.logic.click_power}")
        self.click_upgrade_cost_label.config(text=f"Cost: {self.logic.click_upgrade_cost} eggs")

        # Update rebirth UI as well
        self.rebirth_cost = 500 * (2 ** self.logic.rebirth.count)
        self.rebirth_cost_label.config(text=f"Cost: {self.rebirth_cost} eggs")
        self.rebirth_label.config(text=f"Rebirths: {self.logic.rebirth.count} (Multiplier: x{self.logic.rebirth.get_multiplier()})")

    def on_close(self):
        self.parent.shop_window = None
        self.destroy()
