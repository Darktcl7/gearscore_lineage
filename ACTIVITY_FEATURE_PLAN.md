# Rencana Fitur: Guild Activity & Reward System (Alto Project)

Dokumen ini merinci spesifikasi teknis dan logika bisnis untuk fitur "Activity" yang akan diimplementasikan pada Alto Project. Sistem ini bertujuan untuk melacak keaktifan member guild, menghitung poin bulanan, dan mendistribusikan reward secara adil dan otomatis.

---

## 1. Konsep Dasar
Sistem ini memantau partisipasi member dalam event mingguan Guild (Lineage 2M). Poin diakumulasi setiap bulan untuk menentukan **Rank Tier** dan pembagian **Prize Pool**.

**Target Platform:** Web App (saat ini) & Discord Bot (future roadmap).

---

## 2. Struktur Event & Poin
Terdapat 3 jenis event utama dengan skema poin sebagai berikut:

### A. Invasion (3x per Minggu)
Event ini memiliki 3 Boss spesifik. Poin dihitung **per Boss** yang berhasil dikalahkan saat partisipasi.

| Boss Target | Poin | Catatan |
| :--- | :--- | :--- |
| **Dragon Beast** | **10 pts** | |
| **Carnifex** | **15 pts** | |
| **Orfen** | **25 pts** | |
| **MAX per Sesi** | **50 pts** | Jika ikut dan kill semua 3 boss |
| **MAX per Minggu** | **150 pts** | 3 sesi x 50 pts |

### B. Boss Rush (2x per Minggu)
Durasi ~30 menit. Fokus pada kerjasama tim.

| Aksi | Poin | Syarat |
| :--- | :--- | :--- |
| **Participation** | **20 pts** | Hadir (Join) |
| **Win Bonus** | **+10 pts** | Jika Guild memenangkan match |
| **MAX per Sesi** | **30 pts** | |
| **MAX per Minggu** | **60 pts** | |

### C. Catacombs (2x per Minggu)
Durasi ~30 menit. Fokus pada partisipasi member.

| Aksi | Poin | Syarat |
| :--- | :--- | :--- |
| **Participation** | **15 pts** | Hadir (Join) |
| **Win/Clear Bonus** | **+10 pts** | Jika berhasil clear floor/objective |
| **MAX per Sesi** | **25 pts** | |
| **MAX per Minggu** | **50 pts** | |

---

## 3. Bonus Konsistensi (Bulanan)
Diberikan di akhir bulan berdasarkan persentase kehadiran total (Attendance Rate).
*Total Event per minggu estimasi: (3 Invasion x 3 Boss) + 2 Boss Rush + 2 Catacombs = 13 poin data partisipasi.*

| Attendance Rate | Bonus Poin |
| :--- | :--- |
| **90% - 100%** | **+150 pts** |
| **70% - 89%** | **+100 pts** |
| **50% - 69%** | **+50 pts** |
| **< 50%** | **0 pts** |

---

## 4. Rank Tiers & Kualifikasi
Member dikategorikan berdasarkan **Total Final Score** bulanan.

| Tier | Range Score Bulanan | Status Hadiah |
| :--- | :--- | :--- |
| 🏆 **Elite** | **≥ 900** | ✅ Qualified |
| ⚔️ **Core** | **600 - 899** | ✅ Qualified |
| 🛡️ **Active** | **300 - 599** | ✅ Qualified |
| 🌱 **Casual** | **< 300** | ❌ **DISQUALIFIED** (Tidak dapat jatah prize pool) |

---

## 5. Integrasi Discord (Future Roadmap)
Mengingat event akan dijalankan/dikelola di Discord, sistem Web App akan berperan sebagai **Backend/Database & Visualization Layer**, sementara Discord berperan sebagai **Input/Interaction Layer**.

### Alur Kerja (Workflow)
1.  **Event Creation (Discord)**:
    *   Officer/Bot membuat post event di channel `#events` atau `#schedule`.
    *   Bot generate `Event ID` unik.
2.  **Attendance (Discord)**:
    *   Member melakukan **Reaction** (✅) atau klik **Button** "Check In" di post Discord saat event dimulai.
    *   Bot mencatat User ID Discord peserta.
3.  **Result Reporting (Discord/Web)**:
    *   Setelah event selesai, Officer input hasil (Win/Lose, Boss Killed) via Command Bot (e.g., `/result invasion db:yes carni:yes orfen:no`).
4.  **Data Sync (Discord -> Web)**:
    *   Bot mengirim data partisipasi & hasil ke Web App via API.
    *   Web App menghitung poin otomatis berdasarkan rules yang sudah ditentukan.
