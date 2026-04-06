import re

# =====================
# 1. Fix bot.py
# =====================
path = r'd:\Django Project\Alto Project\discord_bot\bot.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1a. Remove /dkp events command
old_dkp_events = '''    @dkp_group.command(name="events", description="List active DKP events/raids")
    async def dkp_events(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        result = await self.api_request('GET', '/dkp/api/active/')
        
        if result.get('success'):
            if not result['events']:
                await interaction.followup.send("\u2139\ufe0f No active DKP events at this time.", ephemeral=True)
                return
            
            msg = "**\u2694\ufe0f Active DKP Events:**\\n"
            for e in result['events']:
                msg += f"\u2022 **{e['name']}** (ID: {e['id']}) - Reward: {e['points']} DKP\\n"
            msg += "\\nUse /dkp checkin <event_id> <character_name> to check in."
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.followup.send(f"\u274c Error: {result.get('error', 'Connection failed')}", ephemeral=True)



'''
if old_dkp_events in content:
    content = content.replace(old_dkp_events, '')
    changes += 1
    print('1a. /dkp events REMOVED')
else:
    print('1a. /dkp events NOT FOUND')

# 1b. Fix /event_result to support per-clan win/lose
old_result_cmd = '''    @app_commands.command(name="event_result", description="Complete an event and record results")
    @app_commands.describe(
        event_id="The Event ID to complete",
        win="Did the guild win?",
        dragon_beast="[Invasion] Dragon Beast killed?",
        carnifex="[Invasion] Carnifex killed?",
        orfen="[Invasion] Orfen killed?"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def complete_event(
        self, 
        interaction: discord.Interaction, 
        event_id: str,
        win: bool = False,
        dragon_beast: bool = False,
        carnifex: bool = False,
        orfen: bool = False
    ):
        \"\"\"Complete an event and record results (Officers only)\"\"\"
        await interaction.response.defer()
        
        data = {
            'event_id': event_id,
            'is_win': win,
            'bosses_killed': {
                'dragon_beast': dragon_beast,
                'carnifex': carnifex,
                'orfen': orfen,
            }
        }
        
        result = await self.api_request('POST', '/portal/api/activity/event/complete/', data)
        
        if result.get('success'):
            embed = discord.Embed(
                title="\U0001f3c6 EVENT COMPLETED!",
                description=f"Event {event_id} has been completed.",
                color=discord.Color.gold()
            )
            embed.add_field(name="Status", value="\U0001f534 COMPLETED - Check-in closed", inline=False)
            embed.add_field(name="Max Points", value=f"{result['max_points']} pts", inline=True)
            embed.add_field(name="Participants", value=f"{result['participants']} players", inline=True)
            embed.add_field(name="Result", value="\u2705 WIN" if win else "\u274c LOSE", inline=True)
            embed.set_footer(text="Points have been calculated and added to the leaderboard!")
            await interaction.followup.send("@everyone \U0001f4e2 **The event has ended!**", embed=embed)
        else:
            await interaction.followup.send(f"\u274c Error: {result.get('error', 'Unknown error')}", ephemeral=True)'''

new_result_cmd = '''    @app_commands.command(name="event_result", description="Complete an event and record results")
    @app_commands.describe(
        event_id="The Event ID to complete",
        win="Did the guild win? (for non-clan events)",
        win_valkyrie="[Boss Rush/Catacombs/Dimensional] Did Valkyrie win?",
        win_valhalla="[Boss Rush/Catacombs/Dimensional] Did Valhalla win?",
        dragon_beast="[Invasion] Dragon Beast killed?",
        carnifex="[Invasion] Carnifex killed?",
        orfen="[Invasion] Orfen killed?"
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def complete_event(
        self, 
        interaction: discord.Interaction, 
        event_id: str,
        win: bool = False,
        win_valkyrie: bool = False,
        win_valhalla: bool = False,
        dragon_beast: bool = False,
        carnifex: bool = False,
        orfen: bool = False
    ):
        \"\"\"Complete an event and record results (Officers only)\"\"\"
        await interaction.response.defer()
        
        data = {
            'event_id': event_id,
            'is_win': win,
            'is_win_valkyrie': win_valkyrie,
            'is_win_valhalla': win_valhalla,
            'bosses_killed': {
                'dragon_beast': dragon_beast,
                'carnifex': carnifex,
                'orfen': orfen,
            }
        }
        
        result = await self.api_request('POST', '/portal/api/activity/event/complete/', data)
        
        if result.get('success'):
            embed = discord.Embed(
                title="\U0001f3c6 EVENT COMPLETED!",
                description=f"Event {event_id} has been completed.",
                color=discord.Color.gold()
            )
            embed.add_field(name="Status", value="\U0001f534 COMPLETED - Check-in closed", inline=False)
            embed.add_field(name="Max Points", value=f"{result['max_points']} pts", inline=True)
            embed.add_field(name="Participants", value=f"{result['participants']} players", inline=True)
            
            # Per-clan result display
            if win_valkyrie or win_valhalla:
                vk = "\u2705 Win" if win_valkyrie else "\u274c Lose"
                vh = "\u2705 Win" if win_valhalla else "\u274c Lose"
                embed.add_field(name="Valkyrie", value=vk, inline=True)
                embed.add_field(name="Valhalla", value=vh, inline=True)
            else:
                embed.add_field(name="Result", value="\u2705 WIN" if win else "\u274c LOSE", inline=True)
            
            embed.set_footer(text="Points have been calculated and added to the leaderboard!")
            await interaction.followup.send("@everyone \U0001f4e2 **The event has ended!**", embed=embed)
        else:
            await interaction.followup.send(f"\u274c Error: {result.get('error', 'Unknown error')}", ephemeral=True)'''

