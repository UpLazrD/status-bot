import aiohttp
import disnake

###
# Функция получения статуса сервера
###
async def server_status(address):
    try:
        print(f"[INFO] {address}")
        # HTTP-запрос на сервер
        async with aiohttp.ClientSession() as session:
            async with session.get(address) as response:
                data = await response.json()

        # Формирование Embed ответа для последующей передачи боту.
        print(f"[INFO] {data}")
        embed = disnake.Embed(title="Статус игрового сервера Space Station 14", color=disnake.Color.green())
        embed.set_author(name=data['name'], icon_url="https://raw.githubusercontent.com/space-syndicate/space-station-14/master/Resources/Textures/Logo/icon/icon-128x128.png")
        embed.add_field(name="Игроки", value=f"Игроков {data['players']} из {data['soft_max_players']}", inline=False)
        # Проверка по статусу игры. Внутри неё ещё дополнительные проверки, тк некоторые сервера не присылают некоторые данные
        if data['run_level'] == 1:
            embed.add_field(name="Статус игры", value="Игра продолжается", inline=True)
            if 'preset' in data: 
                embed.add_field(name="Режим", value=data['preset'], inline=True)
            if 'map' in data: 
                embed.add_field(name="Карта", value=data['map'], inline=True)
            if 'round_id' in data: 
                embed.add_field(name="Текущий раунд", value=f"Раунд #{data['round_id']}", inline=True)
            if 'round_start_time' in data:
                converted = f"{(disnake.utils.utcnow() - disnake.utils.parse_time(data['round_start_time'])).total_seconds() // 60:.0f}"
                embed.add_field(name="Время раунда", value=f"Идёт {converted} минут", inline=True)
        elif data['run_level'] == 2:
            embed.add_field(name="Статус игры", value="Игра заканчивается - Манифест", inline=False)
            if 'round_start_time' in data:
                converted = f"{(disnake.utils.utcnow() - disnake.utils.parse_time(data['round_start_time'])).total_seconds() // 60:.0f}"
                embed.add_field(name="Время раунда", value=f"Он шёл {converted} минут", inline=True)
        else:
            embed.add_field(name="Статус игры", value="Игра не началась - Лобби", inline=False)
            if 'preset' in data: 
                embed.add_field(name="Предустановленный режим", value=data['preset'], inline=True)

        if data['tags']: 
            embed.add_field(name="Теги сервера", value=", ".join(data['tags']), inline=False)
        else:
            embed.add_field(name="Теги сервера", value="Не указаны", inline=False)

        if 'panic_bunker' in data: 
            embed.add_field(name="Режим бункера", value="Действует" if data['panic_bunker'] else "Отключён", inline=True)
        if 'baby_jail' in data: 
            embed.add_field(name="Режим тюрьмы", value="Действует" if data['baby_jail'] else "Отключён", inline=True) 
        return embed

    except Exception as e:
        embed = disnake.Embed(title="Ошибка", color=disnake.Color.red())
        embed.description = "В процессе выполнения программы, бот не смог совладать с управлением. Ошибка может заключаться в невозможности отправить запрос серверу. Убедитесь, что Вы ввели правильный адрес (тот, по которому вы подключаетесь к серверу), а сам сервер - работает. В ином случае, свяжитесь с разработчиком бота, ошибка была выведена в консоль."
        print(f"[ERRO АХТУНГ ДОЛБОЁБ ОШИБКИ СРАТЬ ЛЕС ЁЛКА СВЕТОФОР] {e}")
        return embed


