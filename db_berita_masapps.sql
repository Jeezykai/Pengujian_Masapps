-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 28 Apr 2026 pada 03.48
-- Versi server: 10.1.38-MariaDB
-- Versi PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_berita_masapps`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `berita`
--

CREATE TABLE `berita` (
  `id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `penulis` varchar(100) NOT NULL,
  `konten` text NOT NULL,
  `tanggal` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_kategori` int(11) DEFAULT NULL,
  `gambar` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `berita`
--

INSERT INTO `berita` (`id`, `judul`, `penulis`, `konten`, `tanggal`, `id_kategori`, `gambar`) VALUES
(3, 'Harga sembako sudah mulai merangkak naik, diperkirakan sudah dapat berjalan dan bisa berlari tahun depan.', 'Bejo Hartanto', 'PASAR SENGGOL – Tim medis ekonomi baru saja memberikan kabar mengejutkan mengenai kondisi kesehatan harga sembako di tanah air. Setelah sekian lama terlihat diam di tempat, kini kumpulan harga beras, telur, hingga minyak goreng dilaporkan sudah mulai bisa merangkak.\r\n\"Awalnya kami kira mereka cuma pegal-pegal, ternyata mereka lagi latihan motorik kasar,\" ujar seorang ibu rumah tangga sambil menatap sedih ke arah dompetnya yang semakin tipis. \"Minggu lalu masih merangkak pelan di angka Rp12.000, eh pagi ini kayaknya sudah mulai belajar berdiri.\"\r\nProses Tumbuh Kembang yang Terlalu Cepat\r\nPara ahli memprediksi bahwa sembako-sembako ini memiliki bakat atletik yang luar biasa. Jika tren \"nutrisi\" inflasi terus diberikan, diperkirakan pada akhir tahun nanti harga-harga tersebut sudah bisa berjalan dengan tegak tanpa perlu berpegangan pada subsidi lagi.\r\nBahkan, yang lebih mencemaskan adalah prediksi tahun depan. Bukannya sekolah atau kuliah, harga sembako ini justru diprediksi akan ikut lomba maraton alias berlari kencang.\r\n\"Kami khawatir tahun depan harga cabai sudah bisa ikut color run atau minimal ikut Car Free Day. Larinya kencang sekali, sampai-sampai gaji masyarakat yang cuma bisa jalan di tempat bakal ketinggalan jauh di belakang,\" ungkap seorang pengamat ekonomi sambil mengelap keringat dingin.\r\nMasyarakat Diminta Latihan Fisik\r\nMenanggapi fenomena harga yang hobi olahraga lari ini, masyarakat disarankan untuk mulai melakukan latihan fisik, terutama otot jantung. Hal ini penting agar saat melihat label harga di pasar tahun depan, warga tidak langsung pingsan di tempat.\r\nBeberapa warga mulai mengusulkan agar pemerintah mengadakan kompetisi tandingan. \"Kalau harga sembako bisa lari, harusnya pendapatan kami minimal bisa naik sepeda motor biar bisa ngejar,\" curhat seorang bapak yang baru saja gagal bernegosiasi dengan tukang tempe.\r\nHingga berita ini diturunkan, harga bawang merah dilaporkan sedang melakukan pemanasan (stretching) di pojok pasar, bersiap-siap untuk melakukan sprint pertama mereka minggu depan.', '2026-04-26 17:43:48', 3, '231206bsembako.jpg'),
(4, 'Penerapan V-Model dalam Software Testing', 'Masparudin Mahmud', 'V-Model merupakan model pengembangan perangkat lunak yang menekankan pada hubungan antara setiap fase pengembangan dengan fase pengujian yang sesuai.', '2026-04-26 18:09:43', 1, 'v-model_1.png'),
(5, 'Tips Coding Python OOP yang Efisien', 'Admin TPL', 'Pemrograman Berorientasi Objek (OOP) memungkinkan pengembang untuk membuat kode yang lebih modular dan mudah dipelihara menggunakan class dan object.', '2026-04-26 18:09:43', 1, '0_kPat5mwo2lVx7sqR.jpg'),
(6, 'Mahasiswa UVERS Raih Hibah Penelitian BIMA', 'Humas Kampus', 'Prestasi membanggakan diraih oleh mahasiswa Teknik Perangkat Lunak dalam kompetisi hibah penelitian tingkat nasional.', '2026-04-26 18:09:43', 2, 'benny-prawira-siauw-bersama-rekan-rekan-fellow-atlantic-1.jpeg'),
(7, 'Efek Samping Menabung Emas', 'Joko Susilo', 'Emas telah lama dielu-elukan sebagai aset safe haven—aset yang nilainya cenderung stabil bahkan meningkat saat kondisi ekonomi global tidak menentu. Emas adalah pilihan populer bagi pemula dan investor jangka panjang yang ingin melindungi nilai kekayaan mereka dari inflasi.\r\n\r\nNamun, di balik citranya yang kokoh dan mengkilap, menabung emas tidaklah bebas risiko. Investor perlu menyadari beberapa \"efek samping\" dan kelemahan yang dapat menggerogoti keuntungan, terutama jika salah dalam strategi dan pengelolaannya.\r\n\r\nBerikut adalah lima risiko utama menabung emas yang wajib Anda ketahui sebelum berinvestasi:\r\n\r\n1. Tidak Menghasilkan Pendapatan Pasif (Tanpa Dividen/Bunga)\r\nKelemahan fundamental emas sebagai investasi adalah sifatnya yang \"diam\" (dead asset). Berbeda dengan saham yang bisa memberikan dividen, obligasi yang membayar kupon bunga, atau properti yang menghasilkan uang sewa, emas fisik maupun digital tidak menghasilkan pendapatan pasif selama Anda memegangnya.\r\n\r\nKeuntungan dari emas hanya dapat direalisasikan melalui satu cara: selisih harga jual dan harga beli (capital gain). Jika harga emas tidak bergerak naik signifikan selama bertahun-tahun, investasi Anda praktis hanya \"tidur\" tanpa memberikan imbal hasil. Emas hanya berfungsi sebagai penyimpan nilai, bukan penghasil arus kas.\r\n\r\n2. Tingginya Nilai Spread (Selisih Harga Jual Beli)\r\nSaat membeli emas, Anda akan langsung menyadari adanya perbedaan signifikan antara harga beli dan harga jual kembali (buyback). Selisih ini, yang dikenal sebagai spread, biasanya cukup tinggi—seringkali di atas 5-7%, bahkan lebih.\r\n\r\nDampak: Anda baru akan mendapat keuntungan jika kenaikan harga emas mampu menutupi spread yang sudah Anda bayar di awal. Inilah mengapa emas sangat tidak cocok untuk investasi jangka pendek. Jika Anda terpaksa menjual dalam waktu singkat, kerugian hampir pasti terjadi karena spread yang tinggi.\r\n\r\n3. Risiko Keamanan dan Biaya Penyimpanan (Khusus Emas Fisik)\r\nBagi investor yang memilih emas batangan atau perhiasan (emas fisik), risiko keamanan menjadi kekhawatiran terbesar. Emas adalah aset yang rentan terhadap pencurian atau kehilangan.\r\n\r\nBiaya Tambahan: Untuk meminimalkan risiko, Anda harus mengeluarkan biaya tambahan, seperti:\r\n\r\nPembelian brankas pribadi yang aman.\r\nMenyewa Safe Deposit Box (SDB) di bank atau pegadaian, yang dikenakan biaya sewa tahunan.\r\nBiaya asuransi.\r\nBiaya-biaya penyimpanan ini secara perlahan mengurangi total keuntungan yang Anda peroleh, terutama jika Anda menyimpan emas dalam jangka waktu yang sangat lama.\r\n\r\n4. Kenaikan Harga yang Lambat dan Memerlukan Kesabaran Ekstra\r\nMeskipun harga emas cenderung positif dalam jangka panjang dan menjadi pelindung inflasi, pergerakan harganya dikenal lambat dibandingkan instrumen pasar modal seperti saham atau reksa dana.\r\n\r\nJendela Waktu: Untuk benar-benar merasakan imbal hasil yang signifikan, emas membutuhkan jangka waktu investasi yang panjang, idealnya di atas lima tahun.\r\n\r\nFaktor Spekulasi: Dalam kondisi perekonomian yang stabil dan sentimen positif pasar saham, harga emas justru bisa melambat atau stagnan, karena investor cenderung memindahkan modal mereka ke aset-aset yang lebih berisiko namun berpotensi return lebih besar.\r\n\r\n5. Risiko Emas Palsu dan Penipuan Platform\r\nRisiko ini mengintai, baik bagi pembeli emas fisik maupun digital.\r\n\r\nEmas Fisik: Risiko mendapatkan emas palsu masih ada, terutama jika membeli dari penjual tidak terpercaya atau non-resmi. Sertifikasi resmi menjadi sangat penting untuk menjamin keaslian.\r\n\r\nEmas Digital/Tabungan Emas: Meskipun praktis, emas digital bergantung pada legalitas dan integritas platform penyedianya. Risiko platform tidak terdaftar atau sistem yang error bisa menghambat proses pencairan atau mengancam kepemilikan Anda.\r\n\r\nEmas tetap merupakan aset diversifikasi yang sangat baik dan alat yang efektif untuk melindungi nilai aset dari inflasi. Namun, investor harus menabung emas dengan pemahaman yang jelas: emas adalah pelari maraton, bukan pelari cepat.\r\n\r\nMengetahui spread harga, memperhitungkan biaya penyimpanan, dan memahami bahwa emas tidak menghasilkan pendapatan pasif adalah kunci untuk menghindari kejutan finansial dan menjadikan emas benar-benar sebagai aset pelindung, bukan jebakan.***\r\n\r\nDisclaimer: Artikel ini dibuat dengan bantuan AI Gemini/ChatGPT yang dimodifikasi oleh editor manusia untuk kenyamanan pembaca.', '2026-04-28 01:42:19', 5, 'th_1.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `berita_hashtag`
--

CREATE TABLE `berita_hashtag` (
  `berita_id` int(11) NOT NULL,
  `hashtag_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `berita_hashtag`
