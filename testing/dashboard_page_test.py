from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class DashboardIntegrasiTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi Chrome WebDriver...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"

    def slow_typing(self, element, text, speed=0.10):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(speed)

    def solve_captcha(self):
        """Membaca dan menghitung CAPTCHA."""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
            if match:
                hasil = int(match.group(1)) + int(match.group(2))
                return str(hasil)
            return "0"
        except:
            return "0"

    def submit_login(self, user, pw, captcha):
        """Input form dengan delay mengetik, lalu langsung klik login."""
        u_field = self.driver.find_element(By.NAME, "username")
        self.slow_typing(u_field, user)

        p_field = self.driver.find_element(By.NAME, "password")
        self.slow_typing(p_field, pw)

        c_field = self.driver.find_element(By.NAME, "captcha")
        self.slow_typing(c_field, captcha, speed=0.15)
        
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print(f"[LOGIN] Mencoba masuk dengan user: {user}")
        
    def run_full_test(self):
            self.driver.get(self.base_url)
            time.sleep(1.5)
            btn_admin = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin Portal")))
            btn_admin.click()

    def test_wrong_captcha(self):
            print("\n[LOGIN] Percobaan 1: CAPTCHA Salah")
            self.submit_login("mhs1", "123", "40")
            time.sleep(1.5)

    def test_wrong_password(self):
            print("[LOGIN] Percobaan 2: Username dan Password Salah")
            jawaban = self.solve_captcha()
            self.submit_login("uvers123", "111222", jawaban)
            time.sleep(1.5)

    def test_successful_login(self):
            print("[LOGIN] Percobaan 3: Berhasil")
            jawaban_final = self.solve_captcha()
            self.submit_login("admin", "12345", jawaban_final)
            
            self.wait.until(EC.url_contains("dashboard"))
            print("[PASS] Masuk Dashboard.")

    def edit_berita(self, judul_baru, konten_baru):
            print("\n[EDIT] Menguji Edit Berita...")
            btn_edit = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-warning")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_edit)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn_edit)

            judul_field = self.wait.until(EC.presence_of_element_located((By.NAME, "judul")))
            self.slow_typing(judul_field, "Kenaikan Harga BBM dikarenakan Perang Iran VS AS", speed=0.05)
            
            konten_field = self.driver.find_element(By.NAME, "konten")
            self.slow_typing(konten_field, "Perubahan ke-1, Ini konten hasil testing", speed=0.05)

            print("[INFO] Scroll ke bawah mencari tombol simpan...")
            simpan_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Simpan Perubahan')]")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", simpan_btn)
            time.sleep(1.5)
            
            self.driver.execute_script("arguments[0].click();", simpan_btn)
            print("[PASS] Edit Berhasil Simpan.")
            time.sleep(2)

    def hapus_berita(self):
            print("\n[HAPUS] Menguji Hapus Berita...")
            list_btn_hapus = self.driver.find_elements(By.CLASS_NAME, "btn-danger")
            if list_btn_hapus:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", list_btn_hapus[0])
                time.sleep(1.0)
                self.driver.execute_script("arguments[0].click();", list_btn_hapus[0])

                try:
                    self.wait.until(EC.alert_is_present())
                    print("[INFO] Pop-up konfirmasi muncul. Menunggu sebentar...")
                    time.sleep(1.5)
                    self.driver.switch_to.alert.accept()
                    print("[PASS] Berita Berhasil Dihapus.")
                except:
                    print("[WARNING] Pop-up tidak muncul.")

    def close(self):
        print("\n[DONE] Pengujian Selesai. Menutup browser...")
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = DashboardIntegrasiTest()
    bot.run_full_test()
    bot.test_wrong_captcha()
    bot.test_wrong_password()
    bot.test_successful_login()
    bot.edit_berita("Perubahan ke-1", "Ini konten hasil testing")
    bot.hapus_berita()
    bot.close()