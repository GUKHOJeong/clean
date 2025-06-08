import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


# .env에서 토큰 로드
load_dotenv()
clean_token = os.getenv("clean_token")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)

MENTION_PROTECTED_CHANNEL_IDS = [1381162021319606322, 1380857846706471004]


@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user.name}")


@bot.command(name="도와줘")
async def show_help(ctx):
    embed = discord.Embed(
        title="📌 사용 가능한 명령어 안내", color=discord.Color.green()
    )

    embed.add_field(
        name="🎵 뮤직봇",
        value="`m!set default vol 5` : 사운드 초기 설정\n"
        "`m!play [링크 or 제목]` : 음악 시작\n"
        "`m!stop` : 음악 정지",
        inline=False,
    )

    embed.add_field(
        name="📅 일정 알림",
        value="`/자기소개`, `/일정추가`, `/내일정`, `/생일확인`",
        inline=False,
    )

    embed.add_field(
        name="📚 짭품타",
        value="`/공부시작`, `/공부종료`, `/랭킹`",
        inline=False,
    )

    embed.add_field(
        name="🧹 청소봇",
        value="`/청소`",
        inline=False,
    )

    embed.add_field(
        name="🌤️ 날씨봇 ",
        value="`/날씨 [지역]`, `/추천`",
        inline=False,
    )
    embed.add_field(
        name="📄 지식봇 ",
        value="`/질문`, `/요약`",
        inline=False,
    )


@bot.command(name="청소")
@commands.has_permissions(manage_messages=True)
async def delete_all_but_top(ctx):
    messages = [msg async for msg in ctx.channel.history(limit=None)]

    if len(messages) <= 1:
        await ctx.send("🟡 삭제할 메시지가 없습니다.", delete_after=3)
        return

    if ctx.channel.id in MENTION_PROTECTED_CHANNEL_IDS:
        to_delete = [
            msg for msg in messages[:-1] if not msg.mentions  # 멘션 없는 메시지만 삭제
        ]
        ctx_msg = f"🧹 이 채널에서 @과 상단1개를  제외하고 {len(to_delete)}개 메시지를 삭제했습니다."
    else:
        to_delete = messages[:-1]
        ctx_msg = f"🧹 이 채널에서 상단1개를 제외하고 {len(to_delete)}개 메시지를 삭제했습니다."
    for i in range(0, len(to_delete), 100):
        await ctx.channel.delete_messages(to_delete[i : i + 100])

    await ctx.send(
        f"{ctx_msg}",
        delete_after=3,
    )


# 봇 실행
bot.run(clean_token)
