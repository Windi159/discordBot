from discord.ext.commands import Bot, Context
from discord import Intents

intent = Intents.default()
intent.message_content = True
bot = Bot(
    command_prefix = "!",
    intents = intent
)

coin = {
    "사볼": 500, "츄니즘": 1000, "와카": 1000,
    "마이마이": 1000, "유비트": 500, "태고": 500,
    "펌프": 1000, "DDR": 1000, "팝픈": 500
}

@bot.event
async def on_ready():
    print("\n/////////////////////////\n")
    print(f"로그인 {bot}\n")
    print("/////////////////////////\n")

@bot.command()
async def test(ctx: Context, *args):
    await ctx.send(args[0])

@bot.command()
async def 코인(ctx: Context, *args):
    if args[0] == "리스트":
        await ctx.send(coin)

bot.run("MTIwOTE0MzYxNTI4OTQyNTk0MA.Gg_UwS.vEmzJrHekmMA2hxugtSFb9AfxGBwAdECLvVMUE")