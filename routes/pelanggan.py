from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

pelanggan_bp = Blueprint('pelanggan', __name__, url_prefix='/pelanggan')

@pelanggan_bp.route('/')
def index():
    warnet = current_app.warnet_system
    list_pelanggan = warnet.get_semua_pelanggan()
    return render_template('pelanggan/index.html', list_pelanggan=list_pelanggan)

@pelanggan_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    warnet = current_app.warnet_system
    if request.method == 'POST':
        nama_pelanggan = request.form.get('nama_pelanggan', '').strip()
        nomor_pelanggan = request.form.get('nomor_pelanggan', '').strip()
        jenis_pelanggan = request.form.get('jenis_pelanggan', '').strip()

        if not nama_pelanggan or not jenis_pelanggan:
            flash('Nama dan Jenis Pelanggan harus diisi', 'danger')
            next_nomor = warnet.generate_nomor_pelanggan()
            return render_template('pelanggan/tambah.html', next_nomor_pelanggan=next_nomor)

        if not nomor_pelanggan:
            nomor_pelanggan = warnet.generate_nomor_pelanggan()

        try:
            warnet.tambah_pelanggan(nama_pelanggan, nomor_pelanggan, jenis_pelanggan)
            flash('Pelanggan baru berhasil ditambahkan', 'success')
            return redirect(url_for('pelanggan.index'))
        except Exception as e:
            flash(f'Gagal menambahkan pelanggan: {str(e)}', 'danger')
            next_nomor = warnet.generate_nomor_pelanggan()
            return render_template('pelanggan/tambah.html', next_nomor_pelanggan=next_nomor)

    next_nomor = warnet.generate_nomor_pelanggan()
    return render_template('pelanggan/tambah.html', next_nomor_pelanggan=next_nomor)

@pelanggan_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    warnet = current_app.warnet_system
    pelanggan = warnet.get_pelanggan(id)
    if not pelanggan:
        flash('Pelanggan tidak ditemukan', 'danger')
        return redirect(url_for('pelanggan.index'))

    if request.method == 'POST':
        nama_pelanggan = request.form.get('nama_pelanggan', '').strip()
        nomor_pelanggan = request.form.get('nomor_pelanggan', '').strip()
        jenis_pelanggan = request.form.get('jenis_pelanggan', '').strip()

        if not nama_pelanggan or not nomor_pelanggan or not jenis_pelanggan:
            flash('Semua data harus diisi', 'danger')
            return render_template('pelanggan/edit.html', pelanggan=pelanggan)

        try:
            warnet.edit_pelanggan(id, nama_pelanggan, nomor_pelanggan, jenis_pelanggan)
            flash('Data pelanggan berhasil diperbarui', 'success')
            return redirect(url_for('pelanggan.index'))
        except Exception as e:
            flash(f'Gagal memperbarui pelanggan: {str(e)}', 'danger')

    return render_template('pelanggan/edit.html', pelanggan=pelanggan)

@pelanggan_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    warnet = current_app.warnet_system
    try:
        warnet.hapus_pelanggan(id)
        flash('Pelanggan berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Gagal menghapus pelanggan: {str(e)}', 'danger')
    return redirect(url_for('pelanggan.index'))