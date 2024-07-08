import pyautogui
import time

# Fungsi untuk membuat teks virtex
def create_virtex():
    virtex = ""
    for i in range(100):  # Atur jumlah pengulangan sesuai kebutuhan
        virtex += "█" * 10 + "\n"
    return virtex

# Fungsi untuk mengirim teks virtex di WhatsApp
def send_virtex_on_whatsapp():
    virtex = create_virtex()
    time.sleep(5)  # Tunggu 5 detik untuk membuka WhatsApp Web dan memilih kontak

    # Tempel teks virtex ke WhatsApp
    pyautogui.typewrite(virtex)
    pyautogui.press('enter')

if __name__ == "__main__":
    send_virtex_on_whatsapp()
