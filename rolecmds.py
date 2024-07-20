import os
import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

Admin = os.getenv("Admin_ID")
Aram = os.getenv("Aram_ID")

class rolecmds(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="roleremove", description="Remove a role from a user.")
    async def role_remove(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if discord.utils.get(interaction.user.roles):
            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(title="User Update:", color=role.color)
                embed.add_field(name="Role Removed", value=f"Successfully removed role <@&{role.id}> from {member.mention}.", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", color=role.color)
                embed.add_field(name="User Role Not Found", value=f"{member.mention} does not have the role <@&{role.id}>.", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Invalid Permissions.", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="Permission Required", value=("You do not have sufficient permissions to use this command."), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="roleadd", description="Add a role to a user.")
    async def role_add(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if discord.utils.get(interaction.user.roles):
            if role not in member.roles:
                await member.add_roles(role)
                embed = discord.Embed(title="User Update:", color=role.color)
                embed.add_field(name="Role Added", value=f"Successfully added role <@&{role.id}> from {member.mention}.", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", color=role.color)
                embed.add_field(name="Role Error", value=f"{member.mention} already has the role <@&{role.id}>.", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=f"Invalid Permissions.", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="Permission Required", value=("You do not have sufficient permissions to use this command."), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="roleinfo", description="Get information about a role.")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        if discord.utils.get(interaction.user.roles):
            mention_text = f"<@&{role.id}>" if role.mentionable else "Not mentionable"
            
            embed = discord.Embed(title=f"Role Information:", color=role.color) 
            embed.add_field(name="ID", value=str(role.id), inline=False)
            embed.add_field(name="Role Name", value=f"<@&{role.id}>", inline=False)
            embed.add_field(name="Mention", value=mention_text, inline=False)
            embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=False)
            embed.add_field(name="Position", value=str(role.position), inline=False)
            embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=False)
            permissions = [permission[0] for permission in role.permissions if permission[1]]
            embed.add_field(name="Key Permissions", value=", ".join(permissions), inline=False)

            creation_date = role.created_at.strftime("%B %d, %Y")
            embed.set_footer(text=f"Role Created • {creation_date}")

            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=f"Invalid Permissions.", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="Permission Required", value=("You do not have sufficient permissions to use this command."), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(rolecmds(client))