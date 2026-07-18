# Arunika Tatto - Studio Management System 🖋️

Aplikasi web komprehensif untuk mengelola Studio Tattoo profesional. Dirancang dengan gaya UI **Neo-Brutalism** yang modern, interaktif, dan responsif. Aplikasi ini mencakup halaman publik (katalog layanan, portofolio, dan pemesanan) serta *Dashboard Admin* untuk mengelola operasional studio secara dinamis.

## 🌟 Fitur Utama

### 1. Halaman Publik (Pelanggan)
- **Beranda Animatif:** Animasi *scroll reveal*, *hover micro-animations*, dan efek transisi yang memberikan kesan premium.
- **Galeri Portofolio:** Menampilkan karya seni seniman tattoo dengan sistem filter yang rapi.
- **Profil Artist:** Kenali seniman (*artist*) kami beserta spesialisasi mereka.
- **Katalog Layanan & Diskon:** Daftar harga beserta promo/diskon yang otomatis terkalkulasi (harga coret).
- **Form Booking:** Pelanggan dapat memilih seniman, layanan, dan tanggal yang diinginkan dengan mudah.

### 2. Dasbor Admin (Manajemen Studio)
- **Kelola Layanan:** Tambah, edit, dan hapus layanan beserta pengaturan diskon (%) secara *real-time*.
- **Kelola Portofolio & Seniman:** Unggah foto portofolio baru dan perbarui profil seniman.
- **Manajemen Booking & Pembayaran:** Lacak status pemesanan pelanggan dan verifikasi pembayaran.
- **Pengaturan Studio Dinamis:** Ubah nama studio, kontak (WhatsApp, Email, Telepon), dan deskripsi langsung dari dasbor tanpa menyentuh kode.
- **Keamanan (Autentikasi):** Sistem login khusus admin berbasis sesi aman.

---

## 🛠️ Teknologi yang Digunakan
- **Backend:** Python 3, Flask, PyMongo (Driver MongoDB)
- **Database:** MongoDB (Local/Atlas)
- **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Custom Neo-Brutalism Design System)

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan Arunika Tatto di komputer Anda:

### Persyaratan Sistem
- Python 3.8+ terinstal di komputer.
- MongoDB terinstal dan berjalan (bisa menggunakan MongoDB Community Server atau MongoDB Atlas).
- Git (untuk *clone* repositori).

### Langkah-Langkah

**1. Clone Repositori**
```bash
git clone https://github.com/Hendardinata/arunika-tatto.git
cd arunika-tatto
```

**2. Buat & Aktifkan Virtual Environment (Sangat Disarankan)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies (Pustaka yang Dibutuhkan)**
```bash
pip install -r requirements.txt
```

**4. Buat File Environment (`.env`)**
Buat file baru bernama `.env` di direktori utama proyek (`arunika-tatto/`), lalu isi dengan konfigurasi berikut:
```env
SECRET_KEY=super-secret-key-inkmaster-2026
MONGO_URI=mongodb://localhost:27017/inkmaster
UPLOAD_FOLDER=frontend/static/uploads
```
*(Catatan: Sesuaikan `MONGO_URI` jika Anda menggunakan database online).*

**5. Jalankan Aplikasi**
```bash
python run_server.py
```
Aplikasi sekarang berjalan! Buka browser Anda dan kunjungi:
- Halaman Utama: `http://127.0.0.1:5000/`
- Dasbor Admin: `http://127.0.0.1:5000/admin`

---

## 🔑 Hak Akses & Cara Penggunaan

### Login Admin
Untuk mengakses Dasbor Admin, Anda perlu login menggunakan kredensial admin (jika database sudah diisi data awal):
- **Email Default:** `admin@inkmaster.id` (Silakan cek/sesuaikan di database Anda)
- **Password Default:** `admin123`

### Menyesuaikan Tampilan
- **Ganti Pengaturan Kontak:** Masuk ke menu `Settings` di Dasbor Admin, lalu ubah nomor WhatsApp, Email, dan lainnya. Tampilan website (Footer & Navigasi) akan berubah otomatis.
- **Membuat Promo:** Masuk ke menu `Services`, edit layanan dan berikan persentase di kolom "Diskon (%)". Harga akan otomatis tercoret di halaman depan pelanggan.

---

## 🤝 Kontribusi
Jika Anda ingin menambahkan fitur atau memperbaiki *bug*, jangan ragu untuk melakukan *Fork* pada repositori ini dan kirimkan *Pull Request*.

## 📄 Lisensi
Proyek ini dibuat untuk keperluan manajemen studio internal dan portofolio pembelajaran. 
*Made with ❤️ for tattoo art by [Hendardinata_](https://github.com/Hendardinata).*
