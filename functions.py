import aiohttp
import disnake
import random
from collection import godness
import json
import asyncio

###
# Функция получения статуса сервера
###
async def server_status(address):
    try:
        # HTTP-запрос на сервер
        print(f"[LOG] {address}")
        timeout = aiohttp.ClientTimeout(total=15)  # Общее время ожидания ответа - 15 секунд
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(address) as response:
                data = await response.json()

        # Формирование Embed ответа для последующей передачи боту.
        print(f"[LOG] {data}")
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

        if 'tags' in data:
            embed.add_field(name="Теги сервера", value=", ".join(data['tags']) if data['tags'] else "Не указаны", inline=False)
        if 'panic_bunker' in data:
            embed.add_field(name="Режим бункера", value="Действует" if data['panic_bunker'] else "Отключён", inline=True)
        return embed
    
    except (asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ClientConnectionError) as e:
        embed = disnake.Embed(title="<:tokarni_stanok:1001097402868039791> Ошибка подключения", color=disnake.Color.red())
        embed.description = "Сервер не работает, либо был введён неправильный адрес. Перепроверьте введённые данные и попробуйте снова."
        print(f"[ERRO] Ошибка подключения: {e}")
        return embed
 
    except json.decoder.JSONDecodeError as e:
        embed = disnake.Embed(title="<:tokarni_stanok:1001097402868039791> Ошибка декодирования", color=disnake.Color.red())
        embed.description = "Не удалось декодировать ответ с сервера. Надеюсь, вы указали не адрес SS13 или чего-то подобного, если нет, то свяжитесь с разработчиком бота."
        print(f"[ERRO] Ошибка декодирования: {e}")
        return embed
    
    except Exception as e:
        embed = disnake.Embed(title="<:tokarni_stanok:1001097402868039791> Сбой в программе", color=disnake.Color.red())
        embed.description = "Случилась непредвиденная ошибка в работе бота. Проверьте правильность введённых данных, в ином случае свяжитесь с разработчиком бота."
        print(f"[ERRO] Иная ошибка: {e}")
        return embed
    
    


async def skibidi_station():
    embed = disnake.Embed(title="ЩКЕБЕДЕ ДОП ДОП ЕС ЕС", color=disnake.Color.yellow())
    embed.set_image(url="https://media.tenor.com/WhXYjpREz1kAAAAM/skibidi-toilet-skibidi.gif")
    embed.set_thumbnail(url="https://steamuserimages-a.akamaihd.net/ugc/2038494310206033069/2FFBA39BB754CF0D0FC83C62636BAE30BE992758/")
    embed.description = "Бррр, щкебеде, доп доп доп, ес ес \nСкибиди дабиди да дап \nSkibidi, dom-dom-dom, yes-yes \nSkibidi-dabudu, nib-nib \nWe ain't here to hurt nobody (skibidi, skibidi, skibidi) \nWanna see you work your body (skibidi, skibidi, skibidi)"
    return embed
    # этот мир больше не спасти

async def e621_troll():
    embed = disnake.Embed(title="Бог недоволен тобой", color=disnake.Color.red())
    embed.set_image(url=random.choice(godness))
    return embed

