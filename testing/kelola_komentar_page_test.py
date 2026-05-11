from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class KelolaKomentarPageTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi WebDriver untuk Kelola Komentar...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"

    def slow_typing(self, element, text, speed=0.05):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(speed)

    def run_full_test(self):
        self.driver.get(self.base_url)
        time.sleep(1.5)
        btn_admin = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin Portal")))
        btn_admin.click()

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

    def navigasi_ke_kelola_komentar(self):
        print("\n[NAVIGASI] Menuju Halaman Kelola Komentar...")
        btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Kelola Komentar')]")))
        btn_menu.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Daftar Komentar Pembaca')]")))
        print("[SUCCESS] Sudah di halaman Kelola Komentar.")
        time.sleep(1)

    def test_hapus_komentar(self):
        print("\n[CRUD - DELETE] Menguji Menghapus Komentar...")
        try:
            rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
            if not rows or "Belum ada" in rows[0].text:
                print("[INFO] Tidak ada komentar yang bisa dihapus (Tabel Kosong).")
                return
            nama_target = rows[0].find_element(By.TAG_NAME, "strong").text
            print(f"[INFO] Target ditemukan: Komentar dari '{nama_target}'")
            btn_hapus = rows[0].find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_hapus)
            time.sleep(1)
            btn_hapus.click()
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"[ALERT] Mengonfirmasi penghapusan: {alert.text}")
            time.sleep(1)
            alert.accept()

            print(f"[PASS] Berhasil menghapus komentar milik '{nama_target}'.")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Gagal menghapus komentar: {e}")

    def close(self):
        print("\n[DONE] Selesai. Menutup browser...")
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = KelolaKomentarPageTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.navigasi_ke_kelola_komentar()
    bot.test_hapus_komentar()
    bot.close()