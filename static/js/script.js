document.addEventListener('DOMContentLoaded', function () {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });
    }

    const selectPelanggan = document.getElementById('sewa_id_pelanggan');
    const inputDurasi = document.getElementById('sewa_durasi');
    const labelTarif = document.getElementById('preview_tarif');
    const labelTotal = document.getElementById('preview_total');
    const labelJenis = document.getElementById('preview_jenis');
    const previewContainer = document.getElementById('biaya_preview_container');

    function formatRupiah(number) {
        return 'Rp ' + new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 }).format(number);
    }

    function hitungBiayaLive() {
        const idPelanggan = selectPelanggan.value;
        const durasi = inputDurasi.value;

        if (idPelanggan && durasi && parseInt(durasi) > 0) {
            fetch('/penyewaan/hitung-biaya', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id_pelanggan: idPelanggan,
                    durasi: parseInt(durasi)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    labelTarif.innerText = formatRupiah(data.tarif_per_jam) + ' / jam';
                    labelTotal.innerText = formatRupiah(data.total_biaya);
                    labelJenis.innerText = data.jenis_pelanggan;
                    previewContainer.classList.remove('d-none');
                } else {
                    previewContainer.classList.add('d-none');
                }
            })
            .catch(error => {
                console.error('Error saat menghitung biaya:', error);
                previewContainer.classList.add('d-none');
            });
        } else {
            previewContainer.classList.add('d-none');
        }
    }

    if (selectPelanggan && inputDurasi) {
        selectPelanggan.addEventListener('change', hitungBiayaLive);
        inputDurasi.addEventListener('input', hitungBiayaLive);
    }

    const chartCanvas = document.getElementById('revenueChart');
    if (chartCanvas) {
        const chartDataRaw = chartCanvas.getAttribute('data-chart-value');
        if (chartDataRaw) {
            try {
                const riwayat = JSON.parse(chartDataRaw);
                const labels = riwayat.map(item => {
                    const parts = item.tanggal.split('-');
                    if (parts.length === 3) {
                        return `${parts[2]}/${parts[1]}/${parts[0]}`;
                    }
                    return item.tanggal;
                });
                const values = riwayat.map(item => item.pendapatan);

                new Chart(chartCanvas, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Pendapatan Harian',
                            data: values,
                            borderColor: '#0d6efd',
                            backgroundColor: 'rgba(13, 110, 253, 0.05)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.3,
                            pointBackgroundColor: '#0d6efd',
                            pointRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        let label = context.dataset.label || '';
                                        if (label) {
                                            label += ': ';
                                        }
                                        if (context.parsed.y !== null) {
                                            label += formatRupiah(context.parsed.y);
                                        }
                                        return label;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function (value) {
                                        return formatRupiah(value);
                                    }
                                },
                                grid: {
                                    color: '#e9ecef'
                                }
                            },
                            x: {
                                grid: {
                                    display: false
                                }
                            }
                        }
                    }
                });
            } catch (e) {
                console.error("Gagal me-render grafik:", e);
            }
        }
    }
});
