# test_integration.py
import pytest
import time
from utils.auth_helper import hash_password, verify_password

def test_bottom_up_auth_helper():
    print("\n[START] Memulai Pengujian Integrasi Bottom-Up...")
    
    # =========================================================================
    # 1. UJI LEVEL BAWAH: Fungsi utilitas enkripsi bekerja mandiri
    # =========================================================================
    plain_password = "AdminUVERS2026!"
    hashed_pwd = hash_password(plain_password)
    
    # Validasi: Hasil hash tidak boleh sama dengan teks biasa (Plaintext)
    assert hashed_pwd != plain_password
    # Validasi: Fungsi verifikasi harus mengembalikan True untuk password yang benar
    assert verify_password(hashed_pwd, plain_password) is True
    
    # =========================================================================
    # 2. SIMULASI INTEGRASI LEVEL MENENGAH (Data Form Login -> Helper -> DB)
    # =========================================================================
    simulasi_db_user_hash = hashed_pwd  # Anggap data ini yang ditarik dari kolom MySQL
    input_form_salah = "AdminUvers2026"  # Simulasi kesalahan ketik (typo) dari pengguna
    
    # Validasi: Fungsi verifikasi harus menolak password yang salah (Mengembalikan False)
    assert verify_password(simulasi_db_user_hash, input_form_salah) is False
    
    print("\n[SUCCESS] Uji Bottom-Up: Modul auth_helper tervalidasi dan siap diintegrasikan ke route /login.")