from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

log_bp = Blueprint('log', __name__, url_prefix='/dashboard/log')

@log_bp.route('/')
def index():
    warnet = current_app.warnet_system
    kategori = request.args.get('kategori', '').strip()
    search = request.args.get('search', '').strip()
    
    list_log = warnet.get_semua_log(kategori=kategori, search=search, limit=200)
    
    all_logs = warnet.get_semua_log(limit=500)
    stats = {
        'total_log': len(all_logs),
        'total_auth': len([l for l in all_logs if l['kategori'] == 'Auth']),
        'total_sewa': len([l for l in all_logs if l['kategori'] == 'Sewa']),
        'total_operasional': len([l for l in all_logs if l['kategori'] in ['Komputer', 'Pelanggan', 'Kontak', 'Sistem']])
    }
    
    return render_template(
        'log_aktivitas.html', 
        list_log=list_log, 
        selected_kategori=kategori, 
        search_query=search,
        stats=stats
    )

@log_bp.route('/bersihkan', methods=['POST'])
def bersihkan():
    warnet = current_app.warnet_system
    try:
        warnet.hapus_semua_log()
        flash('Seluruh riwayat log aktivitas telah berhasil dibersihkan', 'success')
    except Exception as e:
        flash(f'Gagal membersihkan log aktivitas: {str(e)}', 'danger')
    return redirect(url_for('log.index'))
