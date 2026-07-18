class Pelanggan:
    def __init__(self, id_pelanggan, nama_pelanggan, nomor_pelanggan):
        self._id = id_pelanggan
        self._nama_pelanggan = nama_pelanggan
        self._nomor_pelanggan = nomor_pelanggan

    @property
    def id(self):
        return self._id

    @property
    def nama_pelanggan(self):
        return self._nama_pelanggan

    @nama_pelanggan.setter
    def nama_pelanggan(self, value):
        if not value:
            raise ValueError("Nama pelanggan tidak boleh kosong")
        self._nama_pelanggan = value

    @property
    def nomor_pelanggan(self):
        return self._nomor_pelanggan

    @nomor_pelanggan.setter
    def nomor_pelanggan(self, value):
        if not value:
            raise ValueError("Nomor pelanggan tidak boleh kosong")
        self._nomor_pelanggan = value

    @property
    def jenis_pelanggan(self):
        return "Biasa"

    @property
    def tarif_per_jam(self):
        return 8000.0

    def hitung_biaya(self, durasi):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0 jam")
        return durasi * self.tarif_per_jam


class Member(Pelanggan):
    
    @property
    def jenis_pelanggan(self):
        return "Member"

    @property
    def tarif_per_jam(self):
        return 7000.0

    def hitung_biaya(self, durasi):
        if durasi <= 0:
            raise ValueError("Durasi harus lebih dari 0 jam")
        return durasi * self.tarif_per_jam