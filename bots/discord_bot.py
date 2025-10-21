#!/usr/bin/env python3
"""
Discord Bot 主入口
英雄联盟游戏数据分析完整工作流程
"""

import os
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands
import ffmpeg

# 添加services目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

# 导入服务模块
from services.riot_checker import main as get_match_data
from services.match_analyzer import convert_to_chinese_mature_tone, load_json_file
from services.voicv_tts import generate_tts_audio
from services.utils import find_latest_json_file, ensure_directory, cleanup_old_files, get_file_count_info

# 加载环境变量
load_dotenv()

def get_style_display_names():
    """动态生成风格显示名称映射"""
    from services.prompts import STYLE_CONFIGS
    
    # 基础映射
    base_mapping = {
        "default": "搞子风格",
        "kfk_dp": "专业风格", 
        "kfk": "专业风格",
        "azi": "Azi风格",
        "dingzhen": "丁震风格",
        "taffy": "Taffy风格"
    }
    
    # 为所有 STYLE_CONFIGS 中的风格生成显示名称
    result = {}
    for style_name in STYLE_CONFIGS.keys():
        if style_name in base_mapping:
            result[style_name] = base_mapping[style_name]
        else:
            # 如果新风格没有在基础映射中，使用风格名称本身
            result[style_name] = f"{style_name}风格"
    
    return result

# Discord Bot 配置
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# FFMPEG_PATH removed - now using ffmpeg-python

# 初始化Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


