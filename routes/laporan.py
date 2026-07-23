from flask import Blueprint, render_template, request, current_app

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')

@laporan_bp.route('/')
def index():
    warnet = current_app.warnet_system
    
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    filter_start = start_date if start_date else None
    filter_end = end_date if end_date else None

    laporan_data = warnet.get_laporan_pendapatan(filter_start, filter_end)
    
    return render_template(
        'laporan/index.html',
        laporan=laporan_data,
        start_date=start_date,
        end_date=end_date
    )