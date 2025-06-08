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
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user.name}")


@bot.command(name="전부삭제")
@commands.has_permissions(manage_messages=True)
async def delete_all_but_top(ctx):
    messages = [msg async for msg in ctx.channel.history(limit=None)]

    if len(messages) <= 1:
        await ctx.send("🟡 삭제할 메시지가 없습니다.", delete_after=3)
        return

    to_delete = messages[:-1]  # 상단 1개만 남기고

    for i in range(0, len(to_delete), 100):
        await ctx.channel.delete_messages(to_delete[i : i + 100])

    await ctx.send(
        f"🧹 이 채널에서 상단 1개를 제외하고 {len(to_delete)}개 메시지를 삭제했습니다.",
        delete_after=3,
    )


# 봇 실행
bot.run(clean_token)
