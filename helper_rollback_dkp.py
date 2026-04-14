import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from dkp.models import DKPProfile

# Data SEBELUM script dijalankan (dari output terminal)
# Format: "NamaKarakter": poin_sebelum_script
ROLLBACK_DATA = {
    "Nelm": 5227,
    "DELV": 3082,
    "Rale": 0,
    "Grym (VC)": 1203,
    "DadokZ": 0,
    "Barakiel": 0,
    "Evolution": 2478,
    "Ennma": 1364,
    "SONIX": 1526,
    "Zimisu": 2319,
    "SBRX": 1656,
    "KAELs": 0,
    "AYAY": 0,
    "Laccoon": 5297,
    "TheoHue": 0,
    "Vodsky": 2056,
    "ribacGG": 0,
    "xCJP": 1613,
    "Khadatz": 0,
    "Dagun": 0,
    "ironclad": 0,
    "Kaiten": 1775,
    "Seah": 2357,
    "Peggygou": 0,
    "LouisNgo": 1206,
    "OmJahat": 2830,
    "Monyang": 0,
    "Flows": 0,
    "hanawa": 0,
    "sand23man": 1313,
    "Ravelt": 2495,
    "Katyusha": 250,
    "zse": 0,
    "LUKAV": 2923,
    "YMRFlo": 0,
    "Maggi": 1496,
    "ZeebOne": 2407,
    "HOBU": 0,
    "Monvy": 0,
    "Malsea": 2175,
    "Ercoz": 0,
    "HEATON": 2351,
    "Beepo": 1415,
    "Weldayz": 1725,
    "Oxygen": 3801,
    "Skay": 1246,
    "Kidboy": 1301,
}

def rollback():
    print(">> ROLLBACK: Mengembalikan poin ke kondisi sebelum script fix...")
    count = 0
    not_found = []

    for char_name, old_dkp in ROLLBACK_DATA.items():
        try:
            profile = DKPProfile.objects.get(character__name=char_name)
            if profile.current_dkp != old_dkp:
                print(f"  [Rollback] {char_name}: {profile.current_dkp} DKP -> {old_dkp} DKP")
                profile.current_dkp = old_dkp
                profile.save()
                count += 1
            else:
                print(f"  [OK] {char_name}: sudah {old_dkp} DKP")
        except DKPProfile.DoesNotExist:
            not_found.append(char_name)
            print(f"  [NOT FOUND] {char_name}")

    print(f"\n>> ROLLBACK SELESAI! {count} karakter dikembalikan.")
    if not_found:
        print(f">> Tidak ditemukan: {', '.join(not_found)}")

if __name__ == "__main__":
    rollback()
