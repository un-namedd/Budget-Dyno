import os
import discord
import discord.ui
import time
import requests
import json
from discord import ButtonStyle
from discord.ui import View, Button
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

my_secret = 'MTE5MzUzOTY2MTc5NzI2NTQ4OA.G3z9S9.9VEY4HtK_SZzSEujuvpb88kpE_SKy0F0-SAapE'

intents = discord.Intents().all()
intents.messages = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

class RoleButton(Button):
    def __init__(self, role_name, emoji, row):
        super().__init__(style=ButtonStyle.grey, label="", custom_id=role_name, emoji=emoji, row=row)
        self.role_name = role_name

    async def callback(self, interaction):
        member = interaction.user
        role = discord.utils.get(interaction.guild.roles, name=self.role_name)
        if role in member.roles:
            await member.remove_roles(role)
            emb = discord.Embed(title="Role Update!",
                                description=f"Removed {role.mention}",
                                color=discord.Color.blue())
            await interaction.response.send_message(embed=emb, ephemeral=True)
        else:
            await member.add_roles(role)
            emb2 = discord.Embed(title="Role Update!",
                                description=f"Added {role.mention}",
                                color=discord.Color.blue())
            await interaction.response.send_message(embed=emb2, ephemeral=True)

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleButton("Top", "<:topl:1193209344968368189>", row=0))
        self.add_item(RoleButton("Jungle", "<:jungle:1193210201759817829>", row=0))
        self.add_item(RoleButton("Mid", "<:mid:1193209803145752639>", row=0))
        self.add_item(RoleButton("Adc", "<:bot:1193209950462279900>", row=1))
        self.add_item(RoleButton("Support", "<:supp:1193210180658274396>", row=1))
        self.add_item(RoleButton("Fill", "<:fill:1193210237109420063>", row=1))

