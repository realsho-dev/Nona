from discord.ext import commands
import discord
import time
import asyncio
from datetime import datetime, timedelta
import re
import requests

start_time = time.time()

def setup_utility(bot):
    @bot.hybrid_command(name="ping")
    async def ping(ctx):
        """Ping command to check the bot's latency."""
        await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

    @bot.hybrid_command(name="uptime")
    async def uptime(ctx):
        """Shows the bot's uptime since it was last started."""
        seconds = int(time.time() - start_time)
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        await ctx.send(f"Uptime: {h}h {m}m {s}s")

    @bot.hybrid_command(name="stats")
    async def stats(ctx):
        """Shows bot stats including number of servers, users, and commands."""
        embed = discord.Embed(title="Bot Stats")
        embed.add_field(name="Servers", value=len(bot.guilds))
        embed.add_field(name="Users", value=sum(g.member_count for g in bot.guilds))
        embed.add_field(name="Commands", value=len(bot.commands))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="help")
    async def help(ctx):
        """Shows help information for the bot."""
        await ctx.send("Use / to see available commands. Full help command can be added using cogs or manual embeds.")

    @bot.hybrid_command(name="userinfo")
    async def userinfo(ctx, member: discord.Member = None):
        """Shows detailed information about a user (default is the command invoker)."""
        member = member or ctx.author  # If no member is provided, use the command invoker.
        embed = discord.Embed(title=f"{member.name}'s Info")
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles if r.name != "@everyone"]))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="avatar")
    async def avatar(ctx, member: discord.Member = None):
        """Sends the avatar URL of the user (default is the command invoker)."""
        member = member or ctx.author
        await ctx.send(member.avatar.url)

    @bot.hybrid_command(name="roles")
    async def roles(ctx, member: discord.Member = None):
        """Lists the roles of a user (default is the command invoker)."""
        member = member or ctx.author
        await ctx.send(f"Roles: {', '.join([r.name for r in member.roles if r.name != '@everyone'])}")

    @bot.hybrid_command(name="serverinfo")
    async def serverinfo(ctx):
        """Shows information about the current server."""
        g = ctx.guild
        embed = discord.Embed(title=g.name)
        embed.add_field(name="Owner", value=g.owner)
        embed.add_field(name="Members", value=g.member_count)
        embed.add_field(name="Region", value=str(g.region))
        embed.add_field(name="Created", value=g.created_at.strftime("%Y-%m-%d"))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="roleinfo")
    async def roleinfo(ctx, role: discord.Role):
        """Shows information about a role."""
        embed = discord.Embed(title=f"Role Info - {role.name}")
        embed.add_field(name="Color", value=str(role.color))
        embed.add_field(name="Members", value=len(role.members))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="channels")
    async def channels(ctx):
        """Lists all channels in the current server."""
        ch = [c.name for c in ctx.guild.channels]
        await ctx.send("Channels:\n" + "\n".join(ch))

    @bot.hybrid_command(name="emojis")
    async def emojis(ctx):
        """Lists all emojis available in the server."""
        ems = [str(e) for e in ctx.guild.emojis]
        await ctx.send("Emojis:\n" + " ".join(ems))

    @bot.hybrid_command(name="boosts")
    async def boosts(ctx):
        """Shows the number of boosts the server has."""
        await ctx.send(f"Server has {ctx.guild.premium_subscription_count} boosts.")

    @bot.hybrid_command(name="say")
    async def say(ctx, *, text):
        """Bot will repeat any text passed to it."""
        await ctx.send(text)

    @bot.hybrid_command(name="embed")
    async def embed(ctx, *, text):
        """Bot will send a message in an embedded format."""
        em = discord.Embed(description=text)
        await ctx.send(embed=em)

    @bot.hybrid_command(name="poll")
    async def poll(ctx, *, question):
        """Creates a simple poll with 👍 and 👎 reactions."""
        msg = await ctx.send(f"📊 {question}")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @bot.hybrid_command(name="echo")
    async def echo(ctx, *, text):
        """Bot will repeat back the text provided."""
        await ctx.send(text)

    @bot.hybrid_command(name="reverse")
    async def reverse(ctx, *, text):
        """Reverses the given text."""
        await ctx.send(text[::-1])

    @bot.hybrid_command(name="remindme")
    async def remindme(ctx, time_str: str, *, reminder):
        """Sets a reminder after a specified time in minutes/seconds."""
        match = re.match(r"(\d+)([smhd])", time_str)
        if not match:
            await ctx.send("Use format like 10m, 1h.")
            return
        num, unit = int(match.group(1)), match.group(2)
        seconds = num * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
        await ctx.send(f"Reminder set for {num}{unit}")
        await asyncio.sleep(seconds)
        await ctx.send(f"{ctx.author.mention}, Reminder: {reminder}")

    @bot.hybrid_command(name="timer")
    async def timer(ctx, seconds: int):
        """Sets a countdown timer in seconds."""
        await ctx.send(f"Timer for {seconds} seconds started.")
        await asyncio.sleep(seconds)
        await ctx.send("Time's up!")

    @bot.hybrid_command(name="invite")
    async def invite(ctx):
        """Generates an invite link for the bot."""
        perms = discord.Permissions(administrator=True)
        link = discord.utils.oauth_url(bot.user.id, permissions=perms)
        await ctx.send(f"Invite me using this link: {link}")

    @bot.hybrid_command(name="support")
    async def support(ctx):
        """Provides a link to the support server."""
        await ctx.send("Join support server: https://discord.gg/your-support-link")