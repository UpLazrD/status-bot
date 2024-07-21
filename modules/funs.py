from  disnake.ext import commands
import disnake
import random

from .collection import godness


class BotFuns(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Троллинг ГРЕШНИКОВ
    @commands.slash_command(name='e621', description = "[18+] Получить рандомную фурри-картинку из источника e621")
    async def furry_troll(self, inter):
        embed = disnake.Embed(title="Бог недоволен тобой", color=disnake.Color.red())
        embed.set_image(url=random.choice(godness))
        await inter.response.send_message(embed=embed)

    # Бароны.
    @commands.slash_command(name="кальян", description = "Выпустить дух чарона")
    async def kalyan(self, inter):
        embed = disnake.Embed(title="", color=disnake.Color.yellow())
        embed.set_author(name=f'{inter.author.display_name} выпускает дух чарона!', icon_url=inter.author.avatar.url)
        embed.description = f'{inter.author.display_name} решил затянуться делюкс кальяном с гравировкой **"Нищим здесь не место!"**'
        await inter.response.send_message(embed=embed)

    
def setup(bot: commands.Bot):
    bot.add_cog(BotFuns(bot))