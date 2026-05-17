import pytest
import time
from utils.auth_helper import hash_password, verify_password

def test_bottom_up_auth_helper():
    print("\n[START] Memulai Pengujian Integrasi Bottom-Up...")
    
    plain_password = "AdminUVERS2026!"
    hashed_pwd = hash_password(plain_password)

    assert hashed_pwd != plain_password
    assert verify_password(hashed_pwd, plain_password) is True
    
    simulasi_db_user_hash = hashed_pwd
    input_form_salah = "AdminUvers2026"
    
    assert verify_password(simulasi_db_user_hash, input_form_salah) is False
    
    print("\n[SUCCESS] Uji Bottom-Up: Modul auth_helper tervalidasi dan siap diintegrasikan ke route /login.")