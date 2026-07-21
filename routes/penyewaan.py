from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify

penyewaan_bp = Blueprint('penyewaan', __name__, url_prefix='/penyewaan')

@penyewaan_bp.route('/', methods=['GET', 'POST'])
def index():
    warnet = current_app.warnet_system
    if request.method == 'POST':
        id_pelanggan = request.form.get('id_pelanggan', '').strip()
        id_komputer = request.form.get('id_komputer', '').strip()
        durasi = request.form.get('durasi', '').strip()

        if not id_pelanggan or not id_komputer or not durasi:
            flash('Semua kolom sewa wajib diisi', 'danger')
            return redirect(url_for('penyewaan.index'))

        try:
            durasi = int(durasi)
            if durasi <= 0:
                raise ValueError("Durasi harus lebih besar dari 0 jam")
            
            warnet.sewa_komputer(id_pelanggan, id_komputer, durasi)
            flash('Penyewaan komputer berhasil diproses', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            flash(f'Gagal melakukan penyewaan: {str(e)}', 'danger')
            return redirect(url_for('penyewaan.index'))

    list_pelanggan = warnet.get_semua_pelanggan()
    list_komputer = [c for c in warnet.get_semua_komputer() if c.status == 'Tersedia']
    return render_template('penyewaan/index.html', list_pelanggan=list_pelanggan, list_komputer=list_komputer)

@penyewaan_bp.route('/hitung-biaya', methods=['POST'])
def hitung_biaya():
    warnet = current_app.warnet_system
    data = request.get_json() or {}
    id_pelanggan = data.get('id_pelanggan')
    durasi = data.get('durasi')
    
    if not id_pelanggan or not durasi:
        return jsonify({'success': False, 'message': 'Parameter tidak lengkap'}), 400

    try:
        durasi = int(durasi)
        if durasi <= 0:
            return jsonify({'success': False, 'message': 'Durasi tidak valid'}), 400
        
        pelanggan = warnet.get_pelanggan(id_pelanggan)
        if not pelanggan:
            return jsonify({'success': False, 'message': 'Pelanggan tidak ditemukan'}), 404
        
        total_biaya = pelanggan.hitung_biaya(durasi)
        return jsonify({
            'success': True,
            'tarif_per_jam': pelanggan.tarif_per_jam,
            'total_biaya': total_biaya,
            'jenis_pelanggan': pelanggan.jenis_pelanggan
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500