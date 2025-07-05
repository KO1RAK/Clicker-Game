import tkinter as tk
import tkinter.font as tkfont

class ShopWindow(tk.Toplevel):
    def __init__(self, parent, logic, tutorial_callback):
        super().__init__(parent)
        self.logic = logic
        self.tutorial_callback = tutorial_callback  # Function to notify tutorial steps done

        self.geometry("600x400")
        self.config(bg="#ffddee")
        self.overrideredirect(True)  # Remove OS window border

        # Custom close button
        close_btn = tk.Button(self, text="✕", font=("Arial", 12, "bold"),
                              fg="white", bg="red", bd=0,
                              command=self.destroy)
        close_btn.place(x=570, y=5, width=25, height=25)

        # Enable dragging window by mouse
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

        label = tk.Label(self, text="Buy Upgrades", font=("Comic Sans MS", 24), bg="#ffddee")
        label.pack(pady=10)

        self.buy_auto_btn = tk.Button(self, text=f"Buy Autoclicker ({self.logic.autoclicker_cost} eggs)",
                                     font=("Arial", 16), bg="#ffe4e1",
                                     command=self.buy_autoclicker)
        self.buy_auto_btn.pack(pady=15, ipadx=20, ipady=10)

        self.buy_click_upgrade_btn = tk.Button(self, text=f"Buy Click Upgrade ({self.logic.click_upgrade_cost} eggs)",
                                               font=("Arial", 16), bg="#ffe4e1",
                                               command=self.buy_click_upgrade)
        self.buy_click_upgrade_btn.pack(pady=15, ipadx=20, ipady=10)

        self.update_buttons()

    def buy_autoclicker(self):
        if hasattr(self.logic, "buy_autoclicker") and self.logic.buy_autoclicker():
            self.tutorial_callback(2)  # Mark tutorial step 3 done
            self.update_buttons()

    def buy_click_upgrade(self):
        if hasattr(self.logic, "buy_click_upgrade") and self.logic.buy_click_upgrade():
            self.tutorial_callback(3)  # Mark tutorial step 4 done
            self.update_buttons()

    def update_buttons(self):
        self.buy_auto_btn.config(text=f"Buy Autoclicker ({self.logic.autoclicker_cost} eggs)")
        self.buy_click_upgrade_btn.config(text=f"Buy Click Upgrade ({self.logic.click_upgrade_cost} eggs)")
        self.after(1000, self.update_buttons)

    # Dragging support
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f"+{x}+{y}")
