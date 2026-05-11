# utils/auth_helper.py
from werkzeug.security import generate_password_hash, check_password_hash

# def hash_password(password_plaintext):
#     return generate_password_hash(password_plaintext)

# def verify_password(password_hash, password_plaintext):
#     return check_password_hash(password_hash, password_plaintext)

def verifikasi_login(username, password, user_data):
    """
    Memverifikasi apakah input username dan password cocok dengan data dari database.
    user_data adalah hasil fetchone() dari tabel users.
    """
    if user_data:
        # - hashing
        # if username == user_data['username'] and verify_password(user_data['password'], password):
        if username == user_data['username'] and password == user_data['password']:
            return True
    return False