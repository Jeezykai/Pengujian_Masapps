from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

class LoginPageTest:
    def __init__(self):
        """Inisialisasi WebDriver dan buka halaman Login."""
        print("[SETUP] Menginisialisasi Chrome WebDriver untuk Halaman Login...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:5000/login"
        # Buka halaman
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(5)

    def checkElement(self, locator_type, locator_value):
        """Memeriksa keberadaan elemen di halaman login."""
        try:
            if locator_type.lower() == 'name':
                self.driver.find_element(By.NAME, locator_value)
            elif locator_type.lower() == 'id':
                self.driver.find_element(By.ID, locator_value)
            print(f"[PASS] Elemen '{locator_value}' ditemukan.")
            return True
        except:
            print(f"[FAIL] Elemen '{locator_value}' TIDAK ditemukan.")
            return False

    def solve_captcha(self):
        """Membaca teks di layar untuk menemukan soal matematika, menghitungnya, dan mengembalikan hasilnya."""
        try:
            # Ambil seluruh teks yang ada di body halaman
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            # Cari pola angka + angka menggunakan Regex
            match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
            if match:
                angka1 = int(match.group(1))
                angka2 = int(match.group(2))
                hasil = angka1 + angka2
                print(f"[INFO] Bot membaca CAPTCHA: {angka1} + {angka2} = {hasil}")
                return str(hasil)
            print("[WARNING] Pola CAPTCHA tidak ditemukan di layar.")
            return "0"
        except Exception as e:
            print(f"[ERROR] Gagal membaca CAPTCHA: {e}")
            return "0"

    def attempt_login(self, username, password, captcha_answer):
        """Fungsi pembantu untuk mengisi form dan menekan tombol login."""
        time.sleep(1) # Jeda visual
        try:
            # Mengisi Username
            user_field = self.driver.find_element(By.NAME, "username")
            user_field.clear()
            user_field.send_keys(username)
            # Mengisi Password
            pass_field = self.driver.find_element(By.NAME, "password")
            pass_field.clear()
            pass_field.send_keys(password)
            # Mengisi Captcha
            captcha_field = self.driver.find_element(By.NAME, "captcha")
            captcha_field.clear()
            captcha_field.send_keys(captcha_answer)
            # Tekan tombol submit
            submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            time.sleep(2) # Tunggu respons dari server
        except Exception as e:
            print(f"[FAIL] Gagal mengeksekusi form login. Error: {e}")

    def test_wrong_captcha(self):
        """Test Case 1: Username & Password BENAR, tapi CAPTCHA SALAH"""
        print("\n--- Menjalankan Test Case 1: CAPTCHA Salah ---")
        self.attempt_login("admin", "AdminUVERS2026!", "999")
        if "login" in self.driver.current_url:
            print("[PASS] Sistem berhasil MENOLAK login karena CAPTCHA salah.")
        else:
            print("[FAIL] Sistem kebobolan, masuk ke dashboard dengan CAPTCHA salah!")

    def test_wrong_credentials(self):
        """Test Case 2: Username/Password SALAH, tapi CAPTCHA BENAR"""
        print("\n--- Menjalankan Test Case 2: Kredensial Salah ---")
        jawaban_benar = self.solve_captcha()
        self.attempt_login("hacker", "password123", jawaban_benar)
        if "login" in self.driver.current_url:
            print("[PASS] Sistem berhasil MENOLAK kredensial yang salah.")
        else:
            print("[FAIL] Sistem membiarkan user tak dikenal masuk!")

    def test_success_login(self):
        """Test Case 3: Username, Password, dan CAPTCHA BENAR (Happy Path)"""
        print("\n--- Menjalankan Test Case 3: Login Berhasil ---")
        self.driver.get(self.base_url)
        jawaban_benar = self.solve_captcha()
        # Ganti dengan data riil database Anda
        self.attempt_login("mhs1", "123", jawaban_benar)
        if "dashboard" in self.driver.current_url.lower() or self.driver.current_url != self.base_url:
            print("[PASS] Login sukses! Berhasil masuk ke sistem.")
        else:
            print("[FAIL] Login gagal, tidak dialihkan ke dasbor.")

    def closeBrowser(self):
        """Menutup browser."""
        self.driver.quit()
        print("\n[TEARDOWN] Browser telah ditutup.")

# Blok Eksekusi Utama
if __name__ == "__main__":
    test_login = LoginPageTest()
    print("\n[PRE-FLIGHT] Memeriksa Elemen Input Form...")
    test_login.checkElement("name", "username")
    test_login.checkElement("name", "password")
    test_login.checkElement("name", "captcha")
    
    # Eksekusi variasi Test Case
    test_login.test_wrong_captcha()
    test_login.test_wrong_credentials()
    test_login.test_success_login()
    test_login.closeBrowser()