# Paket yang digunakan

Baca panduan ini sambil melihat `app.py`. Setiap paket punya tugas yang berbeda; `requirements.txt` mencatat paket yang perlu dipasang.

| Paket | Peran di aplikasi | Contoh sederhana |
|---|---|---|
| `streamlit` | Membuat antarmuka web, menerima unggahan, menampilkan tabel/grafik, dan menyediakan unduhan. | `st.title("Ruang Statistik")` menampilkan judul. Di `app.py`, `st.file_uploader(...)` meminta file dan `st.toggle(...)` mengubah tema. |
| `pandas` | Membaca serta mengolah tabel data dan menghitung ringkasan statistik. | `df = pd.read_csv("data.csv")`; `df["Nilai"].mean()` menghitung rata-rata. Di aplikasi, `pd.read_excel(upload)` membuka Excel dan `x.mean()`/`x.median()` menghitung ukuran pusat data. |
| `plotly` | Menggambar grafik interaktif. | `px.histogram(df, x="Nilai")` membuat histogram. Di `app.py`, `px.bar(...)` dan `px.pie(...)` dipakai untuk grafik kategori. |
| `openpyxl` | Membaca/menulis berkas `.xlsx`; aplikasi memakainya untuk ekspor ringkasan ke Excel. | `with pd.ExcelWriter(buffer, engine="openpyxl") as writer: hasil.to_excel(writer)` menulis tabel ke workbook Excel. |
| `xlrd` | Membaca format Excel lama `.xls`. | `pd.read_excel("data_lama.xls")` menggunakan `xlrd` agar format lama dapat dibaca. |

## Potongan alur data

```python
if upload.name.lower().endswith(".csv"):
    df = pd.read_csv(upload)
else:
    df = pd.read_excel(upload)

angka = pd.to_numeric(df["Nilai UTS"], errors="coerce").dropna()
rata_rata = angka.mean()
```

`upload` adalah file yang dipilih pengguna. `pandas` mengubahnya menjadi tabel (`DataFrame`), lalu kolom nilai dibersihkan menjadi angka. `errors="coerce"` mengubah isi yang tidak dapat dibaca sebagai angka menjadi nilai kosong; `dropna()` mengabaikannya untuk hitungan rata-rata.

## Catatan belajar

- Mean adalah jumlah nilai dibagi banyaknya nilai.
- Median adalah nilai tengah setelah data diurutkan.
- Varians dan standar deviasi aplikasi menggunakan rumus sampel dengan penyebut `n - 1`.
- Diagram batang/lingkaran menghitung banyaknya setiap kategori. Karena itu data contoh mempunyai 4 kelompok dengan jumlah berbeda, bukan pembagian 50:50.
- Coba ubah kolom, ukuran statistik, jenis grafik, dan metode penanganan nilai kosong; amati bagaimana hasilnya berubah.