class LOLWorkflow:
    def __init__(self, ctx=None):
        self.current_match_file = None
        self.chinese_analysis = None
        self.audio_file = None
        self.voice_id = None  # 从风格配置中获取的voice_id
        self.ctx = ctx  # Discord context for sending status updates
        
    async def step1_get_match_data(self):
        """步骤1: 获取游戏数据"""
        print("步骤1: 获取最新游戏数据...")
        if self.ctx:
            await self.ctx.send("🔍 **步骤1**: 正在获取最新游戏数据...")
        
        try:
            # 运行riot_checker获取数据
            get_match_data()
            
            # 找到最新生成的JSON文件
            self.current_match_file = find_latest_json_file("analysis")
            if not self.current_match_file:
                raise FileNotFoundError("未找到游戏数据文件")
            
            print(f"游戏数据已保存: {self.current_match_file}")
            
            if self.ctx:
                await self.ctx.send("✅ **步骤1完成**: 游戏数据获取成功！")
            return True
            
        except Exception as e:
            print(f"获取游戏数据失败: {e}")
            if self.ctx:
                await self.ctx.send(f"❌ **步骤1失败**: 获取游戏数据失败 - {e}")
            return False
    
    async def step1_get_match_data_with_user(self, game_name, tag_line):
        """步骤1: 获取指定用户的游戏数据"""
        print(f"步骤1: 获取用户 {game_name}#{tag_line} 的最新游戏数据...")
        if self.ctx:
            await self.ctx.send(f"🔍 **步骤1**: 正在获取 {game_name}#{tag_line} 的最新游戏数据...")
        
        try:
            # 导入动态用户数据获取函数
            from services.riot_checker import get_match_data_for_user
            
            # 运行riot_checker获取指定用户的数据
            success = get_match_data_for_user(game_name, tag_line)
            if not success:
                raise Exception("获取用户游戏数据失败")
            
            # 找到最新生成的JSON文件
            self.current_match_file = find_latest_json_file("analysis")
            if not self.current_match_file:
                raise FileNotFoundError("未找到游戏数据文件")
            
            print(f"用户 {game_name}#{tag_line} 的游戏数据已保存: {self.current_match_file}")
            
            if self.ctx:
                await self.ctx.send("✅ **步骤1完成**: 游戏数据获取成功！")
            return True
            
        except Exception as e:
            print(f"获取用户游戏数据失败: {e}")
            if self.ctx:
                await self.ctx.send(f"❌ **步骤1失败**: 获取游戏数据失败 - {e}")
            return False
    
    async def step2_convert_to_chinese(self, prompt=None, system_role=None, style="default"):
        """步骤2: 转换为中文分析
        
        Args:
            prompt (str, optional): 自定义提示词，如果为None则使用风格提示词
            system_role (str, optional): 自定义系统角色，如果为None则使用风格角色
            style (str, optional): 风格名称 (default, professional, humorous)
        """
        print(f"步骤2: 生成中文分析... (风格: {style})")
        if self.ctx:
            await self.ctx.send(f"🤖 **步骤2**: 正在生成AI中文分析... (风格: {style})")
        
        try:
            if not self.current_match_file:
                raise ValueError("没有可用的游戏数据文件")
            
            # 加载JSON数据
            match_data = load_json_file(self.current_match_file)
            if not match_data:
                raise ValueError("无法加载游戏数据")
            
            # 转换为中文分析，获取分析文本和voice_id
            print(f"DEBUG: 调用convert_to_chinese_mature_tone，风格: {style}")
            result = convert_to_chinese_mature_tone(match_data, prompt, system_role, style)
            if not result or result[0] is None:
                raise ValueError("AI分析生成失败")
            
            self.chinese_analysis, self.voice_id = result
            
            print("[OK] 中文分析生成成功")
            print(f"📝 分析内容: {self.chinese_analysis[:100]}...")
            
            if self.ctx:
                await self.ctx.send("✅ **步骤2完成**: AI中文分析生成成功！")
            return True
            
        except Exception as e:
            print(f"[ERROR] 中文分析生成失败: {e}")
            if self.ctx:
                await self.ctx.send(f"❌ **步骤2失败**: 中文分析生成失败 - {e}")
            return False
    
    async def step3_generate_tts(self):
        """步骤3: 生成TTS音频"""
        print("步骤3: 生成语音文件...")
        if self.ctx:
            await self.ctx.send("🎵 **步骤3**: 正在生成语音文件...")
        
        try:
            if not self.chinese_analysis:
                raise ValueError("没有可用的中文分析内容")
            
            # 使用 voicV TTS API生成音频，传入voice_id
            self.audio_file = generate_tts_audio(self.chinese_analysis, voice_id=self.voice_id)
            if not self.audio_file:
                raise ValueError("TTS生成失败")
            
            print(f"[OK] 语音文件生成成功: {self.audio_file}")
            
            if self.ctx:
                await self.ctx.send("✅ **步骤3完成**: 语音文件生成成功！")
            return True
            
        except Exception as e:
            print(f"[ERROR] TTS生成失败: {e}")
            if self.ctx:
                await self.ctx.send(f"❌ **步骤3失败**: TTS生成失败 - {e}")
            return False
    
    async def step4_discord_play(self, voice_channel_id=None):
        """步骤4: Discord播放音频"""
        print("步骤4: Discord播放音频...")
        if self.ctx:
            await self.ctx.send("🔊 **步骤4**: 正在连接语音频道并播放音频...")
        
        try:
            if not self.audio_file or not os.path.exists(self.audio_file):
                raise ValueError("音频文件不存在")
            
            # 这里需要用户指定语音频道或从用户当前频道获取
            if not voice_channel_id:
                print("[ERROR] 需要指定语音频道ID")
                if self.ctx:
                    await self.ctx.send("❌ **步骤4失败**: 需要指定语音频道ID")
                return False
            
            # 连接语音频道
            voice_channel = bot.get_channel(voice_channel_id)
            if not voice_channel:
                raise ValueError("找不到指定的语音频道")
            
            vc = await voice_channel.connect()
            
            # 播放音频 - 使用ffmpeg-python自动查找ffmpeg
            audio_source = discord.FFmpegPCMAudio(self.audio_file)
            done = asyncio.Event()
            
            def after_play(err):
                done.set()
            
            vc.play(audio_source, after=after_play)
            print("🎵 正在播放游戏分析...")
            
            if self.ctx:
                await self.ctx.send("🎵 **正在播放**: 游戏分析音频...")
            
            await done.wait()
            
            # 播放完成后断开连接
            await asyncio.sleep(1)
            await vc.disconnect()
            print("[OK] 播放完成，已退出语音频道")
            
            if self.ctx:
                await self.ctx.send("✅ **步骤4完成**: 音频播放完成！")
            return True
            
        except Exception as e:
            print(f"[ERROR] Discord播放失败: {e}")
            if self.ctx:
                await self.ctx.send(f"❌ **步骤4失败**: Discord播放失败 - {e}")
            return False
    
    async def run_full_workflow(self, voice_channel_id=None, prompt=None, system_role=None, style="default"):
        """运行完整工作流程
        
        Args:
            voice_channel_id (int, optional): Discord语音频道ID
            prompt (str, optional): 自定义提示词
            system_role (str, optional): 自定义系统角色
            style (str, optional): 风格名称 (default, professional, humorous)
        """
        print("开始英雄联盟游戏分析完整流程")
        print("=" * 60)
        
        # 步骤1: 获取游戏数据
        if not await self.step1_get_match_data():
            return False
        
        # 步骤2: 转换为中文分析
        if not await self.step2_convert_to_chinese(prompt, system_role, style):
            return False
        
        # 步骤3: 生成TTS音频
        if not await self.step3_generate_tts():
            return False
        
        # 步骤4: Discord播放
        if voice_channel_id:
            if not await self.step4_discord_play(voice_channel_id):
                return False
        
        # 步骤5: 清理旧文件（只保留最近5次记录）
        print("🧹 清理旧文件...")
        cleanup_stats = cleanup_old_files(keep_count=5)
        if cleanup_stats['analysis'] > 0 or cleanup_stats['audio'] > 0:
            print(f"✅ 清理完成: 删除了 {cleanup_stats['analysis']} 个分析文件, {cleanup_stats['audio']} 个音频文件")
        
        print("🎉 完整流程执行成功!")
        return True
    
    async def run_full_workflow_with_user(self, voice_channel_id=None, game_name=None, tag_line=None, prompt=None, system_role=None, style="default"):
        """运行完整工作流程（支持动态用户）
        
        Args:
            voice_channel_id (int, optional): Discord语音频道ID
            game_name (str, optional): 游戏用户名
            tag_line (str, optional): 用户标签
            prompt (str, optional): 自定义提示词
            system_role (str, optional): 自定义系统角色
            style (str, optional): 风格名称 (default, professional, humorous)
        """
        print("开始英雄联盟游戏分析完整流程（动态用户）")
        print("=" * 60)
        
        # 步骤1: 获取游戏数据（使用动态用户）
        if not await self.step1_get_match_data_with_user(game_name, tag_line):
            return False
        
        # 步骤2: 转换为中文分析
        if not await self.step2_convert_to_chinese(prompt, system_role, style):
            return False
        
        # 步骤3: 生成TTS音频
        if not await self.step3_generate_tts():
            return False
        
        # 步骤4: Discord播放
        if voice_channel_id:
            if not await self.step4_discord_play(voice_channel_id):
                return False
        
        # 步骤5: 清理旧文件（只保留最近5次记录）
        print("🧹 清理旧文件...")
        cleanup_stats = cleanup_old_files(keep_count=5)
        if cleanup_stats['analysis'] > 0 or cleanup_stats['audio'] > 0:
            print(f"✅ 清理完成: 删除了 {cleanup_stats['analysis']} 个分析文件, {cleanup_stats['audio']} 个音频文件")
        
        print("🎉 完整流程执行成功!")
        return True


