from discord.ext.commands import Bot, Context
from discord import Intents
from src.jsonReadWrite import writeJson, readJson
from os import remove

coin_user_default = {
    "user_id": 123456789,
    "user_name": "A",
    "money": 50000,
    "Luna": 0,
    "Doge": 0,
    "Stella": 0
}

ant_name = []
ant_data = []

intent = Intents.default()
intent.message_content = True
bot = Bot(
    command_prefix = "*",
    intents = intent
)

coin = {
    "Luna": 500, "Doge": 1000, "Stella": 1000
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
    if args[0] in list(coin.keys()):
        await ctx.send(coin[args[0]])

    elif args[0] == "리스트" or args[0] == "fltmxm":
        if args[0] == "fltmxm":
            await ctx.send("영어로 쳤노 ㅋㅋ")
        await ctx.send(coin)

    else:
        await ctx.send("잘못 입력함 ㅋㅋ. 다시 입력 ㄱㄱ")

@bot.command()
async def 가입(ctx: Context, *args):
    if readJson(args[0]):
        await ctx.send("이미 있음. 다른 이름 ㄱㄱ")

    else:
        ant_name.append(args[0])
        coin_user_default["user_name"] = args[0]
        coin_user_default["user_id"] = ctx.author.id
        ant_data.append(coin_user_default)

        writeJson(args[0], coin_user_default)

        await ctx.send(f"{ant_name[0]} 가입 완료")

@bot.command()
async def 구매(ctx: Context, *args):
    trade_user = readJson(args[0])

    if trade_user["user_id"] != ctx.author.id:
        await ctx.send("이새끼 사기치노 ㅋㅋ")

    elif trade_user is None:
        await ctx.send("이름 잘못 입력함. 다시 ㄱㄱ")

    elif args[1] not in list(coin.keys()):
        await ctx.send("코인 이름 잘못 입력함. 다시 ㄱㄱ")

    elif trade_user["money"] < coin[args[1]] * int(args[2]):
        await ctx.send("서원탁 통장 잔고랑 똑같노 ㅋㅋ")

    else:
        trade_user["money"] -= coin[args[1]] * int(args[2])
        trade_user[args[1]] += int(args[2])
        writeJson(args[0], trade_user)


@bot.command()
async def 조회(ctx: Context, *args):
    if readJson(args[0]) is not None:
        ident_user = readJson(args[0])
        await ctx.send(ident_user)

    else:
        await ctx.send("없는 사람임. 다시 입력 ㄱㄱ")

@bot.command()
async def 탈퇴(ctx: Context, *args):
    if readJson(args[0]) is not None:
        remove(f".\\userInfo\\{args[0]}.json")
        await ctx.send(f"{args[0]} 탈퇴 완료")
