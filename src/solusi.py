# ============================================================
# Fuzzy Logic Mamdani - Sistem Penilaian Kinerja Operator Produksi
# Kelompok 1 | Kelas 5A Teknik Informatika | UNIPMA
# Anggota:
#   1. Muhamad Sidik Wahyudi (2405101002)
#   2. Hearis Yulia Rachma (2405101061)
#   3. Okky Hendrawan (2405101095)
#   4. Niva Ultiviola (2405101009)
# ============================================================

import os
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')   # mode headless — simpan langsung ke file tanpa window popup
import matplotlib.pyplot as plt

# Direktori dasar proyek agar path output selalu tepat
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

# ----------------------------------------------------------
# 1. FUNGSI KEANGGOTAAN INPUT
#    Ketiga variabel input (Produktivitas, Kualitas,
#    Kedisiplinan) menggunakan pola MF yang sama.
#    Parameter: Rendah [0,0,40,60], Sedang [40,60,80],
#               Tinggi [60,80,100,100]
# ----------------------------------------------------------

def mf_rendah(x):
    """Trapesium kiri: keanggotaan penuh di 0-40, turun ke 0 di 60."""
    if x <= 40:
        return 1.0
    elif x < 60:
        return (60 - x) / 20.0
    return 0.0

def mf_sedang(x):
    """Segitiga: puncak di 60, nol di 40 dan 80."""
    if x <= 40 or x >= 80:
        return 0.0
    elif x <= 60:
        return (x - 40) / 20.0
    return (80 - x) / 20.0

def mf_tinggi(x):
    """Trapesium kanan: mulai naik di 60, penuh di 80-100."""
    if x <= 60:
        return 0.0
    elif x < 80:
        return (x - 60) / 20.0
    return 1.0

# ----------------------------------------------------------
# 2. FUNGSI KEANGGOTAAN OUTPUT (Kinerja Karyawan)
#    Kurang [0,0,30,45], Cukup [30,45,60],
#    Baik [50,65,80], Sangat Baik [70,85,100,100]
# ----------------------------------------------------------

def mf_kurang(z):
    if z <= 30:
        return 1.0
    elif z < 45:
        return (45 - z) / 15.0
    return 0.0

def mf_cukup(z):
    if z <= 30 or z >= 60:
        return 0.0
    elif z <= 45:
        return (z - 30) / 15.0
    return (60 - z) / 15.0

def mf_baik(z):
    if z <= 50 or z >= 80:
        return 0.0
    elif z <= 65:
        return (z - 50) / 15.0
    return (80 - z) / 15.0

def mf_sangat_baik(z):
    if z <= 70:
        return 0.0
    elif z < 85:
        return (z - 70) / 15.0
    return 1.0

MF_OUTPUT = {
    'kurang':      mf_kurang,
    'cukup':       mf_cukup,
    'baik':        mf_baik,
    'sangat_baik': mf_sangat_baik,
}

# ----------------------------------------------------------
# 3. RULE BASE (27 aturan IF-THEN)
#    Indeks: 0=Rendah, 1=Sedang, 2=Tinggi
#    Pemetaan jumlah indeks -> output:
#    3-4 = Kurang | 5 = Cukup | 6-7 = Baik | 8-9 = Sangat Baik
# ----------------------------------------------------------

RULES = []
for pc in range(3):        # Produktivitas: 0=R, 1=S, 2=T
    for qc in range(3):    # Kualitas
        for dc in range(3): # Kedisiplinan
            total = (pc + 1) + (qc + 1) + (dc + 1)   # indeks 1-based
            if total <= 4:
                out = 'kurang'
            elif total == 5:
                out = 'cukup'
            elif total <= 7:
                out = 'baik'
            else:
                out = 'sangat_baik'
            RULES.append((pc, qc, dc, out))

# ----------------------------------------------------------
# 4. FUZZIFIKASI
# ----------------------------------------------------------

def fuzzify(x):
    return [mf_rendah(x), mf_sedang(x), mf_tinggi(x)]

# ----------------------------------------------------------
# 5. INFERENSI MAMDANI + DEFUZZIFIKASI CENTROID
# ----------------------------------------------------------

Z_UNIVERSE = np.arange(0, 100.1, 0.1)   # domain output

def infer(P, Q, D, verbose=True):
    mu_P = fuzzify(P)
    mu_Q = fuzzify(Q)
    mu_D = fuzzify(D)

    if verbose:
        label = ['Rendah', 'Sedang', 'Tinggi']
        print(f"\n{'─'*55}")
        print(f"  Input  → Produktivitas={P}, Kualitas={Q}, Kedisiplinan={D}")
        print(f"{'─'*55}")
        print("  [Langkah 1: Fuzzifikasi]")
        for nama, vals in [("Produktivitas", mu_P),
                           ("Kualitas",      mu_Q),
                           ("Kedisiplinan",  mu_D)]:
            parts = ", ".join(f"{label[i]}={vals[i]:.3f}" for i in range(3))
            print(f"    {nama:15s}: {parts}")

    # Langkah 2: Evaluasi Aturan (Operator DAN = MIN)
    # Langkah 3: Penggabungan Area Grafik (Agregasi MAX)
    agg = np.zeros_like(Z_UNIVERSE)

    fired = []
    for pc, qc, dc, out in RULES:
        alpha = min(mu_P[pc], mu_Q[qc], mu_D[dc])
        if alpha > 0:
            clipped = np.minimum(alpha,
                                 np.array([MF_OUTPUT[out](z) for z in Z_UNIVERSE]))
            agg = np.maximum(agg, clipped)
            fired.append((pc, qc, dc, out, alpha))

    if verbose:
        CAT = ['R', 'S', 'T']
        print(f"\n  [Langkah 2: Evaluasi Aturan yang Aktif (α > 0)]")
        for pc, qc, dc, out, alpha in fired:
            print(f"    P={CAT[pc]} Q={CAT[qc]} D={CAT[dc]}"
                  f"  →  {out:<12s}  α={alpha:.3f}")

    # Langkah 4: Penegasan Nilai Akhir (Defuzzifikasi Centroid)
    try:
        _trapz = np.trapezoid
    except AttributeError:
        _trapz = np.trapz
    num   = _trapz(Z_UNIVERSE * agg, Z_UNIVERSE)
    denom = _trapz(agg, Z_UNIVERSE)
    z_star = num / denom if denom != 0 else 0.0

    if   z_star < 40: kategori = "Kurang"
    elif z_star < 55: kategori = "Cukup"
    elif z_star < 75: kategori = "Baik"
    else:              kategori = "Sangat Baik"

    if verbose:
        print(f"\n  [Langkah 3 & 4: Defuzzifikasi Centroid]")
        print(f"    z* = {z_star:.4f}")
        print(f"    Kategori Kinerja: {kategori}")

    return z_star, kategori

