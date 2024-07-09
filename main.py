# < Сторонние библиотеки >
import disnake
from disnake.ext import commands
import json

# < Файлы проекта >
from servers import lst1, lst2
from functions import server_status
from secret import secret_token

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(f"Бот {bot.user} готов к работе.")
    activity = disnake.Game(name='TREALSIDE')
    await bot.change_presence(status=disnake.Status.online, activity=activity)


# Команда для получения статуса, из словаря, список первый
@bot.slash_command(name='статус_1', description="Получить статус сервера Space Station 14 из первого предложенного списка")
async def status_command_dict1(ctx, адрес: str = commands.Param(
    description="Выберите сервер из предложенного списка",
    choices=lst1
)):
    if адрес == "лол ебать ахахахахах":
        embed = disnake.Embed(title="ЩКЕБЕДЕ ДОП ДОП ЕС ЕС", color=disnake.Color.yellow())
        embed.set_image(url="https://media.tenor.com/WhXYjpREz1kAAAAM/skibidi-toilet-skibidi.gif")
        embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/2038494310206033069/2FFBA39BB754CF0D0FC83C62636BAE30BE992758/")
        embed.description = "Бррр, щкебеде, доп доп доп, ес ес \nСкибиди дабиди да дап \nSkibidi, dom-dom-dom, yes-yes \nSkibidi-dabudu, nib-nib \nWe ain't here to hurt nobody (skibidi, skibidi, skibidi) \nWanna see you work your body (skibidi, skibidi, skibidi)"
        await ctx.send(embed=embed)
    else:
        embed = await server_status(адрес)
        await ctx.send(embed=embed)

# Команда для получения статуса, из словаря, список второй
@bot.slash_command(name='статус_2', description="Получить статус сервера Space Station 14 из второго предложенного списка")
async def status_command_dict2(ctx, адрес: str = commands.Param(
    description="Выберите сервер из предложенного списка",
    choices=lst2
)):
    embed = await server_status(адрес)
    await ctx.send(embed=embed)


# Команда для получения статуса, но уже вручную
@bot.slash_command(name='статус_вручную', description="Получить статус сервера Space Station 14, введя его адрес")
async def status_command_manually(ctx, адрес):
    embed = await server_status(адрес + '/status')
    await ctx.send(embed=embed)



bot.run(secret_token)