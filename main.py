# < Сторонние библиотеки >
import disnake
from disnake.ext import commands
import aiohttp
import json

# < Файлы проекта >
# from servers.py import servers
# from functions.py import server_status


bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())


###
# Функция получения статуса сервера
###
async def server_status(address):
    try:
        print(address)
        # HTTP-запрос на сервер
        async with aiohttp.ClientSession() as session: # < async with 
            async with session.get(address) as response: # < async with 
                data = await response.json()

        # Формирование Embed ответа для последующей передачи боту.
        embed = disnake.Embed(title="Статус игрового сервера Space Station 14", color=disnake.Color.green())
        embed.add_field(name="Игровой сервер", value=data['name'], inline=False)
        embed.add_field(name="Игроки", value=f"Игроков {data['players']} из {data['soft_max_players']}", inline=False)
        
        if data["run_level"] == 1:
            embed.add_field(name="Игровой режим", value=data['preset'], inline=True)
            embed.add_field(name="Карта", value=data['map'], inline=True)
            embed.add_field(name="Статус игры", value="Игра продолжается", inline=False)
            embed.add_field(name="Текущий раунд", value=f"Раунд #{data['round_id']}", inline=True)
            embed.add_field(name="Время раунда", value=f"{(disnake.utils.utcnow() - disnake.utils.parse_time(data['round_start_time'])).total_seconds() // 60:.0f} минут назад", inline=True)
        elif data["run_level"] == 2:
            embed.add_field(name="Статус игры", value="Игра заканчивается (Манифест)", inline=False)
        else:
            embed.add_field(name="Статус игры", value="Игра не началась (Лобби)", inline=False)

        embed.add_field(name="Теги сервера", value=", ".join(data['tags']), inline=False)
        embed.add_field(name="Режим бункера", value="Действует" if data['panic_bunker'] else "Отключён", inline=True)
        embed.add_field(name="Режим тюрьмы", value="Действует" if data['baby_jail'] else "Отключён", inline=True) # ИСПРАВИТЬ ДЛЯ НЕКОТОРЫХ СЕРВЕРОВ 
# (вайтдрим, отсталый от жизни сервер, крашит этого бота)
        return embed

    except Exception as e:
        embed = disnake.Embed(title="Ошибка", color=disnake.Color.red())
        embed.description = "В процессе выполнения программы, бот не смог совладать с управлением. Ошибка может заключаться в невозможности отправить запрос серверу. Убедитесь, что Вы ввели правильный адрес (тот, по которому вы подключаетесь к серверу), а сам сервер - работает. В ином случае, свяжитесь с разработчиком бота, ошибка была выведена в консоль. \n\nНекоторые сообщения от разработчика: сервера White Dream вызывают ошибки в получении статуса, скоро исправлю. Так-же некоторые у некоторых серверов из списка введён неправильный адрес, вы можете исправить это [здесь](https://github.com/uplazrd/status-bot), а заодно добавить другие сервера."
        print(f"Произошла ошибка: {e}")
        return embed


###
# Команда для получения статуса, из словаря
###
@bot.slash_command(name='статус', description="Получить статус сервера Space Station 14 из предложенного списка")
async def status_command_dict(ctx, address: str = commands.Param(
    description="Выберите сервер из предложенного списка",
    choices={ # Убрать нахуй в отдельный файл!
        "🛰 Corvax - Мейн 🚀": "https://game2.station14.ru/main/server/status",
        "🛰 Corvax - Элизиум 🌑": "https://game1.station14.ru/elysium/server/status",
        "🛰 Corvax - Небула ✨": "https://game1.station14.ru/nebula/server/status",
        "🛰 Corvax - Атара 🌀": "https://game1.station14.ru/athara/server/status",
        "🛰 Corvax - Солярис 🌕": "https://game2.station14.ru/solaris/server/status",
        "🛰 Corvax - Эхо ☄": "https://game2.station14.ru/echo/server/status",
        "🛰 Corvax - Нова 🪐": "https://game1.station14.ru/nova/server/status",
        "🛰 Corvax - Ждалкер ☢": "https://game.stalkers14.xyz/status",
        "🛰 Corvax - Колониальные Морпехи 🌎": "https://game1.station14.ru/marines-main/server/status",
        "✅ SS220 - Saggitarius": "https://s3.ss220.club:1214/status",
        "✅ SS220 - Orion": "https://s2.ss220.club:1212/status",
        "✅ SS220 - Perseus": "https://s2.ss220.club:1213/status",
        "🦅 Imperial Space - Кассиопея 🔮": "https://cassiopeia.imperialspace.net/status",
        "🦅 Imperial Space - Эридан 🦄": "https://eridanus.imperialspace.net/status",
        "🦅 Imperial Space - Цефей 👑": "https://cepheus.imperialspace.net/status",
        "🦅 Imperial Space - Пиксис 🧭": "https://pyxis.imperialspace.net/status",
        "🦅 Imperial Space - Форнакс 🔥": "https://fornax.imperialspace.net/status",
        "🦅 Imperial Space - Октансис 🔭": "https://octantis.imperialspace.net/status",
        "🦊 Lost Paradise [HARAM 18+]": "https://station.lost-paradise.space/status",
        "🌆 Project Backmen": "http://46.72.238.71:1212/status",
        "🦽 SUNRISE - Феникс": "https://sunrise14.top/fenix/status",
        "🦽 SUNRISE - Ореол": "https://sunrise14.top/oreol/status",
        "🦽 SUNRISE - Фронтир": "https://sunrise14.top/tether/status",
    }
)):
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


bot.run('')