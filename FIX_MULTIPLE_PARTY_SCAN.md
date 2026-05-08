# Fix: Multiple Party Scan untuk Attendance

## 🐛 Masalah
Sistem attendance hanya bisa scan 1x per clan. Jika ada beberapa party yang perlu di-scan (misalnya party 1, party 2, party 3), scan kedua akan **menghapus** hasil scan pertama.

## 🔍 Penyebab
Di file `record_attendance.html`, setiap kali scan baru dilakukan, JavaScript akan **reset semua party_scan_verified** untuk clan tersebut menjadi `false`, kemudian baru menambahkan hasil scan baru.

**Kode Lama (Line 329-336):**
```javascript
// ❌ MASALAH: Reset semua member sebelum menambahkan hasil baru
document.querySelectorAll('.att-row[data-clan="' + clan + '"]').forEach(function(row) {
    setBadge(row, 'scan', false);  // Reset ke FALSE
    recomputeFinal(row);
});

data.matched.forEach(function(member) {
    // Tambahkan hasil scan baru
    setBadge(row, 'scan', member.party_scan_verified);
});
```

## ✅ Solusi

### 1. **Additive Scan (Scan Menambahkan, Tidak Mengganti)**
Scan baru akan **menambahkan** member tanpa menghapus member yang sudah ter-scan sebelumnya.

**Kode Baru:**
```javascript
// ✅ ADDITIVE SCAN: Hanya update member yang ditemukan di scan ini
data.matched.forEach(function(member) {
    const row = document.querySelector('.att-row[data-character-id="' + member.id + '"]');
    if (!row) return;
    setBadge(row, 'scan', member.party_scan_verified);
    recomputeFinal(row);
});

// Hitung total member yang sudah ter-scan
const clanRows = document.querySelectorAll('.att-row[data-clan="' + clan + '"]');
const totalScanned = Array.from(clanRows).filter(row => hasBadge(row, 'scan')).length;

resultEl.textContent = data.matched_count + ' new matched / ' + data.detected_count + ' detected (Total: ' + totalScanned + ' scanned)';
```

### 2. **Tombol Clear Scan**
Ditambahkan tombol 🗑️ (eraser) untuk clear semua party scan jika diperlukan.

**Fitur:**
- Tombol merah di sebelah tombol "Scan"
- Konfirmasi sebelum clear
- Reset semua party_scan_verified untuk clan tersebut

**Fungsi JavaScript:**
```javascript
function clearClanScan(clan) {
    if (!confirm('Clear all party scan data for ' + clan + '?')) return;
    
    // Reset all party_scan_verified badges for this clan
    document.querySelectorAll('.att-row[data-clan="' + clan + '"]').forEach(function(row) {
        setBadge(row, 'scan', false);
        recomputeFinal(row);
    });
    
    updateCounters();
    resultEl.textContent = 'Cleared - ready to scan';
}
```

## 📋 Perubahan File

### File yang Diubah:
1. ✅ `items/templates/items/record_attendance.html`
   - Update logika scan (line ~329-350)
   - Tambah tombol Clear Scan
   - Tambah fungsi `clearClanScan()`
   - Update scan result message untuk menampilkan total scanned

## 🎯 Cara Kerja Baru

### **Workflow Multiple Scan:**

1. **Scan Party 1:**
   - Upload screenshot party 1
   - Klik "Scan"
   - Hasil: 5 member ter-detect dan ter-mark sebagai "Party Scan" ✅
   - Status: `5 new matched / 5 detected (Total: 5 scanned)`

2. **Scan Party 2:**
   - Upload screenshot party 2
   - Klik "Scan" lagi
   - Hasil: 4 member baru ter-detect dan ter-mark sebagai "Party Scan" ✅
   - **Member dari party 1 tetap ter-mark** ✅
   - Status: `4 new matched / 4 detected (Total: 9 scanned)`

3. **Scan Party 3:**
   - Upload screenshot party 3
   - Klik "Scan" lagi
   - Hasil: 3 member baru ter-detect
   - **Member dari party 1 & 2 tetap ter-mark** ✅
   - Status: `3 new matched / 3 detected (Total: 12 scanned)`

### **Jika Perlu Reset:**
- Klik tombol 🗑️ (eraser) merah
- Konfirmasi "Clear all party scan data for Valkyrie?"
- Semua party scan untuk clan tersebut akan di-reset
- Bisa mulai scan ulang dari awal

## 🧪 Testing

### Test Case 1: Multiple Scan
1. Buka halaman attendance
2. Scan party 1 Valkyrie → Verify 5 member ter-mark
3. Scan party 2 Valkyrie → Verify 4 member baru ter-mark + 5 sebelumnya masih ter-mark
4. Total harus 9 member ter-mark ✅

### Test Case 2: Clear Scan
1. Setelah scan beberapa party
2. Klik tombol 🗑️ Clear
3. Konfirmasi
4. Verify semua party scan ter-reset
5. Scan ulang → Verify bisa scan dari awal ✅

### Test Case 3: Save Attendance
1. Scan beberapa party
2. Klik "Save Attendance"
3. Verify semua member yang ter-mark tersimpan di database ✅

## 📝 Catatan

- ✅ Scan bersifat **additive** (menambahkan, tidak mengganti)
- ✅ Bisa scan **unlimited** kali untuk satu clan
- ✅ Tombol Clear untuk reset jika diperlukan
- ✅ Status message menampilkan total member yang sudah ter-scan
- ✅ Tidak perlu perubahan di backend/views
- ✅ Tidak perlu perubahan di database model

## 🚀 Deploy

```bash
# Push ke GitHub
git add .
git commit -m "Fix: Enable multiple party scan per clan with additive logic"
git push origin main

# Deploy ke VPS
cd /home/valkyrie.id/public_html && \
git pull origin main && \
{ pkill -f "gunicorn.*myproject.wsgi" || true; } && \
sleep 2 && \
gunicorn --workers 3 --bind 127.0.0.1:8001 --timeout 120 --daemon myproject.wsgi:application
```

Tidak perlu `collectstatic` karena hanya perubahan template HTML.

---

**Selesai! Sekarang bisa scan multiple party untuk satu event!** 🎉
