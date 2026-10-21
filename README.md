# Ruang Statistika · 1B

Aplikasi web sederhana untuk menganalisis statistik deskriptif. Dibuat dengan Streamlit dan menyesuaikan tampilan untuk desktop maupun ponsel.

## Menjalankan di komputer

Pastikan Python sudah terpasang. Buka terminal di folder proyek ini, lalu jalankan:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Buka alamat yang ditampilkan di terminal, biasanya `http://localhost:8501`. Unggah salah satu file di folder `data/` atau dataset milik sendiri. Aplikasi tidak memuat data contoh otomatis.

## Isi aplikasi

- Statistik deskriptif: minimum, maksimum, mean, median, modus, varians sampel, simpangan baku, dan kuartil.
- Histogram, boxplot, diagram batang, dan diagram lingkaran/donat.
- Tabel distribusi frekuensi, interpretasi awal, dan penanganan nilai kosong.
- Unduhan hasil analisis CSV atau Excel; tema terang dan malam.

## Deploy online

Hubungkan repositori ini ke Streamlit Community Cloud, lalu pilih branch `main` dan file aplikasi `app.py`. File data contoh tersedia di `data/`.

## Struktur

Lihat `app.py`, `requirements.txt`, `PANDUAN_PAKET.md`, dan folder `data/`.
