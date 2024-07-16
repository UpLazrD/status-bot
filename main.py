# < Сторонние библиотеки >
import disnake
from disnake.ext import commands
import json

# < Файлы проекта >
from collection import servers1, servers2
from functions import *
from secret import secret_token

bot = commands.Bot(command_prefix = '!', intents = disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"[INFO] Великий {bot.user} готов к работе")
    activity = disnake.Game(name = 'анальчике своим пальчиком')
    await bot.change_presence(status = disnake.Status.online, activity=activity)

# Статус Церберов
@bot.slash_command(name='статус_церберы', description = "Получить статус сервера Cerberus Space")
async def status_command_cerberus(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.defer()
    embed = await server_status("http://194.93.2.178:1212/status")
    await interaction.edit_original_response(embed=embed)


# Команда для получения статуса из словаря
@bot.slash_command(name='статус_1', description = "Получить статус сервера Space Station 14 из первого предложенного списка")
async def status_command_dict1(interaction: disnake.ApplicationCommandInteraction,
    адрес: str = commands.Param( 
        description = "Выберите сервер из предложенного списка",
        choices = servers1)):
    await interaction.response.defer()
    embed = await server_status(адрес)
    await interaction.edit_original_response(embed=embed)


@bot.slash_command(name='статус_2', description = "Получить статус сервера Space Station 14 из второго предложенного списка")
async def status_command_dict2(interaction: disnake.ApplicationCommandInteraction,
    адрес: str = commands.Param(
        description = "Выберите сервер из предложенного списка",
        choices = servers2)):
    await interaction.response.defer()
    embed = await server_status(адрес)
    await interaction.edit_original_response(embed=embed)



# Команда для получения статуса, но уже вручную
@bot.slash_command(name='статус_вручную', description = "Получить статус сервера Space Station 14, введя его адрес")
async def status_command_manually(interaction: disnake.ApplicationCommandInteraction,
    адрес: str = commands.Param(
        description = "Введите адрес сервера - тот, по которому вы подключаетесь к игре")):
    await interaction.response.defer()
    embed = await server_status(адрес + '/status')
    await interaction.edit_original_response(embed=embed)


# Троллинг ГРЕШНИКОВ
@bot.slash_command(name='e621', description = "[18+] Получить рандомную фурри-картинку из источника e621")
async def furry_troll(ctx):
    embed = await e621_troll()
    await ctx.send(embed=embed)

# Бароны.
@bot.slash_command(name="кальян", description = "Выпустить дух чарона")
async def kalyan(ctx):
    embed = disnake.Embed(title="", color=disnake.Color.yellow())
    embed.set_author(name=f'{ctx.author.display_name} выпускает дух чарона!', icon_url=ctx.author.avatar.url)
    embed.description = f'{ctx.author.display_name} решил затянуться делюкс кальяном с гравировкой **"Нищим здесь не место!"**'
    await ctx.send(embed=embed)


bot.run(secret_token)