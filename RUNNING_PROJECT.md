# 🚀 Cara Menjalankan Project Alto (Website & Bot Discord)

Panduan praktis untuk menjalankan aplikasi setelah restart PC atau mematikan server.

## Prasyarat
Pastikan Anda membuka **PowerShell** atau Terminal di folder utama project:
> `D:\Django Project\Alto Project`

---

## 1. Menjalankan Website (Django Server)
Buka terminal baru dan jalankan perintah:

```powershell
& "D:\Django Project\Alto Project\venv\Scripts\python.exe" manage.py runserver
```

*   Tunggu muncul pesan: `Watching for file changes with StatReloader` dan `Starting development server at http://127.0.0.1:8000/`
*   Akses website di: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 2. Menjalankan Bot Discord
Buka terminal **kedua** (terpisah) dan jalankan perintah:

```powershell
& "D:\Django Project\Alto Project\venv\Scripts\python.exe" "D:\Django Project\Alto Project\discord_bot\bot.py"
```

*   Tunggu muncul pesan: `✅ bot_guild#xxxx is now running!`
*   Bot sudah siap digunakan di Discord.

---

## Catatan Tambahan
*   **Virtual Environment (venv)** sudah otomatis digunakan dalam perintah di atas (path panjang ke python.exe), jadi Anda tidak perlu mengaktifkannya manual (`activate`).
*   Jika ingin menghentikan server/bot, tekan `Ctrl + C` di terminal masing-masing.
