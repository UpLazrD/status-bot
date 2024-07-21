from  disnake.ext import commands
import disnake
import platform


class BotAbout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.slash_command(name='бот_информация', description='Выводит информацию о боте')
    async def about_bot(self, inter):   
        await inter.response.defer()

        embed = disnake.Embed(title="Информация бота", color=disnake.Color.orange())
        embed.description = (
            'Бот <:altym:1264586102694744084> `Алтым` создан его разработчиком <:uplazrd:1264585587676024914> `UpLazrD` '
            'для получения статуса любых Space Station 14 серверов. ' 
            'Бот имеет [открытый исходный код](<https://github.com/UpLazrD/status-bot>) '
            'и [сервер поддержки](<https://discord.gg/4YRtfWA>) с чейнджлогом бота.'
        )
        embed.add_field(
            name="`🔥` Статистика использования", 
            value=(
                f'**Количество серверов**: {len(self.bot.guilds)}\n'
                f'**Всего пользователей:** {sum(guild.member_count for guild in self.bot.guilds)}\n'
                f'**Выполнено команд**: неизвестно.'
            ), inline=False
        )
        embed.add_field(
            name="`🔧` Техническая информация:", 
            value=(
                f'**Бот написан** на библиотеке Disnake\n'
                f'**Версия бота:** от <t:1721660400:d>\n'
                f'**Версия Python:** {platform.python_version()}\n'
                f'**Задержка бота:** {round(self.bot.latency * 1000)}мс'
            ), inline=False
        )
        embed.set_image(url='https://i.postimg.cc/N0chLB6h/03-14-08-va-UMx3-c1x-Y.png')
        await inter.followup.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(BotAbout(bot))