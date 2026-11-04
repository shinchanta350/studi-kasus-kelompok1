# Studi Kasus AI — Penilaian Kinerja Karyawan

## Identitas Kelompok

| | |
|---|---|
| **Kelompok** | Kelompok 1 |
| **Kelas** | 5A Teknik Informatika — UNIPMA |
| **Anggota** | Yudi, Hearis Yulia Rachma (2405101061), Oki, Niva |

---

## Informasi Studi Kasus

**Judul:** Sistem Penilaian Kinerja Operator Produksi Menggunakan Logika Fuzzy dan Fungsi Keanggotaan

**Topik:** Topik 3 — Logika Fuzzy dan Fungsi Keanggotaan

**Metode AI:** Fuzzy Logic Mamdani dengan defuzzifikasi Centroid

**Latar Belakang:**  
Penilaian kinerja karyawan di perusahaan manufaktur sering bersifat subjektif karena bergantung pada penilaian personal atasan. Sistem berbasis Fuzzy Logic Mamdani digunakan untuk mengolah tiga indikator kinerja (Produktivitas, Kualitas, Kedisiplinan) menjadi nilai akhir yang objektif dan transparan.

**Tujuan:**  
Menghasilkan kategori kinerja karyawan (Kurang / Cukup / Baik / Sangat Baik) secara otomatis berdasarkan tiga indikator terukur.

---

## Kebutuhan Perangkat Lunak

- Python 3.10 ke atas
- numpy
- matplotlib

Install dependensi:
```bash
pip install numpy matplotlib
```

---

## Cara Menjalankan

```bash
cd studi-kasus-kelompok1
python src/solusi.py
```

Program akan menampilkan:
1. Proses fuzzifikasi tiap input
2. Rules yang aktif (α > 0) beserta nilai alpha-nya
3. Hasil defuzzifikasi Centroid (z*)
4. Tabel ringkasan pengujian 3 karyawan
5. File CSV di `results/hasil-pengujian.csv`
6. Grafik fungsi keanggotaan di `results/visualisasi.png`

---

## Contoh Keluaran

```
  Pengujian: Karyawan B
  Input  → Produktivitas=85, Kualitas=90, Kedisiplinan=88
  [Fuzzifikasi]
    Produktivitas  : Rendah=0.000, Sedang=0.000, Tinggi=1.000
    Kualitas       : Rendah=0.000, Sedang=0.000, Tinggi=1.000
    Kedisiplinan   : Rendah=0.000, Sedang=0.000, Tinggi=1.000
  [Evaluasi Rules]
    P=T Q=T D=T  →  sangat_baik   α=1.000
  [Defuzzifikasi Centroid]
    z* = 88.3334
    Kategori Kinerja: Sangat Baik
```

| Nama | Produktivitas | Kualitas | Kedisiplinan | Nilai | Kategori |
|------|-------------|---------|--------------|-------|----------|
| Karyawan A | 55 | 72 | 48 | 45.14 | Cukup |
| Karyawan B | 85 | 90 | 88 | 88.33 | Sangat Baik |
| Karyawan C | 30 | 25 | 40 | 19.00 | Kurang |

---

## Struktur Direktori

```
studi-kasus-kelompok1/
├── README.md
├── src/
│   └── solusi.py
├── results/
│   ├── hasil-pengujian.csv
│   └── visualisasi.png
└── screenshots/
    ├── eksekusi-1.png
    ├── eksekusi-2.png
    └── eksekusi-3.png
```
