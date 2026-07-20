from flask import Blueprint, render_template, current_app, request, jsonify, session, redirect, url_for, flash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def landing():
    warnet = current_app.warnet_system
    stats = warnet.get_statistik()
    list_komputer = warnet.get_status_komputer_lengkap()
    return render_template('landing.html', stats=stats, list_komputer=list_komputer)

@dashboard_bp.route('/dashboard')
def index():
    warnet = current_app.warnet_system
    stats = warnet.get_statistik()
    transaksi_terbaru = warnet.get_transaksi_terbaru(5)
    list_komputer = warnet.get_status_komputer_lengkap()
    log_terbaru = warnet.get_semua_log(limit=6)
    return render_template('dashboard.html', stats=stats, transaksi_terbaru=transaksi_terbaru, list_komputer=list_komputer, log_terbaru=log_terbaru)

@dashboard_bp.route('/simpan-kontak', methods=['POST'])
def simpan_kontak():
    nama = request.form.get('nama', '').strip()
    email = request.form.get('email', '').strip()
    subjek = request.form.get('subjek', '').strip()
    pesan = request.form.get('pesan', '').strip()

    if not nama or not email or not subjek or not pesan:
        return jsonify({
            'status': 'error',
            'message': 'Semua kolom formulir harus diisi!'
        }), 400

    try:
        warnet = current_app.warnet_system
        warnet.simpan_pesan_kontak(nama, email, subjek, pesan)
        return jsonify({
            'status': 'success',
            'message': 'Pesan Anda berhasil disimpan ke database!'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Gagal menyimpan pesan: {str(e)}'
        }), 500

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP').strip()
    return request.remote_addr or '127.0.0.1'

@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard.index'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = 'admin'
            warnet = current_app.warnet_system
            warnet.catat_log('admin', 'LOGIN', 'Auth', 'Administrator berhasil login ke sistem', get_client_ip())
            return redirect(url_for('dashboard.index'))
        else:
            error = 'Username atau Password salah!'

    return render_template('login.html', error=error)

@dashboard_bp.route('/logout')
def logout():
    warnet = current_app.warnet_system
    if session.get('logged_in'):
        warnet.catat_log(session.get('username', 'admin'), 'LOGOUT', 'Auth', 'Administrator keluar dari sistem', get_client_ip())
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('dashboard.landing'))

@dashboard_bp.route('/dashboard/kontak')
def kontak_index():
    warnet = current_app.warnet_system
    list_kontak = warnet.get_semua_kontak()
    return render_template('kontak.html', list_kontak=list_kontak)

@dashboard_bp.route('/dashboard/kontak/hapus/<int:id>', methods=['POST'])
def hapus_kontak(id):
    warnet = current_app.warnet_system
    try:
        warnet.hapus_kontak(id)
        flash('Pesan berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Gagal menghapus pesan: {str(e)}', 'danger')
    return redirect(url_for('dashboard.kontak_index'))