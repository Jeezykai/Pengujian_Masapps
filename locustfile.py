# locustfile.py
from locust import HttpUser, task, between


class BatamInfoUser(HttpUser):
    # Waktu tunggu antar-permintaan (1 hingga 3 detik)
    wait_time = between(1, 3)

    @task
    def akses_beranda(self):
        # Mensimulasikan pengguna yang membuka halaman utama indeks berita
        self.client.get("/")