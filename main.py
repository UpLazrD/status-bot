import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv


load_dotenv('secret.env')

bot = commands.Bot(command_prefix = '!', intents = disnake.Intents.all())
bot.load_extension('modules.status')
bot.load_extension('modules.funs')


@bot.event
async def on_ready():
    print(f"[INFO] Великий {bot.user} готов к работе")
    activity = disnake.Game(name = 'Schizo Station 14')
    await bot.change_presence(status = disnake.Status.online, activity=activity)


bot.run(os.getenv('SECRET_TOKEN'))