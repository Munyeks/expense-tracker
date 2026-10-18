# Expense Tracker - Flask Monolith

Aplikasi manajemen keuangan pribadi berbasis web yang dibangun menggunakan Python (Flask), SQLAlchemy, dan Tailwind CSS. Proyek ini dikembangkan untuk mendemonstrasikan implementasi arsitektur Modular Monolith, keamanan data dasar, dan antarmuka pengguna yang responsif.

## Fitur Utama

* Sistem Autentikasi: Login dan registrasi pengguna dengan hashing kata sandi dan manajemen sesi.
* Manajemen Keuangan (CRUD): Pembuatan kategori kustom serta pencatatan arus kas (pemasukan dan pengeluaran).
* Dashboard Ringkasan: Menampilkan kalkulasi saldo bulan berjalan dan visualisasi proporsi pengeluaran menggunakan Chart.js.
* Integritas Data: Validasi penghapusan kategori untuk mencegah kerusakan data transaksi yang berelasi.
* Ekspor Laporan: Fitur unduh riwayat transaksi ke dalam format dokumen CSV.
* REST API Blueprint: Menyediakan endpoint API terpisah yang mengembalikan data transaksi dalam format JSON murni.
* Desain Responsif: Tata letak antarmuka yang menyesuaikan ukuran layar secara otomatis (Mobile-First Design).

## Teknologi yang Digunakan

* Backend: Python 3, Flask
* Database & ORM: PostgreSQL / SQLite, SQLAlchemy
* Keamanan: Flask-WTF (CSRF Protection), Flask-Login, Werkzeug Security
* Frontend: HTML5, Tailwind CSS, Chart.js

## Arsitektur Proyek

Proyek ini menstrukturkan basis kodenya menggunakan standar pengembangan Flask:
* Application Factory: Memisahkan konfigurasi aplikasi dari eksekusi server untuk mempermudah skalabilitas dan proses pengujian.
* Flask Blueprints: Rute aplikasi dipisah ke dalam tiga modul independen (Auth, Main, dan API) untuk menjaga kode tetap rapi dan terisolasi.

## Panduan Instalasi (Lokal)

Pastikan Python 3 sudah terinstal di sistem Anda sebelum memulai.

1. Kloning repositori ini ke komputer Anda:
   git clone https://github.com/Munyeks/expense-tracker.git
   cd expense-tracker

2. Buat dan aktifkan virtual environment:
   python -m venv venv
   
   Untuk Windows:
   venv\Scripts\activate
   
   Untuk Mac/Linux:
   source venv/bin/activate

3. Instal semua pustaka yang dibutuhkan:
   pip install -r requirements.txt

4. Buat file .env di folder utama (root) proyek dan tambahkan konfigurasi berikut:
   SECRET_KEY=masukkan_kunci_rahasia_anda_di_sini

5. Inisialisasi database lokal dan jalankan aplikasi:
   flask run

6. Buka browser dan akses aplikasi melalui http://127.0.0.1:5000
