import os
import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

Aram = os.getenv('Aram_ID')
Admin = os.getenv('Admin_ID')
Owner = os.getenv('Owner')

class generalcmds(commands.Cog):
    
    def __innit__(self, client:commands.Bot):
        self.client = client

    @app_commands.command(name="nick", description="Change the nickname of a user.")
    @commands.is_owner()
    async def nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        if discord.utils.get(interaction.user.roles):
            await member.edit(nick=nickname)
            embed=discord.Embed(title="User Update:", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="Nick Change", value=f"Successfully changed {member.name}'s nickname to {member.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=f"Invalid Permissions.", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="Permission Required", value=("You do not have sufficient permissions to use this command."), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(generalcmds(client))