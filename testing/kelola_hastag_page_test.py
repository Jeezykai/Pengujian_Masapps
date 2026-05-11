from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class KelolaHashtagPageTest:
    def __init__(self):
        print("[SETUP] Menginisialisasi WebDriver untuk Kelola Hashtag...")
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://127.0.0.1:5000"
        self.target_hashtag = "#Javascript" 

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

    def navigasi_ke_kelola_hashtag(self):
        print("\n[NAVIGASI] Menuju Halaman Kelola Hashtag...")
        btn_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Kelola Hashtag')]")))
        btn_menu.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Daftar Hashtag')]")))
        print("[SUCCESS] Sudah di halaman Kelola Hashtag.")
        time.sleep(1)

    def test_tambah_hashtag(self):
        print(f"\n[CRUD - CREATE] Menguji Tambah Hashtag: {self.target_hashtag}...")
        try:
            input_h = self.wait.until(EC.element_to_be_clickable((By.NAME, "nama_hashtag")))
            self.slow_typing(input_h, self.target_hashtag)
            time.sleep(1)
            btn_simpan = self.driver.find_element(By.XPATH, "//button[contains(., 'Simpan Hashtag')]")
            btn_simpan.click()
        
            print("[INFO] Memverifikasi data baru...")
            xpath_verif = f"//table//code[contains(text(), '{self.target_hashtag}')]"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_verif)))
            
            print(f"[PASS] Hashtag '{self.target_hashtag}' sukses ditambahkan!")
            time.sleep(2)

        except Exception as e:
            print(f"[FAIL] Gagal Tambah Hashtag: {e}")

    # def test_hapus_hashtag(self):
    #     print(f"\n[CRUD - DELETE] Menguji Hapus Hashtag: {self.target_hashtag}...")
    #     try:
    #         xpath_hapus = f"//tr[td/code[contains(text(), '{self.target_hashtag}')]]//button[contains(@class, 'text-danger')]"
    #         btn_hapus = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_hapus)))
    #         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_hapus)
    #         time.sleep(1)
    #         btn_hapus.click()

    #         self.wait.until(EC.alert_is_present())
    #         time.sleep(1)
    #         self.driver.switch_to.alert.accept() 
            
    #         print(f"[PASS] Hashtag '{self.target_hashtag}' berhasil dihapus.")
    #         time.sleep(1.5)

    #     except Exception as e:
    #         print(f"[FAIL] Gagal Hapus Hashtag: {e}")

    def close(self):
        print("\n[DONE] Selesai. Menutup browser...")
        time.sleep(3)
        self.driver.quit()

if __name__ == "__main__":
    bot = KelolaHashtagPageTest()
    bot.run_full_test()
    bot.login_masuk("admin", "12345")
    time.sleep(1)
    bot.navigasi_ke_kelola_hashtag()
    bot.test_tambah_hashtag()
    # bot.test_hapus_hashtag()
    bot.close()