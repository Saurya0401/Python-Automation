import tkinter as tk


class SimpleTimer(tk.Tk):
    def __init__(self, count, func=exit, call_func=False):
        super().__init__()
        self.init_count = count
        self.init_label = "Continuing in: "
        self.count = count
        self.func = func
        self.call_func = call_func
        self.label = tk.Label(text=self.init_label)
        self.counter = tk.Label(text=self.count)
        self.start_btn = tk.Button(text="Start", command=self.start)
        self.reset_btn = tk.Button(text="Reset", command=self.reset)
        for i in (self.label, self.counter, self.start_btn, self.reset_btn):
            i.pack()

    def reset(self):
        self.count = self.init_count
        self.label.config(text=self.init_label)
        self.counter.config(text=self.count)
        self.start_btn.config(state="normal")

    def start(self):
        self.timer()

    def timer(self):
        self.start_btn.config(state="disabled")
        if self.count <= 0:
            self.label.config(text="Time's up!")
            self.func() if self.call_func else self.counter.config(text="0")
        else:
            self.counter.config(text=self.count)
            self.count -= 1
            self.after(1000, self.timer)


if __name__ == "__main__":
    a = SimpleTimer(6)
    a.mainloop()
    exit(0)
