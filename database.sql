CREATE DATABASE IF NOT EXISTS db_warnet;
USE db_warnet;

DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS pelanggan;
DROP TABLE IF EXISTS komputer;
DROP TABLE IF EXISTS kontak;

CREATE TABLE komputer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomor_pc VARCHAR(50) UNIQUE NOT NULL,
    nama_pc VARCHAR(100) NOT NULL,
    spesifikasi VARCHAR(255) NOT NULL DEFAULT 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz',
    status ENUM('Tersedia', 'Digunakan') DEFAULT 'Tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE pelanggan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pelanggan VARCHAR(100) NOT NULL,
    nomor_pelanggan VARCHAR(50) UNIQUE NOT NULL,
    jenis_pelanggan ENUM('Biasa', 'Member') DEFAULT 'Biasa'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE transaksi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pelanggan INT NOT NULL,
    id_komputer INT NOT NULL,
    durasi INT NOT NULL,
    tarif_per_jam DECIMAL(10, 2) NOT NULL,
    total_biaya DECIMAL(10, 2) NOT NULL,
    waktu_transaksi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Aktif', 'Selesai') DEFAULT 'Aktif',
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id) ON DELETE CASCADE,
    FOREIGN KEY (id_komputer) REFERENCES komputer(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO komputer (nomor_pc, nama_pc, spesifikasi, status) VALUES
('PC-01', 'Gaming PC Elite 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-02', 'Gaming PC Elite 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-03', 'Gaming PC Pro 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-04', 'Gaming PC Pro 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-05', 'Streaming PC 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-06', 'Streaming PC 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-07', 'VIP Gaming PC 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-08', 'VIP Gaming PC 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-09', 'E-Sports Arena 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-10', 'E-Sports Arena 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-11', 'Gaming PC Pro 3', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-12', 'Gaming PC Pro 4', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-13', 'Simulator PC 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-14', 'Reguler PC 1', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-15', 'Reguler PC 2', 'RTX 4060, Ryzen 5, 16GB RAM, 165Hz', 'Tersedia'),
('PC-16', 'Godlike Gaming Station 1', 'RTX 5090, Ryzen 9 9950X, 64GB DDR5, 360Hz OLED', 'Tersedia'),
('PC-17', 'Godlike Gaming Station 2', 'RTX 5090, Ryzen 9 9950X, 64GB DDR5, 360Hz OLED', 'Tersedia'),
('PC-18', 'Ultra Esports Arena 3', 'RTX 5080, Intel Core i9-14900KS, 32GB DDR5, 240Hz', 'Tersedia'),
('PC-19', 'Ultra Esports Arena 4', 'RTX 5080, Intel Core i9-14900KS, 32GB DDR5, 240Hz', 'Tersedia'),
('PC-20', 'VIP Motion Simulator Rig', 'RTX 5090, Ryzen 9 7950X3D, 64GB DDR5, Triple 4K OLED', 'Tersedia');

INSERT INTO pelanggan (nama_pelanggan, nomor_pelanggan, jenis_pelanggan) VALUES
('Irfan Syarifudin', 'PLG-001', 'Biasa'),
('Kevin Sufutra Jaya', 'PLG-002', 'Member'),
('Riyan Antony', 'PLG-003', 'Biasa'),
('Michael Aryo Wisanggeni', 'PLG-004', 'Member'),
('Bagas Tegar Pratama', 'PLG-005', 'Biasa'),
('Ahmad Fauzi', 'PLG-006', 'Member'),
('Dian Sastro', 'PLG-007', 'Biasa'),
('Rizky Febian', 'PLG-008', 'Member'),
('Siti Nurhaliza', 'PLG-009', 'Biasa'),
('Budi Santoso', 'PLG-010', 'Member'),
('Citra Kirana', 'PLG-011', 'Biasa'),
('Doni Salmanan', 'PLG-012', 'Member'),
('Eka Putra', 'PLG-013', 'Biasa'),
('Fajar Nugraha', 'PLG-014', 'Member'),
('Gita Gutawa', 'PLG-015', 'Biasa');

INSERT INTO transaksi (id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status) VALUES
(1, 1, 1, 2, 5000.00, 10000.00, DATE_SUB(NOW(), INTERVAL 5 HOUR), 'Selesai'),
(2, 2, 2, 3, 4500.00, 13500.00, DATE_SUB(NOW(), INTERVAL 2 HOUR), 'Selesai'),
(3, 3, 3, 2, 5000.00, 10000.00, NOW(), 'Aktif'),
(4, 4, 4, 3, 4500.00, 13500.00, DATE_SUB(NOW(), INTERVAL 1 DAY), 'Selesai'),
(5, 5, 5, 5, 5000.00, 25000.00, DATE_SUB(NOW(), INTERVAL 12 HOUR), 'Selesai'),
(6, 6, 6, 2, 4500.00, 9000.00, DATE_SUB(NOW(), INTERVAL 4 HOUR), 'Selesai'),
(7, 7, 7, 4, 4500.00, 18000.00, DATE_SUB(NOW(), INTERVAL 3 HOUR), 'Selesai'),
(8, 8, 8, 1, 5000.00, 5000.00, DATE_SUB(NOW(), INTERVAL 1 HOUR), 'Selesai'),
(9, 9, 9, 3, 4500.00, 13500.00, NOW(), 'Aktif'),
(10, 10, 10, 2, 4500.00, 9000.00, NOW(), 'Aktif'),
(11, 11, 1, 4, 4500.00, 18000.00, DATE_SUB(NOW(), INTERVAL 2 DAY), 'Selesai'),
(12, 12, 2, 3, 4500.00, 13500.00, DATE_SUB(NOW(), INTERVAL 3 DAY), 'Selesai'),
(13, 13, 5, 2, 5000.00, 10000.00, DATE_SUB(NOW(), INTERVAL 4 DAY), 'Selesai');

UPDATE komputer SET status = 'Digunakan' WHERE id IN (3, 9, 10);

CREATE TABLE kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subjek VARCHAR(150) NOT NULL,
    pesan TEXT NOT NULL,
    waktu_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO kontak (nama, email, subjek, pesan, waktu_kirim) VALUES
('Rudi Hermawan', 'rudi@gmail.com', 'Saran Spesifikasi', 'Tolong tambahkan headphone gaming di PC-05.', DATE_SUB(NOW(), INTERVAL 1 DAY)),
('Anisa Rahma', 'anisa@yahoo.com', 'Tanya Paket Member', 'Apakah ada paket bergadang untuk member?', DATE_SUB(NOW(), INTERVAL 2 DAY));

DROP TABLE IF EXISTS log_aktivitas;

CREATE TABLE log_aktivitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_username VARCHAR(50) DEFAULT 'admin',
    aksi VARCHAR(100) NOT NULL,
    kategori ENUM('Auth', 'Komputer', 'Pelanggan', 'Sewa', 'Kontak', 'Sistem') NOT NULL,
    deskripsi TEXT NOT NULL,
    ip_address VARCHAR(45) DEFAULT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO log_aktivitas (admin_username, aksi, kategori, deskripsi, ip_address, waktu) VALUES
('admin', 'LOGIN', 'Auth', 'Administrator berhasil login ke sistem', '127.0.0.1', DATE_SUB(NOW(), INTERVAL 3 HOUR)),
('admin', 'MULAI_SEWA', 'Sewa', 'Memulai sewa PC-03 untuk Riyan Antony (2 jam)', '127.0.0.1', DATE_SUB(NOW(), INTERVAL 2 HOUR)),
('admin', 'TAMBAH_PELANGGAN', 'Pelanggan', 'Menambahkan pelanggan baru: Gita Gutawa (PLG-015)', '127.0.0.1', DATE_SUB(NOW(), INTERVAL 1 HOUR)),
('admin', 'TAMBAH_KOMPUTER', 'Komputer', 'Menambahkan unit VIP PC baru: VIP Motion Simulator Rig (PC-20)', '127.0.0.1', DATE_SUB(NOW(), INTERVAL 30 MINUTE));