# Discord Bot 命令
@bot.command(name="lol")
async def lol_analysis(ctx, style: str = "default"):
    """
    运行完整的LOL游戏分析流程
    用法: !lol [风格名称]
    可用风格: 动态从STYLE_CONFIGS获取
    示例: !lol professional
    注意: 需要先加入语音频道
    """
    try:
        # 验证风格名称
        from services.prompts import STYLE_CONFIGS
        valid_styles = list(STYLE_CONFIGS.keys())
        if style not in valid_styles:
            await ctx.reply(f"❌ 无效的风格名称。可用风格: {', '.join(valid_styles)}")
            return
        
        workflow = LOLWorkflow(ctx=ctx)  # 传递Discord上下文
        
        # 检查用户是否在语音频道中
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply("❌ 请先加入语音频道再使用此命令")
            return
        
        voice_channel_id = ctx.author.voice.channel.id
        
        # 动态获取风格名称映射
        style_names = get_style_display_names()
        
        await ctx.reply(f"🎮 **开始{style_names[style]}分析你的最新游戏...**")
        
        # 运行完整流程，传入风格参数
        success = await workflow.run_full_workflow(voice_channel_id, style=style)
        
        if success:
            await ctx.reply(f"🎉 **{style_names[style]}分析完成！** 游戏分析完成，音频已播放完毕。")
        else:
            await ctx.reply("❌ **游戏分析失败**，请检查配置。")
            
    except Exception as e:
        await ctx.reply(f"❌ **执行失败**: {e}")


@bot.command(name="test")
async def test_workflow(ctx):
    """测试工作流程（不播放音频）"""
    try:
        workflow = LOLWorkflow(ctx=ctx)  # 传递Discord上下文
        
        await ctx.reply("🧪 **开始测试工作流程...**")
        
        # 只运行前3步
        if await workflow.step1_get_match_data():
            if await workflow.step2_convert_to_chinese():
                if await workflow.step3_generate_tts():
                    await ctx.reply("✅ **测试成功！** 音频文件已生成。")
                else:
                    await ctx.reply("❌ **TTS生成失败**")
            else:
                await ctx.reply("❌ **中文分析生成失败**")
        else:
            await ctx.reply("❌ **游戏数据获取失败**")
            
    except Exception as e:
        await ctx.reply(f"❌ **测试失败**: {e}")


