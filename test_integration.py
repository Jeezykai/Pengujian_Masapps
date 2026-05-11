import pytest
from utils.auth_helper import hash_password, verify_password

def test_bottom_up_auth_helper():
    # 1. Uji level bawah: Fungsi utilitas bekerja mandiri
    plain_password = "AdminUVERS2026!"
    hashed_pwd = hash_password(plain_password)
    
    assert hashed_pwd != plain_password
    assert verify_password(hashed_pwd, plain_password) == True
    
    # 2. Simulasi Integrasi level menengah (Data dari form login -> helper -> validasi)
    simulasi_db_user_hash = hashed_pwd # Anggap ini data yang ditarik dari MySQL
    input_form_salah = "AdminUvers2026" # Simulasi typo dari pengguna
    
    assert verify_password(simulasi_db_user_hash, input_form_salah) == False
    print("\n[SUCCESS] Uji Bottom-Up: Modul auth_helper tervalidasi dan siap diintegrasikan ke route /login.")
