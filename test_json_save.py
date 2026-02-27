import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from items.forms import CharacterAttributesForm

post_data = {
    'inheritor_books': [],
    'epic_classes_count': 1,
    'epic_agathions_count': 1,
    'enchant_bracelet_holy_prot': 0,
    'enchant_bracelet_influence': 0,
    'enchant_earring_earth': 0,
    'enchant_earring_fire': 0,
    'enchant_seal_eva': 0,
    'aster_erafone': 0,
    'pvp_helmet_enchant': 0,
    'pvp_gloves_enchant': 0,
    'pvp_boots_enchant': 0,
    'pvp_gaiters_enchant': 0,
    'pvp_top_armor_enchant': 0,
    'pvp_cloak_enchant': 0,
    'pvp_sigil_enchant': 0,
    'pvp_necklace_enchant': 0,
    'pvp_ring_left_enchant': 0,
    'pvp_ring_right_enchant': 0,
    'pvp_belt_enchant': 0,
    'stat_dmg': 0,
    'stat_acc': 0,
    'stat_def': 0,
    'stat_reduc': 0,
    'stat_resist': 0,
    'stat_skill_dmg_boost': 0,
    'stat_wpn_dmg_boost': 0,
    'total_legend_codex': 0,
    'total_epic_mount': 0,
    'weapon_enchant': 0,
    'unlocked_skills': '["skill1", "skill2"]'
}

form = CharacterAttributesForm(post_data)
if form.is_valid():
    attrs = form.save(commit=False)
    print('VALID', attrs.unlocked_skills)
else:
    print('INVALID', form.errors)