--

INSERT INTO `berita_hashtag` (`berita_id`, `hashtag_id`) VALUES
(3, 3),
(5, 1),
(5, 2),
(7, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `hashtag`
--

CREATE TABLE `hashtag` (
  `id` int(11) NOT NULL,
  `nama_hashtag` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `hashtag`
--

INSERT INTO `hashtag` (`id`, `nama_hashtag`) VALUES
(2, '#Flask'),
(1, '#Python'),
(3, '#Testing');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kategori`
--

CREATE TABLE `kategori` (
  `id` int(11) NOT NULL,
  `nama_kategori` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `kategori`
--

INSERT INTO `kategori` (`id`, `nama_kategori`) VALUES
(2, 'Akademik'),
(6, 'Beasiswa'),
(5, 'Budaya'),
(3, 'Event'),
(4, 'Pendidikan'),
(1, 'Teknologi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `komentar`
--

CREATE TABLE `komentar` (
  `id` int(11) NOT NULL,
  `berita_id` int(11) NOT NULL,
  `nama_pengomentar` varchar(100) NOT NULL,
  `isi_komentar` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `komentar`
--

INSERT INTO `komentar` (`id`, `berita_id`, `nama_pengomentar`, `isi_komentar`, `created_at`) VALUES
(2, 6, 'Bejo Negoro', 'Mantap kali abangku', '2026-04-27 04:48:05'),
(3, 7, 'Salvatore Sirigu', 'Selain emas investasi perak juga bisa dipertimbangkan!', '2026-04-28 01:43:43');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `role` enum('admin','dosen','mahasiswa') DEFAULT 'admin',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `nama_lengkap`, `role`, `created_at`) VALUES
(2, 'mhs1', '123', 'Verbido Alenia', 'mahasiswa', '2026-04-27 17:17:23');

-- --------------------------------------------------------

--
-- Struktur dari tabel `videos`
--

CREATE TABLE `videos` (
  `id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `youtube_id` varchar(50) NOT NULL,
  `keterangan` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `videos`
--

INSERT INTO `videos` (`id`, `judul`, `youtube_id`, `keterangan`, `created_at`) VALUES
(4, '99% orang bakal anggep HP ini absurd (termasuk saya)', 'G1TRm2B-h1M', 'HP murah spesifikasi ganas', '2026-04-26 18:16:00'),
(5, 'Kebangkrutan Yahoo!', 'oU_RAxtJFdA', 'DARI 125 MILIAR JADI NOL! Kisah Kejatuhan Paling Brutal dalam Sejarah Internet (Yahoo Story)', '2026-04-26 18:38:29'),
(6, 'BIKIN TOWER MINI SENDIRI', '3xJQreyzL1s', 'BIKIN TOWER MINI SENDIRI !!, SINYAL NGGA JADI MASALAH !!, MESHTASTIC MURAH & MUDAH [PEMULA]', '2026-04-26 18:44:02');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `berita`
--
ALTER TABLE `berita`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_berita_kategori` (`id_kategori`);

--
-- Indeks untuk tabel `berita_hashtag`
--
ALTER TABLE `berita_hashtag`
  ADD PRIMARY KEY (`berita_id`,`hashtag_id`),
  ADD KEY `hashtag_id` (`hashtag_id`);

--
-- Indeks untuk tabel `hashtag`
--
ALTER TABLE `hashtag`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nama_hashtag` (`nama_hashtag`);

--
-- Indeks untuk tabel `kategori`
--
ALTER TABLE `kategori`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nama_kategori` (`nama_kategori`);

--
-- Indeks untuk tabel `komentar`
--
ALTER TABLE `komentar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_berita_komentar` (`berita_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `berita`
--
ALTER TABLE `berita`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `hashtag`
--
ALTER TABLE `hashtag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `kategori`
--
ALTER TABLE `kategori`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `komentar`
--
ALTER TABLE `komentar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `berita`
--
ALTER TABLE `berita`
  ADD CONSTRAINT `fk_berita_kategori` FOREIGN KEY (`id_kategori`) REFERENCES `kategori` (`id`) ON DELETE SET NULL;

--
-- Ketidakleluasaan untuk tabel `berita_hashtag`
--
ALTER TABLE `berita_hashtag`
  ADD CONSTRAINT `berita_hashtag_ibfk_1` FOREIGN KEY (`berita_id`) REFERENCES `berita` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `berita_hashtag_ibfk_2` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtag` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `komentar`
--
ALTER TABLE `komentar`
  ADD CONSTRAINT `fk_berita_komentar` FOREIGN KEY (`berita_id`) REFERENCES `berita` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
