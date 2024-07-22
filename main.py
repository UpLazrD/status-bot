import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import mysql.connector

import modules.boss

load_dotenv('secret.env')


conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)


bot = commands.Bot(command_prefix = os.getenv('BOT_PREFIX'), intents = disnake.Intents.all())
bot.load_extension('modules.status')
bot.load_extension('modules.funs')
bot.load_extension('modules.about')
bot.add_cog(modules.boss.BotBoss(bot, conn))


@bot.event
async def on_ready():
    print(f"[INFO] Великий {bot.user} готов к работе")
    activity = disnake.Game(name = 'Schizo Station 14')
    await bot.change_presence(status = disnake.Status.online, activity=activity)



bot.run(os.getenv('SECRET_TOKEN'))