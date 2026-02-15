# Dokumentasi Update Karakteristik & Gear Score (30 Jan 2026)

## 1. Status Pengerjaan (Summary)
- **Fokus**: Perbaikan logika Gear Score (GS) dan UI Form Karakteristik.
- **Status**: ✅ Selesai (Logic & UI updated).
- **Hasil Akhir**: Kalkulasi Gear Score sudah sesuai dengan target Excel referensi (2221 poin untuk data sample).

## 2. Perubahan Teknis

### A. Formula Gear Score
Formula perhitungan di `items/models.py` disesuaikan agar cocok 100% dengan Excel:
1. **Total Score** sekarang **HANYA** komponen Characteristics. 
   - Tidak lagi menjumlahkan Level Karakter atau Bonus Stats (Main/Subclass) ke dalam total ini.
2. **Kalkulasi Point**:
   - `Legend Class Point` & `Legend Agathion Point`: Dijumlahkan langsung sebagai nilai integer (Input Manual).
   - `Conquer`: Dihitung 2 kali dalam rumus (`Conquer * 10` + `Conquer * 10`) sesuai referensi formula Excel (`...+(S2*10)...+(S2*10)`).
   - **Fix Agathion**: Untuk data lama berupa range "10-20", sistem mengambil nilai maksimalnya (20).

### B. Perubahan Input & Database
Field berikut diubah tipe datanya dari **Dropdown (Choice)** menjadi **Input Angka (Inteer)**:
- `Soulshot Level`
- `Valor Level`
- `Legend Class Point` (sebelumnya Epic Classes Count)
- `Legend Agathion Point` (sebelumnya Epic Agathions Count)

**Tindakan Database:**
- Migrasi dilakukan untuk mengubah `CharField` menjadi `IntegerField`.
- Script `tools/fix_data.py` dibuat untuk membersihkan data string lama sebelum migrasi.

### C. Pembersihan UI
- **Horizontal Radio Buttons**: Pilihan radio (seperti Skills) sekarang tampil sejajar menyamping (horizontal) menggunakan Flexbox CSS, membuat tampilan lebih rapi.
- **Stat Grouping**: Input stat dikelompokkan dalam container visual (Base Combat, Multiplied, Progression, Legend) di file `characteristics_form.html`.

## 3. Cara Melanjutkan
1. **Input Data**: Buka halaman Edit Character, masuk ke tab "Gear Score Stats", dan input angka sesuai Excel.
2. **Verifikasi**: Cek nilai "Characteristics Score" di ringkasan profil.

---
**Catatan untuk Developer:**
Jika perlu melakukan reset/migrasi ulang:
1. Jalankan `python tools/fix_data.py` untuk fix format data lama.
2. Jalankan `python manage.py migrate items`.
