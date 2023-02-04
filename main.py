import psutil
import time
import os
import pandas as pd

UPDATE_DELAY = 1  # detik


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


# dapatkan statistik I/O jaringan dari psutil di setiap antarmuka jaringan
# by setting `pernic` to `True`
io = psutil.net_io_counters(
    pernic=True)  # mengembalikan statistik input/output jaringan luas sistem dalam bentuk penghitung
# pernic: Jika True, metode mengembalikan informasi yang sama untuk semua kartu antarmuka jaringan yang berbeda pada sistem


while True:

    time.sleep(UPDATE_DELAY)  # tidur selama `UPDATE_DELAY` detik
    io_2 = psutil.net_io_counters(pernic=True)  # dapatkan statistik I/O jaringan lagi per antarmuka
    data = []  # inisialisasi data untuk dikumpulkan (daftar dicts)
    for iface, iface_io in io.items():
        # kecepatan yang didapat dari statik lama dan baru
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[
            iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "iface": iface,
            "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
        })

    io = io_2  # perbarui statistik I/O untuk iterasi berikutnya
    df = pd.DataFrame(data)  # buat Pandas DataFrame untuk mencetak statistik dalam gaya tabel
    df.sort_values("Download", inplace=True, ascending=False)  # urutkan nilai per kolom

    os.system("cls") if "nt" in os.name else os.system("clear")  # bersihkan layar berdasarkan OS Anda
    print(df.to_string())  # menampilkan statik
