from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

komputer_bp = Blueprint('komputer', __name__, url_prefix='/komputer')

@komputer_bp.route('/')
def index():
    warnet = current_app.warnet_system
    list_komputer = warnet.get_semua_komputer()
    return render_template('komputer/index.html', list_komputer=list_komputer)

@komputer_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nomor_pc = request.form.get('nomor_pc', '').strip()
        nama_pc = request.form.get('nama_pc', '').strip()
        spesifikasi = request.form.get('spesifikasi', '').strip()
        
        if not nomor_pc or not nama_pc or not spesifikasi:
            flash('Semua data harus diisi', 'danger')
            return render_template('komputer/tambah.html')

        warnet = current_app.warnet_system
        try:
            warnet.tambah_komputer(nomor_pc, nama_pc, spesifikasi)
            flash('Komputer baru berhasil ditambahkan', 'success')
            return redirect(url_for('komputer.index'))
        except Exception as e:
            flash(f'Gagal menambahkan komputer: {str(e)}', 'danger')
            
    return render_template('komputer/tambah.html')

@komputer_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    warnet = current_app.warnet_system
    komputer = warnet.get_komputer(id)
    if not komputer:
        flash('Komputer tidak ditemukan', 'danger')
        return redirect(url_for('komputer.index'))

    if request.method == 'POST':
        nomor_pc = request.form.get('nomor_pc', '').strip()
        nama_pc = request.form.get('nama_pc', '').strip()
        status = request.form.get('status', '').strip()
        spesifikasi = request.form.get('spesifikasi', '').strip()

        if not nomor_pc or not nama_pc or not status or not spesifikasi:
            flash('Semua data harus diisi', 'danger')
            return render_template('komputer/edit.html', komputer=komputer)

        try:
            warnet.edit_komputer(id, nomor_pc, nama_pc, status, spesifikasi)
            flash('Data komputer berhasil diperbarui', 'success')
            return redirect(url_for('komputer.index'))
        except Exception as e:
            flash(f'Gagal memperbarui komputer: {str(e)}', 'danger')

    return render_template('komputer/edit.html', komputer=komputer)

@komputer_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    warnet = current_app.warnet_system
    try:
        warnet.hapus_komputer(id)
        flash('Komputer berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Gagal menghapus komputer: {str(e)}', 'danger')
    return redirect(url_for('komputer.index'))