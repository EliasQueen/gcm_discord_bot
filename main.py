import os
import discord
from discord import app_commands
from discord.app_commands import Choice
from db_controller import database_controller
from commission_data_controller import commission_data_controller

import sys
sys.stdout.reconfigure(encoding='utf-8')

MY_GUILD = discord.Object(id=1048702554302853120)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

db_controller = database_controller()
cd_controller = commission_data_controller()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('---------------------------------------------------')

@client.tree.command()
async def locale(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.locale)

@client.tree.command()
async def hello(interaction: discord.Interaction):
    msg = language_handler(check_language(str(interaction.locale)))
    await interaction.response.send_message(msg + interaction.user.mention)

@client.tree.command()
@app_commands.rename(pais='país')
@app_commands.describe(pais='Selecione o país desejado')
@app_commands.choices(pais=[
    Choice(name = 'Mondstadt', value = 1),
    Choice(name = 'Liyue', value = 2),
    Choice(name = 'Inazuma', value = 3),
    Choice(name = 'Sumeru', value = 4),
    Choice(name = 'Fontaine', value = 5),
])
async def listar(interaction: discord.Interaction, pais: int):
    language_id = check_language(str(interaction.locale))
    msg = db_controller.readCommissionList(interaction.user.id, pais, language_id)
    # print(msg)
    # commission_list_handler(msg)

    embed = cd_controller.commission_list_embed_creator(interaction, pais)
    
    await interaction.response.send_message(embed=embed)
    # msg = controller.readCommissionList(pais)
    # await interaction.response.send_message(msg)
    # await interaction.response.send_message(f"{interaction.user.id}, {pais}, {language_id}")
    # await interaction.response.send_message("...")


@client.tree.command()
@app_commands.rename(commission_id='id')
@app_commands.describe(commission_id='Digite o ID da comissão a ser marcada como feita')
async def marcar(interaction: discord.Interaction, commission_id: int):
    await interaction.response.send_message(commission_id)


@client.tree.command()
@app_commands.rename(commission_id='id')
@app_commands.rename(repetitions_value='valor')
@app_commands.describe(commission_id='Digite o ID da comissão que quer atualizar')
@app_commands.describe(repetitions_value='Digite a nova quantidade de repetições que foram concluídas')
async def atualizar(interaction: discord.Interaction, commission_id: int, repetitions_value: int):
    await interaction.response.send_message(commission_id)


@client.tree.command()
@app_commands.rename(pais='país')
@app_commands.describe(pais='Selecione o país desejado')
@app_commands.choices(pais=[
    Choice(name = 'Mondstadt', value = 1),
    Choice(name = 'Liyue', value = 2),
    Choice(name = 'Inazuma', value = 3),
    Choice(name = 'Sumeru', value = 4),
    Choice(name = 'Fontaine', value = 5),
])
async def resetar_ciclo(interaction: discord.Interaction, pais: int):
    await interaction.response.send_message(pais)


def check_language(language_code):
    match (language_code):
        case 'pt-BR':
            return 1
        case _:
            return 2


def language_handler(language_id):
    match (language_id):
        case 1:
            return 'Olá, '
        case _:
            return 'Hi, '


# Carrega as variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Obtém o token do bot a partir da variável de ambiente
my_secret = os.getenv('DISCORD_BOT_SECRET')

# Inicia o bot
client.run(my_secret)