if old_result_cmd in content:
    content = content.replace(old_result_cmd, new_result_cmd)
    changes += 1
    print('1b. /event_result UPDATED with per-clan win')
else:
    print('1b. /event_result NOT FOUND')

# 1c. Fix /event_myscore to show more accurate data
old_myscore = '''    @app_commands.command(name="event_myscore", description="View your current month activity stats")
    async def my_score(self, interaction: discord.Interaction):
        \"\"\"View personal stats\"\"\"
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        result = await self.api_request('GET', f'/portal/api/activity/player/discord/{discord_id}/')
        
        if result.get('success'):
            embed = discord.Embed(
                title=f"\U0001f4ca Stats for {result['player']}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Total Score", value=f"**{result['total_score']}** pts", inline=True)
            embed.add_field(name="Tier", value=result['tier'], inline=True)
            embed.add_field(name="Attendance", value=result['attendance'], inline=True)
            embed.add_field(name="Events Joined", value=f"{result['events_joined']}/{result['total_events']}", inline=True)
            embed.add_field(name="Est. Prize", value=f"\U0001f48e {result['estimated_prize']}", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif result.get('error') == 'Discord not linked to any Character':
            await interaction.followup.send(
                "\u274c **Discord not linked!**\\nPlease link your Discord in website profile first.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f"\u274c {result.get('error', 'Unknown error')}", ephemeral=True)'''

new_myscore = '''    @app_commands.command(name="event_myscore", description="View your current month activity stats")
    async def my_score(self, interaction: discord.Interaction):
        \"\"\"View personal stats\"\"\"
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        result = await self.api_request('GET', f'/portal/api/activity/player/discord/{discord_id}/')
        
        if result.get('success'):
            embed = discord.Embed(
                title=f"\U0001f4ca Stats for {result['player']}",
                description=f"Clan: **{result.get('clan', '-')}**",
                color=discord.Color.blue()
            )
            embed.add_field(name="\U0001f3af Total Score", value=f"**{result['total_score']}** pts", inline=True)
            embed.add_field(name="\U0001f31f Tier", value=result['tier'], inline=True)
            embed.add_field(name="\U0001f4c5 Attendance", value=result['attendance'], inline=True)
            embed.add_field(name="\u2694\ufe0f Events Joined", value=f"{result['events_joined']}/{result['total_events']}", inline=True)
            embed.add_field(name="\U0001f525 Win Streak", value=f"{result.get('current_streak', 0)}x", inline=True)
            embed.add_field(name="\U0001f3c5 Streak Bonus", value=f"+{result.get('total_streak_bonus', 0)} pts", inline=True)
            embed.add_field(name="\u2b50 AP Points", value=f"{result.get('ap_points', 0)} pts", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif result.get('error') == 'Discord not linked to any Character':
            await interaction.followup.send(
                "\u274c **Discord not linked!**\\nPlease link your Discord in website profile first.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f"\u274c {result.get('error', 'Unknown error')}", ephemeral=True)'''

if old_myscore in content:
    content = content.replace(old_myscore, new_myscore)
    changes += 1
    print('1c. /event_myscore UPDATED with streak/AP')
