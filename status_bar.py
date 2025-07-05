import tkinter as tk

class StatusBar(tk.Frame):
    def __init__(self, parent, logic, **kwargs):
        super().__init__(parent, **kwargs)
        self.logic = logic
        self.config(bg="#ffe4e1", bd=4, relief="groove", padx=20, pady=12)

        label_style = {
            "font": ("Comic Sans MS", 18, "bold"),
            "bg": "#ffe4e1",
            "fg": "#b22222",
            "padx": 20,
            "pady": 6,
        }

        self.egg_per_sec_label = tk.Label(self, text="🥚 Eggs per second: 0", **label_style)
        self.egg_per_sec_label.pack(side="left")

        self.autoclicker_level_label = tk.Label(self, text="🤖 Auto-clickers: 0", **label_style)
        self.autoclicker_level_label.pack(side="left")

        self.click_power_label = tk.Label(self, text="🖱️ Click power: 1", **label_style)
        self.click_power_label.pack(side="left")

    def update_status(self):
        eggs_per_sec = self.logic.autoclickers  # or calculate properly if needed
        self.egg_per_sec_label.config(text=f"🥚 Eggs per second: {eggs_per_sec}")
        self.autoclicker_level_label.config(text=f"🤖 Auto-clickers: {self.logic.autoclickers}")
        self.click_power_label.config(text=f"🖱️ Click power: {self.logic.click_power}")
