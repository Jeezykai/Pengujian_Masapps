from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class KelolaVideoPageTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi WebDriver untuk Kelola Video...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"
        self.v_judul = "Testing Upload Video"
        self.v_id = "dQw4w9WgXcQ"
        self.v_ket = "Video ini ditambahkan secara otomatis oleh Bot Testing Ganteng."

    def slow_typing(self, element, text, speed=0.05):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(speed)

    def login_masuk(self, user, pw):
        print(f"[LOGIN] Mencoba masuk sebagai {user}...")
        self.driver.get(f"{self.base_url}/login")
        u_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        self.slow_typing(u_field, user)
        self.slow_typing(self.driver.find_element(By.NAME, "password"), pw)
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
        if match:
            hasil = str(int(match.group(1)) + int(match.group(2)))
            self.slow_typing(self.driver.find_element(By.NAME, "captcha"), hasil)

        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait.until(EC.url_contains("dashboard"))
        print("[PASS] Berhasil Login.")
    
    def run_full_test(self):
            self.driver.get(self.base_url)
            time.sleep(1.5)
            btn_admin = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin Portal")))
            btn_admin.click()

    def test_tambah_video(self):
        print("\n[CRUD - CREATE] Menguji Tambah Video Baru...")
        try:
            btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Kelola Video')]")))
            btn_menu.click()
  
            print("[INFO] Masuk ke halaman daftar video...")
            time.sleep(2) 
            btn_tambah = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '+ Tambah Video')]")))
            btn_tambah.click()
            
            print("[INFO] Masuk ke halaman form tambah video...")
            time.sleep(1.5)

            print(f"[INFO] Mengisi form untuk: {self.v_judul}")
            input_judul = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Contoh: Tutorial Software Testing']")))
            self.slow_typing(input_judul, self.v_judul)

            input_yt_id = self.driver.find_element(By.XPATH, "//input[@placeholder='ID saja, misal: dQw4w9WgXcQ']")
            self.slow_typing(input_yt_id, self.v_id)

            input_ket = self.driver.find_element(By.XPATH, "//textarea")
            self.slow_typing(input_ket, self.v_ket)
            
            time.sleep(2)
            btn_simpan = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Simpan Video')]")
            btn_simpan.click()

            xpath_verif = f"//tr[td//strong[contains(text(), '{self.v_judul}')]]"
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_verif)))
            print(f"[PASS] Video '{self.v_judul}' sukses muncul di tabel!")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Gagal Tambah Video: {e}")

    def test_hapus_video_dinamis(self):
        print(f"\n[CRUD - DELETE] Menguji Hapus Video yang baru dibuat...")
        try:
            xpath_hapus = f"//tr[td//strong[contains(text(), '{self.v_judul}')]]//a[contains(@class, 'btn-danger')]"
            btn_hapus = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_hapus)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_hapus)
            time.sleep(1)
            btn_hapus.click()

            self.wait.until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            
            print(f"[PASS] Video '{self.v_judul}' berhasil dihapus.")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Gagal Hapus Video: {e}")

    def close(self):
        print("\n[DONE] Selesai. Menutup browser...")
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = KelolaVideoPageTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.test_tambah_video()
    time.sleep(1)
    bot.test_hapus_video_dinamis()
    bot.close()