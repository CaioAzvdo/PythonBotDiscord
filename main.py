import discord
import os
import httpx

from discord.app_commands import guilds
from dotenv import load_dotenv
load_dotenv()
from discord import app_commands
class main(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="c",
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} Bot started!")


bot = main()

@bot.tree.command(name="olamundo", description="comando olá mundo")
async def ola_mundo(interaction:discord.Interaction):
    await interaction.response.send_message(f"Olá {interaction.user.mention}!")


#comando pra atribuir uma role especifica de um servidor especifico, acho que isso é muito especifico
@bot.tree.command(name="cargofoda", description="comando para se tornar foda")
async def cargo_foda(interaction:discord.Interaction, user: discord.Member):
    role = interaction.guild.get_role(1343633150760194098)
    if role:
        await user.add_roles(role)
        await interaction.response.send_message(f"O cargo {role.name} foi atribuido")
    else:
        await interaction.response.send_message("Deu bom não meu jovem")
    await interaction.response.send_message(f"{interaction.user.mention} agora é foda!",ephemeral = True)


@bot.tree.command(name="criar_cargo", description="comando para criação de role")
@app_commands.describe(
    role_name="O nome do cargo novo"
)
async def criar_cargo(interaction:discord.Interaction, user: discord.Member, role_name : str):
    guild = interaction.guild
    role = await guild.create_role(name=role_name)
    await interaction.response.send_message(f"A role {role.name} foi criada com sucesso! e atribuida a {user.mention}", ephemeral=True)
    await user.add_roles(role)

@bot.tree.command(name="enviar_saudacoes", description="comando para envio de embed")
async def enviar_embed(interaction:discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="Saudações! Eu me chamo Curi", description="Espero ser útil a você!", color=0x00ff00)
    embed.set_image(url='https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_1.5/c_scale,w_400/ncom/software/switch/70010000033003/cb6c1e805897d052d805039418fb6e7b3ef738e9222f3ff407088b7bd69ea294')
    # embed.add_field(name="Campo 1", value="Valor do Campo 1", inline=False)
    # embed.add_field(name="Campo 2", value="Valor do Campo 2", inline=False)

    await user.send(embed=embed)
    await interaction.response.send_message(f"Embed enviado para {user.mention}", ephemeral=True)


@bot.tree.command(name="criar_chat_voz", description="crie um chat de voz agora mesmo!")
async def criar_chat_voz(interaction:discord.Interaction, nome_chat:str):
    guild = interaction.guild
    await guild.create_voice_channel(name=f"{nome_chat}")
    await interaction.response.send_message(f"Canal de voz criado com sucesso!", ephemeral=True)

@bot.tree.command(name="criar_chat_texto", description="crie um chat de texto agora mesmo!")
async def criar_chat_voz(interaction:discord.Interaction, nome_chat:str):
    guild = interaction.guild
    text_channel = await guild.create_text_channel(name=f"{nome_chat}")
    await text_channel.send("Sou o First! seu panaca")
    await interaction.response.send_message(f"Canal de texto criado com sucesso!", ephemeral=True)


@bot.tree.command(name="buscar_pokemon", description="Pesquise por Pokemons!")
async def buscar_pokemon(interaction:discord.Interaction, nome_pokemon:str):
    async with httpx.AsyncClient() as client:
        url = f"https://pokeapi.co/api/v2/pokemon/{nome_pokemon.lower()}"
        response = await client.get(url)
        embed = discord.Embed(title=f"Parabéns! Você encontrou um {nome_pokemon} selvagem!", description="Tome cuidado! esse Pokemon selvagem parece um pouco bravo.",color=0x00ff00)

        if response.status_code == 200:
            pokemon_data = response.json()
            pokemon_img = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
            name = pokemon_data["name"].upper()
            ability = pokemon_data["abilities"][0]["ability"]["name"].upper()
            embed.set_image(url=pokemon_img)
            # embed.set_thumbnail(url=pokemon_img)
            embed.add_field(name=f"Nome do Pokemon: ", value=name, inline=False)
            embed.add_field(name="Habilidade: ", value=ability, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Pokemon não encontrado.", ephemeral=True)




bot.run(os.getenv("DISCORD_TOKEN_API"))