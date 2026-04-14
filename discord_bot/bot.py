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
from datetime import datetime, timezone, timedelta
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
AUCTION_CHANNEL_ID = int(os.getenv('AUCTION_CHANNEL_ID', '1492512184209506344'))

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

    @tasks.loop(seconds=5)
    async def reminder_loop(self):
        try:
            # 1. PROCESS ALL PENDING ANNOUNCEMENTS
            while True:
                ann_result = await self.api_request('GET', '/portal/api/discord/announcements/') 
                
                if not ann_result.get('success') or not ann_result.get('has_new'):
                    break
                    
                channel = self.bot.get_channel(EVENTS_CHANNEL_ID)
                auction_channel = self.bot.get_channel(AUCTION_CHANNEL_ID)
                if not auction_channel:
                    try:
                        auction_channel = await self.bot.fetch_channel(AUCTION_CHANNEL_ID)
                        print(f"Fetched auction channel: {auction_channel} (type: {type(auction_channel).__name__})")
                    except Exception as e:
                        print(f"Failed to fetch auction channel {AUCTION_CHANNEL_ID}: {e}")
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
                    
                    # ===== AUCTION ANNOUNCEMENTS =====
                    elif msg_content.startswith('[AUCTION_START]'):
                        await self._handle_auction_start(msg_content, auction_channel)
                    elif msg_content.startswith('[AUCTION_END]'):
                        await self._handle_auction_end(msg_content, auction_channel)
                    elif msg_content.startswith('[AUCTION_CANCEL]'):
                        await self._handle_auction_cancel(msg_content, auction_channel)
                    elif msg_content.startswith('[AUCTION_NOBID]'):
                        await self._handle_auction_nobid(msg_content, auction_channel)
                    elif msg_content.startswith('[AUCTION_DELETE]'):
                        await self._handle_auction_delete(msg_content, auction_channel)
                            
                    # ===== EVENT ANNOUNCEMENTS =====
                    elif msg_content.startswith('[EVENT_COMPLETED]'):
                        clean_msg = msg_content.replace('[EVENT_COMPLETED]\n', '').strip()
                        
                        # Send to default events channel
                        if channel:
                            await channel.send(clean_msg)
                            print(f"Event completed sent to primary events channel.")
                            
                        # Send to specific requested channel
                        target_channel_id = 1489269074188963880
                        target_channel = self.bot.get_channel(target_channel_id)
                        if not target_channel:
                            try:
                                target_channel = await self.bot.fetch_channel(target_channel_id)
                            except Exception:
                                pass
                                
                        if target_channel:
                            await target_channel.send(clean_msg)
                            print(f"Event completed sent to secondary channel {target_channel_id}.")
                            
                    # Check if it's a simple notification
                    elif msg_content.startswith('[NOTIFICATION]'):
                        clean_msg = msg_content.replace('[NOTIFICATION]', '').strip()
                        await channel.send(clean_msg)
                        print(f"Notification sent: {clean_msg[:20]}...")
                    else:
                        # If message contains @everyone, send as plain content (embed won't ping)
                        if '@everyone' in msg_content:
                            await channel.send(msg_content)
                            print(f"Broadcast sent (@everyone): {msg_content[:30]}...")
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
            now = datetime.now(timezone(timedelta(hours=7)))  # WIB (GMT+7)
            current_day = now.weekday()
            current_time = now.strftime("%H:%M")
            
            for item in alarms:
                if item['day'] == current_day and item['time'] == current_time:
                    channel = self.bot.get_channel(EVENTS_CHANNEL_ID)
                    if channel:
                        await channel.send(item['msg'])
                        print(f"Sent reminder: {item['msg']}")
            
            # 4. Check for expired auctions (every cycle)
            try:
                expired_result = await self.api_request('GET', '/dkp/api/auction/check-expired/')
                if expired_result.get('success'):
                    for closed in expired_result.get('closed_auctions', []):
                        print(f"Auto-closed auction: {closed['title']}")
            except Exception as e:
                print(f"Error checking expired auctions: {e}")
                        
        except Exception as e:
            print(f"Error in reminder loop: {e}")
    
    # ===== AUCTION ANNOUNCEMENT HANDLERS =====
    
    async def _parse_auction_msg(self, msg):
        """Parse key:value pairs from auction announcement messages"""
        data = {}
        for line in msg.strip().split('\n'):
            if ':' in line and not line.startswith('['):
                key, _, val = line.partition(':')
                data[key.strip()] = val.strip()
        return data
        
    async def _find_auction_thread(self, channel, auction_id, thread_id=None):
        """Helper to find the forum thread for a specific auction ID"""
        
        # 1. Best case: We have the strict thread_id passed from Django
        if thread_id:
            try:
                thread = self.bot.get_channel(int(thread_id))
                if not thread:
                    thread = await channel.guild.fetch_channel(int(thread_id))
                return thread
            except Exception:
                pass
                
        # 2. Fallback for old/legacy ongoing auctions (or if thread_id is missing)
        if not hasattr(channel, 'threads'):
            return None
            
        target_marker = f"[ID:{auction_id}]"
        
        # Check active threads
        for thread in channel.threads:
            if target_marker in thread.name:
                return thread
                
        # Check archived threads just in case
        try:
            async for thread in channel.archived_threads(limit=50):
                if target_marker in thread.name:
                    return thread
        except Exception as e:
            print(f"Error checking archive: {e}")
            
        return None
    
    async def _handle_auction_start(self, msg, channel):
        if not channel:
            print(f"ERROR: Auction channel is None! AUCTION_CHANNEL_ID={AUCTION_CHANNEL_ID}")
            return
        data = await self._parse_auction_msg(msg)
        currency = data.get('CURRENCY', 'DKP')
        currency_icon = '💎' if currency == 'DIAMOND' else '💰'
        start_bid = int(data.get('START_BID', '0'))
        increment = int(data.get('INCREMENT', '10'))
        ends_str = data.get('ENDS', '?')
        
        embed = discord.Embed(
            title=f"🔨 {'[Diamond]' if currency == 'DIAMOND' else '[DKP]'} {data.get('TITLE', 'Unknown Item')}",
            color=discord.Color.blue() if currency == 'DIAMOND' else discord.Color.purple()
        )
        embed.add_field(name="🏷️ Status", value="🟢 **OPEN AUCTION**", inline=True)
        embed.add_field(name="👑 Leader", value="**—**", inline=True)
        embed.add_field(name=f"{currency_icon} Current Bid", value=f"**{start_bid} {currency}**", inline=True)
        embed.add_field(name="🛡️ Eligible", value=data.get('CLAN', 'All'), inline=True)
        embed.add_field(name="📈 Min Inc", value=f"+{increment}", inline=True)
        
        # Use Discord Native Timestamp for live countdown
        ends_ts = data.get('ENDS_TIMESTAMP')
        if ends_ts:
            embed.add_field(name="⏱️ Time Left", value=f"**End: <t:{ends_ts}:R>**", inline=True)
        else:
            embed.add_field(name="⏱️ Time Left", value=f"**Ends: {ends_str}**", inline=True)
        
        image_url = data.get('IMAGE', '')
        if image_url:
            embed.set_image(url=image_url)
        
        embed.set_footer(text=f"Start: {start_bid} {currency} | Inc: +{increment} | Use buttons below or /bid <amount>")
        
        # Create the bid view with buttons
        bid_view = AuctionBidView(
            auction_id=data.get('ID', '0'),
            min_increment=increment,
            current_bid=start_bid,
            currency=currency,
            cog=self
        )
        
        # Omit ID from thread name per user request
        thread_name = data.get('TITLE', 'Unknown Item')
        
        try:
            thread_id = None
            # If the channel is a ForumChannel, use create_thread to start a post
            if isinstance(channel, discord.ForumChannel):
                thread_with_message = await channel.create_thread(
                    name=thread_name,
                    content=f"@everyone 🔨 **{data.get('TITLE', 'Unknown Item')}**\n{data.get('DESC', '')}",
                    embed=embed,
                    view=bid_view,
                    auto_archive_duration=4320
                )
                thread_id = thread_with_message.thread.id
                
                # Send initial bid log message in the thread
                await thread_with_message.thread.send(
                    f"📜 **Bid Log & Winner will appear below** 👇\n"
                    f"@everyone **AUCTION OPEN!** Place your bid using the buttons above or `/bid <amount>`."
                )
            else:
                # Fallback for standard TextChannels: send msg, then create thread from it
                msg_obj = await channel.send(
                    f"@everyone 🔨 **{data.get('TITLE', 'Unknown Item')}**\n{data.get('DESC', '')}",
                    embed=embed,
                    view=bid_view
                )
                thread_obj = await msg_obj.create_thread(name=thread_name, auto_archive_duration=4320)
                thread_id = thread_obj.id
                
                # Send initial bid log message in the thread
                await thread_obj.send(
                    f"📜 **Bid Log & Winner will appear below** 👇\n"
                    f"@everyone **AUCTION OPEN!** Place your bid using the buttons above or `/bid <amount>`."
                )
                
            # Send the thread ID back to the Django API
            if thread_id and data.get('ID'):
                try:
                    await self.api_request('POST', '/dkp/api/auction/thread/', {
                        'auction_id': data.get('ID'),
                        'thread_id': str(thread_id)
                    })
                except Exception as ex:
                    print(f"Failed to record thread ID in API: {ex}")
                    
            print(f"Auction started (Thread): {thread_name}")
        except Exception as e:
            print(f"Failed to create auction thread: {e}")
            # Fallback: send to events channel instead
            try:
                fallback_ch = self.bot.get_channel(EVENTS_CHANNEL_ID)
                if fallback_ch:
                    await fallback_ch.send("@everyone 🔨 **AUCTION IS NOW LIVE!**\n*(Forum post failed)*", embed=embed)
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
            
    async def _handle_auction_end(self, msg, channel):
        if not channel:
            print(f"ERROR: Auction channel is None for AUCTION_END")
            return
        data = await self._parse_auction_msg(msg)
        currency = data.get('CURRENCY', 'DKP')
        currency_icon = '💎' if currency == 'DIAMOND' else '💰'
        
        winner_mention = ''
        discord_id = data.get('DISCORD_ID', '')
        if discord_id:
            winner_mention = f" (<@{discord_id}>)"
        
        deduct_msg = "DKP has been automatically deducted." if currency == 'DKP' else "Please collect the Diamond payment from the winner."
        
        embed = discord.Embed(
            title="🏆 AUCTION ENDED!",
            description=(
                f"**{data.get('TITLE', 'Unknown')}**\n\n"
                f"🎉 Winner: **{data.get('WINNER', '?')}**{winner_mention}\n"
                f"{currency_icon} Winning Bid: **{data.get('AMOUNT', '?')} {currency}**\n\n"
                f"{deduct_msg}"
            ),
            color=discord.Color.blue() if currency == 'DIAMOND' else discord.Color.gold()
        )
        embed.set_footer(text="Congratulations to the winner!")
        
        thread = await self._find_auction_thread(channel, data.get('ID', '?'), data.get('THREAD_ID'))
        if thread:
            await thread.send("@everyone 🏆 **AUCTION CLOSED!**", embed=embed)
            try:
                await thread.edit(archived=True, locked=True)
            except Exception:
                pass
        else:
            # Fallback to events channel
            try:
                fallback_ch = self.bot.get_channel(EVENTS_CHANNEL_ID)
                if fallback_ch:
                    await fallback_ch.send("@everyone 🏆 **AUCTION CLOSED!**", embed=embed)
            except Exception:
                pass
            
        print(f"Auction ended: {data.get('TITLE')} -> Winner: {data.get('WINNER')}")
    
    async def _handle_auction_cancel(self, msg, channel):
        if not channel:
            print(f"ERROR: Auction channel is None for AUCTION_CANCEL")
            return
        data = await self._parse_auction_msg(msg)
        
        embed = discord.Embed(
            title="❌ AUCTION CANCELLED",
            description=(
                f"**{data.get('TITLE', 'Unknown')}**\n\n"
                f"This auction has been cancelled by an admin.\n"
                f"All held DKP has been released."
            ),
            color=discord.Color.red()
        )
        
        thread = await self._find_auction_thread(channel, data.get('ID', '?'), data.get('THREAD_ID'))
        if thread:
            await thread.send(embed=embed)
            try:
                await thread.edit(archived=True, locked=True)
            except Exception:
                pass
        else:
            try:
                fallback_ch = self.bot.get_channel(EVENTS_CHANNEL_ID)
                if fallback_ch:
                    await fallback_ch.send(embed=embed)
            except Exception:
                pass
            
        print(f"Auction cancelled: {data.get('TITLE')}")
    
    async def _handle_auction_nobid(self, msg, channel):
        if not channel:
            print(f"ERROR: Auction channel is None for AUCTION_NOBID")
            return
        data = await self._parse_auction_msg(msg)
        
        embed = discord.Embed(
            title="⏰ AUCTION ENDED - No Bids",
            description=(
                f"**{data.get('TITLE', 'Unknown')}**\n\n"
                f"This auction ended with no bids."
            ),
            color=discord.Color.light_grey()
        )
        
        thread = await self._find_auction_thread(channel, data.get('ID', '?'), data.get('THREAD_ID'))
        if thread:
            await thread.send(embed=embed)
            try:
                await thread.edit(archived=True, locked=True)
            except Exception:
                pass
        else:
            try:
                fallback_ch = self.bot.get_channel(EVENTS_CHANNEL_ID)
                if fallback_ch:
                    await fallback_ch.send(embed=embed)
            except Exception:
                pass
            
        print(f"Auction ended (no bids): {data.get('TITLE')}")

    async def _handle_auction_delete(self, msg, channel):
        if not channel:
            return
        data = await self._parse_auction_msg(msg)
        
        thread = await self._find_auction_thread(channel, data.get('ID', '?'), data.get('THREAD_ID'))
        if thread:
            try:
                await thread.delete()
                print(f"Auction deleted (thread removed): {data.get('TITLE')}")
            except Exception as e:
                print(f"Failed to delete auction thread: {e}")

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
            await interaction.followup.send("Select an event to post:", view=view)
        else:
            await interaction.followup.send("❌ No active events on the website. Please create an event on the website first.", ephemeral=True)


    

    
    @app_commands.command(name="event_result", description="Complete an event and record results")
    @app_commands.describe(
        event_id="The Event ID to complete",
        win="Did the guild win?",
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
        """Complete an event and record results (Officers only)"""
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
                title="🏆 EVENT COMPLETED!",
                description=f"Event `{event_id}` has been completed.",
                color=discord.Color.gold()
            )
            embed.add_field(name="Status", value="🔴 COMPLETED - Check-in closed", inline=False)
            embed.add_field(name="Max Points", value=f"{result['max_points']} pts", inline=True)
            embed.add_field(name="Participants", value=f"{result['participants']} players", inline=True)
            
            if win_valkyrie or win_valhalla or (not win and event_id.lower().startswith(('br_', 'cat_', 'ds_'))):
                vk_result = "✅ WIN" if win_valkyrie else "❌ LOSE"
                vh_result = "✅ WIN" if win_valhalla else "❌ LOSE"
                embed.add_field(name="Valkyrie", value=vk_result, inline=True)
                embed.add_field(name="Valhalla", value=vh_result, inline=True)
            else:
                embed.add_field(name="Result", value="✅ WIN" if win else "❌ LOSE", inline=True)
                
            embed.set_footer(text="Points have been calculated and added to the leaderboard!")
            await interaction.followup.send("@everyone 📢 **The event has ended!**", embed=embed)
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
                description=f"Clan: **{result.get('clan', '-')}**",
                color=discord.Color.blue()
            )
            embed.add_field(name="🎯 Total Score", value=f"**{result['total_score']}** pts", inline=True)
            embed.add_field(name="🌟 Tier", value=result['tier'], inline=True)
            embed.add_field(name="📅 Attendance", value=result['attendance'], inline=True)
            embed.add_field(name="⚔️ Events Joined", value=f"{result['events_joined']}/{result['total_events']}", inline=True)
            embed.add_field(name="🔥 Win Streak", value=f"{result.get('current_streak', 0)}x", inline=True)
            embed.add_field(name="🏅 Streak Bonus", value=f"+{result.get('total_streak_bonus', 0)} pts", inline=True)
            embed.add_field(name="⭐ AP Points", value=f"{result.get('ap_points', 0)} pts", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif result.get('error') == 'Discord not linked to any Character':
            await interaction.followup.send(
                "❌ **Discord not linked!**\nPlease link your Discord in website profile first.",
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
            
            if 'leaderboards_by_clan' in result:
                for clan_name, clan_board in result['leaderboards_by_clan'].items():
                    if clan_board:
                        chunked_text = ""
                        part_num = 1
                        for entry in clan_board:
                            rank = entry['rank']
                            if rank == 1:
                                medal = "🥇"
                            elif rank == 2:
                                medal = "🥈"
                            elif rank == 3:
                                medal = "🥉"
                            else:
                                medal = f"#{rank}"
                            
                            line = f"{medal} **{entry['player']}** - {entry['score']} pts ({entry['tier']})\n"
                            if len(chunked_text) + len(line) > 1020:
                                name_suffix = f" (Part {part_num})" if part_num > 1 else ""
                                embed.add_field(name=f"🛡️ Clan {clan_name}{name_suffix}", value=chunked_text, inline=False)
                                chunked_text = line
                                part_num += 1
                            else:
                                chunked_text += line
                        
                        if chunked_text:
                            name_suffix = f" (Part {part_num})" if part_num > 1 else ""
                            embed.add_field(name=f"🛡️ Clan {clan_name}{name_suffix}", value=chunked_text, inline=False)
                
                if len(embed.fields) == 0:
                    embed.description = "No activity data yet this month."
            elif result.get('leaderboard'):
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
            
            embed.set_footer(text="Use /event_myscore to see your stats!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error', 'Unknown error')}")


    # ==========================================
    # DKP SYSTEM COMMANDS (GROUP /dkp)
    # ==========================================
    
    dkp_group = app_commands.Group(name="dkp", description="Dragon Kill Points System")





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
                "❌ **Discord not linked!**\nPlease link your Discord in website profile first.",
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
            await interaction.followup.send("Select a DKP Event to post:", view=view)
        else:
            await interaction.followup.send("❌ No active DKP events.", ephemeral=True)

    @dkp_group.command(name="leaderboard", description="Top DKP Holders")
    async def dkp_leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = await self.api_request('GET', '/dkp/api/leaderboard/')
        
        if result.get('success'):
            messages_to_send = []
            msg = "🏆 **DKP Leaderboard** 🏆\n"
            if 'leaderboards_by_clan' in result:
                for clan_name, clan_board in result['leaderboards_by_clan'].items():
                    if clan_board:
                        header = f"\n🛡️ **Clan {clan_name}**\n```\n"
                        current_chunk = msg + header if msg else header
                        msg = ""
                        for p in clan_board:
                            line = f"{p['rank']:2}. {p['character']:<15} {p['dkp']} DKP\n"
                            if len(current_chunk) + len(line) > 1900:
                                current_chunk += "```\n"
                                messages_to_send.append(current_chunk)
                                current_chunk = f"🛡️ **Clan {clan_name} (Cont.)**\n```\n" + line
                            else:
                                current_chunk += line
                        current_chunk += "```\n"
                        messages_to_send.append(current_chunk)
            elif result.get('leaderboard'):
                current_chunk = msg + "```\n"
                msg = ""
                for p in result['leaderboard']:
                    line = f"{p['rank']:2}. {p['character']:<15} {p['dkp']} DKP\n"
                    if len(current_chunk) + len(line) > 1900:
                        current_chunk += "```\n"
                        messages_to_send.append(current_chunk)
                        current_chunk = "```\n" + line
                    else:
                        current_chunk += line
                current_chunk += "```\n"
                messages_to_send.append(current_chunk)
            else:
                messages_to_send.append(msg + "\nNo DKP data available.")
                
            for m in messages_to_send:
                await interaction.followup.send(m)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error')}")

    # ==========================================
    # AUCTION COMMANDS
    # ==========================================

    @app_commands.command(name="bid", description="Place a bid on an active auction")
    @app_commands.describe(
        amount="Your bid amount in DKP",
        auction_id="The Auction ID (optional if bidding inside the item's thread)"
    )
    async def auction_bid(self, interaction: discord.Interaction, amount: int, auction_id: int = None):
        """Place a bid on an active auction"""
        
        # Determine the parent channel ID robustly
        parent_id = None
        if hasattr(interaction.channel, 'parent_id'):
            parent_id = interaction.channel.parent_id
        else:
            try:
                # Try fetching the channel if it's a partial object without parent_id
                ch = await interaction.guild.fetch_channel(interaction.channel_id)
                if hasattr(ch, 'parent_id'):
                    parent_id = ch.parent_id
            except Exception:
                pass
                
        is_in_auction_channel = (interaction.channel_id == AUCTION_CHANNEL_ID)
        is_in_auction_thread = (parent_id == AUCTION_CHANNEL_ID)
        
        # If auction_id is not provided, try to extract it from the thread name
        if auction_id is None:
            if not is_in_auction_thread:
                await interaction.response.send_message("❌ Please specify an `auction_id` if you are not bidding inside the item's thread.", ephemeral=True)
                return

        # Only allow in auction channel or its threads
        if AUCTION_CHANNEL_ID and not (is_in_auction_channel or is_in_auction_thread):
            await interaction.response.send_message(
                f"❌ Bidding is only allowed in <#{AUCTION_CHANNEL_ID}>!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Build API payload
        api_data = {
            'discord_id': str(interaction.user.id),
            'bid_amount': amount
        }
        
        if auction_id is not None:
            api_data['auction_id'] = auction_id
        elif is_in_auction_thread:
            api_data['thread_id'] = str(interaction.channel_id)
            
        result = await self.api_request('POST', '/dkp/api/auction/bid/', api_data)
        
        if result.get('success'):
            cur = result.get('currency', 'DKP')
            cur_icon = '💎' if cur == 'DIAMOND' else '💰'
            
            await interaction.followup.send(
                f"✅ You bid **{result['bid_amount']} {cur}** on **{result.get('auction_title', '')}** successfully!",
                ephemeral=True
            )
            
            # Also update the bid log in the thread
            try:
                thread = interaction.channel
                log_msg = None
                async for m in thread.history(oldest_first=True, limit=10):
                    if m.author.id == interaction.client.user.id and "📜 Bid Log" in m.content:
                        log_msg = m
                        break
                
                bidder_mention = f"<@{interaction.user.id}>"
                time_left = result.get('time_remaining', '')
                new_log_line = f"{bidder_mention} placed bid: **{result['bid_amount']} {cur}** ⏱️ {time_left}"
                
                if log_msg:
                    updated_content = log_msg.content + f"\n{new_log_line}"
                    if len(updated_content) > 1900:
                        await thread.send(f"📜 **Bid Log (continued)**\n{new_log_line}")
                    else:
                        await log_msg.edit(content=updated_content)
                else:
                    # Create the log message if it doesn't exist
                    await thread.send(
                        f"📜 **Bid Log & Winner will appear below** 👇\n"
                        f"@everyone **AUCTION OPEN!** Place your bid above.\n\n"
                        f"{new_log_line}"
                    )
            except Exception as e:
                print(f"Error updating bid log from /bid command: {e}")
            
            # Also update the auction embed (Current Bid, Leader, Time Left)
            try:
                thread = interaction.channel
                async for msg in thread.history(oldest_first=True, limit=5):
                    if msg.author.id == interaction.client.user.id and msg.embeds and msg.components:
                        old_embed = msg.embeds[0]
                        new_embed = discord.Embed(
                            title=old_embed.title,
                            color=old_embed.color
                        )
                        
                        for field in old_embed.fields:
                            if field.name and 'Current Bid' in field.name:
                                new_embed.add_field(
                                    name=f"{cur_icon} Current Bid",
                                    value=f"**{result['current_bid']} {cur}**",
                                    inline=True
                                )
                            elif field.name and 'Leader' in field.name:
                                new_embed.add_field(
                                    name="👑 Leader",
                                    value=f"**{result['character_name']}**",
                                    inline=True
                                )
                            elif field.name and 'Time Left' in field.name:
                                ends_ts = result.get('ends_at_timestamp')
                                if ends_ts:
                                    time_value = f"**End: <t:{ends_ts}:R>**"
                                else:
                                    time_value = field.value
                                new_embed.add_field(
                                    name="⏱️ Time Left",
                                    value=time_value,
                                    inline=True
                                )
                            else:
                                new_embed.add_field(
                                    name=field.name,
                                    value=field.value,
                                    inline=field.inline
                                )
                        
                        if old_embed.image:
                            new_embed.set_image(url=old_embed.image.url)
                        if old_embed.footer:
                            new_embed.set_footer(text=old_embed.footer.text)
                        
                        await msg.edit(embed=new_embed)
                        break
            except Exception as e:
                print(f"Error updating auction embed from /bid command: {e}")
        else:
            await interaction.followup.send(
                f"❌ {result.get('error', 'Bid failed')}",
                ephemeral=True
            )

    @app_commands.command(name="auction_list", description="View all active auctions")
    async def auction_list(self, interaction: discord.Interaction):
        """List all active auctions"""
        await interaction.response.defer(ephemeral=True)
        
        result = await self.api_request('GET', '/dkp/api/auction/active/')
        
        if result.get('success'):
            auctions = result.get('auctions', [])
            if not auctions:
                await interaction.followup.send("📭 No active auctions right now.", ephemeral=True)
                return
            
            embed = discord.Embed(
                title="🔨 Active Auctions",
                color=discord.Color.purple()
            )
            
            for a in auctions:
                embed.add_field(
                    name=f"#{a['id']} - {a['title']}",
                    value=(
                        f"💰 Current: **{a['current_bid']} DKP** (+{a['min_increment']})\n"
                        f"👤 Leader: **{a['current_leader']}**\n"
                        f"⏱️ Ends in: **{a['time_remaining']}**\n"
                        f"🛡️ Eligible: {a['clan']} | 📊 {a['total_bids']} bid(s)"
                    ),
                    inline=False
                )
            
            embed.set_footer(text="Use /bid <auction_id> <amount> to place a bid!")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Error: {result.get('error')}", ephemeral=True)


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
            title=f"{type_emoji} EVENT CREATED!",
            description=f"**{event_name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Event ID", value=f"`{event_id}`", inline=True)
        embed.add_field(name="Type", value=event_type.replace('_', ' '), inline=True)
        embed.add_field(name="Status", value="🟢 ACTIVE - Check-in open!", inline=False)
        embed.set_footer(text="⬇️ Click the Check In button below to join!")
        
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
                    f"⚠️ **{result['character']}** already checked in! (No extra points)",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    f"✅ **{result['character']}** successfully checked in! (+{result['points']} pts)",
                    ephemeral=True
                )
        elif result.get('error') == 'Discord not linked':
            await interaction.followup.send(
                "❌ **Discord not linked!**\n\n"
                "Please link your Discord on the website first:\n"
                "1. Go to website → Character Profile\n"
                "2. Click **Link Discord** button\n"
                "3. Enter your Discord ID\n"
                "4. Try Check In again",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ {result.get('message', result.get('error', 'Check-in failed'))}",
                ephemeral=True
            )


# ==========================================
# AUCTION UI VIEWS (Bid Buttons + Custom Bid Modal)
# ==========================================

class AuctionBidView(discord.ui.View):
    """Persistent view with Bid (+increment) button and Custom Bid button"""
    def __init__(self, auction_id: str, min_increment: int, current_bid: int, currency: str, cog: AltoBot):
        super().__init__(timeout=None)
        self.auction_id = auction_id
        self.min_increment = min_increment
        self.current_bid = current_bid
        self.currency = currency
        self.cog = cog
        
        # Update button label dynamically
        cur_icon = '💎' if currency == 'DIAMOND' else '💰'
        self.bid_button.label = f"Bid (+{min_increment})"
        self.bid_button.emoji = cur_icon
    
    @discord.ui.button(label="Bid (+100)", style=discord.ButtonStyle.primary)
    async def bid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Quick bid: current_bid + min_increment"""
        await interaction.response.defer(ephemeral=True)
        
        # Calculate the next bid amount
        bid_amount = self.current_bid + self.min_increment
        if self.current_bid == 0:
            # No bids yet, use starting bid (which IS current_bid from auction start data)
            # The API will validate anyway
            bid_amount = self.current_bid + self.min_increment
        
        api_data = {
            'discord_id': str(interaction.user.id),
            'bid_amount': bid_amount,
            'thread_id': str(interaction.channel_id),
        }
        
        result = await self.cog.api_request('POST', '/dkp/api/auction/bid/', api_data)
        
        if result.get('success'):
            cur = result.get('currency', self.currency)
            cur_icon = '💎' if cur == 'DIAMOND' else '💰'
            
            # Update internal state for next click
            self.current_bid = result.get('current_bid', bid_amount)
            self.bid_button.label = f"Bid (+{self.min_increment})"
            self.bid_button.emoji = cur_icon
            
            # Update the embed message with new bid info
            await self._update_auction_embed(interaction, result)
            
            # Update the bid log message
            await self._append_bid_log(interaction, result)
            
            await interaction.followup.send(
                f"✅ You bid **{bid_amount} {cur}** successfully!",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ {result.get('error', 'Bid failed')}",
                ephemeral=True
            )
    
    @discord.ui.button(label="Custom Bid", style=discord.ButtonStyle.secondary, emoji="✏️")
    async def custom_bid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal for custom bid amount"""
        modal = CustomBidModal(self)
        await interaction.response.send_modal(modal)
    
    async def _update_auction_embed(self, interaction, result):
        """Update the original auction embed with new bid info"""
        try:
            # Find the original message with the embed (first message in thread)
            thread = interaction.channel
            cur = result.get('currency', self.currency)
            cur_icon = '💎' if cur == 'DIAMOND' else '💰'
            
            # Try to find the message with buttons (our message)
            async for msg in thread.history(oldest_first=True, limit=5):
                if msg.author.id == interaction.client.user.id and msg.components:
                    # Found the message with buttons - update the embed
                    if msg.embeds:
                        old_embed = msg.embeds[0]
                        new_embed = discord.Embed(
                            title=old_embed.title,
                            color=old_embed.color
                        )
                        
                        for field in old_embed.fields:
                            if field.name and 'Current Bid' in field.name:
                                new_embed.add_field(
                                    name=f"{cur_icon} Current Bid",
                                    value=f"**{result['current_bid']} {cur}**",
                                    inline=True
                                )
                            elif field.name and 'Leader' in field.name:
                                new_embed.add_field(
                                    name="👑 Leader",
                                    value=f"**{result['character_name']}**",
                                    inline=True
                                )
                            elif field.name and 'Time Left' in field.name:
                                # Use fresh timestamp from API if available (anti-snipe may have extended)
                                ends_ts = result.get('ends_at_timestamp')
                                if ends_ts:
                                    time_value = f"**End: <t:{ends_ts}:R>**"
                                else:
                                    time_value = field.value
                                new_embed.add_field(
                                    name="⏱️ Time Left",
                                    value=time_value,
                                    inline=True
                                )
                            else:
                                new_embed.add_field(
                                    name=field.name,
                                    value=field.value,
                                    inline=field.inline
                                )
                        
                        if old_embed.image:
                            new_embed.set_image(url=old_embed.image.url)
                        if old_embed.footer:
                            new_embed.set_footer(text=old_embed.footer.text)
                        
                        # Update bid button label
                        self.bid_button.label = f"Bid (+{self.min_increment})"
                        
                        await msg.edit(embed=new_embed, view=self)
                    break
        except Exception as e:
            print(f"Error updating auction embed: {e}")
    
    async def _append_bid_log(self, interaction, result):
        """Update the bid log message in the thread"""
        try:
            thread = interaction.channel
            cur = result.get('currency', self.currency)
            log_msg = None
            
            # Find the log message (contains "📜 Bid Log")
            async for msg in thread.history(oldest_first=True, limit=10):
                if msg.author.id == interaction.client.user.id and "📜 Bid Log" in msg.content:
                    log_msg = msg
                    break
            
            bidder_mention = f"<@{interaction.user.id}>"
            time_left = result.get('time_remaining', '')
            new_log_line = f"{bidder_mention} placed bid: **{result['bid_amount']} {cur}** ⏱️ {time_left}"
            
            if log_msg:
                updated_content = log_msg.content + f"\n{new_log_line}"
                # Discord message limit is 2000 chars
                if len(updated_content) > 1900:
                    # Start a new log message
                    await thread.send(f"📜 **Bid Log (continued)**\n{new_log_line}")
                else:
                    await log_msg.edit(content=updated_content)
            else:
                # Create the log message
                await thread.send(
                    f"📜 **Bid Log & Winner will appear below** 👇\n"
                    f"@everyone **AUCTION OPEN!** Place your bid above.\n\n"
                    f"{new_log_line}"
                )
        except Exception as e:
            print(f"Error updating bid log: {e}")


class CustomBidModal(discord.ui.Modal, title="Custom Bid"):
    """Modal for entering a custom bid amount"""
    amount = discord.ui.TextInput(
        label="Amount",
        placeholder="Enter your bid amount...",
        required=True,
        min_length=1,
        max_length=10,
    )
    
    def __init__(self, bid_view: AuctionBidView):
        super().__init__()
        self.bid_view = bid_view
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            bid_amount = int(self.amount.value)
        except ValueError:
            await interaction.followup.send("❌ Please enter a valid number.", ephemeral=True)
            return
        
        if bid_amount <= 0:
            await interaction.followup.send("❌ Bid amount must be greater than 0.", ephemeral=True)
            return
        
        api_data = {
            'discord_id': str(interaction.user.id),
            'bid_amount': bid_amount,
            'thread_id': str(interaction.channel_id),
        }
        
        result = await self.bid_view.cog.api_request('POST', '/dkp/api/auction/bid/', api_data)
        
        if result.get('success'):
            cur = result.get('currency', self.bid_view.currency)
            cur_icon = '💎' if cur == 'DIAMOND' else '💰'
            
            # Update internal state
            self.bid_view.current_bid = result.get('current_bid', bid_amount)
            self.bid_view.bid_button.label = f"Bid (+{self.bid_view.min_increment})"
            self.bid_view.bid_button.emoji = cur_icon
            
            # Update embed and log
            await self.bid_view._update_auction_embed(interaction, result)
            await self.bid_view._append_bid_log(interaction, result)
            
            await interaction.followup.send(
                f"✅ You bid **{bid_amount} {cur}** successfully!",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"❌ {result.get('error', 'Bid failed')}",
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
            description=f"**{name}**\n\nClick the button below to check in!\nPoints will be added after Leader verification.",
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
                 msg = f"⚠️ **{char_name}** already checked in! (No extra points)"
            elif status == 'Verified':
                msg = f"✅ **{char_name}** has been verified!"
            else:
                msg = f"⏳ **{char_name}** successfully checked in!\nStatus: **Pending Verification** (Awaiting Admin)."
                
            await interaction.followup.send(msg, ephemeral=True)
        elif result.get('error') == 'Discord not linked':
            await interaction.followup.send("❌ Discord not linked to any website character!", ephemeral=True)
        else:
            await interaction.followup.send(f"❌ Failed: {result.get('error')}", ephemeral=True)


@bot.event
async def on_ready():
    print(f'[OK] {bot.user} is now running!')
    print(f'[API] API URL: {API_BASE_URL}')
    print(f'[GUILDS] Connected to {len(bot.guilds)} server(s):')
    for g in bot.guilds:
        print(f'  - {g.name} (ID: {g.id})')
    
    # Sync slash commands
    try:
        alto_cog = AltoBot(bot)
        await bot.add_cog(alto_cog)
        
        synced = await bot.tree.sync()
        print(f'[SYNC] Synced {len(synced)} commands (Global)')
    except Exception as e:
        print(f'[ERROR] Error syncing commands: {e}')


def run_bot():
    """Run the Discord bot"""
    if DISCORD_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("[ERROR] Please set DISCORD_BOT_TOKEN environment variable!")
        print("   Example: set DISCORD_BOT_TOKEN=your_token_here")
        return
    
    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    run_bot()
