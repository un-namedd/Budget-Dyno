@bot.tree.command(name="league_stats", description="EUW only. Get info about the given player. e.g Name: Budget Yasuo | (No #) tag: OwO)")
async def summoner(interaction: discord.Interaction, ign: str, tag: str):
    ign.lower()
    ign.capitalize()
    summoner_id = None
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{ign}/{tag}?api_key={Riot_API}") as resp:
            if resp.status == 200:
                data = await resp.json()
                summoner_puuid = data["puuid"]
                ign = data["gameName"]
                tag = data["tagLine"]
                
                async with session.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{summoner_puuid}?api_key={Riot_API}") as encrypted_id_resp:
                    if encrypted_id_resp.status == 200:
                        league_v4_resp = await encrypted_id_resp.json()
                        summoner_id = league_v4_resp["id"]

                        async with session.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_puuid}/top?count=3&api_key={Riot_API}") as mastery_resp:
                            if mastery_resp.status == 200:
                                mastery_data = await mastery_resp.json()

                                top_champions = sorted(mastery_data, key=lambda x: x["championPoints"], reverse=True)[:3]

                                champ_1_points = "{:,}".format(top_champions[0]["championPoints"])
                                champ_2_points = "{:,}".format(top_champions[1]["championPoints"])
                                champ_3_points = "{:,}".format(top_champions[2]["championPoints"])

                                level_emojis = {
                                    i: emoji for i, emoji in [
                                        (10, '<:newmastery10:1240179110878253116>'),
                                        (9, '<:newmastery9:1240179074606043209>'),
                                        (8, '<:newmastery8:1240179050010513539>'),
                                        (7, '<:newmastery7:1240179035305410591>'),
                                        (6, '<:newmastery6:1240179018062364723>'),
                                        (5, '<:newmastery5:1240179004817018950>'),
                                        (4, '<:newmastery4:1240178990858108978>'),
                                        (3, '<:newmastery3:1240178970926776351>'),
                                        (2, '<:newmastery2:1240178955814699048>'),
                                        (1, '<:newmastery1:1240178910725931110>')
                                    ]
                                }
                                
                                level_emojis_default = '<:newmastery10:1240179110878253116>'  # default emoji for levels not in the dictionary

                                champ_levels_num = [top_champions[i]["championLevel"] for i in [0, 1, 2]]
                                champ_levels = [level_emojis.get(level, level_emojis_default) for level in champ_levels_num]
                                champ_ids = [str(top_champions[i]["championId"]) for i in [0, 1, 2]]

                                async with session.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_puuid}/top?count=3&api_key={Riot_API}") as mastery_resp:
                                    if mastery_resp.status == 200:
                                        mastery_data = await mastery_resp.json()

                                        top_champions = sorted(mastery_data, key=lambda x: x["championPoints"], reverse=True)[:3]

                                        champ_1_points = "{:,}".format(top_champions[0]["championPoints"])
                                        champ_2_points = "{:,}".format(top_champions[1]["championPoints"])
                                        champ_3_points = "{:,}".format(top_champions[2]["championPoints"])

                                        level_emojis = {
                                            i: emoji for i, emoji in [
                                                (10, '<:newmastery10:1240179110878253116>'),
                                                (9, '<:newmastery9:1240179074606043209>'),
                                                (8, '<:newmastery8:1240179050010513539>'),
                                                (7, '<:newmastery7:1240179035305410591>'),
                                                (6, '<:newmastery6:1240179018062364723>'),
                                                (5, '<:newmastery5:1240179004817018950>'),
                                                (4, '<:newmastery4:1240178990858108978>'),
                                                (3, '<:newmastery3:1240178970926776351>'),
                                                (2, '<:newmastery2:1240178955814699048>'),
                                                (1, '<:newmastery1:1240178910725931110>')
                                            ]
                                        }
                                        
                                        level_emojis_default = '<:newmastery10:1240179110878253116>'  # default emoji for levels not in the dictionary

                                        champ_levels_num = [top_champions[i]["championLevel"] for i in [0, 1, 2]]
                                        champ_levels = [level_emojis.get(level, level_emojis_default) for level in champ_levels_num]
                                        champ_ids = [str(top_champions[i]["championId"]) for i in [0, 1, 2]]
                                        
                                        async with session.get(f"https://ddragon.leagueoflegends.com/cdn/14.9.1/data/en_US/champion.json") as champ_resp:
                                            if champ_resp.status == 200:
                                                champ_data = await champ_resp.json()

                                                champion_name_key_map = {champion_info["key"]: champion_name for champion_name, champion_info in champ_data["data"].items()}

                                                champ_names = [champion_name_key_map[champ_id] for champ_id in champ_ids]

                                                async with session.get(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={Riot_API}") as rank_resp:
                                                    if rank_resp.status == 200:
                                                        rank_data = await rank_resp.json()

                                                        ranked_flex = None
                                                        wins_flex = 0
                                                        losses_flex = 0
                                                        Lp_flex = 0

                                                        ranked_solo_duo = None
                                                        wins_solo_duo = 0
                                                        losses_solo_duo = 0
                                                        Lp_solo_duo = 0

                                                        emoji_dict = {
                                                            "IRON": "<:iron:1193213193212940429>",
                                                            "BRONZE": "<:bronze:1193213933625032864>",
                                                            "SILVER": "<:silver:1193213895029035008>",
                                                            "GOLD": "<:gold:1193213912439607316>",
                                                            "PLATINUM": "<:platinum:1193213880554500218>",
                                                            "EMERALD": "<:emerald:1193298992000401409>",
                                                            "DIAMOND": "<:diamond:1193213838141693973>",
                                                            "MASTER": "<:master:1193213238616272950>",
                                                            "GRANDMASTER": "<:grandmaster:1193213814586490980>",
                                                            "CHALLENGER": "<:challenger:1193213213152641124>"
                                                        }

                                                        for entry in rank_data:
                                                            if entry["queueType"] == "RANKED_SOLO_5x5":
                                                                tier_name = entry["tier"].upper()
                                                                ranked_solo_duo = f"{emoji_dict[tier_name]} {tier_name.capitalize()} {entry['rank']}"
                                                                Lp_solo_duo = entry["leaguePoints"]
                                                                wins_solo_duo = entry["wins"]
                                                                losses_solo_duo = entry["losses"]
                                                                break

                                                        for entry_2 in rank_data:
                                                            if entry_2["queueType"] == "RANKED_FLEX_SR":
                                                                tier_name = entry_2["tier"].upper()
                                                                ranked_flex = f"{emoji_dict[tier_name]} {tier_name.capitalize()} {entry_2['rank']}"
                                                                Lp_flex = entry_2["leaguePoints"]
                                                                wins_flex = entry_2["wins"]
                                                                losses_flex = entry_2["losses"]
                                                                break

                                                        winrate_solo_duo = round(wins_solo_duo / (wins_solo_duo+losses_solo_duo), 2) * 100 if wins_solo_duo + losses_solo_duo > 0 else "N/A"
                                                        winrate_flex = round(wins_flex / (wins_flex+losses_flex), 2) * 100 if wins_flex + losses_flex > 0 else "N/A"

                                                        embedmain = discord.Embed(title=f"{ign} #{tag}", colour=discord.Colour.brand_red())

                                                        embedmain.add_field(name="Account Level", value=league_v4_resp["summonerLevel"], inline=False)

                                                        embedmain.add_field(name="Ranked Solo/Duo", value=f"{ranked_solo_duo} {Lp_solo_duo} LP", inline=True)
                                                        embedmain.add_field(name="Ranked Flex", value=f"{ranked_flex} {Lp_flex} LP", inline=True)
                                                        embedmain.add_field(name="", value=f"", inline=False)

                                                        embedmain.add_field(name="Winrate Solo/Duo", value=f"{winrate_solo_duo} %", inline=True)
                                                        embedmain.add_field(name="Winrate Flex", value=f"{winrate_flex} %", inline=True)

                                                        embedmain.add_field(name="Top Mastery:", value=f"", inline=False)

                                                        
                                                        for i, (champion_level, champion_name, champ_points, champion_level_num) in enumerate(zip(champ_levels, champ_names, [champ_1_points, champ_2_points, champ_3_points], champ_levels_num)):
                                                            embedmain.add_field(name=f"{champion_level}  {champion_name}: {champ_points} Points (Level {champion_level_num})", value="", inline=i % 2 == 0)

                                                        embedmain.set_footer(text="In development, please expect some bugs. ^^ ")
                                                        embedmain.set_author(name=f"Summoner Data")

                                                        try:
                                                            await interaction.response.send_message(embed=embedmain, ephemeral=False)
                                                        except:
                                                            embed = discord.Embed(title="Error", description="Failed to send data. Please try again.", color=discord.Colour.red())
                                                            await interaction.followup.send(embed=embed)
                                                    else:
                                                        embed = discord.Embed(title=f"Error {rank_resp.status}", description="Failed to retrieve Account Rank. Riot API down?", color=discord.Colour.red())
                                                        await interaction.response.send_message(embed=embed)
                                            else:
                                                embed = discord.Embed(title=f"Error {champ_resp.status}", description="Failed to retrieve champion.json file. Riot API down?", color=discord.Colour.red())
                                                await interaction.response.send_message(embed=embed)
                                    else:
                                        embed = discord.Embed(title=f"Error {mastery_resp.status}", description="Failed to retrieve Account Mastery. Riot API down?", color=discord.Colour.red())
                                        await interaction.response.send_message(embed=embed)
                            else:
                                embed = discord.Embed(title=f"Error {mastery_resp.status}", description="Failed to retrieve Account Mastery. Riot API down?", color=discord.Colour.red())
                                await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(title=f"Error {encrypted_id_resp.status}", description="Failed to retrieve Account ID. Riot API down?", color=discord.Colour.red())
                        await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title=f"Error {resp.status}", description="Failed to retrieve User PUUID. Incorrect IGN or Tag line", color=discord.Colour.red())
                embed.add_field(name="Inccorect provided IGN or Tag Line.", value=f"{ign} #{tag}")
                await interaction.response.send_message(embed=embed, ephemeral=True)