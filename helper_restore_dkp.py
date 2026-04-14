import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.utils import timezone
from django.db.models import Sum
from dkp.models import DKPProfile, DKPLog

# ============================================================
# Data snapshot dari Discord Bot: 13 April 2026, 13:08 (UTC+8)
# Ini adalah data DKP ASLI sebelum insiden salah potong -1200
# ============================================================
DISCORD_SNAPSHOT = {
    "Nelm": 4591,
    "Laccoon": 4579,
    "ZeebOne": 3421,
    "Oxygen": 3264,
    "Ravelt": 3262,
    "DELV": 2875,
    "SDV": 2734,
    "LUKAV": 2519,
    "OmJahat": 2417,
    "Malsea": 2232,
    "Seah": 2217,
    "HEATON": 2205,
    "Evolution": 2151,
    "Zimisu": 1936,
    "Vodsky": 1738,
    "Weldayz": 1674,
    "LouisNgo": 1454,
    "Monvy": 1450,
    "Kaiten": 1443,
    "SBRX": 1395,
    "DadokZ": 1332,
    "Katyusha": 1298,
    "Maggi": 1270,
    "SONIX": 1266,
    "Ennma": 1201,
    "sand23man": 1198,
    "xCJP": 1192,
    "Kidboy": 1163,
    "Skay": 1092,
    "Beepo": 1090,
    "Ercoz": 1069,
    "TheoHue": 867,
    "HOBU": 856,
    "Monyang": 844,
    "hanawa": 770,
    "YMRFlo": 742,
    "Rale": 703,
    "Peggygou": 677,
    "ironclad": 611,
    "BICCONGHODE": 580,
    "Barakiel": 576,
    "Grym (VC)": 483,
    "ribacGG": 474,
    "KAELs": 467,
    "Flows": 440,
    "zse": 398,
    "Khadatz": 188,
    "Dagun": 73,
    "AYAY": 55,
}

def restore_from_discord():
    print("=" * 60)
    print("  RESTORASI DKP DARI DATA DISCORD SNAPSHOT")
    print("  Snapshot: 13 Apr 2026, 13:08 (UTC+8)")
    print("=" * 60)

    # Waktu snapshot Discord: 13 April 2026, 13:08 UTC+8
    # Semua log SETELAH waktu ini yang masih ada di database
    # adalah aktivitas sah (boss, dll) yang harus ditambahkan
    snapshot_time = timezone.make_aware(
        datetime(2026, 4, 13, 13, 8, 0),
        timezone=timezone.get_current_timezone()
    )

    count_fixed = 0
    not_found = []

    for char_name, base_dkp in DISCORD_SNAPSHOT.items():
        try:
            profile = DKPProfile.objects.get(character__name=char_name)
        except DKPProfile.DoesNotExist:
            not_found.append(char_name)
            print(f"  [NOT FOUND] {char_name}")
            continue

        # Hitung semua DKP yang diperoleh/dikeluarkan SETELAH snapshot
        # (log -1200 dan +1200 sudah terhapus, jadi yang tersisa adalah
        #  aktivitas sah seperti boss kill, treasury purchase, dll)
        logs_after = DKPLog.objects.filter(
            profile=profile,
            created_at__gt=snapshot_time
        )

        earned_after = logs_after.aggregate(total=Sum('amount'))['total'] or 0

        # DKP yang benar = Snapshot Discord + aktivitas sah setelahnya
        correct_dkp = base_dkp + earned_after
        if correct_dkp < 0:
            correct_dkp = 0

        old_dkp = profile.current_dkp

        if old_dkp != correct_dkp:
            print(f"  [FIX] {char_name}: {old_dkp} -> {correct_dkp} DKP "
                  f"(base={base_dkp}, earned_after={earned_after:+d})")
            profile.current_dkp = correct_dkp
            profile.save()
            count_fixed += 1
        else:
            print(f"  [OK]  {char_name}: {correct_dkp} DKP (sudah benar)")

    print()
    print(f">> RESTORASI SELESAI! {count_fixed} karakter diperbaiki.")
    if not_found:
        print(f">> Tidak ditemukan: {', '.join(not_found)}")

if __name__ == "__main__":
    restore_from_discord()
