import os
import random
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps
from utils.auth_helper import verifikasi_login

app = Flask(__name__)
app.secret_key = 'secret_key_123'# agar session bisa dienkripsi

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_berita_masapps'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    
    # Ambil berita terbaru (dngan JOIN kategori agar muncul nmanya)
    cur.execute("""
        SELECT berita.*, kategori.nama_kategori 
        FROM berita 
        LEFT JOIN kategori ON berita.id_kategori = kategori.id 
        ORDER BY berita.id DESC LIMIT 6
    """)
    semua_berita = cur.fetchall()
    
    # mbil video trbaru dari database
    cur.execute("SELECT * FROM videos ORDER BY id DESC LIMIT 3")
    semua_video = cur.fetchall()
    
    cur.close()
    return render_template('index.html', 
                           berita=semua_berita, 
                           videos=semua_video, 
                           data="BatamInfo")

# --- Fungsi Dcorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Jika tidak da 'user_id' di dalam session, tndang kembali ke halman login
        if 'user_id' not in session:
            flash("Akses ditolak! Anda harus login terlebih dahulu.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Jika user ada sesion, lngsung  ke dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # 2. Ambil input dari form login
        user_input = request.form.get('username')
        pw_input = request.form.get('password')
        user_captcha = request.form.get('captcha')

        # 3. Validasi CAPTCHA terlebih dahulu
        # Mengonversi input captcha ke integer untuk dibandingkan dengan jawaban di session
        if not user_captcha or int(user_captcha) != session.get('captcha_ans'):
            flash("CAPTCHA salah! Silakan hitung kembali dengan teliti.", "danger")
            return redirect(url_for('login'))

        # 4. Cari data user di database berdasarkan username
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [user_input])
        user_data = cur.fetchone()
        cur.close()

        # 5. Memanggil fungsi verifikasi dari modul auth_helper
        # Memastikan fungsi di utils/auth_helper.py sudah diperbarui untuk menerima parameter user_data
        if verifikasi_login(user_input, pw_input, user_data):
            # 6. Mendaftarkan data ke dalam Session
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['nama_lengkap'] = user_data['nama_lengkap']
            session['role'] = user_data['role']
            
            flash(f"Selamat datang, {user_data['nama_lengkap']}! Login berhasil.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Username atau Password salah!", "danger")
            return redirect(url_for('login'))

    # 7. Logika GET (saat halaman pertama kali dibuka)
    # Membuat pertanyaan CAPTCHA matematika acak
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    session['captcha_ans'] = num1 + num2 # Simpan jawaban di session untuk divalidasi nanti
    pertanyaan_captcha = f"Berapakah {num1} + {num2}?"
    
    return render_template('login.html', captcha_text=pertanyaan_captcha)
    # Jika user sudah login, jangan biarkan masuk ke halaman login lagi
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    pesan = ""
    if request.method == 'POST':
        user_input = request.form.get('username')
        pw_input = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [user_input])
        user_data = cur.fetchone()
        cur.close()

        if verifikasi_login(user_input, pw_input, user_data):
            # --- Mendaftarkan Session ---
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['nama_lengkap'] = user_data['nama_lengkap']
            session['role'] = user_data['role']
            
            flash(f"Selamat datang, {user_data['nama_lengkap']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            pesan = "Username atau Password salah!"
            
    return render_template('login.html', message=pesan)

@app.route('/logout')
def logout():
    # --- Menghapus Session ---
    session.clear()
    flash("Anda telah berhasil logout.", "info")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM berita ORDER BY id DESC")
    data_berita = cur.fetchall()
    cur.close()
    
    return render_template('dashboard.html', berita=data_berita)

# --- CRUD KATEGORI ---
@app.route('/kelola-kategori')
@login_required
def kelola_kategori():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kategori")
    data = cur.fetchall()
    cur.close()
    return render_template('kelola_kategori.html', kategori=data)

@app.route('/add-kategori', methods=['POST'])
@login_required
def add_kategori():
    nama = request.form['nama_kategori']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO kategori (nama_kategori) VALUES (%s)", [nama])
    mysql.connection.commit()
    cur.close()
    flash("Kategori berhasil ditambah!", "success")
    return redirect(url_for('kelola_kategori'))

@app.route('/delete-kategori/<int:id>', methods=['POST'])
@login_required
def delete_kategori(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM kategori WHERE id = %s", (id,))
        mysql.connection.commit()
        flash("Kategori berhasil dihapus!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash("Gagal menghapus! Kategori ini masih terikat dengan data berita.", "danger")
    finally:
        cur.close()
    return redirect(url_for('kelola_kategori'))

# --- CRUD HASHTAG ---
@app.route('/kelola-hashtag')
@login_required
def kelola_hashtag():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hashtag")
    data = cur.fetchall()
    cur.close()
    return render_template('kelola_hashtag.html', hashtag=data)

@app.route('/add-hashtag', methods=['POST'])
@login_required
def add_hashtag():
    nama = request.form['nama_hashtag']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO hashtag (nama_hashtag) VALUES (%s)", [nama])
    mysql.connection.commit()
    cur.close()
    flash("Hashtag berhasil ditambah!", "success")
    return redirect(url_for('kelola_hashtag'))

@app.route('/delete-hashtag/<int:id>', methods=['POST'])
@login_required
def delete_hashtag(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM hashtag WHERE id = %s", (id,))
        mysql.connection.commit()
        flash("Hashtag berhasil dihapus!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash("Gagal menghapus! Hashtag ini masih digunakan.", "danger")
    finally:
        cur.close()
    return redirect(url_for('kelola_hashtag'))

# --- PERBARUI ADD DATA BERITA ---
@app.route('/add-data', methods=['GET', 'POST'])
@login_required
def add_data():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        konten = request.form['konten']
        id_kat = request.form['id_kategori']
        tags = request.form.getlist('hashtags') # Mengambil banyak hashtag
        
        file = request.files['gambar']
        filename = None
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO berita (judul, penulis, konten, id_kategori, gambar) VALUES (%s, %s, %s, %s, %s)", 
                    (judul, penulis, konten, id_kat, filename))
        berita_id = cur.connection.insert_id()


        # Simpan Hashtag ke Junction Table
        for tag_id in tags:
            cur.execute("INSERT INTO berita_hashtag (berita_id, hashtag_id) VALUES (%s, %s)", (berita_id, tag_id))
        
        mysql.connection.commit()
        cur.close()
        flash("Berita berhasil terbit!", "success")
        return redirect(url_for('dashboard'))
    
    # Ambil data kategori & hashtag untuk pilihan di form
    cur.execute("SELECT * FROM kategori")
    kat = cur.fetchall()
    cur.execute("SELECT * FROM hashtag")
    tag = cur.fetchall()
    cur.close()
    return render_template('add_data.html', kategori=kat, hashtag=tag)

@app.route('/edit-data/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_data(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        # 1. Ambil data dari Form
        judul = request.form['judul']
        penulis = request.form['penulis']
        konten = request.form['konten']
        id_kat = request.form['id_kategori']
        tags = request.form.getlist('hashtags')
        
        # 2. Ambil file gambar (jika ada)
        file = request.files.get('gambar')
        
        # 3. Logika Update: Cek apakah ada file baru yang diunggah
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Query Update dengan mengganti GAMBAR
            cur.execute("""
                UPDATE berita 
                SET judul=%s, penulis=%s, konten=%s, id_kategori=%s, gambar=%s 
                WHERE id=%s
            """, (judul, penulis, konten, id_kat, filename, id))
        else:
            # Query Update TANPA mengganti gambar (tetap gunakan gambar lama)
            cur.execute("""
                UPDATE berita 
                SET judul=%s, penulis=%s, konten=%s, id_kategori=%s 
                WHERE id=%s
            """, (judul, penulis, konten, id_kat, id))

        # 4. Kelola Hashtag (Hapus relasi lama di junction table, masukkan yang baru)
        cur.execute("DELETE FROM berita_hashtag WHERE berita_id = %s", [id])
        for tag_id in tags:
            cur.execute("INSERT INTO berita_hashtag (berita_id, hashtag_id) VALUES (%s, %s)", (id, tag_id))
        
        mysql.connection.commit()
        cur.close()
        flash("Data berita berhasil diperbarui!", "info")
        return redirect(url_for('dashboard'))

    # --- BAGIAN GET (Menampilkan Data ke Form saat halaman dibuka) ---
    
    # Ambil data berita yang dipilih
    cur.execute("SELECT * FROM berita WHERE id = %s", [id])
    item = cur.fetchone()

    # Ambil data kategori untuk pilihan Dropdown
    cur.execute("SELECT * FROM kategori")
    kat = cur.fetchall()

    # Ambil data hashtag untuk pilihan Checkbox
    cur.execute("SELECT * FROM hashtag")
    tag = cur.fetchall()

    # Ambil ID hashtag yg sudah terpilih sebelumnya untuk berita ini
    cur.execute("SELECT hashtag_id FROM berita_hashtag WHERE berita_id = %s", [id])
    # ubah hasilnya menjadi list sederhana [1, 3, 5] agar mudah dicek di HTML
    selected_tags = [t['hashtag_id'] for t in cur.fetchall()]

    cur.close()
    
    return render_template('edit_data.html', 
                           item=item, 
                           kategori=kat, 
                           hashtag=tag, 
                           selected_hashtags=selected_tags)
@app.route('/delete-data/<int:id>', methods=['GET'])
@login_required
def delete_data(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM berita WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Data berita telah dihapus!", "warning")
    return redirect(url_for('dashboard'))

@app.route('/berita/<int:id>')
def detail_berita(id):
    cur = mysql.connection.cursor()
    
    # 1. Ambil data berita + Nama Kategori menggunakan JOIN
    query_berita = """
        SELECT berita.*, kategori.nama_kategori 
        FROM berita 
        LEFT JOIN kategori ON berita.id_kategori = kategori.id 
        WHERE berita.id = %s
    """
    cur.execute(query_berita, [id])
    berita_item = cur.fetchone()
    
    # 2. Ambil semua hashtag untuk berita ini menggunakan Junction Table
    query_tags = """
        SELECT hashtag.nama_hashtag 
        FROM berita_hashtag 
        JOIN hashtag ON berita_hashtag.hashtag_id = hashtag.id 
        WHERE berita_hashtag.berita_id = %s
    """
    cur.execute(query_tags, [id])
    hashtags_list = cur.fetchall()
    
    # 3. Ambil semua komentar
    cur.execute("SELECT * FROM komentar WHERE berita_id = %s ORDER BY created_at DESC", [id])
    daftar_komentar = cur.fetchall()
    
    cur.close()
    
    if berita_item:
        return render_template('detail_berita.html', 
                               berita=berita_item, 
                               komentar=daftar_komentar, 
                               hashtags=hashtags_list)
    return "Berita tidak ditemukan", 404
    cur = mysql.connection.cursor()
    
    # Ambil data berita berdasarkan ID
    cur.execute("SELECT * FROM berita WHERE id = %s", [id])
    berita_item = cur.fetchone()
    
    # Ambil semua komentar yang berhubungan dengan berita ini
    cur.execute("SELECT * FROM komentar WHERE berita_id = %s ORDER BY created_at DESC", [id])
    daftar_komentar = cur.fetchall()
    
    cur.close()
    
    if berita_item:
        return render_template('detail_berita.html', berita=berita_item, komentar=daftar_komentar)
    return "Berita tidak ditemukan", 404

@app.route('/tambah-komentar', methods=['POST'])
def tambah_komentar():
    id_berita = request.form.get('berita_id')
    nama = request.form.get('nama')
    isi = request.form.get('isi')

    if nama and isi:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO komentar (berita_id, nama_pengomentar, isi_komentar) VALUES (%s, %s, %s)", 
                    (id_berita, nama, isi))
        mysql.connection.commit()
        cur.close()
        flash("Komentar berhasil ditambahkan!", "success")
    
    return redirect(url_for('detail_berita', id=id_berita))

@app.route('/kelola-komentar')
@login_required
def kelola_komentar():
    cur = mysql.connection.cursor()
    # Mengambil data komentar beserta judul beritanya menggunakan JOIN
    query = """
        SELECT komentar.*, berita.judul as judul_berita 
        FROM komentar 
        JOIN berita ON komentar.berita_id = berita.id 
        ORDER BY komentar.created_at DESC
    """
    cur.execute(query)
    semua_komentar = cur.fetchall()
    cur.close()
    return render_template('kelola_komentar.html', daftar_komentar=semua_komentar)

@app.route('/delete-komentar/<int:id>', methods=['GET'])
@login_required
def delete_komentar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM komentar WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Komentar telah dihapus!", "warning")
    return redirect(url_for('kelola_komentar'))

# --- CRUD VIDEO YOUTUBE ---
@app.route('/kelola-video')
@login_required
def kelola_video():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM videos ORDER BY id DESC")
    data_video = cur.fetchall()
    cur.close()
    return render_template('kelola_video.html', videos=data_video)

@app.route('/add-video', methods=['GET', 'POST'])
@login_required
def add_video():
    if request.method == 'POST':
        judul = request.form['judul']
        yt_id = request.form['youtube_id']
        ket = request.form['keterangan']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO videos (judul, youtube_id, keterangan) VALUES (%s, %s, %s)", (judul, yt_id, ket))
        mysql.connection.commit()
        cur.close()
        flash("Video baru berhasil ditambahkan!", "success")
        return redirect(url_for('kelola_video'))
    return render_template('add_video.html')

@app.route('/delete-video/<int:id>')
@login_required
def delete_video(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM videos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Video berhasil dihapus!", "warning")
    return redirect(url_for('kelola_video'))

@app.route('/profil')
@login_required
def profil():
    # Mengambil ID secara dinamis dari session
    user_id_sekarang = session.get('user_id')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", [user_id_sekarang])
    user_info = cur.fetchone()
    cur.close()
    
    if user_info:
        return render_template('profil.html', user=user_info)
    return "User tidak ditemukan", 404

@app.route('/kelola-user')
@login_required
def kelola_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC")
    daftar_user = cur.fetchall()
    cur.close()
    return render_template('kelola_user.html', users=daftar_user)

@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama_lengkap']
        role = request.form['role']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, nama_lengkap, role) VALUES (%s, %s, %s, %s)", 
                    (username, password, nama, role))
        mysql.connection.commit()
        cur.close()
        flash("User baru berhasil ditambahkan!", "success")
        return redirect(url_for('kelola_user'))
    return render_template('add_user.html')

@app.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        nama = request.form['nama_lengkap']
        role = request.form['role']
        password = request.form['password']

        if password:
            cur.execute("UPDATE users SET username=%s, nama_lengkap=%s, role=%s, password=%s WHERE id=%s", 
                        (username, nama, role, password, id))
        else:
            cur.execute("UPDATE users SET username=%s, nama_lengkap=%s, role=%s WHERE id=%s", 
                        (username, nama, role, id))
            
        mysql.connection.commit()
        cur.close()
        flash("Data user berhasil diperbarui!", "info")
        return redirect(url_for('kelola_user'))
    
    cur.execute("SELECT * FROM users WHERE id = %s", [id])
    user_data = cur.fetchone()
    cur.close()
    return render_template('edit_user.html', user=user_data)

@app.route('/delete-user/<int:id>', methods=['GET'])
@login_required
def delete_user(id):
    # Proteksi: admin tidak boleh menghapus dirinya sendiri
    if id == session.get('user_id'):
        flash("Anda tidak bisa menghapus akun Anda sendiri!", "danger")
        return redirect(url_for('kelola_user'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash("User telah dihapus!", "warning")
    return redirect(url_for('kelola_user'))

@app.route('/video-gallery')
def video_gallery():
    cur = mysql.connection.cursor()
    # Mengambil semua video tanpa batasan LIMIT
    cur.execute("SELECT * FROM videos ORDER BY id DESC")
    semua_video = cur.fetchall()
    cur.close()
    return render_template('video_gallery.html', videos=semua_video)

if __name__ == '__main__':
    app.run(debug=True)