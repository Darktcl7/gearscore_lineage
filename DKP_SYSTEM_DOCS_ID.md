# Dokumentasi Sistem DKP & Activity (Alto Project)

Dokumen ini menjelaskan pemisahan antara sistem **Activity (Kinerja)** yang sudah ada dengan sistem **DKP (Dragon Kill Points)** yang baru dibuat. Kedua sistem ini berjalan secara paralel namun terpisah.

## 1. Perbedaan Konsep

| Fitur | **Activity System (Eksisting)** | **DKP System (Baru)** |
| :--- | :--- | :--- |
| **Tujuan** | Mengukur kinerja dan keaktifan member setiap bulan. | Mengumpulkan poin (mata uang) untuk pembagian Loot/Item Raid. |
| **Sifat Poin** | **Reset setiap bulan.** Hanya untuk ranking & tier. | **Akumulatif (Seumur Hidup).** Poin disimpan terus, bisa berkurang jika dipakai (bid) atau kena Decay. |
| **Output** | Tier (Elite/Core), Monthly Reward, Leaderboard Bulanan. | Saldo DKP untk belanja item, Leaderboard Total DKP. |
| **Bot Command** | `/checkin` (Masuk ke skor aktivitas) | `/dkp checkin` (Masuk ke antrian verifikasi DKP) |
| **Verifikasi** | Otomatis masuk saat check-in. | **Wajib Verifikasi Admin** (Checkbox) baru poin masuk. |

---

## 2. Alur Kerja Sistem DKP (Baru)

### A. Membuat Event DKP (Admin)
1. Login ke **Admin Panel** (`/admin/`).
2. Masuk ke menu **DKP > DKP Events**.
3. Klik **Add DKP Event**.
4. Isi Nama Event (misal: "Raid Antharas"), Tanggal, dan **Points Reward** (misal: 10 poin).
5. Pastikan "Open Check-in" dicentang.

### B. Member Check-in (Discord)
Member menggunakan perintah bot khusus untuk DKP.
*   **Perintah:** `/dkp checkin <nama_event> <nama_karakter>`
*   **Respon Bot:** "Check-in berhasil! Menunggu verifikasi admin untuk mendapatkan poin."
*   Status kehadiran member di database: **Unverified**.

### C. Verifikasi & Pembagian Poin (Admin)
1. Setelah event selesai, Admin kembali ke **Admin Panel > DKP Events**.
2. Buka event yang bersangkutan.
3. Di daftar "Attendances", Admin mencentang kotak **Verified** pada member yang benar-benar hadir.
4. Setelah selesai memilih, Admin kembali ke daftar event, pilih event tersebut, lalu di menu "Action" (atas tabel) pilih: **"Distribute Points to Verified Attendees"**.
5. Klik **Go**. Poin akan masuk ke saldo DKP member dan Log tercatat. Event otomatis ditutup.

### D. Decay & Pengurangan Poin (Opsional)
Jika ingin mengurangi poin member (misal weekly decay atau belanja item):
*   **Manual:** Admin bisa masuk ke **DKP Profiles**, pilih member, dan kurangi poin manual (tercatat di Log).
*   **Sistem Decay:** (Akan ditambahkan tombol khusus jika diperlukan) untuk memotong 10% poin semua member aktif.

---

## 3. Daftar Perintah Bot (Discord)

Bot akan memiliki grup perintah baru khusus DKP agar tidak tertukar.

| Perintah | Fungsi |
| :--- | :--- |
| `/dkp events` | Melihat daftar event DKP yang sedang aktif/buka. |
| `/dkp checkin [event_id] [char]` | Absen kehadiran untuk event DKP. |
| `/dkp me` | Melihat saldo DKP pribadi & total earned. |
| `/dkp leaderboard` | Melihat Top 10 pemilik DKP terbanyak. |

---

## 4. Tampilan Website

*   **Activity Leaderboard:** Halaman yang sudah ada (`/items/activity/`) tetap menampilkan kinerja bulanan.
*   **DKP Leaderboard:** Halaman baru (nanti ditambahkan di menu) khusus menampilkan saldo DKP member untuk keperluan Loot Distribution.

