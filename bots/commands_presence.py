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
        自动检测玩家进入/离开语音频道并启动/停止游戏监控
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
                # 启动游戏监控
                await self._start_game_monitoring(member, after.channel)
            
            # 检测离开语音频道
            elif before.channel is not None and after.channel is None:
                await self._notify_voice_leave(member, riot_id, before.channel)
                # 停止游戏监控
                await self._stop_game_monitoring(member)
            
            # 检测切换语音频道
            elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                await self._notify_voice_switch(member, riot_id, before.channel, after.channel)
                # 重启游戏监控（新频道）
                await self._restart_game_monitoring(member, after.channel)
                
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
    
    @commands.command(name='start_monitoring')
    async def start_monitoring(self, ctx):
        """
        手动启动游戏监控
        Usage: !start_monitoring
        """
        try:
            # 检查用户是否在语音频道中
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send("❌ 请先加入语音频道再使用此命令")
                return
            
            voice_channel = ctx.author.voice.channel
            
            # 启动监控
            from services.game_monitor import monitor_manager
            success = await monitor_manager.start_monitoring_for_user(ctx.author, voice_channel)
            
            if success:
                await ctx.send("✅ **游戏监控已启动**！正在监控你的游戏状态...")
            else:
                await ctx.send("❌ **启动监控失败**，请确保已注册Riot ID")
                
        except Exception as e:
            await ctx.send(f"❌ **启动监控失败**: {str(e)}")
    
    @commands.command(name='stop_monitoring')
    async def stop_monitoring(self, ctx):
        """
        手动停止游戏监控
        Usage: !stop_monitoring
        """
        try:
            # 停止监控
            from services.game_monitor import monitor_manager
            success = await monitor_manager.stop_monitoring_for_user(ctx.author)
            
            if success:
                await ctx.send("✅ **游戏监控已停止**！")
            else:
                await ctx.send("❌ **停止监控失败**，你可能没有正在运行的监控")
                
        except Exception as e:
            await ctx.send(f"❌ **停止监控失败**: {str(e)}")
    
    @commands.command(name='monitoring_status')
    async def monitoring_status(self, ctx):
        """
        查看当前监控状态
        Usage: !monitoring_status
        """
        try:
            from services.game_monitor import monitor_manager
            status = monitor_manager.get_monitoring_status()
            
            embed = discord.Embed(
                title="🎮 游戏监控状态",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="📊 活跃监控数量",
                value=f"`{status['active_count']}` 个",
                inline=True
            )
            
            if status['monitors']:
                monitor_list = []
                for i, monitor in enumerate(status['monitors'][:5], 1):  # 限制显示前5个
                    status_emoji = "🟢" if monitor['is_running'] else "🔴"
                    monitor_list.append(
                        f"{i}. {status_emoji} `{monitor['riot_id']}` "
                        f"({monitor['game_type']}) - {monitor['voice_channel']}"
                    )
                
                if len(status['monitors']) > 5:
                    monitor_list.append(f"... 还有 {len(status['monitors']) - 5} 个监控")
                
                embed.add_field(
                    name="🎮 活跃监控",
                    value="\n".join(monitor_list),
                    inline=False
                )
            else:
                embed.add_field(
                    name="🎮 活跃监控",
                    value="暂无活跃监控",
                    inline=False
                )
            
            await ctx.send(embed=embed)
                
        except Exception as e:
            await ctx.send(f"❌ **获取监控状态失败**: {str(e)}")
    
    @commands.command(name='stop_all_monitoring')
    async def stop_all_monitoring(self, ctx):
        """
        停止所有游戏监控（管理员命令）
        Usage: !stop_all_monitoring
        """
        try:
            # 检查权限（可选）
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ 此命令需要管理员权限")
                return
            
            from services.game_monitor import monitor_manager
            await monitor_manager.stop_all_monitoring()
            
            await ctx.send("✅ **所有游戏监控已停止**！")
                
        except Exception as e:
            await ctx.send(f"❌ **停止所有监控失败**: {str(e)}")
    
    @commands.command(name='user_status')
    async def user_status(self, ctx, riot_id: str = None):
        """
        查看用户的详细状态信息
        Usage: !user_status [RiotID] or !user_status (查看自己)
        """
        try:
            if riot_id:
                # 检查特定 Riot ID
                binding = self.presence_manager.get_binding_by_riot(riot_id)
                if not binding:
                    await ctx.send(f"❌ Riot ID `{riot_id}` 未注册")
                    return
                target_riot_id = riot_id
            else:
                # 检查当前用户
                discord_id = str(ctx.author.id)
                binding = self.presence_manager.get_binding_by_discord(discord_id)
                if not binding:
                    await ctx.send("❌ 你未注册任何 Riot ID")
                    return
                target_riot_id = binding['riot_id']
            
            # 创建状态报告
            embed = discord.Embed(
                title=f"👤 用户状态详情: `{target_riot_id}`",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            
            # 基本注册信息
            embed.add_field(
                name="📋 注册信息",
                value=f"🎮 **游戏类型**: {binding.get('game', 'LOL')}\n"
                      f"📅 **注册时间**: {binding.get('registered_at', 'Unknown')}\n"
                      f"🆔 **Discord ID**: {binding.get('discord_id', 'Unknown')}",
                inline=False
            )
            
            # 实时状态信息
            voice_status = "🎤 在语音频道" if binding.get('is_in_voice', False) else "🔇 不在语音频道"
            game_status = "🎮 在游戏中" if binding.get('is_in_game', False) else "⏸️ 未在游戏"
            active_match = binding.get('active_match', 'None')
            last_check = binding.get('last_check', 'Never')
            
            embed.add_field(
                name="🔄 实时状态",
                value=f"{voice_status}\n{game_status}\n"
                      f"🎯 **活跃比赛**: `{active_match}`\n"
                      f"⏰ **最后检查**: {last_check}",
                inline=False
            )
            
            # 历史信息
            last_match_id = binding.get('last_match_id', 'None')
            embed.add_field(
                name="📊 历史信息",
                value=f"🏆 **最后比赛ID**: `{last_match_id}`",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ **获取用户状态失败**: {str(e)}")
    
    @commands.command(name='maintenance_status')
    async def maintenance_status(self, ctx):
        """
        查看数据维护状态
        Usage: !maintenance_status
        """
        try:
            from services.data_maintenance import data_maintenance
            
            status = data_maintenance.get_maintenance_status()
            
            embed = discord.Embed(
                title="🔧 数据维护状态",
                color=0x0099ff,
                timestamp=datetime.now()
            )
            
            status_emoji = "🟢" if status['is_running'] else "🔴"
            embed.add_field(
                name="📊 维护状态",
                value=f"{status_emoji} {'运行中' if status['is_running'] else '已停止'}",
                inline=True
            )
            
            embed.add_field(
                name="⏱️ 检查间隔",
                value=f"`{status['interval_minutes']} 分钟`",
                inline=True
            )
            
            embed.add_field(
                name="🔄 下次检查",
                value=f"`{status['next_check_in']}`",
                inline=True
            )
            
            embed.add_field(
                name="💡 维护功能",
                value="• 清理过期状态数据\n• 检测异常状态\n• 数据完整性验证",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ **获取维护状态失败**: {str(e)}")
    
    @commands.command(name='start_maintenance')
    async def start_maintenance(self, ctx):
        """
        启动数据维护（管理员命令）
        Usage: !start_maintenance
        """
        try:
            # Check permissions
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ 此命令需要管理员权限")
                return
            
            from services.data_maintenance import data_maintenance
            await data_maintenance.start_maintenance()
            
            await ctx.send("✅ **数据维护已启动**！系统将每5分钟检查一次数据状态。")
            
        except Exception as e:
            await ctx.send(f"❌ **启动维护失败**: {str(e)}")
    
    @commands.command(name='stop_maintenance')
    async def stop_maintenance(self, ctx):
        """
        停止数据维护（管理员命令）
        Usage: !stop_maintenance
        """
        try:
            # Check permissions
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ 此命令需要管理员权限")
                return
            
            from services.data_maintenance import data_maintenance
            await data_maintenance.stop_maintenance()
            
            await ctx.send("✅ **数据维护已停止**！")
            
        except Exception as e:
            await ctx.send(f"❌ **停止维护失败**: {str(e)}")
    
    @commands.command(name='test_game_detection')
    async def test_game_detection(self, ctx, riot_id: str = None):
        """
        测试游戏检测功能
        Usage: !test_game_detection [RiotID] or !test_game_detection (测试自己)
        """
        try:
            if riot_id:
                target_riot_id = riot_id
            else:
                # 检查当前用户
                discord_id = str(ctx.author.id)
                binding = self.presence_manager.get_binding_by_discord(discord_id)
                if not binding:
                    await ctx.send("❌ 你未注册任何 Riot ID")
                    return
                target_riot_id = binding['riot_id']
            
            await ctx.send(f"🔍 **正在测试游戏检测**: `{target_riot_id}`")
            
            # 创建临时的 GameMonitor 来测试检测逻辑
            from services.game_monitor import GameMonitor
            
            # 创建模拟的 Discord 对象
            class MockDiscordUser:
                def __init__(self, name, id):
                    self.name = name
                    self.id = id
                    self.voice = None
            
            class MockVoiceChannel:
                def __init__(self, name, id):
                    self.name = name
                    self.id = id
            
            mock_user = MockDiscordUser("TestUser", 12345)
            mock_voice_channel = MockVoiceChannel("Test Voice", 67890)
            
            # 创建临时监控器
            monitor = GameMonitor(mock_user, target_riot_id, mock_voice_channel, "LOL")
            
            # 测试游戏检测
            active_match = await monitor._get_active_match()
            
            if active_match:
                await ctx.send(f"✅ **检测到活跃比赛**: `{active_match}`")
            else:
                await ctx.send("❌ **未检测到活跃比赛**")
                
            # 显示调试信息
            await ctx.send("📊 **检测详情**: 请查看控制台日志获取详细调试信息")
            
        except Exception as e:
            await ctx.send(f"❌ **测试游戏检测失败**: {str(e)}")
    
    @commands.command(name='force_check_game')
    async def force_check_game(self, ctx, riot_id: str = None):
        """
        强制检查用户游戏状态并更新数据库
        Usage: !force_check_game [RiotID] or !force_check_game (检查自己)
        """
        try:
            if riot_id:
                target_riot_id = riot_id
            else:
                # 检查当前用户
                discord_id = str(ctx.author.id)
                binding = self.presence_manager.get_binding_by_discord(discord_id)
                if not binding:
                    await ctx.send("❌ 你未注册任何 Riot ID")
                    return
                target_riot_id = binding['riot_id']
            
            await ctx.send(f"🔍 **强制检查游戏状态**: `{target_riot_id}`")
            
            # 解析 Riot ID
            if '#' not in target_riot_id:
                await ctx.send("❌ 无效的 Riot ID 格式")
                return
            
            game_name, tag_line = target_riot_id.split('#', 1)
            
            # 导入 Riot API 检查函数
            from services.riot_checker import get_summoner_info, get_recent_matches, get_match_details
            from datetime import datetime
            
            try:
                # 1. 获取召唤师信息
                await ctx.send("📡 正在获取召唤师信息...")
                summoner_info = get_summoner_info(game_name, tag_line)
                if not summoner_info:
                    await ctx.send("❌ 无法获取召唤师信息，请检查 Riot ID 是否正确")
                    return
                
                await ctx.send(f"✅ 召唤师信息: {summoner_info['summoner_name']} (等级 {summoner_info['summoner_level']})")
                
                # 2. 获取最近比赛
                await ctx.send("🎮 正在检查最近比赛...")
                recent_matches = get_recent_matches(summoner_info['puuid'], 1)
                if not recent_matches:
                    await ctx.send("❌ 未找到最近比赛")
                    return
                
                match_id = recent_matches[0]
                await ctx.send(f"📋 最近比赛ID: `{match_id}`")
                
                # 3. 获取比赛详情
                await ctx.send("🔍 正在分析比赛状态...")
                match_data = get_match_details(match_id)
                if not match_data:
                    await ctx.send("❌ 无法获取比赛详情")
                    return
                
                # 4. 分析比赛状态
                game_duration = match_data['info']['gameDuration']
                game_creation = match_data['info']['gameCreation']
                current_time = datetime.now().timestamp() * 1000
                time_since_creation = current_time - game_creation
                
                # 判断比赛是否活跃
                is_recent = time_since_creation < 600000  # 10分钟
                is_short_duration = game_duration < 600  # 10分钟
                is_reasonable_duration = 60 <= game_duration <= 3600  # 1-60分钟
                
                # 创建状态报告
                embed = discord.Embed(
                    title=f"🎮 游戏状态检查: `{target_riot_id}`",
                    color=0x0099ff,
                    timestamp=datetime.now()
                )
                
                embed.add_field(
                    name="📊 比赛信息",
                    value=f"**比赛ID**: `{match_id}`\n"
                          f"**游戏时长**: {game_duration} 秒 ({game_duration/60:.1f} 分钟)\n"
                          f"**开始时间**: {datetime.fromtimestamp(game_creation/1000).strftime('%Y-%m-%d %H:%M:%S')}\n"
                          f"**距离开始**: {time_since_creation/1000/60:.1f} 分钟前",
                    inline=False
                )
                
                # 判断比赛状态
                if is_recent and (is_short_duration or is_reasonable_duration):
                    embed.color = 0x00ff00  # 绿色 - 活跃
                    embed.add_field(
                        name="🎯 检测结果",
                        value="✅ **比赛正在进行中**\n"
                              f"🟢 最近开始: {is_recent}\n"
                              f"🟢 合理时长: {is_short_duration or is_reasonable_duration}",
                        inline=False
                    )
                    
                    # 更新数据库状态
                    self.presence_manager.update_user_status(
                        riot_id=target_riot_id,
                        is_in_voice=True,  # 假设在语音频道
                        is_in_game=True,
                        active_match=match_id,
                        last_check=datetime.now().isoformat()
                    )
                    
                    await ctx.send("✅ **状态已更新**: 用户正在游戏中")
                    
                else:
                    embed.color = 0xff6600  # 橙色 - 可能结束
                    embed.add_field(
                        name="🎯 检测结果",
                        value="⚠️ **比赛可能已结束**\n"
                              f"🔴 最近开始: {is_recent}\n"
                              f"🔴 合理时长: {is_short_duration or is_reasonable_duration}",
                        inline=False
                    )
                    
                    # 更新数据库状态
                    self.presence_manager.update_user_status(
                        riot_id=target_riot_id,
                        is_in_voice=True,  # 假设在语音频道
                        is_in_game=False,
                        active_match=None,
                        last_check=datetime.now().isoformat()
                    )
                    
                    await ctx.send("⚠️ **状态已更新**: 用户不在游戏中")
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ **检查游戏状态失败**: {str(e)}")
                print(f"Error in force_check_game: {e}")
            
        except Exception as e:
            await ctx.send(f"❌ **强制检查失败**: {str(e)}")
    
    async def _start_game_monitoring(self, member, voice_channel):
        """启动游戏监控"""
        try:
            from services.game_monitor import monitor_manager
            success = await monitor_manager.start_monitoring_for_user(member, voice_channel)
            if success:
                print(f"✅ 游戏监控已启动: {member.name}")
            else:
                print(f"❌ 游戏监控启动失败: {member.name}")
        except Exception as e:
            print(f"❌ 启动游戏监控错误: {e}")
    
    async def _stop_game_monitoring(self, member):
        """停止游戏监控"""
        try:
            from services.game_monitor import monitor_manager
            success = await monitor_manager.stop_monitoring_for_user(member)
            if success:
                print(f"✅ 游戏监控已停止: {member.name}")
            else:
                print(f"❌ 游戏监控停止失败: {member.name}")
        except Exception as e:
            print(f"❌ 停止游戏监控错误: {e}")
    
    async def _restart_game_monitoring(self, member, new_voice_channel):
        """重启游戏监控（切换频道时）"""
        try:
            # 先停止旧的监控
            await self._stop_game_monitoring(member)
            # 启动新的监控
            await self._start_game_monitoring(member, new_voice_channel)
        except Exception as e:
            print(f"❌ 重启游戏监控错误: {e}")

def setup(bot):
    bot.add_cog(PresenceCommands(bot))
