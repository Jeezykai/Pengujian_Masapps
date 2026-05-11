from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import re

class KelolaUserPageTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi WebDriver untuk Kelola User...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"
        self.target_user = "Selenium Bot"

    def slow_typing(self, element, text, speed=0.10):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(speed)

    def run_full_test(self):
            self.driver.get(self.base_url)
            time.sleep(1.25)
            btn_admin = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin Portal")))
            btn_admin.click()

    def login_masuk(self, user, pw):
        """Proses login otomatis dengan auto-solve captcha."""
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

    def navigasi_ke_kelola_user(self):
        """Pindah ke halaman Manajemen Pengguna melalui sidebar."""
        print("\n[NAVIGASI] Menuju Halaman Kelola User...")
        btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Kelola User')]")))
        btn_menu.click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Manajemen Pengguna')]")))
        print("[SUCCESS] Berhasil masuk ke halaman Kelola User.")
        time.sleep(1)

    def test_tambah_user(self):
        """Menguji proses Tambah User Baru."""
        print("\n[CRUD - CREATE] Menguji Tambah User Baru...")
        try:
            btn_tambah = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Tambah User')]")))
            btn_tambah.click()

            u_field = self.wait.until(EC.element_to_be_clickable((By.ID, "username")))
            print("[INFO] Mengisi form user baru...")
            
            self.slow_typing(u_field, self.target_user)
            self.slow_typing(self.driver.find_element(By.ID, "nama_lengkap"), "Selenium Testing Bot")

            dropdown_role = Select(self.driver.find_element(By.ID, "role"))
            dropdown_role.select_by_value("dosen")
            
            self.slow_typing(self.driver.find_element(By.ID, "password"), "test123")
            time.sleep(1)

            simpan_btn = self.driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Simpan')]")
            self.driver.execute_script("arguments[0].click();", simpan_btn)

            self.wait.until(EC.url_contains("user"))
            print(f"[PASS] User '{self.target_user}' berhasil dibuat!")
            time.sleep(0.5)

        except Exception as e:
            print(f"[FAIL] Gagal Tambah User: {e}")
            self.driver.get(f"{self.base_url}/user")

    def test_edit_user(self):
        """Menguji proses Edit User."""
        print(f"\n[CRUD - UPDATE] Menguji Edit User: {self.target_user}...")
        try:
            print(f"[INFO] Mencari tombol edit untuk {self.target_user}...")
            xpath_edit = f"//td[.//text()[contains(., '{self.target_user}')]]/following-sibling::td//a[contains(@class, 'btn-warning')]"
            btn_edit = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_edit)))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_edit)
            time.sleep(0.5)
            btn_edit.click()
            print("[INFO] Menunggu halaman edit dimuat...")
            try:
                n_field = WebDriverWait(self.driver, 1.5).until(EC.visibility_of_element_located((By.ID, "nama_lengkap")))
            except:
                n_field = self.driver.find_element(By.NAME, "nama_lengkap")

            print("[INFO] Melakukan perubahan data...")
            self.slow_typing(n_field, "Selenium Testing Bot V2")
            try:
                dropdown_el = self.driver.find_element(By.ID, "role")
            except:
                dropdown_el = self.driver.find_element(By.NAME, "role")
            
            Select(dropdown_el).select_by_value("mahasiswa")
            time.sleep(1)

            simpan_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self.driver.execute_script("arguments[0].click();", simpan_btn)

            self.wait.until(EC.url_contains("user"))
            print("[PASS] User berhasil diperbarui.")
            time.sleep(1)

        except Exception as e:
            print(f"[FAIL] Gagal Edit User: {e}")
            self.driver.get(f"{self.base_url}/user")
            time.sleep(1)

    def test_hapus_user(self):
        """Menguji proses Hapus User dengan konfirmasi."""
        print(f"\n[CRUD - DELETE] Menguji Hapus User: {self.target_user}...")
        try:
            xpath_hapus = f"//td[contains(., '{self.target_user}')]/following-sibling::td//a[contains(@class, 'btn-danger')]"
            btn_hapus = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_hapus)))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_hapus)
            time.sleep(1)
            btn_hapus.click()

            print("[INFO] Menunggu konfirmasi alert...")
            self.wait.until(EC.alert_is_present())
            time.sleep(1)
            self.driver.switch_to.alert.accept() 
            
            print(f"[PASS] User '{self.target_user}' telah dihapus.")
            time.sleep(1)

        except Exception as e:
            print(f"[FAIL] Gagal Hapus User: {e}")

    def close(self):
        print("\n[DONE] Selesai. Menutup browser dalam 5 detik...")
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = KelolaUserPageTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.navigasi_ke_kelola_user()
    time.sleep(1)
    bot.test_tambah_user()
    time.sleep(1)
    bot.test_edit_user()
    time.sleep(1)
    bot.test_hapus_user()
    bot.close()