5.  **Feedback (Web -> Discord)**:
    *   Web App bisa mengirim rekap mingguan/bulanan "Leaderboard Update" ke channel `#leaderboard`.
    *   Member bisa cek skor mereka via Web Profile atau command `/myscore`.

### Persiapan Data Model
Untuk mendukung ini, kita perlu menyimpan `discord_id` pada model User/Character agar bisa di-link dengan data dari Discord.

---

## 6. Sistem Distribusi Prize Pool
Total Prize Pool contoh: **10,000** (Diamonds/Items).
Sistem distribusi menggunakan 2 lapisan:
1. **Alokasi per Tier:** Persentase fix dari total pool.
2. **Distribusi Member:** Proporsional berdasarkan skor individu di dalam tier tersebut.

### Alokasi Pool
| Tier | Alokasi % | Alokasi Nilai (dari 10k) |
| :--- | :--- | :--- |
| **Elite** Group | **40%** | 4,000 |
| **Core** Group | **30%** | 3,000 |
| **Active** Group | **20%** | 2,000 |
| **Casual** Group | **10%** | 0 (Disqualified/Hangus atau dialihkan) |

### Rumus Kalkulasi Hadiah Individu
Untuk setiap member *User A* di Tier *X*:

$$
\text{Hadiah User A} = \left( \frac{\text{Skor User A}}{\text{Total Skor Semua Member di Tier X}} \right) \times \text{Alokasi Pool Tier X}
$$

*Contoh:*
Jika Pool Tier Elite = 4,000.
Total Skor semua member Elite = 5,000.
Skor User A (Elite) = 1,000.
Maka User A dapat: (1,000 / 5,000) * 4,000 = **800**.

---

## 7. Rencana Implementasi Database (Draft Schema)

Untuk mendukung fitur ini, kita akan membutuhkan model baru di Django:

**1. ActivityEvent**
*   `event_id`: String (Unique ID dari Discord/System)
*   `name`: (Invasion, Boss Rush, Catacombs)
*   `date`: DateTime
*   `type`: (e.g., INVASION, BOSS_RUSH, CATACOMBS)
*   `is_completed`: Boolean Result (Win/Lose for Boss Rush/Cata)
*   `bosses_killed`: JSON (Khusus Invasion)

**2. PlayerActivity**
*   `player`: ForeignKey ke User/Character
*   `event`: ForeignKey ke ActivityEvent
*   `discord_user_id`: String (Untuk mapping jika Character belum link)
*   `status`: (Attended, Absent)
*   `points_earned`: Integer (Calculated)

**3. MonthlyReport** (Untuk caching/history)
*   `month`: Date
*   `player`: ForeignKey
*   `total_score`: Integer
*   `tier`: String (Elite/Core/Active)
*   `final_prize`: Integer

---

## 8. Roadmap Pengerjaan

| # | Task | Status |
|---|------|--------|
| 1 | **Database Design**: Model Django (`ActivityEvent`, `PlayerActivity`, `MonthlyReport`) | ✅ Done |
| 2 | **Backend Logic**: Kalkulasi poin & tier di `services.py` | ✅ Done |
| 3 | **Input Interface (Web)**: Halaman Admin untuk input manual | ✅ Done |
| 4 | **Frontend**: Halaman "Activity Leaderboard" dan "My Activity" | ✅ Done |
| 5 | **API Endpoints**: REST API untuk Discord Bot | ✅ Done |
| 6 | **Discord Bot**: Setup bot template dan commands | ✅ Done |
| 7 | **Management Commands**: Tools untuk maintenance & testing | ✅ Done |
| 8 | **Discord Integration**: Deploy bot ke server Discord | 🔜 Setup Token |

---

## 9. API Endpoints (Untuk Discord Bot)

Base URL: `http://127.0.0.1:8000/items/`
Header: `X-API-Key: alto-discord-bot-key-2026`

### Create Event
```
POST /api/activity/event/create/
Body: {
    "event_type": "INVASION",
    "name": "Weekly Invasion #10",
    "date": "2026-01-31T20:00:00"
}
```

### Record Check-in
```
POST /api/activity/checkin/
Body: {
    "event_id": "INVASION_ABC12345",
    "discord_user_id": "123456789012345678",
    "character_name": "SonOfZeus"
}
```

### Complete Event
```
POST /api/activity/event/complete/
Body: {
    "event_id": "INVASION_ABC12345",
    "is_win": true,
    "bosses_killed": {
        "dragon_beast": true,
        "carnifex": true,
        "orfen": false
    }
}
```

### Get Leaderboard
```
GET /api/activity/leaderboard/
```

### Get Player Stats
```
GET /api/activity/player/{character_name}/
```
