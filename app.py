from flask import Flask, session, redirect, url_for, request
from config import Config
from models.warnet import Warnet
from routes import (
    dashboard_bp,
    komputer_bp,
    pelanggan_bp,
    penyewaan_bp,
    transaksi_bp,
    laporan_bp,
    log_bp
)
from datetime import datetime, timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.warnet_system = Warnet(Config)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(komputer_bp)
    app.register_blueprint(pelanggan_bp)
    app.register_blueprint(penyewaan_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(log_bp)

    @app.template_filter('rupiah')
    def rupiah_filter(value):
        try:
            val = float(value)
            formatted = f"{val:,.0f}".replace(",", ".")
            return f"Rp {formatted}"
        except (ValueError, TypeError):
            return f"Rp {value}"

    @app.template_filter('datetime_format')
    def datetime_format_filter(value):
        if not value:
            return ""
        
        dt = None
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    dt = datetime.fromisoformat(value)
                except ValueError:
                    return f"{value} WIB" if "WIB" not in str(value) else value
        elif isinstance(value, datetime):
            dt = value

        if dt:
            dt_wib = dt + timedelta(hours=7)
            return f"{dt_wib.strftime('%d/%m/%Y %H:%M')} WIB"

        return f"{value} WIB"

    @app.before_request
    def check_login():
        allowed_paths = ['/', '/login', '/simpan-kontak']
        if request.path not in allowed_paths and not request.path.startswith('/static/'):
            if not session.get('logged_in'):
                return redirect(url_for('dashboard.login'))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)