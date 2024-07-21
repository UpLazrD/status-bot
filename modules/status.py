# <!-- БИБЛИОТЕКИ -->
import disnake
from disnake.ext import commands
import aiohttp
import asyncio
import json

# <!-- ФАЙЛЫ ПРОЕКТА -->
from .collection import servers1, servers2


class ServerStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # <!-- ГЛАВНАЯ ФУНКЦИЯ ЭТОГО КОГА, МАТЬ ВАШУ! -->
    async def server_status(self, address):
        try:
            # HTTP-запрос на игровой сервер
            print(f"[LOG] {address}")
            timeout = aiohttp.ClientTimeout(total=10)  # Общее время ожидания ответа - 10 секунд
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(address) as response:
                    data = await response.json()

            # Формирование Embed ответа для последующей передачи боту.
            print(f"[LOG] {data}")
            embed = disnake.Embed(title="Статус игрового сервера Space Station 14", color=disnake.Color.green())
            embed.set_author(name=data['name'], icon_url="https://raw.githubusercontent.com/space-syndicate/space-station-14/master/Resources/Textures/Logo/icon/icon-128x128.png")
            embed.add_field(name="Игроки", value=f"Игроков {data['players']} из {data['soft_max_players']}", inline=False)
            
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
            embed = disnake.Embed(title="<:tokarni_stanok:1001097402868039791> Ошибка в программе", color=disnake.Color.red())
            embed.description = "Случилась непредвиденная ошибка в работе бота. Проверьте правильность введённых данных, в ином случае свяжитесь с разработчиком бота."
            print(f"[ERRO] Иная ошибка: {e}")
            return embed


    # Статус Церберов
    @commands.slash_command(name='статус_церберы', description = "Получить статус сервера Cerberus Space")
    async def status_command_cerberus(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()
        embed = await self.server_status("http://194.93.2.178:1212/status")
        await interaction.edit_original_response(embed=embed)


    # Команда для получения статуса из словаря
    @commands.slash_command(name='статус_1', description = "Получить статус сервера Space Station 14 из первого предложенного списка")
    async def status_command_dict1(self, interaction: disnake.ApplicationCommandInteraction,
        адрес: str = commands.Param( 
            description = "Выберите сервер из предложенного списка",
            choices = servers1)):
        await interaction.response.defer()
        embed = await self.server_status(адрес)
        await interaction.edit_original_response(embed=embed)


    @commands.slash_command(name='статус_2', description = "Получить статус сервера Space Station 14 из второго предложенного списка")
    async def status_command_dict2(self, interaction: disnake.ApplicationCommandInteraction,
        адрес: str = commands.Param(
            description = "Выберите сервер из предложенного списка",
            choices = servers2)):
        await interaction.response.defer()
        embed = await self.server_status(адрес)
        await interaction.edit_original_response(embed=embed)


    # Команда для получения статуса, но уже вручную
    @commands.slash_command(name='статус_вручную', description = "Получить статус сервера Space Station 14, введя его адрес")
    async def status_command_manually(self, interaction: disnake.ApplicationCommandInteraction,
        адрес: str = commands.Param(
            description = "Введите адрес сервера - тот, по которому вы подключаетесь к игре")):
        if адрес.startswith("ss14://"):
            адрес = "http://" + адрес[7:]
        elif адрес.startswith("ss14s://"):
            адрес = "https://" + адрес[8:]

        await interaction.response.defer()
        embed = await self.server_status(адрес + '/status')
        await interaction.edit_original_response(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ServerStatus(bot))