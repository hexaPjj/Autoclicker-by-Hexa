import customtkinter as ctk
import tkinter as tk
import keyboard
import threading
import time
import ctypes
from plyer import notification


Green = "\033[32m"
Renk_sıfırlama = "\033[0m"

window = ctk.CTk()
window.title("HexClicker")
window.geometry('600x400')
window.resizable(False,False)

selected_key = None  # Atanan tuşu saklamak için
clicking = False  # Tıklama durumunu kontrol etmek için


# Otomatik tıklayıcı fonksiyon
def autoclicker():
    global clicking
    while True:
        if clicking:
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Sol tık bas
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Sol tık bırak
        time.sleep(1 / Slider.get())


# Tuş atama butonu işlevi
def set_key():
    global selected_key
    key_label.configure(text="Bir tuşa basın...")
    key = keyboard.read_event().name
    selected_key = key
    key_label.configure(text=f"Tuş Atandı: {key}")
    keyboard.add_hotkey(selected_key, toggle_clicker)
    print(f"{Green}Atadığınız key {key}{Renk_sıfırlama}")
    send_windows_notification(f"Assigned key {key}",f"HexClicker")


# Autoclicker'ı başlat/durdur
def toggle_clicker():
    global clicking
    clicking = not clicking
    status_label.configure(text="Active" if clicking else "Passive")

def send_windows_notification(message, title="Hexclicker"):
    """Windows bildirimini gönderir."""
    notification.notify(
        title=title,
        message=message,
        timeout=20  # Bildirimin 20 saniye gösterilmesini sağlar
    )


# Label
title_label = ctk.CTkLabel(window, text="HexClicker", font=("Arial", 24))
title_label.pack(pady=20)

leftcpslabel = ctk.CTkLabel(window,text="Left Click CPS",font=("Arial",18))
leftcpslabel.pack(pady=10)

# Slider ve CPS gösterimi
Sliderframe = ctk.CTkFrame(master=window, width=300, height=100, corner_radius=10)
Sliderframe.pack(pady=20, padx=20)

Slider = ctk.CTkSlider(master=Sliderframe, width=200, from_=1, to=100, number_of_steps=99)
Slider.set(10)  # Varsayılan CPS
Slider.pack(side="left", padx=20, pady=10)

slider_value_label = ctk.CTkLabel(Sliderframe, text=f"CPS: {int(Slider.get())}")
slider_value_label.pack(side="left", padx=10)


# Slider güncelleme fonksiyonu
def update_slider_label(value):
    slider_value_label.configure(text=f"CPS: {int(value)}")


Slider.configure(command=update_slider_label)

# Tuş atama butonu
key_button = ctk.CTkButton(window, text="Assign a key", command=set_key)
key_button.pack(pady=10)

key_label = ctk.CTkLabel(window, text="Assigned key: None")
key_label.pack(pady=5)

# Otomatik tıklayıcı durumu
status_label = ctk.CTkLabel(window, text="Passive", fg_color="gray", width=100,corner_radius=10)
status_label.pack(pady=10)

# Autoclicker iş parçacığı başlatma
threading.Thread(target=autoclicker, daemon=True).start()

window.mainloop()
