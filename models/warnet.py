from abc import ABC, abstractmethod
import pymysql
from models.komputer import Komputer
from models.pelanggan import Pelanggan, Member
from models.transaksi import Transaksi
from datetime import datetime, timedelta

class BaseWarnet(ABC):
    @abstractmethod
    def get_semua_komputer(self):
        pass

    @abstractmethod
    def get_status_komputer_lengkap(self):
        pass

    @abstractmethod
    def get_komputer(self, id_komputer):
        pass

    @abstractmethod
    def tambah_komputer(self, nomor_pc, nama_pc, spesifikasi):
        pass

    @abstractmethod
    def edit_komputer(self, id_komputer, nomor_pc, nama_pc, status, spesifikasi):
        pass

    @abstractmethod
    def hapus_komputer(self, id_komputer):
        pass

    @abstractmethod
    def get_semua_pelanggan(self):
        pass

    @abstractmethod
    def get_pelanggan(self, id_pelanggan):
        pass

    @abstractmethod
    def tambah_pelanggan(self, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        pass

    @abstractmethod
    def edit_pelanggan(self, id_pelanggan, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        pass

    @abstractmethod
    def generate_nomor_pelanggan(self):
        pass

    @abstractmethod
    def hapus_pelanggan(self, id_pelanggan):
        pass

    @abstractmethod
    def sewa_komputer(self, id_pelanggan, id_komputer, durasi):
        pass

    @abstractmethod
    def selesaikan_sewa(self, id_transaksi):
        pass

    @abstractmethod
    def get_semua_transaksi(self):
        pass

    @abstractmethod
    def get_transaksi(self, id_transaksi):
        pass

    @abstractmethod
    def simpan_pesan_kontak(self, nama, email, subjek, pesan):
        pass

    @abstractmethod
    def get_semua_kontak(self):
        pass

    @abstractmethod
    def hapus_kontak(self, id_kontak):
        pass

    @abstractmethod
    def catat_log(self, admin_username, aksi, kategori, deskripsi, ip_address=None):
        pass

    @abstractmethod
    def get_semua_log(self, kategori=None, search=None, limit=100):
        pass

    @abstractmethod
    def hapus_semua_log(self):
        pass


class Warnet(BaseWarnet):
    def __init__(self, db_config):
        self._db_config = db_config
        self._init_db()

    def _init_db(self):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS log_aktivitas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        admin_username VARCHAR(50) DEFAULT 'admin',
                        aksi VARCHAR(100) NOT NULL,
                        kategori ENUM('Auth', 'Komputer', 'Pelanggan', 'Sewa', 'Kontak', 'Sistem') NOT NULL,
                        deskripsi TEXT NOT NULL,
                        ip_address VARCHAR(45) DEFAULT NULL,
                        waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                connection.commit()
        except Exception as e:
            print(f"Error initializing log table: {e}")
        finally:
            connection.close()

    def _get_connection(self):
        return pymysql.connect(
            host=self._db_config.MYSQL_HOST,
            port=self._db_config.MYSQL_PORT,
            user=self._db_config.MYSQL_USER,
            password=self._db_config.MYSQL_PASSWORD,
            database=self._db_config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )

    def auto_selesaikan_sesi_habis(self):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                sql_get_expired = """
                    SELECT id, id_komputer 
                    FROM transaksi 
                    WHERE status = 'Aktif' 
                      AND DATE_ADD(waktu_transaksi, INTERVAL durasi HOUR) <= NOW()
                """
                cursor.execute(sql_get_expired)
                expired_transactions = cursor.fetchall()
                
                if expired_transactions:
                    for trx in expired_transactions:
                        cursor.execute(
                            "UPDATE transaksi SET status = 'Selesai' WHERE id = %s",
                            (trx['id'],)
                        )
                        cursor.execute(
                            "UPDATE komputer SET status = 'Tersedia' WHERE id = %s",
                            (trx['id_komputer'],)
                        )
                    connection.commit()
        except Exception as e:
            print(f"Auto-release session error: {str(e)}")
        finally:
            connection.close()

    def get_semua_komputer(self):
        self.auto_selesaikan_sesi_habis()
        connection = self._get_connection()
        komputer_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nomor_pc, nama_pc, status, spesifikasi FROM komputer ORDER BY CAST(SUBSTRING(nomor_pc, 4) AS UNSIGNED) ASC")
                results = cursor.fetchall()
                for row in results:
                    komputer = Komputer(row['id'], row['nomor_pc'], row['nama_pc'], row['status'], row['spesifikasi'])
                    komputer_list.append(komputer)
        finally:
            connection.close()
        return komputer_list

    def get_komputer(self, id_komputer):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nomor_pc, nama_pc, status, spesifikasi FROM komputer WHERE id = %s", (id_komputer,))
                row = cursor.fetchone()
                if row:
                    return Komputer(row['id'], row['nomor_pc'], row['nama_pc'], row['status'], row['spesifikasi'])
        finally:
            connection.close()
        return None

    def tambah_komputer(self, nomor_pc, nama_pc, spesifikasi):
        connection = self._get_connection()
        try:
            temp_pc = Komputer(None, nomor_pc, nama_pc, "Tersedia", spesifikasi)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO komputer (nomor_pc, nama_pc, status, spesifikasi) VALUES (%s, %s, 'Tersedia', %s)",
                    (temp_pc.nomor_pc, temp_pc.nama_pc, temp_pc.spesifikasi)
                )
                connection.commit()
            self.catat_log('admin', 'TAMBAH_KOMPUTER', 'Komputer', f"Menambahkan unit komputer baru: {temp_pc.nama_pc} ({temp_pc.nomor_pc})")
        finally:
            connection.close()

    def edit_komputer(self, id_komputer, nomor_pc, nama_pc, status, spesifikasi):
        connection = self._get_connection()
        try:
            pc = self.get_komputer(id_komputer)
            if not pc:
                raise ValueError("Komputer tidak ditemukan")
            
            pc.nomor_pc = nomor_pc
            pc.nama_pc = nama_pc
            pc.ubah_status(status)
            pc.spesifikasi = spesifikasi

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE komputer SET nomor_pc = %s, nama_pc = %s, status = %s, spesifikasi = %s WHERE id = %s",
                    (pc.nomor_pc, pc.nama_pc, pc.status, pc.spesifikasi, pc.id)
                )
                connection.commit()
            self.catat_log('admin', 'EDIT_KOMPUTER', 'Komputer', f"Memperbarui data unit {pc.nama_pc} ({pc.nomor_pc}) - Status: {pc.status}")
        finally:
            connection.close()

    def hapus_komputer(self, id_komputer):
        connection = self._get_connection()
        try:
            pc = self.get_komputer(id_komputer)
            if not pc:
                raise ValueError("Komputer tidak ditemukan")
            if pc.status == "Digunakan":
                raise ValueError("Komputer sedang aktif digunakan, tidak dapat dihapus")

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM komputer WHERE id = %s", (id_komputer,))
                connection.commit()
            self.catat_log('admin', 'HAPUS_KOMPUTER', 'Komputer', f"Menghapus unit komputer {pc.nama_pc} ({pc.nomor_pc})")
        finally:
            connection.close()

    def get_semua_pelanggan(self):
        connection = self._get_connection()
        pelanggan_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nama_pelanggan, nomor_pelanggan, jenis_pelanggan FROM pelanggan ORDER BY nama_pelanggan ASC")
                results = cursor.fetchall()
                for row in results:
                    if row['jenis_pelanggan'] == 'Member':
                        plg = Member(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    else:
                        plg = Pelanggan(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    pelanggan_list.append(plg)
        finally:
            connection.close()
        return pelanggan_list

    def get_pelanggan(self, id_pelanggan):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nama_pelanggan, nomor_pelanggan, jenis_pelanggan FROM pelanggan WHERE id = %s", (id_pelanggan,))
                row = cursor.fetchone()
                if row:
                    if row['jenis_pelanggan'] == 'Member':
                        return Member(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
                    else:
                        return Pelanggan(row['id'], row['nama_pelanggan'], row['nomor_pelanggan'])
        finally:
            connection.close()
        return None

    def generate_nomor_pelanggan(self):
        import re
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT nomor_pelanggan FROM pelanggan")
                rows = cursor.fetchall()
                
                existing_numbers = set()
                max_num = 0
                
                for row in rows:
                    no_plg = row['nomor_pelanggan']
                    if no_plg:
                        existing_numbers.add(no_plg)
                        digits = re.findall(r'\d+', no_plg)
                        if digits:
                            num = int(digits[-1])
                            if num > max_num:
                                max_num = num

                next_num = max_num + 1
                candidate = f"PLG-{next_num:03d}"
                
                while candidate in existing_numbers:
                    next_num += 1
                    candidate = f"PLG-{next_num:03d}"
                    
                return candidate
        finally:
            connection.close()

    def tambah_pelanggan(self, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        if not nomor_pelanggan or not nomor_pelanggan.strip():
            nomor_pelanggan = self.generate_nomor_pelanggan()
        else:
            nomor_pelanggan = nomor_pelanggan.strip()
            connection = self._get_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM pelanggan WHERE nomor_pelanggan = %s", (nomor_pelanggan,))
                    if cursor.fetchone():
                        nomor_pelanggan = self.generate_nomor_pelanggan()
            finally:
                connection.close()

        connection = self._get_connection()
        try:
            if jenis_pelanggan == 'Member':
                temp_plg = Member(None, nama_pelanggan, nomor_pelanggan)
            else:
                temp_plg = Pelanggan(None, nama_pelanggan, nomor_pelanggan)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pelanggan (nama_pelanggan, nomor_pelanggan, jenis_pelanggan) VALUES (%s, %s, %s)",
                    (temp_plg.nama_pelanggan, temp_plg.nomor_pelanggan, temp_plg.jenis_pelanggan)
                )
                connection.commit()
            self.catat_log('admin', 'TAMBAH_PELANGGAN', 'Pelanggan', f"Menambahkan pelanggan baru: {temp_plg.nama_pelanggan} ({temp_plg.nomor_pelanggan} - {temp_plg.jenis_pelanggan})")
        finally:
            connection.close()

    def edit_pelanggan(self, id_pelanggan, nama_pelanggan, nomor_pelanggan, jenis_pelanggan):
        connection = self._get_connection()
        try:
            plg = self.get_pelanggan(id_pelanggan)
            if not plg:
                raise ValueError("Pelanggan tidak ditemukan")
            
            plg.nama_pelanggan = nama_pelanggan
            plg.nomor_pelanggan = nomor_pelanggan

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE pelanggan SET nama_pelanggan = %s, nomor_pelanggan = %s, jenis_pelanggan = %s WHERE id = %s",
                    (plg.nama_pelanggan, plg.nomor_pelanggan, jenis_pelanggan, id_pelanggan)
                )
                connection.commit()
            self.catat_log('admin', 'EDIT_PELANGGAN', 'Pelanggan', f"Memperbarui data pelanggan {nama_pelanggan} ({nomor_pelanggan} - {jenis_pelanggan})")
        finally:
            connection.close()

    def hapus_pelanggan(self, id_pelanggan):
        connection = self._get_connection()
        try:
            plg = self.get_pelanggan(id_pelanggan)
            plg_info = f"{plg.nama_pelanggan} ({plg.nomor_pelanggan})" if plg else f"ID {id_pelanggan}"
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM transaksi WHERE id_pelanggan = %s AND status = 'Aktif'", (id_pelanggan,))
                if cursor.fetchone():
                    raise ValueError("Pelanggan sedang memiliki sesi sewa aktif, tidak dapat dihapus")

                cursor.execute("DELETE FROM pelanggan WHERE id = %s", (id_pelanggan,))
                connection.commit()
            self.catat_log('admin', 'HAPUS_PELANGGAN', 'Pelanggan', f"Menghapus data pelanggan {plg_info}")
        finally:
            connection.close()

    def sewa_komputer(self, id_pelanggan, id_komputer, durasi):
        connection = self._get_connection()
        try:
            pelanggan = self.get_pelanggan(id_pelanggan)
            if not pelanggan:
                raise ValueError("Pelanggan tidak ditemukan")

            komputer = self.get_komputer(id_komputer)
            if not komputer:
                raise ValueError("Komputer tidak ditemukan")

            if komputer.status == "Digunakan":
                raise ValueError("Komputer sedang digunakan oleh pelanggan lain")

            total_biaya = pelanggan.hitung_biaya(durasi)
            tarif_per_jam = pelanggan.tarif_per_jam

            komputer.ubah_status("Digunakan")

            with connection.cursor() as cursor:
                connection.begin()

                cursor.execute(
                    """INSERT INTO transaksi (id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, status)
                       VALUES (%s, %s, %s, %s, %s, 'Aktif')""",
                    (pelanggan.id, komputer.id, durasi, tarif_per_jam, total_biaya)
                )

                cursor.execute(
                    "UPDATE komputer SET status = 'Digunakan' WHERE id = %s",
                    (komputer.id,)
                )

                connection.commit()
            self.catat_log('admin', 'MULAI_SEWA', 'Sewa', f"Memulai sewa unit {komputer.nama_pc} ({komputer.nomor_pc}) untuk pelanggan {pelanggan.nama_pelanggan} ({durasi} jam, total Rp {total_biaya:,.0f})")
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def selesaikan_sewa(self, id_transaksi):
        transaksi = self.get_transaksi(id_transaksi)
        if not transaksi:
            raise ValueError("Transaksi tidak ditemukan")

        transaksi.selesaikan()

        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                connection.begin()

                cursor.execute(
                    "UPDATE transaksi SET status = 'Selesai' WHERE id = %s",
                    (transaksi.id,)
                )

                cursor.execute(
                    "UPDATE komputer SET status = 'Tersedia' WHERE id = %s",
                    (transaksi.komputer.id,)
                )

                connection.commit()
            self.catat_log('admin', 'SELESAI_SEWA', 'Sewa', f"Menyelesaikan sewa transaksi #{transaksi.id} - {transaksi.komputer.nama_pc} ({transaksi.komputer.nomor_pc}) oleh {transaksi.pelanggan.nama_pelanggan}")
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    def get_semua_transaksi(self):
        self.auto_selesaikan_sesi_habis()
        connection = self._get_connection()
        transaksi_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi ORDER BY waktu_transaksi DESC
                """)
                results = cursor.fetchall()
                for row in results:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    trx = Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
                    transaksi_list.append(trx)
        finally:
            connection.close()
        return transaksi_list

    def get_transaksi(self, id_transaksi):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi WHERE id = %s
                """, (id_transaksi,))
                row = cursor.fetchone()
                if row:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    return Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
        finally:
            connection.close()
        return None

    def get_transaksi_terbaru(self, limit=5):
        self.auto_selesaikan_sesi_habis()
        connection = self._get_connection()
        transaksi_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, id_pelanggan, id_komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi, status 
                    FROM transaksi ORDER BY waktu_transaksi DESC LIMIT %s
                """, (limit,))
                results = cursor.fetchall()
                for row in results:
                    pelanggan = self.get_pelanggan(row['id_pelanggan'])
                    komputer = self.get_komputer(row['id_komputer'])
                    trx = Transaksi(
                        row['id'],
                        pelanggan,
                        komputer,
                        row['durasi'],
                        row['tarif_per_jam'],
                        row['total_biaya'],
                        row['waktu_transaksi'],
                        row['status']
                    )
                    transaksi_list.append(trx)
        finally:
            connection.close()
        return transaksi_list

    def get_status_komputer_lengkap(self):
        self.auto_selesaikan_sesi_habis()
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        k.id, 
                        k.nomor_pc, 
                        k.nama_pc, 
                        k.spesifikasi,
                        k.status,
                        t.waktu_transaksi,
                        t.durasi,
                        p.nama_pelanggan
                    FROM komputer k
                    LEFT JOIN transaksi t ON k.id = t.id_komputer AND t.status = 'Aktif'
                    LEFT JOIN pelanggan p ON t.id_pelanggan = p.id
                    ORDER BY CAST(SUBSTRING(k.nomor_pc, 4) AS UNSIGNED) ASC
                """
                cursor.execute(query)
                results = cursor.fetchall()
                
                komputer_lengkap = []
                for row in results:
                    sisa_menit = 0
                    sisa_waktu_str = "-"
                    waktu_selesai_str = "-"
                    
                    if row['status'] == 'Digunakan' and row['waktu_transaksi'] and row['durasi']:
                        start_time = row['waktu_transaksi']
                        durasi_jam = row['durasi']
                        end_time = start_time + timedelta(hours=durasi_jam)
                        now = datetime.now()
                        
                        diff = end_time - now
                        diff_seconds = diff.total_seconds()
                        
                        if diff_seconds > 0:
                            sisa_menit = int(diff_seconds // 60)
                            jam = sisa_menit // 60
                            menit = sisa_menit % 60
                            if jam > 0:
                                sisa_waktu_str = f"{jam} jam {menit} menit"
                            else:
                                sisa_waktu_str = f"{menit} menit"
                            waktu_selesai_str = end_time.strftime("%H:%M") + " WIB"
                        else:
                            sisa_waktu_str = "Sesi Habis"
                            waktu_selesai_str = "Selesai"
                            
                    komputer_lengkap.append({
                        'id': row['id'],
                        'nomor_pc': row['nomor_pc'],
                        'nama_pc': row['nama_pc'],
                        'spesifikasi': row['spesifikasi'],
                        'status': row['status'],
                        'waktu_transaksi': row['waktu_transaksi'],
                        'durasi': row['durasi'],
                        'nama_pelanggan': row['nama_pelanggan'],
                        'sisa_menit': sisa_menit,
                        'sisa_waktu': sisa_waktu_str,
                        'waktu_selesai': waktu_selesai_str
                    })
                return komputer_lengkap
        finally:
            connection.close()

    def get_statistik(self):
        self.auto_selesaikan_sesi_habis()
        connection = self._get_connection()
        stats = {}
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM komputer")
                stats['total_komputer'] = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(*) as total FROM komputer WHERE status = 'Tersedia'")
                stats['komputer_tersedia'] = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(*) as total FROM komputer WHERE status = 'Digunakan'")
                stats['komputer_digunakan'] = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(*) as total FROM pelanggan")
                stats['total_pelanggan'] = cursor.fetchone()['total']

                cursor.execute("SELECT COUNT(*) as total FROM transaksi")
                stats['total_transaksi'] = cursor.fetchone()['total']

                cursor.execute("""
                    SELECT COALESCE(SUM(total_biaya), 0) as total 
                    FROM transaksi 
                    WHERE DATE(waktu_transaksi) = CURDATE()
                """)
                stats['pendapatan_hari_ini'] = float(cursor.fetchone()['total'])

                cursor.execute("SELECT COALESCE(SUM(total_biaya), 0) as total FROM transaksi")
                stats['pendapatan_keseluruhan'] = float(cursor.fetchone()['total'])
        finally:
            connection.close()
        return stats

    def get_laporan_pendapatan(self, start_date=None, end_date=None):
        connection = self._get_connection()
        laporan = {
            'total_pendapatan': 0.0,
            'jumlah_transaksi': 0,
            'riwayat': [],
            'pc_terpopuler': []
        }
        try:
            with connection.cursor() as cursor:
                where_clause = ""
                params = []
                if start_date and end_date:
                    where_clause = "WHERE DATE(waktu_transaksi) BETWEEN %s AND %s"
                    params = [start_date, end_date]
                elif start_date:
                    where_clause = "WHERE DATE(waktu_transaksi) >= %s"
                    params = [start_date]
                elif end_date:
                    where_clause = "WHERE DATE(waktu_transaksi) <= %s"
                    params = [end_date]

                sql_summary = f"""
                    SELECT COALESCE(SUM(total_biaya), 0) as total_biaya, COUNT(*) as jumlah_transaksi 
                    FROM transaksi {where_clause}
                """
                cursor.execute(sql_summary, params)
                summary = cursor.fetchone()
                laporan['total_pendapatan'] = float(summary['total_biaya'])
                laporan['jumlah_transaksi'] = summary['jumlah_transaksi']

                sql_riwayat = f"""
                    SELECT DATE(waktu_transaksi) as tanggal, COALESCE(SUM(total_biaya), 0) as pendapatan
                    FROM transaksi
                    {where_clause}
                    GROUP BY DATE(waktu_transaksi)
                    ORDER BY DATE(waktu_transaksi) ASC
                """
                cursor.execute(sql_riwayat, params)
                results = cursor.fetchall()
                for row in results:
                    laporan['riwayat'].append({
                        'tanggal': row['tanggal'].strftime('%Y-%m-%d') if isinstance(row['tanggal'], datetime) or hasattr(row['tanggal'], 'strftime') else str(row['tanggal']),
                        'pendapatan': float(row['pendapatan'])
                    })

                sql_pc = f"""
                    SELECT 
                        k.nomor_pc, 
                        k.nama_pc, 
                        k.spesifikasi,
                        COUNT(t.id) as total_kali_disewa,
                        COALESCE(SUM(t.durasi), 0) as total_durasi_jam,
                        COALESCE(SUM(t.total_biaya), 0) as total_pendapatan
                    FROM komputer k
                    JOIN transaksi t ON k.id = t.id_komputer
                    {where_clause}
                    GROUP BY k.id, k.nomor_pc, k.nama_pc, k.spesifikasi
                    ORDER BY total_durasi_jam DESC, total_kali_disewa DESC
                    LIMIT 5
                """
                cursor.execute(sql_pc, params)
                pc_results = cursor.fetchall()
                for row in pc_results:
                    laporan['pc_terpopuler'].append({
                        'nomor_pc': row['nomor_pc'],
                        'nama_pc': row['nama_pc'],
                        'spesifikasi': row['spesifikasi'],
                        'total_kali_disewa': row['total_kali_disewa'],
                        'total_durasi_jam': row['total_durasi_jam'],
                        'total_pendapatan': float(row['total_pendapatan'])
                    })
        finally:
            connection.close()
        return laporan

    def simpan_pesan_kontak(self, nama, email, subjek, pesan):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO kontak (nama, email, subjek, pesan) VALUES (%s, %s, %s, %s)",
                    (nama, email, subjek, pesan)
                )
                connection.commit()
        finally:
            connection.close()

    def get_semua_kontak(self):
        connection = self._get_connection()
        kontak_list = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nama, email, subjek, pesan, waktu_kirim FROM kontak ORDER BY waktu_kirim DESC")
                results = cursor.fetchall()
                for row in results:
                    kontak_list.append({
                        'id': row['id'],
                        'nama': row['nama'],
                        'email': row['email'],
                        'subjek': row['subjek'],
                        'pesan': row['pesan'],
                        'waktu_kirim': row['waktu_kirim']
                    })
        finally:
            connection.close()
        return kontak_list

    def hapus_kontak(self, id_kontak):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM kontak WHERE id = %s", (id_kontak,))
                connection.commit()
            self.catat_log('admin', 'HAPUS_KONTAK', 'Kontak', f"Menghapus pesan kontak ID #{id_kontak}")
        finally:
            connection.close()

    def catat_log(self, admin_username, aksi, kategori, deskripsi, ip_address=None):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO log_aktivitas (admin_username, aksi, kategori, deskripsi, ip_address) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (admin_username or 'admin', aksi, kategori, deskripsi, ip_address)
                )
                connection.commit()
        except Exception as e:
            print(f"Error catat_log: {e}")
        finally:
            connection.close()

    def get_semua_log(self, kategori=None, search=None, limit=100):
        connection = self._get_connection()
        logs = []
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, admin_username, aksi, kategori, deskripsi, ip_address, waktu FROM log_aktivitas WHERE 1=1"
                params = []
                if kategori and kategori.strip():
                    sql += " AND kategori = %s"
                    params.append(kategori.strip())
                if search and search.strip():
                    sql += " AND (deskripsi LIKE %s OR aksi LIKE %s OR admin_username LIKE %s)"
                    search_param = f"%{search.strip()}%"
                    params.extend([search_param, search_param, search_param])
                sql += " ORDER BY waktu DESC LIMIT %s"
                params.append(int(limit))
                
                cursor.execute(sql, params)
                results = cursor.fetchall()
                for row in results:
                    logs.append({
                        'id': row['id'],
                        'admin_username': row['admin_username'],
                        'aksi': row['aksi'],
                        'kategori': row['kategori'],
                        'deskripsi': row['deskripsi'],
                        'ip_address': row['ip_address'],
                        'waktu': row['waktu']
                    })
        finally:
            connection.close()
        return logs

    def hapus_semua_log(self):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE log_aktivitas")
                connection.commit()
            self.catat_log('admin', 'KOSONGKAN_LOG', 'Sistem', "Mengosongkan seluruh riwayat log aktivitas")
        finally:
            connection.close()