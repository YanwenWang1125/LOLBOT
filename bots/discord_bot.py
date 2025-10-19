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
from services.json_to_chinese_lu import convert_to_chinese_mature_tone, load_json_file
from services.voicv_tts import generate_tts_audio
from services.utils import find_latest_json_file, ensure_directory

# 加载环境变量
load_dotenv()

# Discord Bot 配置
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICV_API_KEY = os.getenv("VOICV_API_KEY")
VOICV_VOICE_ID = os.getenv("VOICV_VOICE_ID")
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
    
    async def step2_convert_to_chinese(self):
        """步骤2: 转换为中文分析"""
        print("步骤2: 生成中文分析...")
        if self.ctx:
            await self.ctx.send("🤖 **步骤2**: 正在生成AI中文分析...")
        
        try:
            if not self.current_match_file:
                raise ValueError("没有可用的游戏数据文件")
            
            # 加载JSON数据
            match_data = load_json_file(self.current_match_file)
            if not match_data:
                raise ValueError("无法加载游戏数据")
            
            # 转换为中文分析
            self.chinese_analysis = convert_to_chinese_mature_tone(match_data)
            if not self.chinese_analysis:
                raise ValueError("AI分析生成失败")
            
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
            
            # 使用 voicV TTS API生成音频
            self.audio_file = generate_tts_audio(self.chinese_analysis)
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
    
    async def run_full_workflow(self, voice_channel_id=None):
        """运行完整工作流程"""
        print("开始英雄联盟游戏分析完整流程")
        print("=" * 60)
        
        # 步骤1: 获取游戏数据
        if not await self.step1_get_match_data():
            return False
        
        # 步骤2: 转换为中文分析
        if not await self.step2_convert_to_chinese():
            return False
        
        # 步骤3: 生成TTS音频
        if not await self.step3_generate_tts():
            return False
        
        # 步骤4: Discord播放
        if voice_channel_id:
            if not await self.step4_discord_play(voice_channel_id):
                return False
        
        print("🎉 完整流程执行成功!")
        return True


# Discord Bot 命令
@bot.command(name="lol")
async def lol_analysis(ctx, voice_channel_id: int = None):
    """
    运行完整的LOL游戏分析流程
    用法: !lol [语音频道ID]
    """
    try:
        workflow = LOLWorkflow(ctx=ctx)  # 传递Discord上下文
        
        # 如果没有指定语音频道，尝试使用用户当前频道
        if not voice_channel_id:
            if ctx.author.voice and ctx.author.voice.channel:
                voice_channel_id = ctx.author.voice.channel.id
            else:
                await ctx.reply("❌ 请先加入语音频道或指定语音频道ID")
                return
        
        await ctx.reply("🎮 **开始分析你的最新游戏...**")
        
        # 运行完整流程
        success = await workflow.run_full_workflow(voice_channel_id)
        
        if success:
            await ctx.reply("🎉 **完整流程执行成功！** 游戏分析完成，音频已播放完毕。")
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


@bot.event
async def on_ready():
    print(f"✅ Discord Bot已登录: {bot.user}")
    print("🎮 LOL工作流程机器人已就绪!")
    print("可用命令:")
    print("  !lol [语音频道ID] - 运行完整分析流程")
    print("  !test - 测试工作流程（不播放音频）")


def main():
    """主函数 - 检查配置并启动"""
    print("英雄联盟游戏分析工作流程")
    print("=" * 50)
    
    # 检查必要的环境变量
    required_vars = ["RIOT_API_KEY", "GAME_NAME", "TAG_LINE", "OPENAI_API_KEY", "DISCORD_TOKEN", "VOICV_API_KEY", "VOICV_VOICE_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在.env文件中设置这些变量")
        return
    
    print("✅ 所有配置检查通过")
    print("🚀 启动Discord Bot...")
    
    # 启动Discord Bot
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ Bot启动失败: {e}")


if __name__ == "__main__":
    main()
