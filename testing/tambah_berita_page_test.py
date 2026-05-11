from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import re
import os

class TambahBeritaTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi Chrome WebDriver untuk Tambah Berita...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"

    def slow_typing(self, element, text, speed=0.07):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(speed)

    def solve_captcha(self):
        """Membaca dan menghitung CAPTCHA secara otomatis."""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
            if match:
                hasil = int(match.group(1)) + int(match.group(2))
                return str(hasil)
            return "0"
        except:
            return "0"
    
    def run_full_test(self):
            self.driver.get(self.base_url)
            time.sleep(1.5)
            btn_admin = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Admin Portal")))
            btn_admin.click()

    def login_masuk(self, user, pw):
        """Proses login sebelum masuk ke dashboard."""
        print(f"[LOGIN] Mencoba masuk sebagai {user}...")
        self.driver.get(f"{self.base_url}/login")
        
        u_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        self.slow_typing(u_field, user)
        
        p_field = self.driver.find_element(By.NAME, "password")
        self.slow_typing(p_field, pw)
        
        jawaban = self.solve_captcha()
        c_field = self.driver.find_element(By.NAME, "captcha")
        self.slow_typing(c_field, jawaban, speed=0.15)
        
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait.until(EC.url_contains("dashboard"))
        print("[PASS] Login Berhasil, Sekarang di Dashboard.")

    def test_tambah_berita_baru(self):
        print("\n[ACTION] Memulai Proses Tambah Berita Baru...")
        try:
            btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Tambah Berita')]")))
            btn_menu.click()
            time.sleep(1.5)

            judul_field = self.wait.until(EC.presence_of_element_located((By.NAME, "judul")))
            self.slow_typing(judul_field, "Harga Emas Meningkat", speed=0.05)

            penulis_field = self.driver.find_element(By.NAME, "penulis")
            self.slow_typing(penulis_field, "John Philip", speed=0.05)

            konten_field = self.driver.find_element(By.NAME, "konten")
            self.slow_typing(konten_field, "Kenaikan Harga Emas dikarenakan adanya inflasi.", speed=0.05)

            print("[INFO] Mencari file gambar di folder Downloads...")
            nama_file = "test.jpg"
            path_gambar = os.path.join(os.path.expanduser("~"), "Downloads", nama_file)
            
            if os.path.exists(path_gambar):
                file_input = self.driver.find_element(By.NAME, "gambar")
                file_input.send_keys(path_gambar)
                print(f"[SUCCESS] File {nama_file} berhasil dipilih.")
            else:
                print(f"[WARNING] File {nama_file} tidak ditemukan. Melewati upload.")
            time.sleep(1)

            print("[INFO] Memilih kategori berita...")
            try:
                dropdown_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@name, 'kategori') or contains(@id, 'kategori')]")))
                dropdown_kategori = Select(dropdown_element)
                dropdown_kategori.select_by_index(1) 
                print("[SUCCESS] Kategori berhasil dipilih.")
            except Exception as e:
                print(f"[WARNING] Gagal memilih kategori lewat Select: {e}")
                self.driver.execute_script("arguments[0].click();", dropdown_element)
            
            print("[INFO] Memilih hashtag...")
            try:
                hastag_pertama = "#Python"
                hashtag_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[contains(., '{hastag_pertama}')]")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hashtag_element)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", hashtag_element)

                hastag_kedua = "#Testing"
                hashtag_kedua = self.driver.find_element(By.XPATH, f"//label[contains(., '{hastag_kedua}')]")
                self.driver.execute_script("arguments[0].click();", hashtag_kedua)
                
                print(f"[SUCCESS] Hashtag {hastag_pertama} dan {hastag_kedua} dipilih.")
            except Exception as e:
                print(f"[WARNING] Gagal pilih hashtag: {e}")

            simpan_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Simpan Berita')]")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", simpan_btn)
            time.sleep(2)
            
            self.driver.execute_script("arguments[0].click();", simpan_btn)
            print("[PASS] Berita Berhasil Disimpan!")
            
            self.wait.until(EC.url_contains("dashboard"))
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Error saat tambah berita: {e}")

    def close(self):
        print("\n[DONE] Selesai. Menutup browser...")
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = TambahBeritaTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.test_tambah_berita_baru()
    bot.close()