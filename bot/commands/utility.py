# utility.py
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
        await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

    @bot.hybrid_command(name="uptime")
    async def uptime(ctx):
        seconds = int(time.time() - start_time)
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        await ctx.send(f"Uptime: {h}h {m}m {s}s")

    @bot.hybrid_command(name="stats")
    async def stats(ctx):
        embed = discord.Embed(title="Bot Stats")
        embed.add_field(name="Servers", value=len(bot.guilds))
        embed.add_field(name="Users", value=sum(g.member_count for g in bot.guilds))
        embed.add_field(name="Commands", value=len(bot.commands))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="help")
    async def help(ctx):
        await ctx.send("Use / to see available commands. Full help command can be added using cogs or manual embeds.")

    @bot.hybrid_command(name="userinfo")
    async def userinfo(ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Info")
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles if r.name != "@everyone"]))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="avatar")
    async def avatar(ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(member.avatar.url)

    @bot.hybrid_command(name="roles")
    async def roles(ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"Roles: {', '.join([r.name for r in member.roles if r.name != '@everyone'])}")

    @bot.hybrid_command(name="nickname")
    async def nickname(ctx, member: discord.Member, *, name):
        await member.edit(nick=name)
        await ctx.send(f"Nickname changed to {name}")

    @bot.hybrid_command(name="resetnick")
    async def resetnick(ctx, member: discord.Member):
        await member.edit(nick=None)
        await ctx.send("Nickname reset")

    @bot.hybrid_command(name="serverinfo")
    async def serverinfo(ctx):
        g = ctx.guild
        embed = discord.Embed(title=g.name)
        embed.add_field(name="Owner", value=g.owner)
        embed.add_field(name="Members", value=g.member_count)
        embed.add_field(name="Region", value=str(g.region))
        embed.add_field(name="Created", value=g.created_at.strftime("%Y-%m-%d"))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="roleinfo")
    async def roleinfo(ctx, role: discord.Role):
        embed = discord.Embed(title=f"Role Info - {role.name}")
        embed.add_field(name="Color", value=str(role.color))
        embed.add_field(name="Members", value=len(role.members))
        await ctx.send(embed=embed)

    @bot.hybrid_command(name="channels")
    async def channels(ctx):
        ch = [c.name for c in ctx.guild.channels]
        await ctx.send("Channels:\n" + "\n".join(ch))

    @bot.hybrid_command(name="emojis")
    async def emojis(ctx):
        ems = [str(e) for e in ctx.guild.emojis]
        await ctx.send("Emojis:\n" + " ".join(ems))

    @bot.hybrid_command(name="boosts")
    async def boosts(ctx):
        await ctx.send(f"Server has {ctx.guild.premium_subscription_count} boosts.")

    @bot.hybrid_command(name="say")
    async def say(ctx, *, text):
        await ctx.send(text)

    @bot.hybrid_command(name="embed")
    async def embed(ctx, *, text):
        em = discord.Embed(description=text)
        await ctx.send(embed=em)

    @bot.hybrid_command(name="poll")
    async def poll(ctx, *, question):
        msg = await ctx.send(f"📊 {question}")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @bot.hybrid_command(name="echo")
    async def echo(ctx, *, text):
        await ctx.send(text)

    @bot.hybrid_command(name="reverse")
    async def reverse(ctx, *, text):
        await ctx.send(text[::-1])

    @bot.hybrid_command(name="remindme")
    async def remindme(ctx, time_str: str, *, reminder):
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
        await ctx.send(f"Timer for {seconds} seconds started.")
        await asyncio.sleep(seconds)
        await ctx.send("Time's up!")

    @bot.hybrid_command(name="createtextchannel")
    async def createtextchannel(ctx, name):
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"Text channel '{name}' created.")

    @bot.hybrid_command(name="createvoicechannel")
    async def createvoicechannel(ctx, name):
        await ctx.guild.create_voice_channel(name)
        await ctx.send(f"Voice channel '{name}' created.")

    @bot.hybrid_command(name="deletechannel")
    async def deletechannel(ctx, *, name):
        ch = discord.utils.get(ctx.guild.channels, name=name)
        if ch:
            await ch.delete()
            await ctx.send(f"Deleted channel {name}")
        else:
            await ctx.send("Channel not found")

    @bot.hybrid_command(name="renamechannel")
    async def renamechannel(ctx, *, name):
        await ctx.channel.edit(name=name)
        await ctx.send(f"Channel renamed to {name}")

    @bot.hybrid_command(name="move")
    async def move(ctx, member: discord.Member, channel: discord.VoiceChannel):
        await member.move_to(channel)
        await ctx.send(f"Moved {member.name} to {channel.name}")

    @bot.hybrid_command(name="invite")
    async def invite(ctx):
        perms = discord.Permissions(administrator=True)
        link = discord.utils.oauth_url(bot.user.id, permissions=perms)
        await ctx.send(f"Invite me using this link: {link}")

    @bot.hybrid_command(name="support")
    async def support(ctx):
        await ctx.send("Join support server: https://discord.gg/your-support-link")