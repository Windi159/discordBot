from discord.ext.commands import Bot, Context
from discord import Intents
from src.jsonReadWrite import writeJson, readJson
from os import remove
from os.path import isfile
import random

coin_user_default = {
    "user_id": 123456789,
    "user_name": "A",
    "money": 50000,
    "Luna": 0,
    "Doge": 0,
    "Stella": 0
}

ant_id_list = {"user_id": "user_name"}

intent = Intents.default()
intent.message_content = True

bot = Bot(
    command_prefix = "*",
    intents = intent
)

coin = {
    "Luna": 500, "Doge": 1000, "Stella": 2000
}

@bot.event
async def on_ready():
    print("\n/////////////////////////\n")
    print(f"로그인 {bot}\n")
    print("/////////////////////////\n")

# args[0] : 코인 리스트
@bot.command()
async def 코인(ctx: Context, *args):
    if args[0] in list(coin.keys()):
        await ctx.send(coin[args[0]])

    elif args[0] == "리스트" or args[0] == "fltmxm":
        await ctx.send(coin)

    else:
        await ctx.send("잘못 입력함 ㅋㅋ. 다시 입력 ㄱㄱ")

# args[0] : 사용자 이름
@bot.command()
async def 가입(ctx: Context, *args):
    if isfile(f".\\userInfo\\{ctx.author.id}.json"):
        await ctx.send("이미 만들어둔거 있던데? 찾아보셈")

    else:
        coin_user_default["user_name"] = args[0]
        coin_user_default["user_id"] = ctx.author.id

        writeJson(ctx.author.id, coin_user_default)

        await ctx.send(f"{args[0]} 가입 완료")

# arg[0] : 사용자 이름  args[1] : 코인 이름  args[2] : 구매할 코인 갯수
@bot.command()
async def 구매(ctx: Context, *args):
    trade_user = readJson(ctx.author.id)

    if not isfile(f".\\userInfo\\{ctx.author.id}.json"):
        await ctx.send("다른 사람임. 다시 ㄱㄱ")

    elif trade_user["user_name"] != args[0]:
        await ctx.send("이름 잘못 입력함. 다시 ㄱㄱ")

    elif args[1] not in list(coin.keys()):
        await ctx.send("코인 이름 잘못 입력함. 다시 ㄱㄱ")

    elif trade_user["money"] > coin[args[1]] * int(args[2]):
        await ctx.send("서원탁 통장 잔고랑 똑같노 ㅋㅋ")

    else:
        trade_user["money"] -= coin[args[1]] * int(args[2])
        trade_user[args[1]] += int(args[2])
        writeJson(ctx.author.id, trade_user)

        await ctx.send(f"구매 성공, {args[0]}의 잔고 : {trade_user['money']}\n"
                       f"거래 내역: 코인{trade_user[args[1]]}개")


# arg[0] : 사용자  args[1] : 코인 이름  args[2] : 판매할 코인 갯수
@bot.command()
async def 판매(ctx: Context, *args):
    trade_user = readJson(ctx.author.id)

    if trade_user["user_id"] != ctx.author.id:
        await ctx.send("다른 사람임. 다시 ㄱㄱ")

    elif trade_user["user_name"] != args[0]:
        await ctx.send("이름 잘못 입력함. 다시 ㄱㄱ")

    elif args[1] not in list(coin.keys()):
        await ctx.send("코인 이름 잘못 입력함. 다시 ㄱㄱ")

    elif trade_user[args[1]] < int(args[2]):
        await ctx.send("이새끼 사기치노 ㅋㅋ")

    else:
        trade_user["money"] += coin[args[1]] * int(args[2])
        trade_user[args[1]] -= int(args[2])
        writeJson(ctx.author.id, trade_user)

        await ctx.send(f"구매 성공, {args[0]}의 잔고 : {trade_user['money']}\n"
                       f"거래 내역: 코인{trade_user[args[1]]}개")

@bot.command()
async def 조회(ctx: Context, *args):
    if isfile(f".\\userInfo\\{ctx.author.id}.json") is not False:
        ident_user = readJson(ctx.author.id)
        await ctx.send(ident_user)

    else:
        await ctx.send("없는 사람임. 다시 입력 ㄱㄱ")

@bot.command()
async def 찾기(ctx: Context):
    if not isfile(f".\\userInfo\\{ctx.author.id}.json"):
        await ctx.send("가입 안한것 같은디?")

    else:
        if ctx.message.author.dm_channel:
            await ctx.message.author.dm_channel.send(f"가입한 이름 : {readJson(ctx.author.id)['user_name']}")

        elif ctx.message.author.dm_channel is None:
            channel = await ctx.message.author.create_dm()
            await channel.send(f"가입한 이름 : {readJson(ctx.author.id)['user_name']}")

#args[0] : 사용자 이름
@bot.command()
async def 탈퇴(ctx: Context, *args):
    if readJson(ctx.author.id) is not False:
        remove(f".\\userInfo\\{ctx.author.id}.json")
        await ctx.send(f"{args[0]} 탈퇴 완료")

@bot.command()
async def 가격갱신(ctx: Context, *args):
    if args[0] == 1:
        coin["Luna"] *= random.randrange(1, 100)
        coin["Doge"] *= random.randrange(1, 100)
        coin["Stella"] *= random.randrange(1, 100)

    else:
        coin["Luna"] /= random.randrange(1, 100)
        coin["Doge"] /= random.randrange(1, 100)
        coin["Stella"] /= random.randrange(1, 100)

    await ctx.send(f"코인 가격이 변동되었습니다!\n"
                   f"Luna : {coin['Luna']} \nDoge : {coin['Doge']} \nStella : {coin['Stella']}")

    writeJson("coin_list", coin)

bot.run("MTIwOTE0MzYxNTI4OTQyNTk0MA.GktRu7.sOcHHUvR9yIi0QuvRUGa6ZK3awIfIdtJ_Lk8uk")
