from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Character, SubclassStats, GearScoreLog

# This function will be triggered after a Character or SubclassStats object is saved.
@receiver(post_save, sender=Character)
@receiver(post_save, sender=SubclassStats)
def log_gear_score_change(sender, instance, **kwargs):
    """
    Logs the character's gear score whenever the character or
    their subclass stats are updated.
    """
    # Determine the character instance
    if sender == Character:
        character = instance
    elif sender == SubclassStats:
        character = instance.character
    else:
        return # Should not happen

    # Calculate the new gear score breakdown
    breakdown = character.calculate_gear_score_breakdown()

    # Get the latest log entry for this character
    latest_log = GearScoreLog.objects.filter(character=character).first()

    # Check if the score has actually changed to avoid creating duplicate logs
    if latest_log and abs(latest_log.total_score - breakdown['total_score']) < 0.01:
        return # No significant change, so don't create a new log

    # Create a new log entry with fields that exist in GearScoreLog model
    GearScoreLog.objects.create(
        character=character,
        total_score=breakdown['total_score'],
        dmg=breakdown.get('dmg', 0),
        acc=breakdown.get('acc', 0),
        def_stat=breakdown.get('def_stat', 0),
        reduc=breakdown.get('reduc', 0),
        resist=breakdown.get('resist', 0),
        skill_dmg_boost=breakdown.get('skill_dmg_boost', 0),
        wpn_dmg_boost=breakdown.get('wpn_dmg_boost', 0),
        soulshot=breakdown.get('soulshot', 0),
        valor=breakdown.get('valor', 0),
        guardian=breakdown.get('guardian', 0),
        reason=f'{sender.__name__} updated'
    )
