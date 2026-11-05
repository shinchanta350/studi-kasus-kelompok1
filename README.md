# Pojek UTS Kecerdasan Buatan dengan Studi Kasus — Sistem Penilaian Kinerja Operator Produksi

Proyek tugas Ujian Tengah Semester (UTS) mata kuliah **Kecerdasan Buatan** yang mengimplementasikan **Logika Fuzzy metode Mamdani** untuk menilai kinerja operator produksi di lingkungan pabrik manufaktur secara objektif, adil, dan transparan.

---

## Identitas Kelompok

| | |
|---|---|
| **Kelompok** | Kelompok 1 |
| **Kelas** | 5A Teknik Informatika — Universitas PGRI Madiun (UNIPMA) |
| **Anggota** | 1. Muhamad Sidik Wahyudi (2405101002)<br>2. Hearis Yulia Rachma (2405101061)<br>3. Okky Hendrawan (2405101095)<br>4. Niva Ultiviola (2405101009) |

---

## Informasi Studi Kasus

- **Judul Proyek:** Sistem Penilaian Kinerja Operator Produksi Menggunakan Logika Fuzzy dan Fungsi Keanggotaan
- **Topik:** Topik 3 — Logika Fuzzy dan Fungsi Keanggotaan
- **Metode AI:** Fuzzy Inference System Mamdani dengan Penegasan Nilai Titik Berat (*Centroid Defuzzification*)
- **Latar Belakang:**  
  Dalam operasional kerja pabrik, evaluasi kinerja karyawan sering kali bersifat subjektif jika hanya mengandalkan penilaian sepihak dari atasan. Selain itu, karyawan sering memiliki nilai yang tidak hitam-putih (misalnya: hasil kerja cepat dan banyak namun kurang rapi, atau kerja berkecepatan sedang namun selalu rapi dan tepat waktu). Sistem berbasis Logika Fuzzy Mamdani dirancang untuk menggabungkan tiga indikator kinerja (*Produktivitas*, *Kualitas*, dan *Kedisiplinan*) menggunakan aturan logika sederhana (JIKA-MAKA) yang meniru pertimbangan manusiawi.
- **Tujuan:**  
  Menghasilkan nilai kinerja pasti ($z^*$) dan predikat kategori (*Kurang*, *Cukup*, *Baik*, *Sangat Baik*) secara konsisten, teratur, dan dapat dipertanggungjawabkan.

---

## Pemodelan Fuzzy

### 1. Variabel Input (Skala 0–100)
Ketiga variabel input menggunakan pola fungsi keanggotaan yang sama:
- **Rendah:** Trapesium $[0, 0, 40, 60]$
- **Sedang:** Segitiga $[40, 60, 80]$
- **Tinggi:** Trapesium $[60, 80, 100, 100]$

### 2. Variabel Output (Skala 0–100)
Kategori kinerja karyawan:
- **Kurang:** Trapesium $[0, 0, 30, 45]$
- **Cukup:** Segitiga $[30, 45, 60]$
- **Baik:** Segitiga $[50, 65, 80]$
- **Sangat Baik:** Trapesium $[70, 85, 100, 100]$

### 3. Aturan Logika (27 Aturan JIKA-MAKA)
Total kombinasi disusun dari $3 \times 3 \times 3 = 27$ aturan dengan metode penjumlahan bobot kategori:
$$\text{Bobot: Rendah = 1, Sedang = 2, Tinggi = 3}$$

| Total Bobot Nilai | Predikat Kategori | Contoh Kombinasi |
|:---:|:---:|---|
| **3 – 4** | **Kurang** | $1+1+1 = 3$ (R, R, R) atau $1+1+2 = 4$ (R, R, S) |
| **5** | **Cukup** | $1+2+2 = 5$ (R, S, S) atau $1+1+3 = 5$ (R, R, T) |
| **6 – 7** | **Baik** | $2+2+2 = 6$ (S, S, S) atau $2+2+3 = 7$ (S, S, T) |
| **8 – 9** | **Sangat Baik** | $2+3+3 = 8$ (S, T, T) atau $3+3+3 = 9$ (T, T, T) |

