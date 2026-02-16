# D:\Django Project\Alto Project\discord_bot\bot.py
"""
Alto Guild Activity Discord Bot
This bot integrates with the Alto Project web app to track guild activities.

Commands (Officers):
- /event create <type> - Create a new event with check-in button
- /result <event_id> - Complete event and record results
- /leaderboard post - Post leaderboard to events channel

Commands (All Members):
- /checkin <event_id> <character> - Manual check-in
- /myscore <character> - View your stats
- /leaderboard - View top 10

Channel Flow:
1. Officer creates event with /event -> Bot posts announcement in #events channel
2. Members click "Check In" button -> Bot records attendance
3. Officer completes event with /result -> Bot updates and posts summary
"""

import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_BASE_URL = os.getenv('ALTO_API_URL', 'http://127.0.0.1:8000') # Fixed URL structure to Root
API_KEY = os.getenv('ALTO_API_KEY', 'alto-discord-bot-key-2026')
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')

# Channel Configuration
EVENTS_CHANNEL_ID = int(os.getenv('EVENTS_CHANNEL_ID', '0'))
LEADERBOARD_CHANNEL_ID = int(os.getenv('LEADERBOARD_CHANNEL_ID', '0'))

# Reminder Schedule (Day: 0=Mon, 1=Tue, ..., 6=Sun)
# Format 24h: 'HH:MM'
# Reminder Config is now fetched from API

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

from discord.ext import tasks

class AltoBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.reminder_loop.start() # Start reminder loop
    
    def cog_unload(self):
        self.reminder_loop.cancel()
        if self.session:
            self.bot.loop.create_task(self.session.close())
    
    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        try:
            # 1. PROCESS ALL PENDING ANNOUNCEMENTS
            while True:
                ann_result = await self.api_request('GET', '/portal/api/discord/announcements/') 
                
                if not ann_result.get('success') or not ann_result.get('has_new'):
                    break
                    
                channel = self.bot.get_channel(EVENTS_CHANNEL_ID)
                if channel:
                    msg_content = ann_result['message']
                    
                    # Check for Direct Message (DM) Request
                    if msg_content.startswith('[DM:'):
                        # Format: [DM:123456789] Message
                        try:
                            end_bracket = msg_content.find(']')
                            if end_bracket != -1:
                                user_id = int(msg_content[4:end_bracket])
                                dm_msg = msg_content[end_bracket+1:].strip()
                                
                                user = self.bot.get_user(user_id)
                                if not user:
                                    # Try fetching if not in cache
                                    try:
                                        user = await self.bot.fetch_user(user_id)
                                    except:
                                        pass
                                
                                if user:
                                    try:
                                        await user.send(dm_msg)
                                        print(f"DM sent to {user.name}: {dm_msg[:20]}...")
                                    except discord.Forbidden:
                                        print(f"Failed to DM {user.name} (Closed DMs)")
                                else:
                                    print(f"User {user_id} not found for DM")
                        except Exception as e:
                            print(f"Error parsing DM: {e}")
                            
                    # Check if it's a simple notification
                    elif msg_content.startswith('[NOTIFICATION]'):
                        clean_msg = msg_content.replace('[NOTIFICATION]', '').strip()
                        await channel.send(clean_msg)
                        print(f"Notification sent: {clean_msg[:20]}...")
                    else:
                        embed = discord.Embed(
                            description=msg_content,
                            color=discord.Color.blue()
                        )
                        await channel.send("📢 **ANNOUNCEMENT**", embed=embed)
                        print(f"Broadcast sent: {msg_content[:20]}...")
                
                # Small delay to prevent rate limits
                import asyncio
                await asyncio.sleep(1)

            # 2. Sync Alarms (Once per cycle is enough)
            alarm_result = await self.api_request('GET', '/portal/api/discord/alarms/')
            alarms = []
            if alarm_result.get('success'):
                alarms = alarm_result.get('alarms', [])

            # 3. Check Alarms
            now = datetime.now()
            current_day = now.weekday()
            current_time = now.strftime("%H:%M")
            
            for item in alarms:
                if item['day'] == current_day and item['time'] == current_time:
                    channel = self.bot.get_channel(EVENTS_CHANNEL_ID)
                    if channel:
                        await channel.send(item['msg'])
                        print(f"Sent reminder: {item['msg']}")
                        
        except Exception as e:
            print(f"Error in reminder loop: {e}")

    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()
    
    async def api_request(self, method, endpoint, data=None):
        """Make API request to Alto web app"""
        url = f"{API_BASE_URL}{endpoint}"
        headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                async with self.session.get(url, headers=headers) as resp:
                    return await resp.json()
            elif method == 'POST':
                async with self.session.post(url, headers=headers, json=data) as resp:
                    return await resp.json()
        except Exception as e:
            return {'error': str(e)}
    
    # ==========================================
    # SLASH COMMANDS
    # ==========================================
    
    @app_commands.command(name="event_post", description="Post active event from website for check-in")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_event(self, interaction: discord.Interaction):
        """Post an active event (Officers only)"""
        await interaction.response.defer(ephemeral=True)
        
        # Get active events from API
        result = await self.api_request('GET', '/portal/api/activity/events/active/')
        
        if result.get('success') and result.get('events'):
            # Create dropdown menu
            view = EventSelectView(result['events'], self)
            await interaction.followup.send("Pilih event yang ingin di-post:", view=view)
        else:
            await interaction.followup.send("❌ Tidak ada event aktif di website. Silakan buat event di website terlebih dahulu.", ephemeral=True)


    

    
    @app_commands.command(name="event_result", description="Complete an event and record results")
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
        """Complete an event and record results (Officers only)"""
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
                title="🏆 EVENT SELESAI!",
                description=f"Event `{event_id}` telah diselesaikan.",
                color=discord.Color.gold()
            )
            embed.add_field(name="Status", value="🔴 SELESAI - Check-in ditutup", inline=False)
            embed.add_field(name="Max Points", value=f"{result['max_points']} pts", inline=True)
            embed.add_field(name="Peserta", value=f"{result['participants']} player", inline=True)
            embed.add_field(name="Hasil", value="✅ WIN" if win else "❌ LOSE", inline=True)
            embed.set_footer(text="Poin sudah dihitung dan ditambahkan ke leaderboard!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error', 'Unknown error')}", ephemeral=True)
    
    @app_commands.command(name="event_myscore", description="View your current month activity stats")
    async def my_score(self, interaction: discord.Interaction):
        """View personal stats"""
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        result = await self.api_request('GET', f'/portal/api/activity/player/discord/{discord_id}/')
        
        if result.get('success'):
            embed = discord.Embed(
                title=f"📊 Stats for {result['player']}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Total Score", value=f"**{result['total_score']}** pts", inline=True)
            embed.add_field(name="Tier", value=result['tier'], inline=True)
            embed.add_field(name="Attendance", value=result['attendance'], inline=True)
            embed.add_field(name="Events Joined", value=f"{result['events_joined']}/{result['total_events']}", inline=True)
            embed.add_field(name="Est. Prize", value=f"💎 {result['estimated_prize']}", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif result.get('error') == 'Discord not linked to any Character':
            await interaction.followup.send(
                "❌ **Discord belum ter-link!**\nSilakan link Discord di website profile terlebih dahulu.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f"❌ {result.get('error', 'Unknown error')}", ephemeral=True)
    
    @app_commands.command(name="event_leaderboard", description="View this month's activity leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        """View leaderboard"""
        await interaction.response.defer()
        
        result = await self.api_request('GET', '/portal/api/activity/leaderboard/')
        
        if result.get('success'):
            embed = discord.Embed(
                title=f"🏆 Activity Leaderboard - {result['month']}",
                color=discord.Color.gold()
            )
            
            if result['leaderboard']:
                leaderboard_text = ""
                for entry in result['leaderboard']:
                    rank = entry['rank']
                    if rank == 1:
                        medal = "🥇"
                    elif rank == 2:
                        medal = "🥈"
                    elif rank == 3:
                        medal = "🥉"
                    else:
                        medal = f"#{rank}"
                    
                    leaderboard_text += f"{medal} **{entry['player']}** - {entry['score']} pts ({entry['tier']})\n"
                
                embed.description = leaderboard_text
            else:
                embed.description = "No activity data yet this month."
            
            embed.set_footer(text="Use /myscore <character> to see your stats!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error', 'Unknown error')}")


    # ==========================================
    # DKP SYSTEM COMMANDS (GROUP /dkp)
    # ==========================================
    
    dkp_group = app_commands.Group(name="dkp", description="Dragon Kill Points System")

    @dkp_group.command(name="events", description="List active DKP events/raids")
    async def dkp_events(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        result = await self.api_request('GET', '/dkp/api/active/')
        
        if result.get('success'):
            if not result['events']:
                await interaction.followup.send("ℹ️ Tidak ada event DKP yang aktif saat ini.", ephemeral=True)
                return
            
            msg = "**⚔️ Active DKP Events:**\n"
            for e in result['events']:
                msg += f"• **{e['name']}** (ID: {e['id']}) - Reward: {e['points']} DKP\n"
            msg += "\nGunakan `/dkp checkin <event_id> <character_name>` untuk absen."
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error', 'Connection failed')}", ephemeral=True)



    @dkp_group.command(name="me", description="Check your DKP balance")
    async def dkp_me(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        discord_id = str(interaction.user.id)
        result = await self.api_request('GET', f'/dkp/api/me/discord/{discord_id}/')
        
        if result.get('success'):
            await interaction.followup.send(
                f"📊 **DKP Status: {result['character']}**\n"
                f"💰 Current DKP: **{result['current_dkp']}**",
                ephemeral=True
            )
        elif result.get('error') == 'Discord not linked to any Character':
            await interaction.followup.send(
                "❌ **Discord belum ter-link!**\nSilakan link Discord di website profile terlebih dahulu.",
                ephemeral=True
            )
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error', 'Unknown error')}", ephemeral=True)

    @dkp_group.command(name="post", description="Post DKP Event with Check-in Button")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def dkp_post(self, interaction: discord.Interaction):
        """Post active DKP event to channel"""
        await interaction.response.defer(ephemeral=True)
        result = await self.api_request('GET', '/dkp/api/active/')
        
        if result.get('success') and result.get('events'):
            view = DKPEventSelectView(result['events'], self)
            await interaction.followup.send("Pilih Event DKP yang ingin diposting:", view=view)
        else:
            await interaction.followup.send("❌ Tidak ada event DKP aktif.", ephemeral=True)

    @dkp_group.command(name="leaderboard", description="Top DKP Holders")
    async def dkp_leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await self.api_request('GET', '/dkp/api/leaderboard/')
        
        if result.get('success'):
            msg = "🏆 **DKP Leaderboard (Top 20)** 🏆\n```"
            for p in result['leaderboard']:
                msg += f"{p['rank']:2}. {p['character']:<15} {p['dkp']} DKP\n"
            msg += "```"
            await interaction.followup.send(msg)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error')}")


class EventSelectView(discord.ui.View):
    """View to select an active event"""
    def __init__(self, events: list, cog: AltoBot):
        super().__init__()
        self.add_item(EventSelect(events, cog))

class EventSelect(discord.ui.Select):
    """Dropdown to select an event"""
    def __init__(self, events: list, cog: AltoBot):
        self.cog = cog
        options = []
        for event in events:
            label = f"{event['name']}"
            # Truncate label if too long
            if len(label) > 90: label = label[:87] + "..."
            
            desc = f"{event['type']} | {event['participants']} participants"
            # Store type in value: "EVENT_ID|EVENT_TYPE"
            value = f"{event['event_id']}|{event['type']}"
            options.append(discord.SelectOption(label=label, value=value, description=desc))
        
        super().__init__(placeholder="Select an event to post...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Parse value "EVENT_ID|EVENT_TYPE"
        selection = self.values[0].split('|')
        event_id = selection[0]
        event_type = selection[1] if len(selection) > 1 else "OTHER"
        
        # Find label for display
        selected_option = next((opt for opt in self.options if opt.value == self.values[0]), None)
        event_name = selected_option.label
        
        # Determine emoji based on ACTUAL type from API
        type_emoji = "📅"
        if event_type == "INVASION": type_emoji = "🐉"
        elif event_type == "BOSS_RUSH": type_emoji = "⚔️"
        elif event_type == "CATACOMBS": type_emoji = "🏛️"
        
        embed = discord.Embed(
            title=f"{type_emoji} EVENT DIBUAT!",
            description=f"**{event_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Event ID", value=f"`{event_id}`", inline=True)
        embed.add_field(name="Type", value=event_type.replace('_', ' '), inline=True)
        embed.add_field(name="Status", value="🟢 AKTIF - Check-in dibuka!", inline=False)
        embed.set_footer(text="⬇️ Klik tombol Check In di bawah untuk bergabung!")
        
        view = CheckInView(event_id, self.cog)
        await interaction.response.send_message(embed=embed, view=view)


class CheckInView(discord.ui.View):
    """Button view for quick check-in"""
    def __init__(self, event_id: str, cog: AltoBot):
        super().__init__(timeout=None)  # No timeout for long-running events
        self.event_id = event_id
        self.cog = cog
    
    @discord.ui.button(label="✅ Check In", style=discord.ButtonStyle.green)
    async def checkin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Auto check-in based on linked Discord ID"""
        await interaction.response.defer(ephemeral=True)
        
        # Send check-in request with Discord ID (no character name needed)
        data = {
            'event_id': self.event_id,
            'discord_user_id': str(interaction.user.id),
            # No character_name - API will find by discord_id
        }
        
        result = await self.cog.api_request('POST', '/portal/api/activity/checkin/', data)
        
        if result.get('success'):
            if result.get('already_checked_in'):
                await interaction.followup.send(
                    f"⚠️ **{result['character']}** sudah check-in sebelumnya! (Poin tidak bertambah)",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"✅ **{result['character']}** berhasil check-in! (+{result['points']} pts)",
                    ephemeral=True
                )
        elif result.get('error') == 'Discord not linked':
            await interaction.followup.send(
                "❌ **Discord belum ter-link!**\n\n"
                "Silakan link Discord kamu di website terlebih dahulu:\n"
                "1. Buka website → Character Profile\n"
                "2. Klik tombol **Link Discord**\n"
                "3. Masukkan Discord ID kamu\n"
                "4. Coba Check In lagi",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ {result.get('message', result.get('error', 'Check-in gagal'))}",
                ephemeral=True
            )



# ==========================================
# DKP UI VIEWS
# ==========================================

class DKPEventSelectView(discord.ui.View):
    def __init__(self, events, cog):
        super().__init__()
        self.add_item(DKPEventSelect(events, cog))

class DKPEventSelect(discord.ui.Select):
    def __init__(self, events, cog):
        self.cog = cog
        options = []
        for e in events:
            label = f"{e['name']} ({e['points']} DKP)"
            options.append(discord.SelectOption(label=label, value=str(e['id']), description=f"ID: {e['id']}"))
        super().__init__(placeholder="Select DKP Event...", options=options)

    async def callback(self, interaction: discord.Interaction):
        event_id = self.values[0]
        # Get selected option label
        selected = next(opt for opt in self.options if opt.value == event_id)
        name = selected.label
        
        embed = discord.Embed(
            title="⚔️ DKP RAID EVENT",
            description=f"**{name}**\n\nKlik tombol di bawah untuk Check-in kehadiran!\nPoin akan masuk setelah diverifikasi Leader.",
            color=discord.Color.gold()
        )
        embed.set_footer(text="Only verified characters will receive DKP.")
        
        view = DKPCheckInButtonView(event_id, self.cog)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Event posted!", ephemeral=True)

class DKPCheckInButtonView(discord.ui.View):
    def __init__(self, event_id, cog):
        super().__init__(timeout=None)
        self.event_id = event_id
        self.cog = cog

    @discord.ui.button(label="✅ Check In", style=discord.ButtonStyle.success)
    async def checkin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        data = {
            'event_id': self.event_id,
            'discord_user_id': str(interaction.user.id)
        }
        
        result = await self.cog.api_request('POST', '/dkp/api/checkin/', data)
        
        if result.get('success'):
            status = result.get('status', 'Pending')
            char_name = result.get('character', 'Unknown')
            
            if result.get('already_checked_in'):
                 msg = f"⚠️ **{char_name}** sudah check-in sebelumnya! (Poin tidak bertambah)"
            elif status == 'Verified':
                msg = f"✅ **{char_name}** sudah terverifikasi!"
            else:
                msg = f"⏳ **{char_name}** berhasil absen!\nStatus: **Pending Verification** (Menunggu Admin)."
                
            await interaction.followup.send(msg, ephemeral=True)
        elif result.get('error') == 'Discord not linked':
            await interaction.followup.send("❌ Discord belum terhubung ke karakter website!", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Gagal: {result.get('error')}", ephemeral=True)


@bot.event
async def on_ready():
    print(f'✅ {bot.user} is now running!')
    print(f'📡 API URL: {API_BASE_URL}')
    
    # Sync slash commands
    try:
        alto_cog = AltoBot(bot)
        await bot.add_cog(alto_cog)
        
        # Sync Global Commands (Includes DKP Group inside AltoBot)
        synced = await bot.tree.sync()
        print(f'⚡ Synced {len(synced)} commands (AltoBot)')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')


def run_bot():
    """Run the Discord bot"""
    if DISCORD_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Please set DISCORD_BOT_TOKEN environment variable!")
        print("   Example: set DISCORD_BOT_TOKEN=your_token_here")
        return
    
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    run_bot()