# ----------------------------------------------------------
# 6. VISUALISASI FUNGSI KEANGGOTAAN
# ----------------------------------------------------------

def visualisasi_mf():
    x = np.linspace(0, 100, 500)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.suptitle("Fungsi Keanggotaan — Sistem Penilaian Kinerja Karyawan (Fuzzy Mamdani)", fontsize=13, fontweight='bold')

    # Input MF
    ax = axes[0]
    ax.plot(x, [mf_rendah(xi) for xi in x], color='#E41A1C', lw=2.2, label='Rendah')
    ax.plot(x, [mf_sedang(xi) for xi in x], color='#1B9E77', lw=2.2, label='Sedang')
    ax.plot(x, [mf_tinggi(xi) for xi in x], color='#377EB8', lw=2.2, label='Tinggi')
    ax.set_title("Variabel Input (Produktivitas / Kualitas / Kedisiplinan)", fontsize=11)
    ax.set_xlabel("Nilai Indikator (0–100)", fontsize=10)
    ax.set_ylabel("Derajat Keanggotaan (μ)", fontsize=10)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.legend(loc='center right', framealpha=0.9)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(-0.05, 1.08)

    # Output MF
    ax2 = axes[1]
    ax2.plot(x, [mf_kurang(xi)      for xi in x], color='#E41A1C', lw=2.2, label='Kurang')
    ax2.plot(x, [mf_cukup(xi)       for xi in x], color='#FF7F00', lw=2.2, label='Cukup')      # oranye kontras tinggi
    ax2.plot(x, [mf_baik(xi)        for xi in x], color='#377EB8', lw=2.2, label='Baik')
    ax2.plot(x, [mf_sangat_baik(xi) for xi in x], color='#4DAF4A', lw=2.2, label='Sangat Baik')
    ax2.set_title("Variabel Output (Kategori Kinerja Karyawan)", fontsize=11)
    ax2.set_xlabel("Nilai Kinerja (0–100)", fontsize=10)
    ax2.set_ylabel("Derajat Keanggotaan (μ)", fontsize=10)
    ax2.set_xticks([0, 30, 45, 60, 70, 85, 100])
    ax2.legend(loc='center right', framealpha=0.9)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.set_ylim(-0.05, 1.08)

    plt.tight_layout()
    chart_path = os.path.join(RESULTS_DIR, 'visualisasi.png')
    plt.savefig(chart_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"\n  Grafik diperbarui → {chart_path}")

# ----------------------------------------------------------
# 7. MAIN — 3 Data Pengujian
# ----------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("  SISTEM PENILAIAN KINERJA KARYAWAN")
    print("  Fuzzy Logic Mamdani | Kelompok 1 | 5A UNIPMA")
    print("=" * 55)

    data_uji = [
        ("Karyawan A", 55, 72, 48),   # campuran → Cukup
        ("Karyawan B", 85, 90, 88),   # tinggi semua → Sangat Baik
        ("Karyawan C", 30, 25, 40),   # rendah semua → Kurang
    ]

    hasil = []
    for nama, P, Q, D in data_uji:
        print(f"\n{'═'*55}")
        print(f"  Pengujian: {nama}")
        z_star, kategori = infer(P, Q, D, verbose=True)
        hasil.append((nama, P, Q, D, round(z_star, 2), kategori))

    # Tabel ringkasan
    print(f"\n\n{'═'*55}")
    print("  TABEL HASIL PENGUJIAN")
    print(f"{'═'*55}")
    header = f"{'Nama':<14} {'Prod':>5} {'Kual':>5} {'Disp':>5} {'Nilai':>7}  {'Kategori'}"
    print(f"  {header}")
    print(f"  {'─'*53}")
    for r in hasil:
        row = f"{r[0]:<14} {r[1]:>5} {r[2]:>5} {r[3]:>5} {r[4]:>7.2f}  {r[5]}"
        print(f"  {row}")

    # Simpan CSV
    csv_path = os.path.join(RESULTS_DIR, 'hasil-pengujian.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Nama', 'Produktivitas', 'Kualitas', 'Kedisiplinan',
                    'Nilai_Kinerja', 'Kategori'])
        w.writerows(hasil)
    print(f"\n  CSV disimpan → {csv_path}")

    # Visualisasi
    visualisasi_mf()