### 4. Defuzzifikasi Centroid
Mengubah bidang kurva gabungan menjadi satu nilai angka tegas ($z^*$):
$$z^* = \frac{\sum (z \cdot \mu(z))}{\sum \mu(z)}$$

---

## Kebutuhan Perangkat Lunak

- Python 3.10 ke atas
- `numpy`
- `matplotlib`

Instalasi dependensi:
```bash
pip install numpy matplotlib
```

---

## Cara Menjalankan

Jalankan program dari direktori utama proyek:
```bash
python src/solusi.py
```

Program akan memproses alur Fuzzy Mamdani:
1. **Langkah 1: Fuzzifikasi** — menghitung derajat keanggotaan tiap indikator.
2. **Langkah 2: Evaluasi Aturan** — mencari aturan yang aktif ($\alpha > 0$) menggunakan operator `MIN`.
3. **Langkah 3: Penggabungan (Agregasi)** — menyatukan kurva keluaran menggunakan operator `MAX`.
4. **Langkah 4: Defuzzifikasi Centroid** — menghitung titik berat nilai tegas ($z^*$).
5. **Ekspor Hasil** — menyimpan tabel ringkasan ke `results/hasil-pengujian.csv` dan grafik ke `results/visualisasi.png`.

---

## Hasil Pengujian Simulasi

Tiga skenario pengujian karyawan simulasi:

| Nama Karyawan | Produktivitas | Kualitas | Kedisiplinan | Nilai Kinerja ($z^*$) | Predikat Kategori | Analisis Singkat |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **Karyawan A** | 55 | 72 | 48 | **45.14** | **Cukup** | Kualitas baik (72), namun kedisiplinan rendah (48) menarik turun nilai akhir. |
| **Karyawan B** | 85 | 90 | 88 | **88.33** | **Sangat Baik** | Semua indikator bernilai tinggi konsisten, memicu aturan Sangat Baik penuh. |
| **Karyawan C** | 30 | 25 | 40 | **19.00** | **Kurang** | Semua indikator berada di batas bawah, menghasilkan nilai tegas rendah. |

### Contoh Keluaran Terminal (Karyawan A)
```text
  Pengujian: Karyawan A
  Input  → Produktivitas=55, Kualitas=72, Kedisiplinan=48
  [Langkah 1: Fuzzifikasi]
    Produktivitas  : Rendah=0.250, Sedang=0.750, Tinggi=0.000
    Kualitas       : Rendah=0.000, Sedang=0.400, Tinggi=0.600
    Kedisiplinan   : Rendah=0.600, Sedang=0.400, Tinggi=0.000

  [Langkah 2: Evaluasi Aturan yang Aktif (α > 0)]
    P=R Q=S D=R  →  kurang        α=0.250
    P=R Q=S D=S  →  cukup         α=0.250
    P=R Q=T D=R  →  cukup         α=0.250
    P=R Q=T D=S  →  baik          α=0.250
    P=S Q=S D=R  →  cukup         α=0.400
    P=S Q=S D=S  →  baik          α=0.400
    P=S Q=T D=R  →  baik          α=0.600
    P=S Q=T D=S  →  baik          α=0.400

  [Langkah 3 & 4: Defuzzifikasi Centroid]
    z* = 45.1364
    Kategori Kinerja: Cukup
```

---

## Struktur Direktori Proyek

```text
studi-kasus-kelompok1/
├── .gitignore
├── README.md
├── Studi Kasus_UTS Kelompok1.docx
├── results/
│   ├── hasil-pengujian.csv
│   └── visualisasi.png
├── screenshots/
│   └── eksekusi-1.png
└── src/
    └── solusi.py
```
