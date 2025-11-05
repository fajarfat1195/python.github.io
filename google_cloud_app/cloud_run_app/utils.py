# File: utils.py
# File ini berisi fungsi-fungsi utilitas yang dapat diimpor dan digunakan
# oleh file aplikasi utama (main.py).

def calculate_time_based_message():
    """
    Mengembalikan pesan sapaan berdasarkan waktu saat ini.
    (Membuat mock data karena waktu sebenarnya tidak tersedia di lingkungan build).
    """
    # Di aplikasi sebenarnya, Anda akan menggunakan datetime.datetime.now()
    # Untuk tujuan demo, kita akan mengembalikan pesan statis.
    
    current_hour_mock = 10 # Anggap sekarang jam 10 pagi

    if 6 <= current_hour_mock < 12:
        return "Selamat Pagi! Waktunya memulai hari Anda."
    elif 12 <= current_hour_mock < 18:
        return "Selamat Siang! Semoga hari Anda menyenangkan."
    else:
        return "Selamat Sore/Malam! Saatnya bersantai."

# Anda bisa menambahkan fungsi-fungsi lain di sini, misalnya untuk manipulasi data, log, dll.
