# < Сторонние библиотеки >
import disnake
from disnake.ext import commands
import json

# < Файлы проекта >
from servers import lst
from functions import server_status
from secret import secret_token

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())


###
# Команда для получения статуса, из словаря
###
@bot.slash_command(name='статус', description="Получить статус сервера Space Station 14 из предложенного списка")
async def status_command_dict(ctx, address: str = commands.Param(
    description="Выберите сервер из предложенного списка",
    choices=lst
)):
    if address == "лол ебать ахахахахах":
        embed = disnake.Embed(title="ЩКЕБЕДЕ ДОП ДОП ЕС ЕС", color=disnake.Color.yellow())
        embed.set_image(url="https://media.tenor.com/WhXYjpREz1kAAAAM/skibidi-toilet-skibidi.gif")
        embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/2038494310206033069/2FFBA39BB754CF0D0FC83C62636BAE30BE992758/")
        embed.description = "Бррр, щкебеде, доп доп доп, ес ес \nСкибиди дабиди да дап \nSkibidi, dom-dom-dom, yes-yes \nSkibidi-dabudu, nib-nib \nWe ain't here to hurt nobody (skibidi, skibidi, skibidi) \nWanna see you work your body (skibidi, skibidi, skibidi)"
        await ctx.send(embed=embed)
    else:
        embed = await server_status(address)
        await ctx.send(embed=embed)


###
# Команда для получения статуса, но уже вручную
###
@bot.slash_command(name='статус_вручную', description="Получить статус сервера Space Station 14, введя его адрес")
async def status_command_manually(ctx, address):
    embed = await server_status(address + '/status')
    await ctx.send(embed=embed)


###
# Запуск злоебучего бота
###
@bot.event
async def on_ready():
    print(f"Бот {bot.user} готов к работе.")
    activity = disnake.Game(name='TREALSIDE')
    await bot.change_presence(status=disnake.Status.online, activity=activity)

bot.run(secret_token)