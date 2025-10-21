"""
Discord Presence Commands Module
Provides Discord command interfaces for Riot ID binding and presence management
"""

import discord
from discord.ext import commands
import json
import os
from datetime import datetime
from services.presence_manager import PresenceManager

class PresenceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_manager = PresenceManager()
        self.voice_log_channel = None  # 用于记录语音活动的频道
    
    @commands.command(name='register_riot')
    async def register_riot(self, ctx, riot_id: str):
        """
        Register a Riot ID for the current Discord user
        Usage: !register_riot YanwenWang#NA1
        """
        try:
            # Validate Riot ID format (basic validation)
            if '#' not in riot_id:
                await ctx.send("❌ Invalid Riot ID format. Please use: `Name#TAG` (e.g., YanwenWang#NA1)")
                return
            
            discord_id = str(ctx.author.id)
            
            # Check if user is already registered
            existing_binding = self.presence_manager.get_binding_by_discord(discord_id)
            if existing_binding:
                await ctx.send(f"❌ You are already registered with Riot ID: `{existing_binding['riot_id']}`\n"
                              f"Use `!unregister_riot` first to change your binding.")
                return
            
            # Check if Riot ID is already taken by another user
            existing_riot = self.presence_manager.get_binding_by_riot(riot_id)
            if existing_riot:
                await ctx.send(f"❌ Riot ID `{riot_id}` is already registered by another user.")
                return
            
            # Register the binding
            success = self.presence_manager.register_binding(discord_id, riot_id, "LOL")
            
            if success:
                await ctx.send(f"✅ Successfully registered Riot ID: `{riot_id}`\n"
                              f"🎮 Game: League of Legends\n"
                              f"📅 Registered: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                await ctx.send("❌ Failed to register Riot ID. Please try again.")
                
        except Exception as e:
            await ctx.send(f"❌ Error registering Riot ID: {str(e)}")
    
    @commands.command(name='unregister_riot')
    async def unregister_riot(self, ctx):
        """
        Unregister the current Discord user's Riot ID
        Usage: !unregister_riot
        """
        try:
            discord_id = str(ctx.author.id)
            
            # Check if user is registered
            existing_binding = self.presence_manager.get_binding_by_discord(discord_id)
            if not existing_binding:
                await ctx.send("❌ You are not currently registered with any Riot ID.")
                return
            
            # Unregister the binding
            success = self.presence_manager.unregister_binding(discord_id)
            
            if success:
                await ctx.send("✅ Successfully unregistered your Riot ID.")
            else:
                await ctx.send("❌ Failed to unregister Riot ID. Please try again.")
                
        except Exception as e:
            await ctx.send(f"❌ Error unregistering Riot ID: {str(e)}")
    
    @commands.command(name='check_presence')
    async def check_presence(self, ctx, riot_id: str = None):
        """
        Check Discord presence status for a Riot ID
        Usage: !check_presence [RiotID] or !check_presence (checks your own)
        """
        try:
            if riot_id:
                # Check specific Riot ID
                presence = self.presence_manager.check_discord_presence(riot_id, self.bot)
            else:
                # Check current user's Riot ID
                discord_id = str(ctx.author.id)
                binding = self.presence_manager.get_binding_by_discord(discord_id)
                if not binding:
                    await ctx.send("❌ You are not registered with any Riot ID.\n"
                                  f"Use `!register_riot <RiotName#TAG>` to register.")
                    return
                presence = self.presence_manager.check_discord_presence(binding['riot_id'], self.bot)
            
            if not presence:
                await ctx.send(f"❌ Riot ID `{riot_id}` is not registered.")
                return
            
            # Create status message
            status_emoji = "🟢" if presence['is_online'] else "🔴"
            voice_emoji = "🎤" if presence['in_voice'] else "🔇"
            
            status_msg = f"**{status_emoji} Discord Status for `{presence['riot_id']}`**\n"
            status_msg += f"🟢 Online: {'Yes' if presence['is_online'] else 'No'}\n"
            status_msg += f"{voice_emoji} In Voice: {'Yes' if presence['in_voice'] else 'No'}\n"
            
            if presence['in_voice']:
                status_msg += f"🎵 Voice Channel: `{presence['voice_channel']}`\n"
                status_msg += f"🏠 Server: `{presence['guild_name']}`\n"
            elif presence['is_online']:
                status_msg += f"🏠 Server: `{presence['guild_name']}`\n"
            
            await ctx.send(status_msg)
                
        except Exception as e:
            await ctx.send(f"❌ Error checking presence: {str(e)}")
    
    @commands.command(name='online_players')
    async def online_players(self, ctx):
        """
        Show all online players with their presence status
        Usage: !online_players
        """
        try:
            online_players = self.presence_manager.get_online_players(self.bot)
            
            if not online_players:
                await ctx.send("📋 No online players found.")
                return
            
            # Create embed for better formatting
            embed = discord.Embed(
                title="🟢 Online Players",
                color=0x00ff00
            )
            
            for i, player in enumerate(online_players[:10], 1):  # Limit to 10 for readability
                voice_status = "🎤 In Voice" if player['in_voice'] else "🔇 Not in Voice"
                channel_info = f" in `{player['voice_channel']}`" if player['in_voice'] else ""
                
                embed.add_field(
                    name=f"{i}. {player['riot_id']}",
                    value=f"🏠 {player['guild_name']}\n{voice_status}{channel_info}",
                    inline=False
                )
            
            if len(online_players) > 10:
                embed.set_footer(text=f"Showing 10 of {len(online_players)} online players")
            
            await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"❌ Error getting online players: {str(e)}")
    
    @commands.command(name='voice_players')
    async def voice_players(self, ctx):
        """
        Show all players currently in voice channels
        Usage: !voice_players
        """
        try:
            voice_players = self.presence_manager.get_voice_players(self.bot)
            
            if not voice_players:
                await ctx.send("📋 No players in voice channels.")
                return
            
            # Create embed for better formatting
            embed = discord.Embed(
                title="🎤 Players in Voice Channels",
                color=0x0099ff
            )
            
            for i, player in enumerate(voice_players[:10], 1):  # Limit to 10 for readability
                embed.add_field(
                    name=f"{i}. {player['riot_id']}",
                    value=f"🏠 {player['guild_name']}\n🎵 `{player['voice_channel']}`",
                    inline=False
                )
            
            if len(voice_players) > 10:
                embed.set_footer(text=f"Showing 10 of {len(voice_players)} voice players")
            
            await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"❌ Error getting voice players: {str(e)}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        自动检测玩家进入/离开语音频道
        """
        try:
            # 检查这个用户是否已注册
            discord_id = str(member.id)
            binding = self.presence_manager.get_binding_by_discord(discord_id)
            
            if not binding:
                return  # 用户未注册，忽略
            
            riot_id = binding['riot_id']
            
            # 检测进入语音频道
            if before.channel is None and after.channel is not None:
                await self._notify_voice_join(member, riot_id, after.channel)
            
            # 检测离开语音频道
            elif before.channel is not None and after.channel is None:
                await self._notify_voice_leave(member, riot_id, before.channel)
            
            # 检测切换语音频道
            elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                await self._notify_voice_switch(member, riot_id, before.channel, after.channel)
                
        except Exception as e:
            print(f"Error in voice state update: {e}")
    
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """
        自动检测玩家在线状态变化
        """
        try:
            # 检查这个用户是否已注册
            discord_id = str(after.id)
            binding = self.presence_manager.get_binding_by_discord(discord_id)
            
            if not binding:
                return  # 用户未注册，忽略
            
            riot_id = binding['riot_id']
            
            # 检测从离线变为在线
            if (before.status in [discord.Status.offline, discord.Status.invisible] and 
                after.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]):
                await self._notify_status_online(after, riot_id)
            
            # 检测从在线变为离线
            elif (before.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd] and 
                  after.status in [discord.Status.offline, discord.Status.invisible]):
                await self._notify_status_offline(after, riot_id)
                
        except Exception as e:
            print(f"Error in presence update: {e}")
    
    async def _notify_voice_join(self, member, riot_id, channel):
        """通知玩家进入语音频道 - 只在红温时刻频道发送"""
        try:
            # 查找日志频道（只允许红温时刻频道）
            log_channel = await self._get_log_channel(member.guild)
            if log_channel and log_channel.name == "红温时刻":
                embed = discord.Embed(
                    title="🎤 玩家进入语音频道",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🎮 Riot ID", value=f"`{riot_id}`", inline=True)
                embed.add_field(name="👤 Discord用户", value=f"{member.mention}", inline=True)
                embed.add_field(name="🎵 语音频道", value=f"`{channel.name}`", inline=True)
                embed.add_field(name="🏠 服务器", value=f"`{member.guild.name}`", inline=True)
                
                await log_channel.send(embed=embed)
                print(f"✅ 通知已发送到红温时刻频道: {riot_id} 进入语音频道")
            else:
                print(f"⚠️ 跳过通知发送: 未找到红温时刻频道或频道不匹配")
            
            print(f"🎤 {riot_id} ({member.name}) 进入了语音频道: {channel.name}")
            
        except Exception as e:
            print(f"Error notifying voice join: {e}")
    
    async def _notify_voice_leave(self, member, riot_id, channel):
        """通知玩家离开语音频道 - 只在红温时刻频道发送"""
        try:
            # 查找日志频道（只允许红温时刻频道）
            log_channel = await self._get_log_channel(member.guild)
            if log_channel and log_channel.name == "红温时刻":
                embed = discord.Embed(
                    title="🔇 玩家离开语音频道",
                    color=0xff6600,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🎮 Riot ID", value=f"`{riot_id}`", inline=True)
                embed.add_field(name="👤 Discord用户", value=f"{member.mention}", inline=True)
                embed.add_field(name="🎵 语音频道", value=f"`{channel.name}`", inline=True)
                embed.add_field(name="🏠 服务器", value=f"`{member.guild.name}`", inline=True)
                
                await log_channel.send(embed=embed)
                print(f"✅ 通知已发送到红温时刻频道: {riot_id} 离开语音频道")
            else:
                print(f"⚠️ 跳过通知发送: 未找到红温时刻频道或频道不匹配")
            
            print(f"🔇 {riot_id} ({member.name}) 离开了语音频道: {channel.name}")
            
        except Exception as e:
            print(f"Error notifying voice leave: {e}")
    
    async def _notify_voice_switch(self, member, riot_id, old_channel, new_channel):
        """通知玩家切换语音频道 - 只在红温时刻频道发送"""
        try:
            # 查找日志频道（只允许红温时刻频道）
            log_channel = await self._get_log_channel(member.guild)
            if log_channel and log_channel.name == "红温时刻":
                embed = discord.Embed(
                    title="🔄 玩家切换语音频道",
                    color=0x0099ff,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🎮 Riot ID", value=f"`{riot_id}`", inline=True)
                embed.add_field(name="👤 Discord用户", value=f"{member.mention}", inline=True)
                embed.add_field(name="🎵 从", value=f"`{old_channel.name}`", inline=True)
                embed.add_field(name="🎵 到", value=f"`{new_channel.name}`", inline=True)
                embed.add_field(name="🏠 服务器", value=f"`{member.guild.name}`", inline=True)
                
                await log_channel.send(embed=embed)
                print(f"✅ 通知已发送到红温时刻频道: {riot_id} 切换语音频道")
            else:
                print(f"⚠️ 跳过通知发送: 未找到红温时刻频道或频道不匹配")
            
            print(f"🔄 {riot_id} ({member.name}) 从 {old_channel.name} 切换到 {new_channel.name}")
            
        except Exception as e:
            print(f"Error notifying voice switch: {e}")
    
    async def _notify_status_online(self, member, riot_id):
        """通知玩家上线 - 只在红温时刻频道发送"""
        try:
            # 查找日志频道（只允许红温时刻频道）
            log_channel = await self._get_log_channel(member.guild)
            if log_channel and log_channel.name == "红温时刻":
                embed = discord.Embed(
                    title="🟢 玩家上线",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🎮 Riot ID", value=f"`{riot_id}`", inline=True)
                embed.add_field(name="👤 Discord用户", value=f"{member.mention}", inline=True)
                embed.add_field(name="🏠 服务器", value=f"`{member.guild.name}`", inline=True)
                
                await log_channel.send(embed=embed)
                print(f"✅ 通知已发送到红温时刻频道: {riot_id} 上线")
            else:
                print(f"⚠️ 跳过通知发送: 未找到红温时刻频道或频道不匹配")
            
            print(f"🟢 {riot_id} ({member.name}) 上线了")
            
        except Exception as e:
            print(f"Error notifying status online: {e}")
    
    async def _notify_status_offline(self, member, riot_id):
        """通知玩家离线 - 只在红温时刻频道发送"""
        try:
            # 查找日志频道（只允许红温时刻频道）
            log_channel = await self._get_log_channel(member.guild)
            if log_channel and log_channel.name == "红温时刻":
                embed = discord.Embed(
                    title="🔴 玩家离线",
                    color=0xff0000,
                    timestamp=datetime.now()
                )
                embed.add_field(name="🎮 Riot ID", value=f"`{riot_id}`", inline=True)
                embed.add_field(name="👤 Discord用户", value=f"{member.mention}", inline=True)
                embed.add_field(name="🏠 服务器", value=f"`{member.guild.name}`", inline=True)
                
                await log_channel.send(embed=embed)
                print(f"✅ 通知已发送到红温时刻频道: {riot_id} 离线")
            else:
                print(f"⚠️ 跳过通知发送: 未找到红温时刻频道或频道不匹配")
            
            print(f"🔴 {riot_id} ({member.name}) 离线了")
            
        except Exception as e:
            print(f"Error notifying status offline: {e}")
    
    async def _get_log_channel(self, guild):
        """获取日志频道 - 只允许在红温时刻频道发送通知"""
        try:
            # 优先使用设置的日志频道
            if self.voice_log_channel:
                # 验证设置的频道是否为红温时刻
                if self.voice_log_channel.name == "红温时刻":
                    return self.voice_log_channel
                else:
                    print(f"⚠️ 设置的日志频道不是红温时刻，重新查找...")
                    self.voice_log_channel = None
            
            # 只查找名为 "红温时刻" 的频道
            for channel in guild.text_channels:
                if channel.name == "红温时刻":
                    print(f"✅ 找到红温时刻频道: {channel.name} ({channel.id})")
                    return channel
            
            # 如果没有找到红温时刻频道，返回 None（不发送通知）
            print(f"❌ 未找到红温时刻频道，跳过通知发送")
            return None
            
        except Exception as e:
            print(f"Error getting log channel: {e}")
            return None
    
    @commands.command(name='check_user_status')
    async def check_user_status(self, ctx, riot_id: str = None):
        """
        检查用户是否在 LOLBOT 的 Discord 服务器中
        Usage: !check_user_status [RiotID] or !check_user_status (检查自己)
        """
        try:
            if riot_id:
                # 检查特定 Riot ID
                binding = self.presence_manager.get_binding_by_riot(riot_id)
                if not binding:
                    await ctx.send(f"❌ Riot ID `{riot_id}` 未注册")
                    return
                discord_id = int(binding['discord_id'])
                target_riot_id = riot_id
            else:
                # 检查当前用户
                discord_id = ctx.author.id
                binding = self.presence_manager.get_binding_by_discord(str(discord_id))
                if not binding:
                    await ctx.send("❌ 你未注册任何 Riot ID")
                    return
                target_riot_id = binding['riot_id']
            
            # 检查用户是否在 LOLBOT 的服务器中
            user_found = False
            user_info = []
            
            for guild in self.bot.guilds:
                member = guild.get_member(discord_id)
                if member:
                    user_found = True
                    # 获取用户状态信息
                    is_online = member.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]
                    in_voice = member.voice is not None
                    voice_channel = member.voice.channel.name if member.voice else None
                    
                    user_info.append({
                        'guild_name': guild.name,
                        'guild_id': guild.id,
                        'is_online': is_online,
                        'in_voice': in_voice,
                        'voice_channel': voice_channel,
                        'member': member
                    })
            
            if not user_found:
                await ctx.send(f"❌ 用户 `{target_riot_id}` 不在 LOLBOT 的任何服务器中")
                return
            
            # 创建状态报告
            embed = discord.Embed(
                title=f"👤 用户状态报告: `{target_riot_id}`",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            
            for i, info in enumerate(user_info, 1):
                status_emoji = "🟢" if info['is_online'] else "🔴"
                voice_emoji = "🎤" if info['in_voice'] else "🔇"
                
                field_value = f"🏠 **服务器**: `{info['guild_name']}`\n"
                field_value += f"{status_emoji} **在线状态**: {'在线' if info['is_online'] else '离线'}\n"
                field_value += f"{voice_emoji} **语音状态**: {'在语音频道' if info['in_voice'] else '不在语音频道'}\n"
                
                if info['in_voice']:
                    field_value += f"🎵 **语音频道**: `{info['voice_channel']}`"
                
                embed.add_field(
                    name=f"服务器 {i}",
                    value=field_value,
                    inline=False
                )
            
            embed.set_footer(text=f"Discord ID: {discord_id}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error checking user status: {str(e)}")
    
    @commands.command(name='show_data_location')
    async def show_data_location(self, ctx):
        """
        显示用户数据存储位置
        Usage: !show_data_location
        """
        try:
            embed = discord.Embed(
                title="📁 用户数据存储信息",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            
            # 显示数据文件路径
            data_path = self.presence_manager.data_path
            embed.add_field(
                name="📄 数据文件路径",
                value=f"`{data_path}`",
                inline=False
            )
            
            # 显示当前注册用户数量
            bindings = self.presence_manager.get_all_active_bindings()
            embed.add_field(
                name="👥 注册用户数量",
                value=f"`{len(bindings)}` 人",
                inline=True
            )
            
            # 显示数据文件大小
            import os
            if os.path.exists(data_path):
                file_size = os.path.getsize(data_path)
                embed.add_field(
                    name="💾 文件大小",
                    value=f"`{file_size} bytes`",
                    inline=True
                )
            else:
                embed.add_field(
                    name="💾 文件状态",
                    value="`文件不存在`",
                    inline=True
                )
            
            # 显示数据格式说明
            embed.add_field(
                name="📋 数据格式",
                value="```json\n{\n  \"players\": [\n    {\n      \"discord_id\": \"用户Discord ID\",\n      \"riot_id\": \"游戏ID#标签\",\n      \"game\": \"游戏类型\",\n      \"registered_at\": \"注册时间\",\n      \"last_match_id\": \"最后比赛ID\"\n    }\n  ]\n}```",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Error showing data location: {str(e)}")

def setup(bot):
    bot.add_cog(PresenceCommands(bot))
