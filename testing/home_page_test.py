from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class HomePageTest:
    def __init__(self):
        """Metode inisialisasi untuk menyiapkan WebDriver dan membuka browser."""
        print("[SETUP] Menginisialisasi Chrome WebDriver...")
        # Konfigurasi opsi Chrome (opsional, misalnya agar tidak langsung tertutup)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:5000"
        
        # Buka halaman utama
        self.driver.get(self.base_url)
        # Tunggu maksimal 5 detik jika elemen belum muncul
        self.driver.implicitly_wait(5)

    def checkElement(self, locator_type, locator_value):
        """Memeriksa apakah sebuah elemen ada di halaman menggunakan ID atau CSS Selector."""
        try:
            if locator_type.lower() == 'id':
                element = self.driver.find_element(By.ID, locator_value)
            elif locator_type.lower() == 'css':
                element = self.driver.find_element(By.CSS_SELECTOR, locator_value)
            else:
                print(f"[ERROR] Tipe locator '{locator_type}' tidak didukung.")
                return False
            
            print(f"[PASS] Elemen dengan {locator_type}='{locator_value}' berhasil ditemukan.")
            return True
        except Exception as e:
            print(f"[FAIL] Elemen dengan {locator_type}='{locator_value}' TIDAK ditemukan.")
            return False

    def clickToggleMenu(self):
        """Mengklik tombol toggle menu (hamburger menu) pada tampilan mobile."""
        try:
            # Menggunakan class navbar-toggler standar Bootstrap
            toggle_btn = self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler")
            toggle_btn.click()
            print("[PASS] Tombol Toggle Menu berhasil diklik.")
            time.sleep(1) # Jeda visual
        except Exception as e:
            print("[FAIL] Tombol Toggle Menu tidak ditemukan atau tidak bisa diklik.")

    def clickButtonLihatSemuaVideo(self):
        """Mengklik tombol menuju galeri video."""
        try:
            # 1. Gunakan titik (.) pada XPath agar Selenium membaca seluruh teks di dalam <a> termasuk ikon <i>
            btn = self.driver.find_element(By.XPATH, "//a[contains(., 'Lihat Semua Video')]")
            # 2. Instruksikan browser untuk men-scroll halaman sampai tombol tersebut berada di tengah layar
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
            # Beri sedikit jeda agar animasi scroll selesai sebelum diklik
            time.sleep(1)
            # 3. Klik tombolnya
            btn.click()
            print("[PASS] Tombol 'Lihat Semua Video' berhasil diklik.")
            time.sleep(2) # Jeda visual untuk melihat perpindahan halaman
        except Exception as e:
            # Tambahkan print detail error agar kita tahu persis masalahnya jika masih gagal
            print(f"[FAIL] Gagal mengklik tombol 'Lihat Semua Video'. Detail Error: {e}")

    def closeBrowser(self):
        """Menutup browser dan mengakhiri sesi WebDriver."""
        self.driver.quit()
        print("[TEARDOWN] Browser telah ditutup.")

# Blok Eksekusi Utama
if __name__ == "__main__":
    # Pastikan server Flask MasApps sedang berjalan di terminal lain sebelum mengeksekusi ini!
    test_home = HomePageTest()
    print("\n--- Memulai Pengujian ---")
    
    # 1. Cek elemen Video Section (menggunakan ID)
    test_home.checkElement("id", "video")
    
    # 2. Cek elemen Logo/Brand Navbar (menggunakan CSS Selector)
    test_home.checkElement("css", ".navbar-brand")
    
    # 3. Uji interaksi tombol navigasi video
    test_home.clickButtonLihatSemuaVideo()
    
    print("--- Pengujian Selesai ---\n")
    # Menutup browser
    test_home.closeBrowser()