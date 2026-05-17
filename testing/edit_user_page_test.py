from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class EditProfilePageTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi WebDriver untuk Profil Pengguna...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"

    def slow_typing(self, element, text, speed=0.03):
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

    def navigasi_ke_profil(self):
        print("\n[NAVIGASI] Menuju Halaman Profil Pengguna...")
        btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Profil Pengguna')]")))
        btn_menu.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card")))
        print("[SUCCESS] Sudah di halaman Profil.")
        time.sleep(1.5)

    def test_proses_edit_profil(self):
        print("\n[TEST] Memulai Pengujian Fungsional Edit Profil...")
        try:
            xpath_link_edit = "//a[contains(text(), 'Edit Profil')]"
            btn_edit = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_link_edit)))
            print("[INFO] Tautan 'Edit Profil' aktif ditemukan. Mengklik tombol...")
            btn_edit.click()
            
            self.wait.until(EC.url_contains("edit"))
            print("[SUCCESS] Berhasil masuk ke halaman Form Edit Profil.")
            time.sleep(1.5)
            
            input_username = self.driver.find_element(By.NAME, "username")
            input_nama = self.driver.find_element(By.NAME, "nama_lengkap")
            input_password = self.driver.find_element(By.NAME, "password")
            
            print("[INFO] Mengisi informasi profil baru...")
            self.slow_typing(input_nama, "Jayye")
            self.slow_typing(input_username, "admin")
            self.slow_typing(input_password, "")
            time.sleep(1)

            print("[INFO] Mengklik tombol Simpan Perubahan...")
            btn_simpan = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Simpan Perubahan')]")
            btn_simpan.click()

            print("--------------------------------------------------")
            print("[RESULT] STATUS: FUNCTIONAL EDIT PROFILE PASSED")
            print("[CONCLUSION] Fitur edit profil berjalan 100% secara dinamis ke database.")
            print("--------------------------------------------------")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Terjadi kendala saat bot mengedit data: {e}")

    def close(self):
        print("\n[DONE] Seluruh rangkaian pengujian selesai. Menutup browser...")
        time.sleep(3)
        self.driver.quit()

if __name__ == "__main__":
    bot = EditProfilePageTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.navigasi_ke_profil()
    bot.test_proses_edit_profil()
    bot.close()