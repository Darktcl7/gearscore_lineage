import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alto.settings")
django.setup()

from dkp.models import DKPProfile, DKPLog

def restore_points():
    print(">> Memulai Reparasi Database DKP...")
    
    # 1. Hapus Log yang salah kaprah (-1200 dan +1200) khusus clan Valkyrie
    bad_remove = DKPLog.objects.filter(profile__character__clan="Valkyrie", reason__contains="exchange - Dark Legion", amount=-1200)
    bad_add = DKPLog.objects.filter(profile__character__clan="Valkyrie", reason__contains="revisi dkp", amount=1200)
    
    count_remove = bad_remove.count()
    count_add = bad_add.count()
    
    bad_remove.delete()
    bad_add.delete()
    
    print(f">> Berhasil menghapus {count_remove} log (-1200) yang salah.")
    print(f">> Berhasil menghapus {count_add} log (+1200) revisi sementara.")
    
    # 2. Hitung ulang DKP Profile bedasarkan history sejak lahir (khusus clan Valkyrie)
    profiles = DKPProfile.objects.filter(character__clan="Valkyrie")
    count_fixed = 0
    
    for p in profiles:
        logs = DKPLog.objects.filter(profile=p).order_by('created_at', 'id')
        val = 0
        for l in logs:
            val += l.amount
            if val < 0:
                val = 0 # mensimulasikan mekanisme mentok di 0 yang selama ini berjalan
        
        if p.current_dkp != val:
            print(f" [Diperbaiki] {p.character.name}: {p.current_dkp} DKP -> {val} DKP")
            p.current_dkp = val
            p.save()
            count_fixed += 1
            
    print(f">> Reparasi Selesai! {count_fixed} karater telah dikembalikan ke poin aslinya.")

if __name__ == "__main__":
    restore_points()
