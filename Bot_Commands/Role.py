@bot.tree.command(name="role_remove", description="Remove a role from a user.")
async def role_remove(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=Aram):
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
        embed = discord.Embed(title="Invalid Permissions.", color='black')
        embed.add_field(name="Permission Required", value=("You do not have permission to use this command."), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="role_add", description="Add a role to a user.")
async def role_add(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=Aram):
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
        embed = discord.Embed(title=f"Invalid Permissions.", color='black')
        embed.add_field(name="Permission Required", value=("You do not have permission to use this command."), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="role_info", description="Get information about a role.")
async def role_info(interaction: discord.Interaction, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=Aram):
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
        embed = discord.Embed(title=f"Invalid Permissions.", color='black')
        embed.add_field(name="Permission Required", value=("You do not have permission to use this command."), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)