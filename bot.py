import discord  # For discord
from discord.ext import commands  # For discord
from pathlib import Path  # For paths
import aiohttp
import aiofiles
import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


bot = commands.Bot(command_prefix="$", case_insensitive=True)
bot.remove_command("help")
bot.config_token = "NzM2MTIzMDE0MjEwMzg3OTY5.XxqN-w.2bxi47qNJ9dq3fx4h6Rd9mr1iDQ"


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: $\n-----")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"{len(bot.guilds)} servers\nUse $help to get started!"))

@bot.event
async def on_message(message):
    if f"<@!{bot.user.id}>" in message.content:
        prefixMsg = await message.channel.send(f"My prefix here is `$`")
        await prefixMsg.add_reaction('👀')

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        embed = discord.Embed(title=f":x: Can't find the User.", colour=discord.colour.Color.blue())
        embed.description = f":warning: Are you sure you spelled the name right? If yes, he isn't in this server :warning:"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
        raise (error)


@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, amount: int = None):
    if amount is None:
        embed = discord.Embed(title=f"Help Purge", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** purges the messages specified \n**Usage ❯** $purge [amount] \n**Example ❯** $purge 3 \n**Perms ❯** you need administrator permission"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:
        amount += 1
        await ctx.channel.purge(limit=amount)


@bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, *, pre='$'):
    data = cogs._json.read_json('prefixes')
    data[str(ctx.message.guild.id)] = pre
    cogs._json.write_json(data, 'prefixes')
    await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}prefix <prefix>` to change it again!")


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong", colour=discord.colour.Color.blue())
    # embed.add_field(name=":heartbeat: **Heartbeat** " + str(f"{round(bot.latency*1000)}ms"))
    embed.description = ":heartbeat: **Heartbeat** " + str(f"{round(bot.latency * 1000)}ms")

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    if user is None:
        embed = discord.Embed(title=f"Help Info", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** shows useful info about the user specified \n**Usage ❯** $info [username] \n**Example ❯** $info Johnny_JTH"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:

        date_format = "%a, %d %b %Y %I:%M %p"

        embed = discord.Embed(title=f"{user.name + '#' + user.discriminator}'s Information", color=discord.colour.Color.blue())
        embed.description = '{0}{1}{2}{3}{4}{5}'.format(
            "General Information \n**❯The user's name is: **{}".format(user.name),
            "\n**❯The user's ID is: **{}".format(user.id),
            "\n**❯The user's current status is: **{}".format(user.status),
            "\n**❯The user's highest role is: **{}".format(user.top_role),
            "\n\nProfile Information"
            "\n**❯Joined at: **{}".format(user.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")),
            "\n**❯Created at: **{}".format(user.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")))
        await ctx.send(embed=embed)


output_file = "temp.png"


@bot.command()
async def cape(ctx, username: str = None):
    if username is None:
        embed = discord.Embed(title=f"Help Cape", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** shows the cape of the Account specified \n**Usage ❯** $cape [minecraft username] \n**Example ❯** $cape Johnny_JTH"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:
        async with aiohttp.ClientSession() as session:  # Start up the asynced function
            url = f'https://optifine.net/capes/{username}.png'  # URL
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        # f = open("temp.png", "w+")
                        f = await aiofiles.open(output_file, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                embed = discord.Embed(colour=discord.colour.Color.blue())
                # embed.set_image(url=f"attachment://{output_file}")
                file = discord.File(output_file, filename="image.png")
                embed.set_image(url="attachment://image.png")
                await ctx.send(file=file, embed=embed)

                from os import remove  # only allow remove to be used within this function
                remove(output_file)
            except:
                embed = discord.Embed(title=f":x: Can't find the cape of {username}.",
                                      colour=discord.colour.Color.blue())
                embed.description = f":warning: Are you sure you spelled the name right? If yes, {username} doesent have a cape :warning:"
                embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                await ctx.send(embed=embed)


@bot.command()
async def head(ctx, username: str = None):
    if username is None:
        embed = discord.Embed(title=f"Help Head", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** shows the head of the Account specified \n**Usage ❯** $head [minecraft username] \n**Example ❯** $head Johnny_JTH"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:
        async with aiohttp.ClientSession() as session:  # Start up the asynced function
            url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
            try:
                async with session.get(url) as resp:
                    data = await resp.json()
                    #print(data['id'])
                    uuid = data['id']
            except:
                embed = discord.Embed(title=f":x: Can't find the head of {username}.", colour=discord.colour.Color.blue())
                embed.description = f":warning: Are you sure you spelled the name right? If yes, {username} doesent have a minecraft Account :warning:"
                embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                await ctx.send(embed=embed)

            output_file2 = "temp2.png"
            async with aiohttp.ClientSession() as session:  # Start up the asynced function
                url = f'https://crafatar.com/renders/head/{uuid}.png?scale=10'  # URL
                try:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            # f = open("temp.png", "w+")
                            f = await aiofiles.open(output_file2, mode='wb')
                            await f.write(await resp.read())
                            await f.close()

                            embed = discord.Embed(colour=discord.colour.Color.blue())
                            # embed.set_image(url=f"attachment://{output_file}")
                            file = discord.File(output_file2, filename="image.png")
                            embed.set_image(url="attachment://image.png")
                            await ctx.send(file=file, embed=embed)

                    from os import remove  # only allow remove to be used within this function
                    remove(output_file2)
                except:
                    embed = discord.Embed(title=f":x: something went wrong.",
                                          colour=discord.colour.Color.blue())
                    embed.description = f":warning: contact Johnny_JTH#0001 if it doesent work second time either :warning:"
                    embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                    await ctx.send(embed=embed)


@bot.command()
async def skin(ctx, username: str = None):
    if username is None:
        embed = discord.Embed(title=f"Help Skin", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** shows the skin of the Account specified \n**Usage ❯** $skin [minecraft username] \n**Example ❯** $skin Johnny_JTH"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:
        async with aiohttp.ClientSession() as session:  # Start up the asynced function
            url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
            try:
                async with session.get(url) as resp:
                    data = await resp.json()
                    print(data['id'])
                    uuid = data['id']
            except:
                embed = discord.Embed(title=f":x: Can't find the skin of {username}.", colour=discord.colour.Color.blue())
                embed.description = f":warning: Are you sure you spelled the name right? If yes, {username} doesent have a minecraft Account :warning:"
                embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                await ctx.send(embed=embed)

            output_file3 = "temp2.png"
            async with aiohttp.ClientSession() as session:  # Start up the asynced function
                url = f'https://crafatar.com/renders/body/{uuid}.png?scale=10'  # URL
                try:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            # f = open("temp.png", "w+")
                            f = await aiofiles.open(output_file3, mode='wb')
                            await f.write(await resp.read())
                            await f.close()

                            embed = discord.Embed(colour=discord.colour.Color.blue())
                            # embed.set_image(url=f"attachment://{output_file}")
                            file = discord.File(output_file3, filename="image.png")
                            embed.set_image(url="attachment://image.png")
                            await ctx.send(file=file, embed=embed)

                    from os import remove  # only allow remove to be used within this function
                    remove(output_file3)
                except:
                    embed = discord.Embed(title=f":x: something went wrong.",
                                          colour=discord.colour.Color.blue())
                    embed.description = f":warning: contact Johnny_JTH#0001 if it doesent work second time either :warning:"
                    embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                    await ctx.send(embed=embed)


@bot.command()
async def uuid(ctx, username: str = None):
    if username is None:
        embed = discord.Embed(title=f"Help UUID", colour=discord.colour.Color.blue())
        embed.description = f"**Info ❯** shows the UUID of the Minecraft Account specified \n**Usage ❯** $UUID [minecraft username] \n**Example ❯** $UUID Johnny_JTH"
        embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
        await ctx.send(embed=embed)
    else:
        async with aiohttp.ClientSession() as session:  # Start up the asynced function
            url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
            try:
                async with session.get(url) as resp:
                    data = await resp.json()
                    uuid = data['id']
            except:
                embed = discord.Embed(title=f":x: Can't find the uuid of {username}.", colour=discord.colour.Color.blue())
                embed.description = f":warning: Are you sure you spelled the name right? If yes, {username} doesent have a minecraft Account :warning:"
                embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
                await ctx.send(embed=embed)

            embed = discord.Embed(title=f"UUID of {username}", color=discord.colour.Color.blue())
            embed.description = uuid
            await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    async with aiohttp.ClientSession() as session:  # Start up the asynced function
        url = 'https://status.mojang.com/check'
        try:
            async with session.get(url) as resp:
                data = await resp.json()
                status = data
        except:
            embed = discord.Embed(title=f":x: Can't get the status.", colour=discord.colour.Color.blue())
            embed.description = f":warning: sometimes the Minecraft API isn't working :warning:"
            embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"Minecraft Status", color=discord.colour.Color.blue(), timestamp=ctx.message.created_at)

            if status[1]['session.minecraft.net'] == "green":
                embed.add_field(name="Session = :white_check_mark:", value="---", inline=False)
            elif status[1]['session.minecraft.net'] == "yellow":
                embed.add_field(name="Session = :warning:", value="---", inline=False)
            else:
                embed.add_field(name="Session = :x:", value="---", inline=False)

            if status[2]['account.mojang.com'] == "green":
                embed.add_field(name="Accounts = :white_check_mark:", value="---", inline=False)
            elif status[2]['account.mojang.com'] == "yellow":
                embed.add_field(name="Accounts = :warning:", value="---", inline=False)
            else:
                embed.add_field(name="Accounts = :x:", value="---", inline=False)

            if status[3]['authserver.mojang.com'] == "green":
                embed.add_field(name="Authentication = :white_check_mark:", value="---", inline=False)
            elif status[3]['authserver.mojang.com'] == "yellow":
                embed.add_field(name="Authentication = :warning:", value="---", inline=False)
            else:
                embed.add_field(name="Authentication = :x:", value="---", inline=False)

            if status[5]['api.mojang.com'] == "green":
                embed.add_field(name="API = :white_check_mark:", value="---", inline=False)
            elif status[5]['api.mojang.com'] == "yellow":
                embed.add_field(name="API = :warning:", value="---", inline=False)
            else:
                embed.add_field(name="API = :x:", value="---", inline=False)

            if status[6]['textures.minecraft.net'] == "green":
                embed.add_field(name="Textures = :white_check_mark:", value="---", inline=False)
            elif status[6]['textures.minecraft.net'] == "yellow":
                embed.add_field(name="Textures = :warning:", value="---", inline=False)
            else:
                embed.add_field(name="Textures = :x:", value="---", inline=False)

            embed.description = "Some statuses in the API are broken, so they are not shown"
            embed.set_footer(text="Optifine Cape Preview", icon_url=bot.user.avatar_url)
            await ctx.send(embed=embed)


@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Invite Me", color=discord.colour.Color.blue())
    embed.description = "❯ https://discord.com/api/oauth2/authorize?client_id=736123014210387969&permissions=8&scope=bot"
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help", color=discord.colour.Color.blue())
    embed.description = "General Commands \n**❯Help: **shows this help message""\n**❯Ping: **shows the bot's ping""\n**❯Info: **shows information about the username specified""\n\nMinecraft Commands""\n**❯Cape: **shows the player's optifine cape""\n**❯Skin: **shows the player's minecraft skin""\n**❯Head: **shows the player's minecraft head""\n**❯UUID: **shows the UUID of the Minecraft Account specified""\n\nAdmin Commands""\n**❯Purge: **purges the amount of messages specified""\n**❯Prefix: **changes the bot's prefix""\n\n**❯Invite: **Invite the bot to your server"
    embed.set_footer(text='experience any problems or bugs? Message Johnny_JTH#0001')
    await ctx.send(embed=embed)


bot.run(bot.config_token)
