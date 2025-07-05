import tkinter as tk
import tkinter.font as tkfont
import itertools

class TutorialBox(tk.Frame):
    def __init__(self, parent, steps, on_complete=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.steps = [{"text": step, "done": False} for step in steps]
        self.on_complete = on_complete
        self.config(bg="#fff176", bd=6, relief="ridge")
        self.pack_propagate(False)
        self.tutorial_title = tk.Label(self, text="Tutorial",
                                       font=("Comic Sans MS", 18, "bold"),
                                       fg="#ff6f00", bg="#fff176")
        self.tutorial_title.pack(pady=(5, 10))
        self.labels = []
        for step in self.steps:
            lbl = tk.Label(self, text=step["text"],
                           font=("Comic Sans MS", 14), anchor="w",
                           bg="#fff176", fg="#6d4c41")
            lbl.pack(fill="x", padx=10, pady=3)
            self.labels.append(lbl)
        self.glow_colors = itertools.cycle(["#ff6f00", "#ffa000", "#ffd54f", "#ffa000"])
        self.animate_glow()
    def animate_glow(self):
        glow_color = next(self.glow_colors)
        self.config(highlightbackground=glow_color, highlightcolor=glow_color, highlightthickness=6)
        self.after(600, self.animate_glow)
    def mark_step_done(self, index):
        print(f"Marking step {index} done")
        if 0 <= index < len(self.steps) and not self.steps[index]["done"]:
            self.steps[index]["done"] = True
            font = tkfont.Font(font=self.labels[index].cget("font"))
            font.configure(overstrike=1)
            self.labels[index].config(font=font, fg="gray")
            self.check_complete()
    def check_complete(self):
        print("Checking if all steps done")
        if all(step["done"] for step in self.steps):
            print("All steps done! Showing congrats.")
            for lbl in self.labels:
                lbl.pack_forget()
            self.tutorial_title.config(text="🎉 Congratulations! 🎉", fg="#388e3c")
            congrats_label = tk.Label(self, text="You completed all objectives!",
                                      font=("Comic Sans MS", 14, "bold"),
                                      bg="#fff176", fg="#388e3c")
            congrats_label.pack(pady=10)
            self.after(3000, self.destroy)
            if self.on_complete:
                self.on_complete()
