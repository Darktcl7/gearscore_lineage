# 📜 DKP System Documentation
**Alto Project - Dragon Kill Points System**

Sistem DKP digunakan untuk mendistribusikan poin reward kepada member yang mengikuti Raid atau Event khusus (di luar aktivitas harian rutin).

## 🔄 Alur Kerja (Workflow)

### 1. Memulai Event (Admin)
Event DKP bersifat *Ad-hoc* (dibuat saat dibutuhkan).
1.  Buka Website: **[Menu Staff]** -> **DKP Control**.
2.  Di bagian "Start New Event", masukkan:
    *   **Name:** Nama Event (contoh: `Zaken Raid`).
    *   **Code:** Kode Singkat (contoh: `ZAK01`). *Akan digabung ke nama.*
    *   **Pts:** Jumlah poin reward (contoh: `10`).
3.  Klik tombol **START EVENT**.
4.  Event sekarang **AKTIF** dan muncul di Discord.

### 2. Member Check-in (Discord)
Member melakukan absen melalui Bot Discord.
1.  Cek Event Aktif:
    ```
    /dkp events
    ```
    *Bot akan membalas dengan Nama Event dan ID Event (misal: ID: 5).*

2.  Lakukan Check-in:
    ```
    /dkp checkin event_id:5 character:NamaChar
    ```
    *Contoh: `/dkp checkin 5 Batman`*

3.  **Sukses:** Poin langsung bertambah ke karakter tersebut.

### 3. Cek Poin & Leaderboard
Member bisa melihat perolehan poin mereka kapan saja.

*   **Cek Poin Sendiri (Discord):**
    ```
    /dkp me character:NamaChar
    ```
*   **Cek Leaderboard (Discord):**
    ```
    /dkp leaderboard
    ```
*   **Website:**
    *   **My DKP:** Melihat riwayat poin pribadi secara detail.
    *   **DKP Points:** Melihat papan klasemen (Leaderboard) lengkap.

### 4. Menutup Event (Admin)
Setelah Raid/Event selesai, Admin wajib menutup event agar tidak disalahgunakan.
1.  Buka Website: **DKP Control**.
2.  Lihat tabel "Recent Events".
3.  Klik tombol **End Event** (Merah).
4.  Status berubah menjadi **CLOSED**. Check-in dimatikan.

---

## 🛠️ Perbedaan dengan "Activity System" (Lama)

| Fitur | **Activity System** (Lama) | **DKP System** (Baru) |
| :--- | :--- | :--- |
| **Tujuan** | Event Rutin (Invasion, Boss Rush) | Setup Raid, GvG, Special Event |
| **URL** | `/portal/` | `/dkp/` |
| **Menu Admin** | Battle Command | DKP Control |
| **Poin** | Activity Points & Tier | Dragon Kill Points (Currency) |
| **Discord Cmd** | `/post_event`, `/checkin` | `/dkp events`, `/dkp checkin` |
