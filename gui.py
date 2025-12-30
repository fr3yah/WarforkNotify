from pystray import MenuItem as item
import customtkinter
from PIL import Image, ImageDraw, ImageTk
import pystray
import scraper
import time
import threading
from bs4 import BeautifulSoup
import requests
from winotify import Notification

stop_event = threading.Event()

class WarforkNotifyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.stop_event = threading.Event()
        self.running = False


        self.title("Warfork Notify")
        self.geometry("200x300")
        self.iconbitmap("icon.ico")


        self.protocol('WM_DELETE_WINDOW', self.withdraw_window)

        self.server_label = customtkinter.CTkLabel(self, font=("Arial", 17), text="Servers")
        self.server_label.pack(padx=10, pady=4, anchor="w")

        self.NA_var = customtkinter.BooleanVar(value=False)
        self.NA_checkbox = customtkinter.CTkCheckBox(
            self, text="NA", command=self.checkbox_event,
            variable=self.NA_var, onvalue="on", offvalue="off",
            checkbox_width=14, checkbox_height=14
        )
        self.NA_checkbox.pack(padx=10, pady=4, anchor="w")

        self.SA_var = customtkinter.BooleanVar(value=False)
        self.SA_checkbox = customtkinter.CTkCheckBox(
            self, text="SA", command=self.checkbox_event,
            variable=self.SA_var, onvalue="on", offvalue="off",
            checkbox_width=14, checkbox_height=14
        )
        self.SA_checkbox.pack(padx=10, pady=4, anchor="w")

        self.EU_var = customtkinter.BooleanVar(value=False)
        self.EU_checkbox = customtkinter.CTkCheckBox(
            self, text="EU", command=self.checkbox_event,
            variable=self.EU_var, onvalue="on", offvalue="off",
            checkbox_width=14, checkbox_height=14
        )
        self.EU_checkbox.pack(padx=10, pady=4, anchor="w")

        self.AS_var = customtkinter.BooleanVar(value=False)
        self.AS_checkbox = customtkinter.CTkCheckBox(
            self, text="AS", command=self.checkbox_event,
            variable=self.AS_var, onvalue="on", offvalue="off",
            checkbox_width=14, checkbox_height=14
        )
        self.AS_checkbox.pack(padx=10, pady=4, anchor="w")

        self.player_label = customtkinter.CTkLabel(self, font=("Arial", 17), text="Player Count")
        self.player_label.pack(padx=10, pady=4, anchor="w")

        self.sliderVal = None
        self.slider = customtkinter.CTkSlider(
            self, from_=1, to=10, command=self.slider_event, variable=self.sliderVal,
            number_of_steps=9
        )
        self.slider.pack(padx=10, pady=4, anchor="w")

        self.button = customtkinter.CTkButton(self, text="Start Notifier", command=self.button_event)
        self.button.pack(padx=10, pady=15)

    def checkbox_event(self):
        self.regions = [self.NA_var.get(), self.SA_var.get(), self.EU_var.get(), self.AS_var.get()]
        pass

    def slider_event(self, value):
        self.sliderVal = self.slider.get()
        self.player_label.configure(text="Player Count: " + str(self.sliderVal))

    def button_event(self):

        if not self.running:
            self.thread = threading.Thread(target=self.background_loop, daemon=True)
            self.thread.start()
            self.running = True
        else:
            self.stop_event.set()
            self.button.configure(text="Starting...")
            time.sleep(10)
            self.thread = threading.Thread(target=self.background_loop, daemon=True)
            self.thread.start()
            self.stop_event.clear()

        self.withdraw_app()
        self.button.configure(text="Start Notifier")



    def withdraw_window(self):
        self.withdraw()

    def quit_app(self, icon, item):
        self.stop_event.set()
        icon.stop()
        self.destroy()

    def show_app(self, icon, item):
        icon.stop()
        self.after(0, app.deiconify)

    def withdraw_app(self):
        self.withdraw()
        image = Image.open("icon.ico")
        menu = (item('Quit', self.quit_app), item('Show Settings', self.show_app))
        icon = pystray.Icon("name", image, "Warfork Notify", menu)
        icon.run()

    def background_loop(self):
        self.previous = []
        print("hey")
        while not self.stop_event.is_set():
            print("hey)")
            previous_names = [s.name for s in self.previous]
            new = scraper.checkServers(self.regions, self.sliderVal)
            print(new)
            print(previous_names)
            for server in new:
                if server.name not in previous_names:
                    text = "\n".join(f"{server.name} - {server.player} player{'s' if server.player != 1 else ''}" for server in new)
                    toast = Notification(app_id="Warfork Notify",
                                         title="New Servers Active",
                                         msg=text)
                    toast.show()
                    break


            self.previous = new
            time.sleep(6)


app = WarforkNotifyApp()

app.protocol('WM_DELETE_WINDOW', app.withdraw_app)
app.mainloop()
