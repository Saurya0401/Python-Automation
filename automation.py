from PIL import Image
import csv
import pyautogui
import pyzbar.pyzbar
import os
import requests
import sys
import time
import tkinter as tk
import urllib.parse
import webbrowser

home_path = os.environ['HOMEPATH']
auto_path = f"{home_path}\\Desktop\\Python Projects\\Automation"


class DelayMsgBox(tk.Tk):
    def __init__(self, msg, count):
        super().__init__()
        DelayMsgBox.title(self, "Warning")
        self.id = None
        self.count = count
        self.msg = tk.Label(text=msg, font=("TkDefaultFont", 16))
        self.counter = tk.Label(text=self.count, font=("TkDefaultFont", 22), fg="red1")
        self.msg.pack(padx=5, pady=(10, 0))
        self.counter.pack(pady=(5, 15))
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.start_timer()

    def close_window(self):
        self.after_cancel(self.id)
        self.destroy()

    def start_timer(self):
        if self.count <= 0:
            self.close_window()
        else:
            self.counter.config(text=self.count)
            self.count -= 1
            self.id = self.after(1000, self.start_timer)


def click_icon(icon, region=(0, 0, 1920, 1080), r_count=0, r_max=20, r_delay=0.5):
    # todo: pass r_max, r_delay as sys args
    try:
        x, y = pyautogui.locateCenterOnScreen(image=f"{auto_path}\\icons\\{icon}", region=region)
    except TypeError:
        print(f"{icon} not found, trying again...retries={r_count}")
        time.sleep(r_delay)
        if r_count < r_max:
            click_icon(icon, region, r_count + 1)
        else:
            exit_with_errmsg("Retry count exceeded.")
    except FileNotFoundError:
        exit_with_errmsg(f"File \"{icon}\" not found. ")
    else:
        pyautogui.click(x, y)


def delay_message(message="Continuing in", delay_seconds=5, gui=False):
    if gui:
        d = DelayMsgBox(message, delay_seconds)
        d.mainloop()
    else:
        print(message, end=" ", flush=True)
        for i in range(delay_seconds, 0, -1):
            print(i, end="", flush=True)
            for _ in range(3):
                time.sleep(0.25)
                print(".", end="", flush=True)
            time.sleep(0.25)


def display_msg(msg="", title="", button=""):
    pyautogui.alert(text=msg, title=title, button=button)


def exit_with_errmsg(msg="Unknown error."):
    display_msg(msg, "Error", "Exit")
    raise SystemExit


def get_coords(file="all_coords.csv"):
    coords = {}
    try:
        with open(f"{auto_path}\\coords\\{file}", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                coords[row["name"]] = (row["icon"], tuple([int(row[x]) for x in ("left", "top", "xrange", "yrange")]))
    except FileNotFoundError:
        exit_with_errmsg(f"File \"{file}\" not found.")
    else:
        return coords


def get_weather(city="here"):
    ip_loc = False
    if city == "here":
        try:
            ip = requests.get('https://api.ipify.org').text
            loc_resp = requests.api.get(
                url=f"https://api.ipgeolocation.io/ipgeo?apiKey=064f6ca33a9140c2905defe5b09059fd&ip={ip}").json()
            city = f"{loc_resp['city']}, {loc_resp['country_code2']}"
        except requests.exceptions.RequestException as e:
            exit_with_errmsg(f"Error retrieving location via IP. Try again later. Details:\n\n{e.args[0]}")
        else:
            ip_loc = True
    parameters = {'q': str(city), 'APPID': 'eb40ee84dcd396fe4f4c745a79b01809'}
    try:
        response = requests.api.get(url='http://api.openweathermap.org/data/2.5/weather', params=parameters)
    except requests.exceptions.RequestException as e:
        exit_with_errmsg(f"Error: Connection Error. Details:\n\n{e.args[0]}")
    else:
        if response.status_code == 200:
            cur_weather = response.json()
            display_msg("\nWeather Report".upper() + "\n-----------------------" +
                        f"\nCity: {cur_weather['name']}, {cur_weather['sys']['country']}" +
                        f"\nTemperature: {'%.1f' % (cur_weather['main'].get('temp') - 273.15)}°C, "
                        f"(Minimum: {'%.1f' % (cur_weather['main'].get('temp_min') - 273.15)}°C, " +
                        f"Maximum: {'%.1f' % (cur_weather['main'].get('temp_max') - 273.15)}°C)" +
                        f"\nHumidity: {cur_weather['main'].get('humidity')}%" +
                        f"\n{cur_weather['weather'][0].get('description').capitalize()}." +
                        "\n-----------------------" +
                        f"\nWeather service provided by openweathermap.org."
                        f"{' Location acquired from ip address, may not be accurate.' if ip_loc else ''}",
                        "Weather Report", "Ok")
        else:
            errors = {400: "400: Bad request.",
                      401: "401: Auth token expired.",
                      404: f"404: \"{city.capitalize()}\" not located, check city name and/or country code.",
                      500: "500: Internal server error.",
                      503: "503: Weather service currently unavailable."}
            exit_with_errmsg(errors[response.status_code])


def get_item(concatenator=" "):
    return concatenator.join(sys.argv[1:]) if len(sys.argv) > 1 else ''


def google_search(term=''):
    # todo: error handling for url parsing
    term_url = urllib.parse.quote_plus(term, safe='')
    term_url = f"&q={term_url}" if term_url else term_url
    open_default_browser(url=f"www.google.com/search?{term_url}")


def open_default_browser(new_window=True, url="www.google.com"):
    try:
        webbrowser.open(url=url, new=1 if new_window else 2)
    except webbrowser.Error as e:
        exit_with_errmsg(e.args[0])


def qr_reader(qr_img):
    if type(qr_img) == str:
        try:
            qr_img = Image.open(qr_img)
        except (FileNotFoundError, AttributeError):
            exit_with_errmsg("Invalid image path.")
    try:
        qr_url = pyzbar.pyzbar.decode(qr_img)[0][0]
        qr_url = qr_url.decode("utf-8")
    except IndexError:
        exit_with_errmsg("QR code image incomplete/not located.")
    except (pyzbar.pyzbar.PyZbarError, UnicodeError) as e:
        exit_with_errmsg(e.args[0])
    else:
        open_default_browser(url=qr_url)


def screencap(region=(0, 0, 1920, 1080), img_file="", delay_seconds=5, gui=False):
    delay_message("Bring relevant window to foreground.\nScript executing in: ", delay_seconds, gui=gui)
    capture = pyautogui.screenshot(imageFilename=img_file if img_file else None, region=region)
    return capture


if __name__ == "__main__":
    # testbed for new functions
    delay_message(gui=True)
    exit(0)
