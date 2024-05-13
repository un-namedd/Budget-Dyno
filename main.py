import discord
import discord.ui
import aiohttp
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

#Roles, User ID's
admin_role_id = 1145872122992930907
me_intsuo = 769070942440914946
API_KEY = "RGAPI-add7ff21-eb59-496f-9c5b-f1af7642438a"

intents = discord.Intents().all()
intents.messages = True
intents.reactions = True
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="you rn.")

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all(), status = discord.Status.do_not_disturb, activity=activity)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="role_remove", description="Remove a role from a user.")
async def role_remove(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if discord.utils.get(interaction.user.roles, id=admin_role_id):
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
    if discord.utils.get(interaction.user.roles, id=admin_role_id):
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
    if discord.utils.get(interaction.user.roles, id=admin_role_id):
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


@bot.tree.command(name="nick", description="Change the nickname of a user.")
async def nick(interaction: discord.Interaction, member: discord.Member, nickname: str):
    if discord.utils.get(interaction.user.roles, id=admin_role_id):
        await member.edit(nick=nickname)
        embed=discord.Embed(title="User Update:", color='black')
        embed.add_field(name="Nick Change", value=f"Successfully changed {member.mention}'s nickname to {nickname}.", ephemeral=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title=f"Invalid Permissions.", color='black')
        embed.add_field(name="Permission Required", value=("You do not have permission to use this command."), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="league_stats", description="EUW only. Get info about the given player. e.g Name: Budget Yasuo | (No #) tag: OwO)")
async def summoner(interaction: discord.Interaction, ign: str, tag: str):
    ign.lower()
    ign.capitalize()
    summoner_id = None
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{ign}/{tag}?api_key={API_KEY}") as resp:
            if resp.status == 200:
                data = await resp.json()
                summoner_puuid = data["puuid"]
                
                async with session.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{summoner_puuid}?api_key={API_KEY}") as ign_tag:
                    if ign_tag.status == 200:
                        ign_tag = await ign_tag.json()
                        ign = ign_tag["gameName"]
                        tag = ign_tag["tagLine"]
                        
                        async with session.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{summoner_puuid}?api_key={API_KEY}") as encrypted_id_resp:
                            if encrypted_id_resp.status == 200:
                                league_v4_resp = await encrypted_id_resp.json()
                                summoner_id = league_v4_resp["id"]
                                
                                async with session.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_puuid}/top?count=3&api_key={API_KEY}") as mastery_resp:
                                    if mastery_resp.status == 200:
                                        mastery_data = await mastery_resp.json()

                                        top_champions = sorted(mastery_data, key=lambda x: x["championPoints"], reverse=True)[:3]

                                        champ_1_mastery = "{:,}".format(top_champions[0]["championPoints"])
                                        champ_2_mastery = "{:,}".format(top_champions[1]["championPoints"])
                                        champ_3_mastery = "{:,}".format(top_champions[2]["championPoints"])
                                        
                                        champ_1 = str(top_champions[0]["championId"])
                                        champ_2 = str(top_champions[1]["championId"])
                                        champ_3 = str(top_champions[2]["championId"])

                                        async with session.get(f"https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion.json") as champ_resp:
                                            if champ_resp.status == 200:
                                                champ_data = await champ_resp.json()

                                                champion_name_key_map = {}

                                                for champion_name, champion_info in champ_data["data"].items():
                                                    champion_key = champion_info["key"]
                                                    champion_name_key_map[champion_key] = champion_name

                                                champion_name_1 = champion_name_key_map[champ_1]
                                                champion_name_2 = champion_name_key_map[champ_2]
                                                champion_name_3 = champion_name_key_map[champ_3]
                                                    
                                                async with session.get(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={API_KEY}") as rank_resp:
                                                    if rank_resp.status == 200:
                                                        rank_data = await rank_resp.json()

                                                        ranked_flex = None
                                                        wins_flex = 0
                                                        losses_flex = 0
                                                        Lp_flex = 0

                                                        ranked_solo_duo = ""
                                                        wins_solo_duo = 0
                                                        losses_solo_duo = 0
                                                        Lp_solo_duo = 0

                                                        for entry in rank_data:
                                                            if entry["queueType"] == "RANKED_SOLO_5x5":
                                                                ranked_solo_duo = entry["tier"].lower().capitalize() + " " + entry["rank"]
                                                                if "Iron" in ranked_solo_duo:
                                                                    ranked_solo_duo = "<:platinum:1193213880554500218> " + entry["tier"].capitalize() + " " + entry["rank"]
                                                                    
                                                                elif "Platinum" in ranked_solo_duo:
                                                                    ranked_solo_duo = "<:platinum:1193213880554500218> " + entry["tier"].capitalize() + " " + entry["rank"]
                                                                    
                                                                else:
                                                                    ranked_solo_duo = entry["tier"].lower().capitalize() + " " + entry["rank"]
                                                                Lp_solo_duo = entry["leaguePoints"]
                                                                wins_solo_duo = entry["wins"]
                                                                losses_solo_duo = entry["losses"]
                                                                break
                                                            
                                                        for entry_2 in rank_data:
                                                            if entry_2["queueType"] == "RANKED_FLEX_SR":
                                                                ranked_flex = entry_2["tier"].lower().capitalize() + " " + entry_2["rank"]
                                                                Lp_flex = entry_2["leaguePoints"]
                                                                wins_flex = entry_2["wins"]
                                                                losses_flex = entry_2["losses"]
                                                                break
                                                        
                                                        winrate_solo_duo = round(wins_solo_duo / (wins_solo_duo+losses_solo_duo), 2) * 100 if wins_solo_duo + losses_solo_duo > 0 else "N/A"
                                                        winrate_flex = round(wins_flex / (wins_flex+losses_flex), 2) * 100 if wins_flex + losses_flex > 0 else "N/A"
                                                        
                                                        embed = discord.Embed(title=f"Summoner Data: {ign} #{tag}", colour=discord.Colour.brand_red())
                                                        
                                                        embed.add_field(name="Ranked Solo/Duo", value=f"{ranked_solo_duo} {Lp_solo_duo} LP", inline=True)
                                                        embed.add_field(name="Ranked Flex", value=f"{ranked_flex} {Lp_flex} LP", inline=True)
                                                        embed.add_field(name="", value=f"", inline=False)
                                                        
                                                        
                                                        embed.add_field(name="Win Rate", value=f"{winrate_solo_duo}%", inline=True)
                                                        embed.add_field(name="Win Rate", value=f"{winrate_flex}%", inline=True)
                                                        
                                                        embed.add_field(name="Top Mastery:", value=f"", inline=False)
                                                        embed.add_field(name="1.", value=f"{champion_name_1}: {champ_1_mastery} Points", inline=False)
                                                        embed.add_field(name="2.", value=f"{champion_name_2}: {champ_2_mastery} Points", inline=True)
                                                        embed.add_field(name="3.", value=f"{champion_name_3}: {champ_3_mastery} Points", inline=False)
                                                        
                                                        embed.add_field(name="Account Level", value=league_v4_resp["summonerLevel"], inline=False)
                                                        embed.set_footer(text="In development, expect some bugs.")
                                                        embed.set_author(name=f"Intsuo", icon_url=f"https://cdn.discordapp.com/avatars/769070942440914946/5a3f6552462c96dc32a1d88c716b2c90.webp?size=32")
                                                        await interaction.response.send_message(embed=embed, ephemeral=True)
                                    else:
                                        embed = discord.Embed(title="Error", description="Failed to retrieve Account Rank. Riot API down?", color=discord.Colour.red())
                                        await interaction.response.send_message(embed=embed)
                            else:
                                embed = discord.Embed(title="Error", description="Failed to retrieve Account ID. Riot API down?", color=discord.Colour.red())
                                await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(title="Error", description="Failed to retrieve Game Details. Riot API down?", color=discord.Colour.red())
                        await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="Failed to retrieve PUUID. Make sure you've entered your correct Username and tag!", color=discord.Colour.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run('MTE5MzUzOTY2MTc5NzI2NTQ4OA.G3z9S9.9VEY4HtK_SZzSEujuvpb88kpE_SKy0F0-SAapE')