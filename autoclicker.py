import ctypes
import customtkinter as ctk
from threading import Thread
import time
import keyboard

# Mouse event constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_ABSOLUTE = 0x8000


# Click function using ctypes
def click(mouse_button):
    if mouse_button == "left":
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    elif mouse_button == "right":
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# Autoclicker class
class AutoClicker:
    def __init__(self, interval=0.1, mouse_button="left"):
        self.interval = interval
        self.mouse_button = mouse_button
        self.running = False
        self.thread = None

    def start_clicking(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self._click_loop)
            self.thread.start()

    def stop_clicking(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

    def _click_loop(self):
        while self.running:
            click(self.mouse_button)
            time.sleep(self.interval)

    def set_interval(self, interval):
        self.interval = interval

    def toggle_clicking(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

# GUI class
class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("350x300")
        ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

        # Interval input
        self.interval_label = ctk.CTkLabel(root, text="Click Interval (seconds):")
        self.interval_label.pack(pady=10)
        self.interval_entry = ctk.CTkEntry(root)
        self.interval_entry.pack(pady=10)
        self.interval_entry.insert(0, "0.1")

        # Mouse button selection
        self.button_label = ctk.CTkLabel(root, text="Choose Click Button:")
        self.button_label.pack(pady=10)
        self.button_option = ctk.CTkOptionMenu(root, values=["left", "right"])
        self.button_option.pack(pady=10)
        self.button_option.set("left")

        # Start button
        self.start_button = ctk.CTkButton(root, text="Start", command=self.start_clicker)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = ctk.CTkButton(root, text="Stop", command=self.stop_clicker)
        self.stop_button.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(root, text="Status: Stopped")
        self.status_label.pack(pady=10)

        self.clicker = AutoClicker()
        self.set_hotkey()  # Set fixed hotkey for toggling clicking

        # Track changes to interval entry field
        self.interval_entry.bind("<KeyRelease>", self.update_interval)

    def set_hotkey(self):
        # Fixed hotkey to start/stop the autoclicker
        hotkey = "ctrl+shift+a"
        keyboard.add_hotkey(hotkey, self.toggle_clicker)
        self.status_label.configure(text=f"Hotkey: {hotkey}")

    def start_clicker(self):
        interval = float(self.interval_entry.get())
        mouse_button = self.button_option.get()
        self.clicker.interval = interval
        self.clicker.mouse_button = mouse_button
        self.clicker.start_clicking()
        self.status_label.configure(text="Status: Running")

    def stop_clicker(self):
        self.clicker.stop_clicking()
        self.status_label.configure(text="Status: Stopped")

    def toggle_clicker(self):
        self.clicker.toggle_clicking()
        if self.clicker.running:
            self.status_label.configure(text="Status: Running")
        else:
            self.status_label.configure(text="Status: Stopped")

    def update_interval(self, event=None):
        try:
            interval = float(self.interval_entry.get())
            self.clicker.set_interval(interval)
        except ValueError:
            pass  # Ignore invalid input

# Main loop
if __name__ == "__main__":
    root = ctk.CTk()
    app = AutoClickerApp(root)
    root.mainloop()
