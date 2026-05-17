from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password_plaintext):
    """Mengamankan password plaintext menggunakan algoritma hashing bawaan Werkzeug."""
    return generate_password_hash(password_plaintext)

def verify_password(password_hash, password_plaintext):
    """Memverifikasi apakah password plaintext cocok dengan hash yang tersimpan."""
    return check_password_hash(password_hash, password_plaintext)

def verifikasi_login(username, password, user_data):
    """
    Memverifikasi apakah input username dan password cocok dengan data dari database.
    user_data adalah hasil fetchone() dari tabel users.
    """
    if user_data:
        if username == user_data['username'] and password == user_data['password']:
            return True
    return False