from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

transaksi_bp = Blueprint('transaksi', __name__, url_prefix='/transaksi')

@transaksi_bp.route('/')
def index():
    warnet = current_app.warnet_system
    list_transaksi = warnet.get_semua_transaksi()
    return render_template('transaksi/index.html', list_transaksi=list_transaksi)

@transaksi_bp.route('/detail/<int:id>')
def detail(id):
    warnet = current_app.warnet_system
    transaksi = warnet.get_transaksi(id)
    if not transaksi:
        flash('Transaksi tidak ditemukan', 'danger')
        return redirect(url_for('transaksi.index'))
    return render_template('transaksi/detail.html', transaksi=transaksi)

@transaksi_bp.route('/selesai/<int:id>', methods=['POST'])
def selesai(id):
    warnet = current_app.warnet_system
    try:
        warnet.selesaikan_sewa(id)
        flash('Sesi penyewaan komputer telah berhasil diselesaikan', 'success')
    except Exception as e:
        flash(f'Gagal menyelesaikan sewa: {str(e)}', 'danger')
    
    ref = request.referrer
    if ref and 'transaksi' in ref:
        return redirect(url_for('transaksi.index'))
    return redirect(url_for('dashboard.index'))