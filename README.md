# Sistem Manajemen Warnet Gaming (NetGaming Esports Arena)

> 🌐 **Live Demo / Link Aplikasi**: [https://gaming-internet-cafe-management-sys.vercel.app/](https://gaming-internet-cafe-management-sys.vercel.app/)  
> **Proyek Ujian Mata Kuliah Pemrograman Web**  
> Aplikasi Manajemen Warnet Modular, Real-Time, dan Responsive Berbasis Web.  
> *(Kredensial Login Administrator: Username `admin` | Password `admin`)*

Sistem Manajemen Warnet Gaming adalah aplikasi berbasis web modern yang dirancang untuk mengelola operasional warnet secara modular, efisien, dan terstruktur. Aplikasi ini dikembangkan untuk memenuhi tugas dan ujian akhir mata kuliah **Pemrograman Web** dengan mengimplementasikan arsitektur web client-server, komunikasi data asinkronus (AJAX), manajemen basis data relasional MySQL, styling visual responsive modern (Bootstrap 5 & Custom CSS), serta penerapan paradigma Object-Oriented Programming (OOP) pada layer back-end Python Flask.

---

## Pengembang / Anggota Kelompok

1. **Irfan Syarifudin** (24.83.1127)
2. **Sufutra Jaya Inathsalen** (24.83.1147)
3. **Riyan** (24.84.1113)

---

## Fokus Materi Ujian Mata Kuliah Pemrograman Web

Aplikasi ini mencakup pilar-pilar utama dalam kurikulum Pemrograman Web modern:

### 1. Arsitektur Client-Server & Web Framework (Flask)
* **Modular Routing (Flask Blueprints)**: Kode aplikasi terbagi secara terstruktur ke dalam blueprint terpisah (`dashboard`, `komputer`, `pelanggan`, `penyewaan`, `transaksi`, `laporan`, `log`).
* **Handling Request & Response**: Penanganan metode HTTP (GET, POST), pembacaan parameter formulir & query string, serta pengembalian HTTP Status Code dan JSON Response (`jsonify`).
* **Template Engine (Jinja2)**: Reusabilitas komponen HTML (`base.html`), pewarisan layout (`{% extends %}`), serta custom template filters (`rupiah` dan `datetime_format`).

### 2. Front-End Development & Responsive Design
* **HTML5 Semantik & Modern Layout**: Penggunaan elemen semantik HTML5 (`<header>`, `<main>`, `<section>`, `<footer>`, `<article>`).
* **Styling Hybrid**: Kombinasi Bootstrap 5 untuk framework UI grid/responsive dengan **Custom CSS** (CSS Variables, Glassmorphism, Micro-animations, Neon Theme, Dark Mode).
* **CSS Media Query Thermal Print**: Penyesuaian tampilan khusus saat pencetakan struk transaksi (`@media print`) agar pas dengan format printer thermal.
* **Integrasi Library JavaScript Third-Party**:
  * **Chart.js**: Visualisasi grafik analitik tren pendapatan dan performa operasional.
  * **Tom Select JS**: Dropdown pilihan interaktif dengan fitur autocomplete & live search internal.
  * **html2pdf.js**: Ekspor tampilan laporan web ke format dokumen PDF A4 secara client-side.

### 3. Asynchronous Web Communication (AJAX / RESTful API Endpoints)
* **Live Tariff Calculator API**: Kalkulasi total biaya sewa secara otomatis di latar belakang melalui endpoint `/penyewaan/hitung-biaya` tanpa mereload halaman web.
* **Asynchronous Contact Form**: Pengiriman pesan dari pengunjung pada Landing Page (`/simpan-kontak`) menggunakan AJAX Fetch API dengan umpan balik berupa modal/alert dinamis.

### 4. Back-End & Database Management System (MySQL)
* **Relational Database Management**: Koneksi basis data MySQL via `PyMySQL` menggunakan prepared statements untuk mencegah SQL Injection.
* **Skema Database Relasional**: Mengelola tabel `komputer`, `pelanggan`, `transaksi`, `log_aktivitas`, dan `pesan_kontak` dengan kunci utama dan referensi terintegrasi.
* **Aggregation Queries**: Query SQL kompleks untuk agregasi total pendapatan, tren harian, sesi aktif, serta pemeringkatan unit PC terpopuler.

### 5. Keamanan Web & Manajemen Sesi (Session Authentication)
* **Session State Management**: Proteksi akses halaman admin menggunakan Flask `session`.
* **Security Middleware (`@app.before_request`)**: Membatasi dan mengalihkan (*redirect*) pengguna yang belum diautentikasi jika mencoba mengakses area internal `/dashboard/*`.
* **Audit Log Trail**: Pengambilan IP address pengakses (`X-Forwarded-For` / `remote_addr`) untuk pencatatan riwayat aktivitas login, logout, dan transaksi sensitif.

### 6. Optimasi Web & Metadata Engine
* **Structured Metadata**: Dukungan Open Graph (OG) Meta Tags dan JSON-LD Structured Data Schema untuk keterbacaan Search Engine dan AI Crawlers.

### 7. Back-End Object-Oriented Programming (OOP)
* **Class & Object**: Pengorganisasian logika domain bisnis dalam kelas Python (`Warnet`, `Komputer`, `Pelanggan`, `Member`, `Transaksi`).
* **Encapsulation**: Perlindungan state objek dan validasi mutasi atribut internal melalui properti getter/setter.
* **Inheritance**: Kelas `Member` mewarisi properti dari `Pelanggan`.
* **Polymorphism**: Metode `hitung_biaya(durasi)` yang berperilaku berbeda antara Pelanggan Regular (Rp 8.000/jam) dan Member (Rp 7.000/jam).
* **Abstraction**: Penggunaan `ABC` (`BaseWarnet`) untuk mendefinisikan interface/kontrak operasi sistem warnet.

---

## Fitur-Fitur Utama Aplikasi

1. **Esports Public Landing Page (`/`)**  
   Halaman depan publik bertema Cyber Gaming Arena yang menyajikan visualisasi ketersediaan PC real-time, informasi fasilitas, daftar harga paket billing, ulasan pengguna, dan formulir kontak interaktif.

2. **Formulir Kontak Asinkronus (AJAX Contact Form)**  
   Fasilitas pengiriman pesan pengunjung pada Landing Page yang memproses input secara asinkron tanpa *page reload*, serta menyimpan pesan ke basis data MySQL.

3. **Autentikasi & Keamanan Dashboard Admin (`/login`, `/logout`)**  
   Halaman login terproteksi untuk administrator dengan verifikasi sesi dan pencatatan audit log otomatis saat administrator masuk maupun keluar dari sistem.

4. **Dashboard Admin Analytics & Visual PC Grid Map**  
   Visual peta tata letak komputer interaktif yang menampilkan status *Tersedia* (Hijau) atau *Digunakan* (Merah), dilengkapi countdown timer sisa waktu sewa secara live, detail pengguna yang aktif, serta ringkasan kartu statistik operasional.

5. **Auto-Standby / Release Sesi Otomatis**  
   Sistem pemindai durasi sewa yang secara otomatis mengubah status transaksi menjadi selesai dan mereset status PC kembali menjadi *Tersedia* segera setelah durasi sewa habis.

6. **Form Penyewaan Modern (Tom Select & Live Tariff Calculator)**  
   Form transaksi penyewaan komputer dengan fitur pencarian cepat pada dropdown pelanggan/PC menggunakan Tom Select, serta kalkulasi estimasi total biaya sewa secara live via AJAX berdasarkan kategori pelanggan.

7. **Manajemen Data Komputer (CRUD Komputer)**  
   Pengelolaan data unit PC secara penuh (Tambah, Edit, Hapus, Lihat) mencakup nomor PC, nama unit, spesifikasi teknis (VGA RTX 50 Series, CPU, RAM, Monitor Hz), dan status unit.

8. **Manajemen Data Pelanggan & Member (CRUD Pelanggan)**  
   Pengelolaan data pengguna warnet dengan pemisahan otomatis antara Pelanggan Regular dan Member, serta fitur auto-generate ID pelanggan unik (`PEL...` / `MBR...`).

9. **Manajemen Transaksi & Cetak Struk Thermal**  
   Pencatatan riwayat transaksi penyewaan, tombol penghentian sewa manual, dan fitur cetak nota/invoice dengan tampilan yang disesuaikan khusus untuk ukuran printer thermal 58mm/80mm.

10. **Laporan Keuangan, Analitik & Ekspor PDF**  
    Visualisasi tren pendapatan harian menggunakan Chart.js, pemeringkatan 5 Komputer Terpopuler (berdasarkan frekuensi sewa dan pendapatan), serta tombol unduh laporan PDF A4 rapi secara instan.

11. **System Activity Log & Audit Trail (`/dashboard/log`)**  
    Halaman khusus audit log aktivitas sistem yang merekam setiap peristiwa (Auth, Sewa, Komputer, Pelanggan, Kontak, Sistem) secara rinci beserta timestamp dan IP address client, dilengkapi filter kategori, pencarian kata kunci, serta fitur pembersihan log.

12. **Pengelolaan Inbox Pesan Kontak (`/dashboard/kontak`)**  
    Halaman kelola pesan masuk dari pengunjung yang dikirim via formulir kontak Landing Page, memungkinkan admin membaca detail pesan serta menghapus pesan yang tidak lagi diperlukan.

13. **Optimasi Web & Engine Metadata**  
    Integrasi Open Graph Meta Tags dan JSON-LD schema untuk optimasi tampilan dan keterbacaan mesin.

---

## Teknologi yang Digunakan

### Back-End & Database
* **Python 3**: Bahasa pemrogramam utama back-end.
* **Flask**: Micro-framework web Python untuk pengolahan routing dan controller.
* **PyMySQL**: Pustaka konektor MySQL berbasis Python.
* **Python-dotenv**: Pengelolaan variabel lingkungan (`.env`).

### Front-End & UI Design
* **HTML5 & CSS3**: Struktur semantik dan penataan gaya visual custom.
* **Bootstrap 5 & Bootstrap Icons**: Framework CSS responsive dan ikonografi modern.
* **Google Fonts**: Tipografi modern (Inter & Rajdhani / Roboto).

### Client-Side JavaScript & Libraries
* **JavaScript (ES6+)**: Logika pemrosesan client-side, DOM manipulation, & Fetch API.
* **Chart.js**: Rendering grafik analitik keuangan dan operasional.
* **Tom Select**: UI dropdown select dengan fitur live search & autocomplete.
* **html2pdf.js**: Pustaka konversi elemen HTML menjadi dokumen PDF.

---

## Panduan Instalasi dan Menjalankan Aplikasi

### 1. Prasyarat Sistem
* **Python 3.8+** terpasang di sistem operasi Anda.
* **MySQL Server** (Laragon, XAMPP, atau MySQL Community Server) aktif pada port `3306`.

### 2. Langkah Instalasi

1. **Salin / Kloning Repositori**  
   Buka terminal dan navigasikan ke direktori kerja Anda.

2. **Pengaturan Basis Data**  
   * Buat basis data baru bernama `db_warnet` pada MySQL Anda melalui phpMyAdmin atau MySQL Client:
     ```sql
     CREATE DATABASE db_warnet;
     ```
   * Impor berkas `database.sql` yang tersedia di direktori root ke dalam basis data `db_warnet`.

3. **Konfigurasi Environment (`.env`)**  
   Pastikan berkas `.env` telah disesuaikan dengan kredensial MySQL lokal Anda:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=db_warnet
   SECRET_KEY=warnet_gaming_secret_key_2026
   ```

4. **Instalasi Dependensi Python**  
   Jalankan perintah berikut di terminal:
   ```bash
   pip install -r requirements.txt
   ```

5. **Menjalankan Server Aplikasi**  
   Eksekusi perintah berikut untuk memulai server Flask:
   ```bash
   python app.py
   ```

6. **Akses Aplikasi melalui Browser**  
   * **Halaman Depan Publik (Landing Page)**: [http://localhost:5000/](http://localhost:5000/)
   * **Halaman Login Admin**: [http://localhost:5000/login](http://localhost:5000/login)  
     *(Kredensial Default Admin - Username: `admin` | Password: `admin`)*
   * **Dashboard Administrator**: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

---

## Struktur Direktori Proyek

```text
sistem-warnet-gaming/
│
├── api/                    # Handler serverless / API entry points
├── models/                 # Model Data & Logika OOP Python
│   ├── __init__.py
│   ├── komputer.py         # Subclass / Entity Komputer
│   ├── pelanggan.py        # Entity Pelanggan & Member (Inheritance & Polymorphism)
│   ├── transaksi.py        # Entity Transaksi Penyewaan
│   └── warnet.py           # Core System Controller (BaseWarnet ABC & MySQL Operations)
│
├── routes/                 # Flask Blueprints (Modular Controller Routing)
│   ├── __init__.py
│   ├── dashboard.py        # Landing page, Auth Admin, Dashboard & Kontak
│   ├── komputer.py         # CRUD Komputer
│   ├── pelanggan.py        # CRUD Pelanggan & Member
│   ├── penyewaan.py        # Form Sewa & AJAX Calculator API
│   ├── transaksi.py        # Pengelolaan Transaksi & Cetak Struk
│   ├── laporan.py          # Analitik & Laporan Finansial
│   └── log.py              # Audit Log Activity Management
│
├── static/                 # Aset Statis Front-End
│   ├── css/                # Custom Stylesheets & Printing CSS
│   └── js/                 # Client-side Scripts & Libraries
│
├── templates/              # HTML Templates (Jinja2 Template Engine)
│   ├── base.html           # Layout Induk Admin Dashboard
│   ├── landing.html        # Public Esports Landing Page
│   ├── login.html          # Form Auth Login Admin
│   ├── dashboard.html      # Main Admin Dashboard & PC Map Grid
│   ├── log_aktivitas.html  # System Audit Trail Logs View
│   ├── kontak.html         # Management Inbox Pesan Kontak Admin
│   ├── komputer/           # Templates CRUD Komputer
│   ├── pelanggan/          # Templates CRUD Pelanggan
│   ├── penyewaan/          # Template Form Penyewaan
│   ├── transaksi/          # Template Transaksi & Invoice Thermal Struk
│   └── laporan/            # Template Laporan & Chart Analytics
│
├── app.py                  # Entry Point Utama Aplikasi Flask & Custom Filters
├── config.py               # Konfigurasi Aplikasi & Environment Variable Database
├── database.sql            # Skema Relasional Database & Initial Mock Data
├── requirements.txt        # Daftar Dependensi Package Python
└── README.md               # Dokumentasi Proyek
```

---

## Poin Penting untuk Presentasi Ujian Pemrograman Web

Saat mempresentasikan aplikasi ini di hadapan penguji / dosen mata kuliah Pemrograman Web, berikut adalah poin-poin kunci yang dapat didemonstrasikan:

1. **Alur HTTP Request & Response**: Tunjukkan bagaimana route Flask memproses request GET/POST dan merender template Jinja2 atau merespons dengan JSON.
2. **Interaktivitas Asinkron (AJAX)**: Demonstrasikan kalkulator sewa otomatis di halaman `/penyewaan` dan form kirim kontak di Landing Page tanpa refresh halaman.
3. **Responsive Web Design**: Tunjukkan tampilan aplikasi saat diakses dalam mode Desktop maupun tampilan Mobile/Tablet menggunakan Breakpoint Bootstrap 5.
4. **Cetak Struk Thermal**: Tunjukkan fitur cetak nota transaksi dan jelaskan penggunaan CSS `@media print` yang menyembunyikan elemen UI non-cetak.
5. **Keamanan & Proteksi Sesi**: Uji akses langsung ke URL `/dashboard` tanpa login untuk menunjukkan mekanisme proteksi middleware `@app.before_request`.
6. **Integrasi Database Relasional**: Jelaskan skema tabel MySQL dan bagaimana data diambil, diubah, serta dihapus menggunakan fungsi PyMySQL pada model `Warnet`.
7. **Penerapan OOP**: Jelaskan bagaimana `Pelanggan` dan `Member` menggunakan Pewarisan (*Inheritance*) dan Polimorfisme (*Polymorphism*) dalam menghitung tarif sewa.
