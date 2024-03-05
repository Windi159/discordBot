from discord.ext.commands import Bot, Context
from discord.ext import tasks
from discord import Intents
from src.jsonReadWrite import writeJson, readJson
from os import remove
from os.path import isfile
import random
from math import floor

class WontakBot(Bot):
    def __init__(self):
        self._coin_user_default = {
            "user_id": 123456789,
            "user_name": "A",
            "money": 1000000,
            "Luna": 0,
            "Doge": 0,
            "Stella": 0
        }

        self.user_info = ".\\userInfo\\"
        self.lotto_info = ".\\lottoinfo\\"
        self.lotto_try = 0

        intent = Intents.default()
        intent.message_content = True

        self._coin = {
            "Luna": 50000, "Doge": 100000, "Stella": 200000
        }

        super(WontakBot, self).__init__(command_prefix="*", intents=intent)

        self.setup_command()

        self.run("Token")

    def setup_command(self):
        @self.event
        async def on_ready():
            print("\n/////////////////////////\n")
            print(f"로그인 {self}\n")
            print("/////////////////////////\n")

            가격갱신.start()
            번호_재추첨.start()

        # args[0] : 코인 리스트
        @self.command()
        async def 코인(ctx: Context, *args):
            if args[0] in list(self._coin.keys()):
                await ctx.send(self._coin[args[0]])

            elif args[0] == "리스트" or args[0] == "fltmxm":
                await ctx.send(f"Luna : {self._coin["Luna"]}\n"
                               f"Doge : {self._coin["Doge"]}\n"
                               f"Stella : {self._coin["Stella"]}")

            elif args[0] in list(self._coin.keys()):
                await ctx.send(f"{args[0]} : {self._coin[args[0]]}")

            else:
                await ctx.send("잘못 입력함 ㅋㅋ. 다시 입력 ㄱㄱ")

        # args[0] : 사용자 이름
        @self.command()
        async def 가입(ctx: Context, *args):
            if isfile(f"{self.user_info}{ctx.author.id}.json"):
                await ctx.send("이미 만들어둔거 있던데? 찾아보셈")

            else:
                self._coin_user_default["user_name"] = args[0]
                self._coin_user_default["user_id"] = ctx.author.id

                writeJson(ctx.author.id, self._coin_user_default)

                await ctx.send(f"{args[0]} 가입 완료")

        # arg[0] : 사용자 이름  args[1] : 코인 이름  args[2] : 구매할 코인 갯수
        @self.command()
        async def 구매(ctx: Context, *args):
            trade_user = readJson(f"{self.user_info}{ctx.author.id}")

            if args[0] == "로또":
                if isfile(f"{self.lotto_info}{ctx.author.id}.json"):
                    await ctx.send("로또는 갱신되기 전에 1개밖에 못 삼")

                else:
                    num = random.randint(1, 46)
                    writeJson(f"{self.lotto_info}{ctx.author.id}", num)

                    await ctx.send(f"너가 받은 번호는 {num} 이야.")

            elif not isfile(f"{self.user_info}{ctx.author.id}.json"):
                await ctx.send("다른 사람임. 다시 ㄱㄱ")

            elif trade_user["user_name"] != args[0]:
                await ctx.send("이름 잘못 입력함. 다시 ㄱㄱ")

            elif args[1] not in list(self._coin.keys()):
                await ctx.send("코인 이름 잘못 입력함. 다시 ㄱㄱ")

            elif trade_user["money"] < self._coin[args[1]] * int(args[2]):
                await ctx.send("서원탁 통장 잔고랑 똑같노 ㅋㅋ")

            else:
                trade_user["money"] -= self._coin[args[1]] * int(args[2])
                trade_user[args[1]] += int(args[2])
                writeJson(f"{self.user_info}{ctx.author.id}", trade_user)

                await ctx.send(f"구매 성공, {args[0]}의 잔고 : {trade_user['money']}\n"
                               f"거래 내역: {args[1]} : {trade_user[args[1]]} 개")


        # arg[0] : 사용자  args[1] : 코인 이름  args[2] : 판매할 코인 갯수
        @self.command()
        async def 판매(ctx: Context, *args):
            trade_user = readJson(f"{self.user_info}{ctx.author.id}")

            if trade_user["user_id"] != ctx.author.id:
                await ctx.send("다른 사람임. 다시 ㄱㄱ")

            elif trade_user["user_name"] != args[0]:
                await ctx.send("이름 잘못 입력함. 다시 ㄱㄱ")

            elif args[1] not in list(self._coin.keys()):
                await ctx.send("코인 이름 잘못 입력함. 다시 ㄱㄱ")

            elif trade_user[args[1]] < int(args[2]):
                await ctx.send("이새끼 사기치노 ㅋㅋ")

            else:
                trade_user["money"] += self._coin[args[1]] * int(args[2])
                trade_user[args[1]] -= int(args[2])
                writeJson(f"{self.user_info}{ctx.author.id}", trade_user)

                await ctx.send(f"구매 성공, {args[0]}의 잔고 : {trade_user['money']}\n"
                               f"거래 내역: {args[1]} : {trade_user[args[1]]}개")

        @self.command()
        async def 조회(ctx: Context):
            if isfile(f"{self.user_info}{ctx.author.id}.json") is not False:
                ident_user = readJson(f"{self.user_info}{ctx.author.id}")
                await ctx.send(ident_user)

            else:
                await ctx.send("없는 사람임. 다시 입력 ㄱㄱ")

        @self.command()
        async def 찾기(ctx: Context):
            if not isfile(f".\\userInfo\\{ctx.author.id}.json"):
                await ctx.send("가입 안한것 같은디?")

            else:
                if ctx.message.author.dm_channel:
                    await ctx.message.author.dm_channel.send(f"가입한 이름 : {readJson(f"{self.user_info}{ctx.author.id}")['user_name']}")

                elif ctx.message.author.dm_channel is None:
                    channel = await ctx.message.author.create_dm()
                    await channel.send(f"가입한 이름 : {readJson(f"{self.user_info}{ctx.author.id}")['user_name']}")

        # args[0] : 사용자 이름
        @self.command()
        async def 탈퇴(ctx: Context, *args):
            if readJson(ctx.author.id) is not False:
                remove(f"{self.user_info}{ctx.author.id}.json")
                await ctx.send(f"{args[0]} 탈퇴 완료")

        @tasks.loop(seconds=random.randint(30, 180))
        async def 가격갱신():
            for name in list(self._coin.keys()):
                if random.randint(1, 2) == 1:
                    self._coin[name] *= random.randrange(1, 100)
                    self._coin[name] = floor(self._coin[name])

                else:
                    self._coin[name] /= random.randrange(1, 100)
                    self._coin[name] = floor(self._coin[name])

            chennel = self.get_channel(1155796809969578035)

            await chennel.send(f"코인 가격이 변동되었습니다!\n"
                               f"Luna : {self._coin['Luna']} \nDoge : {self._coin['Doge']} \nStella : {self._coin['Stella']}")

            writeJson(f"{self.user_info}coin_list", self._coin)

        @tasks.loop(minutes=1)
        async def 번호_재추첨():
            if isfile(".\\lottoInfo\\lotto.json"):
                chennel = self.get_channel(1155796809969578035)
                last_num = readJson(f"{self.lotto_info}lotto")
                remove(f"{self.lotto_info}")
                await chennel.send(f"로또 번호가 바뀌었습니다.\n"
                                   f"이전 로또 번호는 {last_num} 입니다.")


            writeJson(f"{self.lotto_info}lotto", random.randint(1, 46))

            self.lotto_try += 1

if __name__ == '__main__':
    WontakBot()
