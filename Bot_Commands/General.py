@bot.tree.command(name="nick", description="Change the nickname of a user.")
async def nick(interaction: discord.Interaction, member: discord.Member, nickname: str):
    if discord.utils.get(interaction.user.roles, id=Aram):
        await member.edit(nick=nickname)
        embed=discord.Embed(title="User Update:", color='black')
        embed.add_field(name="Nick Change", value=f"Successfully changed {member.mention}'s nickname to {nickname}.", ephemeral=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=f"Invalid Permissions.", color='black')
        embed.add_field(name="Permission Required", value=("You do not have permission to use this command."), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)