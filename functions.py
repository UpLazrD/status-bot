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
        embed.add_field(name="Игровой сервер", value=data['name'], inline=False)
        embed.add_field(name="Игроки", value=f"Игроков {data['players']} из {data['soft_max_players']}", inline=False)
        
        if data['run_level'] == 1:
            embed.add_field(name="Статус игры", value="Игра продолжается", inline=True)
            if 'preset' in data: embed.add_field(name="Режим", value=data['preset'], inline=True)
            if 'map' in data: embed.add_field(name="Карта", value=data['map'], inline=True)
            if'round_id' in data: embed.add_field(name="Текущий раунд", value=f"Раунд #{data['round_id']}", inline=True)
            embed.add_field(name="Время раунда", value=f"{(disnake.utils.utcnow() - disnake.utils.parse_time(data['round_start_time'])).total_seconds() // 60:.0f} минут назад", inline=True)
        elif data['run_level'] == 2:
            embed.add_field(name="Статус игры", value="Игра заканчивается (Манифест)", inline=False)
        else:
            embed.add_field(name="Статус игры", value="Игра не началась (Лобби)", inline=False)
            
        if data['tags']: embed.add_field(name="Теги сервера", value=", ".join(data['tags']), inline=False)
        if 'panic_bunker' in data: embed.add_field(name="Режим бункера", value="Действует" if data['panic_bunker'] else "Отключён", inline=True)
        if 'baby_jail' in data: embed.add_field(name="Режим тюрьмы", value="Действует" if data['baby_jail'] else "Отключён", inline=True) 
        return embed

    except Exception as e:
        embed = disnake.Embed(title="Ошибка", color=disnake.Color.red())
        embed.description = "В процессе выполнения программы, бот не смог совладать с управлением. Ошибка может заключаться в невозможности отправить запрос серверу. Убедитесь, что Вы ввели правильный адрес (тот, по которому вы подключаетесь к серверу), а сам сервер - работает. В ином случае, свяжитесь с разработчиком бота, ошибка была выведена в консоль."
        print(f"[ERRO АХТУНГ ДОЛБОЁБ ОШИБКИ СРАТЬ ЛЕС ЁЛКА СВЕТОФОР] {e}")
        return embed


