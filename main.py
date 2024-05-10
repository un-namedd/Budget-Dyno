import discord
import discord.ui
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents().all()
intents.messages = True
intents.reactions = True
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="you rn.")

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all(), status = discord.Status.do_not_disturb, activity=activity)


@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#########################################################################################################################################
######################################################       Roles       ################################################################
#########################################################################################################################################

@bot.tree.command(name="role_remove", description="Remove a role from a user.")
async def role_remove(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=1145872122992930907):
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Successfully removed role <@&{role.id}> from @{member.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{member.mention} does not have the role <@&{role.id}>.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="role_add", description="Add a role to a user.")
async def role_add(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=1145872122992930907):
        if role not in member.roles:
            await member.add_roles(role)
            await interaction.response.send_message(f"Successfully added role <@&{role.id}> to @{member.mention}.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{member.mention} already has the role <@&{role.id}>.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="role_info", description="Get information about a role.")
async def role_info(interaction: discord.Interaction, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=1145872122992930907):
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

        # Format the creation date
        creation_date = role.created_at.strftime("%B %d, %Y")
        embed.set_footer(text=f"Role Created • {creation_date}")

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

#########################################################################################################################################
######################################################        Nick       ################################################################
#########################################################################################################################################

@bot.tree.command(name="nick", description="Change the nickname of a user.")
async def nick(interaction: discord.Interaction, member: discord.Member, nickname: str):
        await member.edit(nick=nickname)
        await interaction.response.send_message(f"Successfully changed {member.name}'s nickname to {nickname}.", ephemeral=True)

bot.run('MTE5MzUzOTY2MTc5NzI2NTQ4OA.G3z9S9.9VEY4HtK_SZzSEujuvpb88kpE_SKy0F0-SAapE')