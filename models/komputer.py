class Komputer:
    def __init__(self, id_komputer, nomor_pc, nama_pc, status="Tersedia", spesifikasi="RTX 4060, Ryzen 5, 16GB RAM, 165Hz"):
        self._id = id_komputer
        self._nomor_pc = nomor_pc
        self._nama_pc = nama_pc
        self._status = status
        self._spesifikasi = spesifikasi

    @property
    def id(self):
        return self._id

    @property
    def nomor_pc(self):
        return self._nomor_pc

    @nomor_pc.setter
    def nomor_pc(self, value):
        if not value:
            raise ValueError("Nomor PC tidak boleh kosong")
        self._nomor_pc = value

    @property
    def nama_pc(self):
        return self._nama_pc

    @nama_pc.setter
    def nama_pc(self, value):
        if not value:
            raise ValueError("Nama PC tidak boleh kosong")
        self._nama_pc = value

    @property
    def spesifikasi(self):
        return self._spesifikasi

    @spesifikasi.setter
    def spesifikasi(self, value):
        if not value:
            raise ValueError("Spesifikasi tidak boleh kosong")
        self._spesifikasi = value

    @property
    def status(self):
        return self._status

    def ubah_status(self, status_baru):
        if status_baru in ["Tersedia", "Digunakan"]:
            self._status = status_baru
        else:
            raise ValueError("Status komputer harus 'Tersedia' atau 'Digunakan'")