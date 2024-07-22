from disnake.ext import commands
import disnake
import sys
import os
from dotenv import load_dotenv

load_dotenv('../secret.env')

class BotBoss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.id == int(os.getenv('AUTHORIZED_USER_ID')):
            return True
        else:
            await ctx.send("<:bruh:1061578510411501628> Сосунок, ты зачем косплеишь феменисток? У тебя НЕТ ПРАВ для того, чтобы управлять мной.")
            return False

    @commands.command(name='bot_restart')
    async def boss_restart(self, ctx, cog: str = 'all'):
        if cog == 'all':
            await ctx.send('<:billymaster:1126199675234570240> ПЕРЕЗАГРУЖАЮСЬ!...')
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            try:
                self.bot.reload_extension(f'modules.{cog}')
                await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} перезагружен.')
                print(f'[INFO] Модуль бота `modules.{cog}` перезагружен.')
            except Exception as e:
                print(f'[ERRO] Ошибка перезагрузки кога: {e}')
                await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} не найден или его не удалось перезагрузить.')

    @commands.command(name='bot_disable')
    async def boss_disable(self, ctx, cog: str):
        try:
            self.bot.unload_extension(f'modules.{cog}')
            await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} отключен.')
            print(f'[INFO] Модуль бота `modules.{cog}` отключён.')
        except Exception as e:
            print(f'[ERRO] Ошибка отключения кога: {e}')
            await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} не найден или его не удалось отключить.')

    @commands.command(name='bot_enable')
    async def boss_enable(self, ctx, cog: str):
        try:
            self.bot.load_extension(f'modules.{cog}')
            await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} включен.')
            print(f'[INFO] Модуль бота `modules.{cog}` включён.')
        except Exception as e:
            print(f'[ERRO] Ошибка включения кога: {e}')
            await ctx.send(f'<:billymaster:1126199675234570240> Модуль {cog} не найден или его не удалось включить.')


def setup(bot: commands.Bot):
    bot.add_cog(BotBoss(bot))