from datetime import datetime

class Transaksi:
    def __init__(self, id_transaksi, pelanggan, komputer, durasi, tarif_per_jam, total_biaya, waktu_transaksi=None, status="Aktif"):
        self._id = id_transaksi
        self._pelanggan = pelanggan
        self._komputer = komputer
        self._durasi = int(durasi)
        self._tarif_per_jam = float(tarif_per_jam)
        self._total_biaya = float(total_biaya)
        self._waktu_transaksi = waktu_transaksi or datetime.now()
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def pelanggan(self):
        return self._pelanggan

    @property
    def komputer(self):
        return self._komputer

    @property
    def durasi(self):
        return self._durasi

    @property
    def tarif_per_jam(self):
        return self._tarif_per_jam

    @property
    def total_biaya(self):
        return self._total_biaya

    @property
    def waktu_transaksi(self):
        return self._waktu_transaksi

    @property
    def status(self):
        return self._status

    def selesaikan(self):
        if self._status == "Selesai":
            raise ValueError("Transaksi sudah berstatus selesai")
        self._status = "Selesai"
        self._komputer.ubah_status("Tersedia")