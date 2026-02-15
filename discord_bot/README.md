# Alto Guild Activity Discord Bot

Bot Discord untuk tracking aktivitas guild dan integrasi dengan Alto Project web app.

## 📋 Channel Setup

Siapkan 2 channel di Discord Server:

| Channel | Tujuan |
|---------|--------|
| `#events` | Pengumuman event guild (Invasion, Boss Rush, Catacombs) |
| `#leaderboard` | Auto-post ranking bulanan |

## 🎮 Flow Kerja

```
┌─────────────────────────────────────────────────────────────────┐
│                        DISCORD SERVER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  #events channel                                                │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  📅 INVASION EVENT                                     │     │
│  │  ══════════════════════════════════════════════════    │     │
│  │  🐉 Weekly Invasion #15                                │     │
│  │  📆 Tonight at 20:00 WIB                               │     │
│  │  🎯 Bosses: Dragon Beast, Carnifex, Orfen              │     │
│  │                                                        │     │
│  │  Event ID: INVASION_ABC12345                           │     │
│  │                                                        │     │
│  │  ┌──────────────┐  ┌────────────────┐                  │     │
│  │  │ ✅ Check In  │  │ 👥 Participants │                  │     │
│  │  └──────────────┘  └────────────────┘                  │     │
│  └───────────────────────────────────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  CHECK-IN MODAL                                        │     │
│  │  ════════════════                                      │     │
│  │  Character Name: [________________]                    │     │
│  │                                                        │     │
│  │  ┌──────────┐                                          │     │
│  │  │  Submit  │                                          │     │
│  │  └──────────┘                                          │     │
│  └───────────────────────────────────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  ✅ SonOfZeus checked in! (+50 pts)                    │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ALTO WEB APP (Backend)                      │
├─────────────────────────────────────────────────────────────────┤
│  - Menyimpan data event & attendance                            │
│  - Menghitung poin & tier otomatis                              │
│  - Update leaderboard real-time                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Setup

### 1. Buat Bot di Discord Developer Portal

1. Buka https://discord.com/developers/applications
2. Klik "New Application" → beri nama "Alto Bot"
3. Pergi ke tab **Bot** → klik "Add Bot"
4. **Copy Token** (ini adalah `DISCORD_BOT_TOKEN`)
5. Aktifkan:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

### 2. Invite Bot ke Server

1. Pergi ke tab **OAuth2** → **URL Generator**
2. Centang scopes: `bot`, `applications.commands`
3. Centang permissions: Send Messages, Embed Links, Use Slash Commands
4. Copy URL dan buka di browser

### 3. Dapatkan Channel IDs

1. Aktifkan Developer Mode di Discord Settings
2. Klik kanan channel `#events` → Copy ID
3. Klik kanan channel `#leaderboard` → Copy ID

### 4. Konfigurasi Environment

**Windows:**
```cmd
set DISCORD_BOT_TOKEN=your_bot_token_here
set ALTO_API_URL=http://127.0.0.1:8000/items
set ALTO_API_KEY=alto-discord-bot-key-2026
set EVENTS_CHANNEL_ID=123456789012345678
set LEADERBOARD_CHANNEL_ID=123456789012345679
```

### 5. Install & Run

```bash
cd discord_bot
pip install -r requirements.txt
python bot.py
```

## 📝 Commands

### Untuk Officers (Manage Guild permission)

| Command | Deskripsi |
|---------|-----------|
| `/event <type> [name]` | Buat event baru dengan tombol Check-In |
| `/result <event_id> [options]` | Complete event dan record hasil |

### Untuk Semua Member

| Command | Deskripsi |
|---------|-----------|
| Klik **✅ Check In** button | Check-in ke event (paling mudah!) |
| `/checkin <event_id> <character>` | Manual check-in |
| `/myscore <character>` | Lihat statistik pribadi |
| `/leaderboard` | Lihat top 10 bulan ini |

## 🔗 Discord Account Linking

Agar bot bisa mengenali member secara otomatis:

1. Member buka website → Character Profile
2. Klik tombol **Link Discord** (biru)
3. Masukkan Discord User ID (18 digit)
4. Simpan

Setelah link, member tidak perlu input character name saat check-in - bot akan otomatis mengenali berdasarkan Discord ID.