@bot.command(name="lol_custom")
async def lol_custom_analysis(ctx, *, custom_prompt: str = None):
    """
    运行自定义LOL游戏分析流程
    用法: !lol_custom [自定义提示词]
    示例: !lol_custom "请生成一个专业的游戏分析"
    注意: 需要先加入语音频道
    """
    try:
        workflow = LOLWorkflow(ctx=ctx)  # 传递Discord上下文
        
        # 检查用户是否在语音频道中
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply("❌ 请先加入语音频道再使用此命令")
            return
        
        voice_channel_id = ctx.author.voice.channel.id
        await ctx.reply("🎮 **开始自定义分析你的最新游戏...**")
        
        # 运行完整流程，传入自定义参数
        success = await workflow.run_full_workflow(voice_channel_id, custom_prompt)
        
        if success:
            await ctx.reply("🎉 **自定义分析完成！** 游戏分析完成，音频已播放完毕。")
        else:
            await ctx.reply("❌ **自定义分析失败**，请检查配置。")
            
    except Exception as e:
        await ctx.reply(f"❌ **执行失败**: {e}")


@bot.command(name="lol_style")
async def lol_style_analysis(ctx, style: str = "default"):
    """
    运行指定风格的LOL游戏分析流程
    用法: !lol_style [风格名称]
    可用风格: 动态从STYLE_CONFIGS获取
    示例: !lol_style professional
    注意: 需要先加入语音频道
    """
    try:
        # 验证风格名称
        from services.prompts import STYLE_CONFIGS
        valid_styles = list(STYLE_CONFIGS.keys())
        if style not in valid_styles:
            await ctx.reply(f"❌ 无效的风格名称。可用风格: {', '.join(valid_styles)}")
            return
        
        workflow = LOLWorkflow(ctx=ctx)  # 传递Discord上下文
        
        # 检查用户是否在语音频道中
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply("❌ 请先加入语音频道再使用此命令")
            return
        
        voice_channel_id = ctx.author.voice.channel.id
        
        # 动态获取风格名称映射
        style_names = get_style_display_names()
        
        await ctx.reply(f"🎮 **开始{style_names[style]}分析你的最新游戏...**")
        
        # 运行完整流程，传入风格参数
        success = await workflow.run_full_workflow(voice_channel_id, style=style)
        
        if success:
            await ctx.reply(f"🎉 **{style_names[style]}分析完成！** 游戏分析完成，音频已播放完毕。")
        else:
            await ctx.reply("❌ **风格分析失败**，请检查配置。")
            
    except Exception as e:
        await ctx.reply(f"❌ **执行失败**: {e}")


