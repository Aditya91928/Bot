import discord
from discord.ext import commands
from discord.utils import get
import asyncio

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # remove default help

# ========== EVENTS ==========

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ========== HELP COMMAND ==========

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Bot Commands",
        description="Here is a list of all available commands",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🔨 Moderation",
        value="""
`!kick @user reason`
`!ban @user reason`
`!unban user#1234`
`!mute @user`
`!unmute @user`
`!clear amount`
""",
        inline=False
    )

    embed.add_field(
        name="⚙ Utility",
        value="""
`!ping`
`!serverinfo`
`!userinfo @user`
`!avatar @user`
`!say message`
""",
        inline=False
    )

    embed.set_footer(text="Like Carl-bot but homemade 😎")
    await ctx.send(embed=embed)

# ========== UTILITY COMMANDS ==========

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="📊 Server Info", color=discord.Color.green())
    embed.add_field(name="Name", value=guild.name)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Owner", value=guild.owner)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="👤 User Info", color=discord.Color.purple())
    embed.add_field(name="Username", value=member)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%d %b %Y"))
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.avatar)

# ========== MODERATION COMMANDS ==========

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {amount} messages", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    name, discrim = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (name, discrim):
            await ctx.guild.unban(user)
            await ctx.send(f"♻ Unbanned {user}")
            return

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)

    await member.add_roles(role)
    await ctx.send(f"🔇 Muted {member}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"🔊 Unmuted {member}")

# ========== ERROR HANDLING ==========

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠ Missing arguments.")
    else:
        await ctx.send("⚠ An error occurred.")

# ========== RUN BOT ==========
z = input("Bot token here:")
bot.run("MTQ2Nzc5NjE1NDg3NDg1OTU0MQ.Gra8i8.A5cVUwzMBf95VTBk_M5wFMj53r2V7RXy67khdQ")
