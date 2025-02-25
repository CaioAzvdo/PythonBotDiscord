import discord
import os

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
async def olaMundo(interaction:discord.Interaction):
    await interaction.response.send_message(f"Olá {interaction.user.mention}!")

@bot.tree.command(name="soma", description="comando para somar dois numeros")
@app_commands.describe(
    number1 = "Primeiro número a somar",
    number2 = "Segundo número a somar"
)
async def olaMundo(interaction:discord.Interaction, number1:int, number2:int):
    result = number1 + number2
    await interaction.response.send_message(f"O resultado é igual a {result} {interaction.user.mention}",ephemeral = True)

@bot.tree.command(name="cargofoda", description="comando para se tornar foda")
async def cargoFoda(interaction:discord.Interaction, user: discord.Member):
    # role = interaction.guild.get_role(role_id)
    role = interaction.guild.get_role(1343633150760194098)
    if role:
        # await user.add_roles(role)
        await user.add_roles(role)
        await interaction.response.send_message(f"O cargo {role.name} foi atribuido")
    else:
        await interaction.response.send_message("Deu bom não meu jovem")
    # await user.add_roles(1343633150760194098)
    await interaction.response.send_message(f"{interaction.user.mention} agora é foda!",ephemeral = True)


@bot.tree.command(name="criar_cargo", description="comando para criação de role")
@app_commands.describe(
    role_name="O nome do cargo novo"
)
async def criarCargo(interaction:discord.Interaction, user: discord.Member, role_name : str):
    guild = interaction.guild
    role = await guild.create_role(name=role_name)
    await interaction.response.send_message(f"A role {role.name} foi criada com sucesso! e atribuida a {user.mention}", ephemeral=True)
    await user.add_roles(role)

@bot.tree.command(name="enviar_saudacoes", description="comando para envio de embed")
async def enviar_embed(interaction:discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="Saudações! eu me chamo Curi", description="Espero ser útil a você!", color=0x00ff00)
    embed.set_image(url='https://assets.nintendo.com/image/upload/ar_16:9,b_auto:border,c_lpad/b_white/f_auto/q_auto/dpr_1.5/c_scale,w_400/ncom/software/switch/70010000033003/cb6c1e805897d052d805039418fb6e7b3ef738e9222f3ff407088b7bd69ea294')
    # embed.add_field(name="Campo 1", value="Valor do Campo 1", inline=False)
    # embed.add_field(name="Campo 2", value="Valor do Campo 2", inline=False)

    await user.send(embed=embed)
    await interaction.response.send_message(f"Embed enviado para {user.mention}", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN_API"))