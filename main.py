# < Сторонние библиотеки >
import disnake
from disnake.ext import commands
import json

# < Файлы проекта >
from servers import lst1, lst2
from functions import server_status, skibidi_station
from secret import secret_token

bot = commands.Bot(command_prefix = '!', intents = disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"[INFO] Великий {bot.user} готов к работе")
    activity = disnake.Game(name = 'TREALSIDE')
    await bot.change_presence(status = disnake.Status.online, activity=activity)


# Команда для получения статуса из словаря
@bot.slash_command(name='статус_1', description = "Получить статус сервера Space Station 14 из первого предложенного списка")
async def status_command_dict1(ctx, 
    адрес: str = commands.Param( 
        description = "Выберите сервер из предложенного списка",
        choices = lst1)):

    if адрес == "скибиди стейшен ис реал...":
        embed = await skibidi_station()
        await ctx.send(embed=embed)
    else:
        embed = await server_status(адрес)
        await ctx.send(embed=embed)
 

@bot.slash_command(name='статус_2', description = "Получить статус сервера Space Station 14 из второго предложенного списка")
async def status_command_dict2(ctx, 
    адрес: str = commands.Param(
        description = "Выберите сервер из предложенного списка",
        choices = lst2)):

    embed = await server_status(адрес)
    await ctx.send(embed=embed)


# Команда для получения статуса, но уже вручную
@bot.slash_command(name='статус_вручную', description = "Получить статус сервера Space Station 14, введя его адрес")
async def status_command_manually(ctx, 
    адрес: str = commands.Param(
        description = "Введите адрес сервера - тот, по которому вы подключаетесь к игре")):
    
    embed = await server_status(адрес + '/status')
    await ctx.send(embed=embed)



bot.run(secret_token)