@bot.command()
async def menu2(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar

    embed = discord.Embed(title="What role(s) do you play?",
                          description="",
                          colour=0xFF0000)
    embed.set_author(
        name="Intsuo",
        icon_url="https://cdn.discordapp.com/avatars/769070942440914946/b1d3dc88c77b4d96adfc8a899e4c4838.webp?size=80")
    embed.add_field(name="<:topl:1193209344968368189> Top",
                    value="",
                    inline=False)
    embed.add_field(name="<:jungle:1193210201759817829> Jungle",
                    value="",
                    inline=False)
    embed.add_field(name="<:mid:1193209803145752639> Mid",
                    value="",
                    inline=False)
    embed.add_field(name="<:bot:1193209950462279900> Adc",
                    value="",
                    inline=False)
    embed.add_field(name="<:supp:1193210180658274396> Support",
                    value="",
                    inline=False)
    embed.add_field(name="<:fill:1193210237109420063> Fill",
                    value="",
                    inline=False)

    msg = await ctx.send(embed=embed, view=RoleView())


class MySelect(View):

  @discord.ui.select(
      placeholder="Choose an option",
      options=[
          discord.SelectOption(label="Challenger",
                               value="1",
                               description="Pick this if you're Challenger.",
                               emoji="<:challenger:1193213213152641124>"),
          discord.SelectOption(label="Grandmaster",
                               value="2",
                               description="Pick this if you're Grandmaster.",
                               emoji="<:grandmaster:1193213814586490980>"),
          discord.SelectOption(label="Master",
                               value="3",
                               description="Pick this if you're Masters.",
                               emoji="<:master:1193213238616272950>"),
          discord.SelectOption(label="Diamond",
                               value="4",
                               description="Pick this if you're Diamond.",
                               emoji="<:diamond:1193213838141693973>"),
          discord.SelectOption(label="Emerald",
                               value="5",
                               description="Pick this if you're Emerald.",
                               emoji="<:emerald:1193298992000401409>"),
          discord.SelectOption(label="Platinum",
                               value="6",
                               description="Pick this if you're Platinum.",
                               emoji="<:platinum:1193213880554500218>"),
          discord.SelectOption(label="Gold",
                               value="7",
                               description="Pick this if you're Gold.",
                               emoji="<:gold:1193213912439607316>"),
          discord.SelectOption(label="Silver",
                               value="8",
                               description="Pick this if you're Silver.",
                               emoji="<:silver:1193213895029035008>"),
          discord.SelectOption(label="Bronze",
                               value="9",
                               description="Pick this if you're Bronze.",
                               emoji="<:bronze:1193213933625032864>"),
          discord.SelectOption(label="Iron",
                               value="10",
                               description="Pick this if you're Iron.",
                               emoji="<:iron:1193213193212940429>"),
          discord.SelectOption(label="Unranked",
                               value="11",
                               description="Pick this if you're Unranked."),
          discord.SelectOption(label="Remove rank role",
                               value="12",
                               description="Pick this if you want to remove any rank you previously picked (from this list).",
                               emoji="\u274C")
      ])
  async def select_callback(self, interaction, select):
    select.disabled = True
    user = interaction.user
    guild = interaction.guild

    # Define a list with the names of all rank roles
    rank_roles = ["Unranked", "Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Masters", "Grand Master", "Challenger"]

    # Remove all existing rank roles from the user and keep track of the removed role
    removed_role = None
    for rank in rank_roles:
        role = discord.utils.get(guild.roles, name=rank)
        if role in user.roles:
            await user.remove_roles(role)
            removed_role = role

    # Add the newly selected role to the user
    new_role = None
    if select.values[0] == "1":
        new_role = discord.utils.get(guild.roles, name="Challenger")
    elif select.values[0] == "2":
        new_role = discord.utils.get(guild.roles, name="Grand Master")
    elif select.values[0] == "3":
        new_role = discord.utils.get(guild.roles, name="Masters")
    elif select.values[0] == "4":
        new_role = discord.utils.get(guild.roles, name="Diamond")
    elif select.values[0] == "5":
        new_role = discord.utils.get(guild.roles, name="Emerald")
    elif select.values[0] == "6":
        new_role = discord.utils.get(guild.roles, name="Platinum")
    elif select.values[0] == "7":
        new_role = discord.utils.get(guild.roles, name="Gold")
    elif select.values[0] == "8":
        new_role = discord.utils.get(guild.roles, name="Silver")
    elif select.values[0] == "9":
        new_role = discord.utils.get(guild.roles, name="Bronze")
    elif select.values[0] == "10":
        new_role = discord.utils.get(guild.roles, name="Iron")
    elif select.values[0] == "11":
        new_role = discord.utils.get(guild.roles, name="Unranked")

    if new_role:
      await user.add_roles(new_role)
      if removed_role:
          embed = discord.Embed(title="Rank Update!", description=f"Removed {removed_role.mention}!\n\nAdded {new_role.mention}!", color=discord.Color.blue())
          await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
          embed = discord.Embed(title="Rank Update!", description=f"Added {new_role.mention}!", color=discord.Color.blue())
          await interaction.response.send_message(embed=embed, ephemeral=True)
    elif select.values[0] == "12":
        await interaction.response.send_message("Removed all ranks!", ephemeral=True)

@bot.command()
async def menu(ctx):
    emb = discord.Embed(title="What's your current rank in the game?",
                          description="",
                          colour=0xFF0000)
    emb.set_author(
    name="Intsuo",
    icon_url="https://cdn.discordapp.com/avatars/769070942440914946/b1d3dc88c77b4d96adfc8a899e4c4838.webp?size=80")
    view = MySelect()
    view.timeout = None
    await ctx.send(embed=emb, view=view)

@bot.slash(name="role_remove", description="Remove a role from a user.")
async def role_remove(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if interaction.user.guild_permissions.administrator or any(role.name == "admins" for role in interaction.user.roles):
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Successfully removed role {role.name} from {member.name}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{member.name} does not have the role {role.name}.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True

bot.run('MTE5MzUzOTY2MTc5NzI2NTQ4OA.G3z9S9.9VEY4HtK_SZzSEujuvpb88kpE_SKy0F0-SAapE')
