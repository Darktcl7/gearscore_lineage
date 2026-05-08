# Feature: Edit Attendance Points untuk Event

## ✨ Fitur Baru
Menambahkan fungsi untuk **edit attendance points** di halaman Manage Events, sehingga admin bisa mengubah points tanpa perlu membuat event baru.

## 🎯 Lokasi
**URL:** http://127.0.0.1:8000/portal/activity/events/
**Halaman:** Manage Events

## 📋 Yang Ditambahkan

### 1. **Tombol Edit Points** ✅
- Icon: 🖊️ (Edit icon)
- Warna: Orange (#f39c12)
- Posisi: Di kolom Actions, setelah tombol "Manage Attendance"
- Tooltip: "Edit Attendance Points"

### 2. **Modal Edit Points** ✅
- **Header:** "Edit Attendance Points"
- **Input:** Number input untuk points (0-9999)
- **Note untuk Invasion:** Menampilkan catatan khusus untuk event Invasion
- **Buttons:** Cancel & Save Points

### 3. **Backend Endpoint** ✅
- **URL:** `/portal/activity/events/<event_pk>/update-points/`
- **Method:** POST
- **Auth:** Requires Event Admin permission
- **Body:** `{ "event_points": 150 }`
- **Response:** `{ "success": true, "event_points": 150, "message": "..." }`

## 🔧 File yang Diubah

### 1. **Frontend (Template)**
**File:** `items/templates/items/manage_events.html`

**Perubahan:**
- ✅ Tambah tombol "Edit Points" di action column
- ✅ Tambah modal "Edit Points" dengan form input
- ✅ Tambah JavaScript functions:
  - `openEditPointsModal()` - Buka modal
  - `closeEditPointsModal()` - Tutup modal
  - `saveEventPoints()` - Save via AJAX

### 2. **Backend (API)**
**File:** `items/api_views.py`

**Fungsi Baru:**
```python
@login_required
@require_http_methods(["POST"])
def update_event_points(request, event_pk):
    """
    Update attendance points for an event.
    """
    # Validasi admin permission
    # Validasi input (0-9999)
    # Update event.event_points
    # Return JSON response
```

### 3. **URL Routes**
**File:** `items/urls.py`

**Route Baru:**
```python
path('activity/events/<int:event_pk>/update-points/', 
     update_event_points, 
     name='update-event-points'),
```

## 🎮 Cara Menggunakan

### **Langkah-langkah:**

1. **Buka Manage Events**
   - URL: http://127.0.0.1:8000/portal/activity/events/

2. **Klik Tombol Edit (🖊️)**
   - Tombol orange di kolom Actions
   - Modal akan muncul

3. **Edit Points**
   - Masukkan nilai points baru (0-9999)
   - Untuk Invasion: Note akan muncul menjelaskan bahwa ini base points

4. **Save**
   - Klik "Save Points"
   - Halaman akan reload otomatis
   - Points ter-update ✅

## 📝 Validasi

### **Input Validation:**
- ✅ Points harus angka
- ✅ Minimum: 0
- ✅ Maximum: 9999
- ✅ Required field

### **Permission:**
- ✅ Hanya Event Admin yang bisa edit
- ✅ Return 403 jika bukan admin

### **Error Handling:**
- ✅ Event not found → 404
- ✅ Invalid input → 400
- ✅ Server error → 500

## 🔍 Catatan Khusus

### **Untuk Event Invasion:**
Modal akan menampilkan note:
> **Note:** For Invasion events, this is the base points. Boss-specific points can be edited in the attendance page.

Artinya:
- `event_points` = Base points untuk attendance
- Boss points (Dragon Beast, Carnifex, Orfen) bisa di-edit di halaman attendance

### **Tidak Mempengaruhi:**
- ❌ Event yang sudah completed (points tetap bisa di-edit)
- ❌ Player activity yang sudah ada (tidak recalculate otomatis)
- ✅ Hanya mengubah `event.event_points` field

## 🚀 Deploy

```bash
# Push ke GitHub
git add .
git commit -m "Feature: Add edit attendance points for events in manage page"
git push origin main

# Deploy ke VPS
cd /home/valkyrie.id/public_html && \
git pull origin main && \
source venv/bin/activate && \
{ pkill -f "gunicorn.*myproject.wsgi" || true; } && \
sleep 2 && \
gunicorn --workers 3 --bind 127.0.0.1:8001 --timeout 120 --daemon myproject.wsgi:application && \
echo "Deployed!"
```

## 🧪 Testing

### **Test Case 1: Edit Points Normal Event**
1. Buka Manage Events
2. Klik Edit pada event "Boss Rush"
3. Ubah points dari 100 → 150
4. Save
5. ✅ Verify points ter-update di tabel

### **Test Case 2: Edit Points Invasion Event**
1. Klik Edit pada event "Invasion"
2. ✅ Verify note muncul tentang boss-specific points
3. Ubah points dari 50 → 75
4. Save
5. ✅ Verify points ter-update

### **Test Case 3: Validation**
1. Klik Edit
2. Masukkan nilai -10 (negative)
3. ✅ Verify error message
4. Masukkan nilai 99999 (too large)
5. ✅ Verify error message

### **Test Case 4: Permission**
1. Login sebagai non-admin
2. Try to access endpoint directly
3. ✅ Verify 403 Forbidden

---

**Feature Complete!** 🎊
