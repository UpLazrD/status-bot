# < Сторонние библиотеки >
import os
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

# < Файлы проекта >
from collection import servers1, servers2
from functions import *

load_dotenv('secret.env')
bot = commands.Bot(command_prefix = '!', intents = disnake.Intents.all())

@bot.event
async def on_ready():
    print(f"[INFO] Великий {bot.user} готов к работе")
    activity = disnake.Game(name = 'Schizo Station 14')
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
    if адрес.startswith("ss14://"):
        адрес = "http://" + адрес[7:]
    elif адрес.startswith("ss14s://"):
       адрес = "https://" + адрес[8:]

    await interaction.response.defer()
    embed = await server_status(адрес + '/status')
    await interaction.edit_original_response(embed=embed)


# Троллинг ГРЕШНИКОВ
@bot.slash_command(name='e621', description = "[18+] Получить рандомную фурри-картинку из источника e621")
async def furry_troll(inter):
    embed = await e621_troll()
    await inter.response.send_message(embed=embed)

# Бароны.
@bot.slash_command(name="кальян", description = "Выпустить дух чарона")
async def kalyan(inter):
    embed = disnake.Embed(title="", color=disnake.Color.yellow())
    embed.set_author(name=f'{inter.author.display_name} выпускает дух чарона!', icon_url=inter.author.avatar.url)
    embed.description = f'{inter.author.display_name} решил затянуться делюкс кальяном с гравировкой **"Нищим здесь не место!"**'
    await inter.response.send_message(embed=embed)


# Камень Ножницы Бумага!
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Червы', 'Бубны', 'Трефы', 'Пики']
                      for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Королева', 'Король', 'Туз']]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.players_hand = []
        self.dealers_hand = []

    def deal_initial_cards(self):
        self.players_hand.append(self.deck.draw_card())
        self.dealers_hand.append(self.deck.draw_card())
        self.players_hand.append(self.deck.draw_card())
        self.dealers_hand.append(self.deck.draw_card())

    def show_hands(self, reveal_dealer=False):
        dealer_hand = "Скрыта, " + str(self.dealers_hand[1]) if not reveal_dealer else ", ".join(map(str, self.dealers_hand))
        player_hand = ", ".join(map(str, self.players_hand))
        return f"Рука дилера: {dealer_hand}\nРука игрока: {player_hand}"

@bot.slash_command(name='блекджэк', description="Играй в Blackjack прямо в Discord!")
async def blackjack(inter: disnake.ApplicationCommandInteraction):
    game = Blackjack()
    game.deal_initial_cards()
    message = game.show_hands()
    await inter.response.send_message(message)


bot.run(os.getenv('SECRET_TOKEN'))