else:
    print('1c. /event_myscore NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'bot.py: {changes} changes applied')


# =====================
# 2. Fix api_views.py - api_player_stats_discord (accurate stats)
# =====================
path2 = r'd:\Django Project\Alto Project\items\api_views.py'
with open(path2, 'r', encoding='utf-8') as f:
    content2 = f.read()

old_api_stats = '''def api_player_stats_discord(request, discord_id):
    \"\"\"
    Get a player's current month stats by Discord ID.
    GET /api/activity/player/discord/<discord_id>/
    \"\"\"
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        from django.utils import timezone
        today = timezone.now()
        
        character = Character.objects.filter(discord_id=discord_id).first()
        
        if not character:
            return JsonResponse({'error': 'Discord not linked to any Character'}, status=404)
        
        report = MonthlyReport.objects.filter(
            player=character,
            month__year=today.year,
            month__month=today.month
        ).first()
        
        if report:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': report.total_score,
                'tier': report.get_tier_display(),
                'attendance': f"{report.attendance_rate * 100:.1f}%",
                'events_joined': report.attended_events,
                'total_events': report.total_events,
                'estimated_prize': report.prize_amount if report.is_qualified else 0,
            })
        else:
            return JsonResponse({
                'success': True,
                'player': character.name,
                'total_score': 0,
                'tier': '\U0001f331 Casual',
                'attendance': '0%',
                'events_joined': 0,
                'total_events': 0,
                'estimated_prize': 0,
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)'''

new_api_stats = '''def api_player_stats_discord(request, discord_id):
    \"\"\"
    Get a player's current month stats by Discord ID.
    Calculates directly from PlayerActivity for accuracy.
    GET /api/activity/player/discord/<discord_id>/
    \"\"\"
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        from django.utils import timezone
        from django.db.models import Sum
        from datetime import timedelta
        today = timezone.now()
        month_ago = today - timedelta(days=30)
        
        character = Character.objects.filter(discord_id=discord_id).first()
        
        if not character:
            return JsonResponse({'error': 'Discord not linked to any Character'}, status=404)
        
        # Calculate stats directly from PlayerActivity (like my_activity view)
        activities = PlayerActivity.objects.filter(
            player=character,
            event__date__gte=month_ago,
            event__is_completed=True
        ).select_related('event')
        
        # Base points (excluding AP adjustments)
        total_points_base = activities.exclude(
            event__name__startswith='AP Adjustment:'
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        total_streak_bonus = activities.exclude(
            event__name__startswith='AP Adjustment:'
        ).aggregate(total=Sum('win_streak_bonus'))['total'] or 0
        
        total_score = total_points_base + total_streak_bonus
        
        # AP points
        ap_points = activities.filter(
            event__name__startswith='AP Adjustment:'
        ).aggregate(total=Sum('points_earned'))['total'] or 0
        
        # Attendance
        attended_count = activities.exclude(
            event__name__startswith='AP Adjustment:'
        ).exclude(
            event__name__startswith='Score Adjustment:'
        ).filter(status='ATTENDED').count()
        
        total_events = ActivityEvent.objects.exclude(
            name__startswith='AP Adjustment:'
        ).exclude(
            name__startswith='Score Adjustment:'
        ).filter(
            date__gte=month_ago,
            is_completed=True
        ).count()
        
        attendance_rate = (attended_count / total_events * 100) if total_events > 0 else 0
        
        # Current win streak
        current_streak = 0
        recent_activities = activities.exclude(
            event__name__startswith='AP Adjustment:'
        ).exclude(
            event__name__startswith='Score Adjustment:'
        ).filter(status='ATTENDED').order_by('-event__date')
        
        for act in recent_activities:
            evt = act.event
            if evt.event_type in ('BOSS_RUSH', 'CATACOMBS', 'DIMENSIONAL'):
                is_win = evt.is_win_valhalla if character.clan == 'Valhalla' else evt.is_win_valkyrie
            else:
                is_win = evt.is_win
            if is_win:
                current_streak += 1
            else:
                break
        
        # Tier
        if total_score > 950:
            tier = '\U0001f451 Core'
        elif total_score > 675:
            tier = '\U0001f6e1\ufe0f Elite'
        elif total_score > 400:
            tier = '\u2694\ufe0f Active'
        else:
            tier = '\U0001f4a4 Inactive'
        
        return JsonResponse({
            'success': True,
            'player': character.name,
            'clan': character.clan or 'Valkyrie',
            'total_score': total_score,
            'tier': tier,
            'attendance': f"{attendance_rate:.1f}%",
            'events_joined': attended_count,
            'total_events': total_events,
            'current_streak': current_streak,
            'total_streak_bonus': total_streak_bonus,
            'ap_points': ap_points,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)'''

if old_api_stats in content2:
    content2 = content2.replace(old_api_stats, new_api_stats)
    print('2. api_player_stats_discord UPDATED')
else:
    print('2. api_player_stats_discord NOT FOUND')

# 3. Fix api_complete_event to support per-clan win
old_complete = '''        # Update event results
        event.is_completed = True
        event.is_win = data.get('is_win', False)'''

new_complete = '''        # Update event results
        event.is_completed = True
        if event.event_type in ('BOSS_RUSH', 'CATACOMBS', 'DIMENSIONAL'):
            event.is_win_valkyrie = data.get('is_win_valkyrie', data.get('is_win', False))
            event.is_win_valhalla = data.get('is_win_valhalla', data.get('is_win', False))
            event.is_win = event.is_win_valkyrie or event.is_win_valhalla
        else:
            event.is_win = data.get('is_win', False)
            event.is_win_valkyrie = event.is_win
            event.is_win_valhalla = event.is_win'''

if old_complete in content2:
    content2 = content2.replace(old_complete, new_complete)
    print('3. api_complete_event UPDATED with per-clan')
else:
    print('3. api_complete_event NOT FOUND')

with open(path2, 'w', encoding='utf-8') as f:
    f.write(content2)

print('ALL DONE')