@bot.command(name="lolcheck")
async def lolcheck_analysis(ctx, *, args: str = None):
    """
    检查指定用户的最新游戏数据
    用法: !lolcheck username#tag [风格名称]
    示例: !lolcheck Faker#KR1 professional
    注意: 需要先加入语音频道
    """
    try:
        if not args:
            await ctx.reply("❌ 请提供用户名和标签，格式: `!lolcheck username#tag [风格]`")
            return
        
        # 解析参数：username#tag [style]
        # 处理用户名和标签可能被空格分隔的情况
        parts = args.split()
        
        if len(parts) < 1:
            await ctx.reply("❌ 请提供用户名和标签，格式: `!lolcheck username#tag [风格]`")
            return
        
        # 重新组合用户名和标签
        username_tag = None
        style = "default"
        
        # 导入 STYLE_CONFIGS 一次
        from services.prompts import STYLE_CONFIGS
        
        # 查找包含#的部分或组合用户名#标签
        for i, part in enumerate(parts):
            if '#' in part:
                # 如果这个部分包含#，直接使用
                username_tag = part
                # 检查后面是否还有参数作为风格
                if i + 1 < len(parts):
                    potential_style = parts[i + 1]
                    if potential_style in STYLE_CONFIGS:
                        style = potential_style
                break
            elif i + 1 < len(parts) and parts[i + 1].startswith('#'):
                # 如果当前部分没有#，但下一部分以#开头，组合它们
                username_tag = part + parts[i + 1]
                # 检查后面是否还有参数作为风格
                if i + 2 < len(parts):
                    potential_style = parts[i + 2]
                    # 只有当它是有效的风格名称时才使用
                    if potential_style in STYLE_CONFIGS:
                        style = potential_style
                    # 如果不是有效风格，保持默认值，忽略这个参数
                break
        
        if not username_tag:
            await ctx.reply("❌ 格式错误，请使用 `username#tag` 格式")
            return
        
        # 解析用户名和标签
        if '#' not in username_tag:
            await ctx.reply("❌ 格式错误，请使用 `username#tag` 格式")
            return
        
        username_parts = username_tag.split('#', 1)
        if len(username_parts) != 2:
            await ctx.reply("❌ 格式错误，请使用 `username#tag` 格式")
            return
        
        game_name, tag_line = username_parts[0].strip(), username_parts[1].strip()
        
        if not game_name or not tag_line:
            await ctx.reply("❌ 用户名和标签不能为空")
            return
        
        # 验证风格名称
        valid_styles = list(STYLE_CONFIGS.keys())
        if style not in valid_styles:
            await ctx.reply(f"❌ 无效的风格名称 '{style}'。可用风格: {', '.join(valid_styles)}")
            return
        
        # 检查用户是否在语音频道中
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply("❌ 请先加入语音频道再使用此命令")
            return
        
        voice_channel_id = ctx.author.voice.channel.id
        
        # 风格名称映射 - 从 STYLE_CONFIGS 动态生成
        # 动态获取风格名称映射
        style_names = get_style_display_names()
        
        await ctx.reply(f"🎮 **开始{style_names[style]}分析 {game_name}#{tag_line} 的最新游戏...**")
        
        # 创建支持动态用户的工作流程
        workflow = LOLWorkflow(ctx=ctx)
        
        # 运行完整流程，传入动态用户参数和风格
        success = await workflow.run_full_workflow_with_user(voice_channel_id, game_name, tag_line, style=style)
        
        if success:
            await ctx.reply(f"🎉 **{game_name}#{tag_line} 的{style_names[style]}分析完成！** 游戏分析完成，音频已播放完毕。")
        else:
            await ctx.reply("❌ **游戏分析失败**，请检查用户名和标签是否正确。")
            
    except Exception as e:
        await ctx.reply(f"❌ **执行失败**: {e}")


@bot.command(name="files")
async def show_file_stats(ctx):
    """
    显示文件统计信息
    用法: !files
    """
    try:
        stats = get_file_count_info()
        
        stats_msg = f"📊 **文件统计信息**\n"
        stats_msg += f"📄 分析文件: {stats['analysis']} 个\n"
        stats_msg += f"🎵 音频文件: {stats['audio']} 个\n"
        stats_msg += f"📝 中文分析: {stats['chinese_analysis']} 个\n"
        stats_msg += f"💾 总计: {sum(stats.values())} 个文件"
        
        await ctx.reply(stats_msg)
        
    except Exception as e:
        await ctx.reply(f"❌ **获取统计失败**: {e}")


@bot.event
async def on_ready():
    print(f"✅ Discord Bot已登录: {bot.user}")
    print("🎮 LOL工作流程机器人已就绪!")
    print("可用命令:")
    print("  !lol [风格] - 运行完整分析流程（默认搞子风格）")
    print("  !lol_style [风格] - 运行指定风格分析流程")
    print("  !lol_custom [自定义提示词] - 运行自定义分析流程")
    print("  !lolcheck username#tag [风格] - 检查指定用户的最新游戏数据")
    print("  !test - 测试工作流程（不播放音频）")
    print("  !files - 显示文件统计信息")
    # 动态获取可用风格
    from services.prompts import STYLE_CONFIGS
    available_styles = list(STYLE_CONFIGS.keys())
    print(f"  可用风格: {', '.join(available_styles)}")
    print("  示例: !lol kfk_dp 或 !lol_style azi")
    print("  示例: !lolcheck Faker#KR1 或 !lolcheck Faker#KR1 taffy")
    print("  注意: 使用前请先加入语音频道")
    print("  文件管理: 自动保留最近5次记录，无需手动清理")


def main():
    """主函数 - 检查配置并启动"""
    print("英雄联盟游戏分析工作流程")
    print("=" * 50)
    
    # 检查必要的环境变量（无默认值的）
    required_vars = ["RIOT_API_KEY", "OPENAI_API_KEY", "DISCORD_TOKEN", "VOICV_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在.env文件中设置这些变量")
        return
    
    # 检查可选环境变量并设置默认值
    game_name = os.getenv("GAME_NAME", "exm233")
    tag_line = os.getenv("TAG_LINE", "233")
    
    print(f"📝 默认用户: {game_name}#{tag_line} (可通过!lolcheck命令动态指定)")
    
    print("✅ 所有配置检查通过")
    print("🚀 启动Discord Bot...")
    
    # 启动Discord Bot
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Bot启动失败: {e}")


if __name__ == "__main__":
    main()
