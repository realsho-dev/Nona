from discord.ext import commands
import discord
import asyncio
from datetime import timedelta

log_channel = None
warnings_db = {}
last_deleted_message = None


def setup_moderation(bot):
    async def log_action(action, target, reason, moderator, extra_info=""):
        if log_channel:
            channel = bot.get_channel(log_channel)
            if channel:
                embed = discord.Embed(
                    title=f"Log: {action}",
                    description=f"Target: {target}\nReason: {reason or 'None'}\nBy: {moderator}\n{extra_info}",
                    color=0x708090
                )
                await channel.send(embed=embed)

    @bot.hybrid_command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member = None, *, reason: str = None):
        if not member:
            return await ctx.send("Please mention a user to kick.")
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.name} for: {reason}")
        await log_action("Kick", member.name, reason, ctx.author)

    @bot.hybrid_command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member = None, *, reason: str = None):
        if not member:
            return await ctx.send("Please mention a user to ban.")
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.name} for: {reason}")
        await log_action("Ban", member.name, reason, ctx.author)

    @bot.hybrid_command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, *, user):
        banned_users = await ctx.guild.bans()
        name, discriminator = user.split("#")
        for ban_entry in banned_users:
            if ban_entry.user.name == name and ban_entry.user.discriminator == discriminator:
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"Unbanned {user}")
                return
        await ctx.send("User not found in ban list.")

    @bot.hybrid_command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(ctx, member: discord.Member = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
        await member.add_roles(role)
        await ctx.send(f"Muted {member.name}")
        await log_action("Mute", member.name, None, ctx.author)

    @bot.hybrid_command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(ctx, member: discord.Member = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"Unmuted {member.name}")
        await log_action("Unmute", member.name, None, ctx.author)

    @bot.hybrid_command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(ctx, member: discord.Member, duration: int):
        await member.timeout(discord.utils.utcnow() + timedelta(seconds=duration))
        await ctx.send(f"Timed out {member.name} for {duration} seconds")

    @bot.hybrid_command(name="untimeout")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"Removed timeout from {member.name}")

    @bot.hybrid_command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member.id not in warnings_db:
            warnings_db[member.id] = []
        warnings_db[member.id].append(reason)
        await ctx.send(f"Warned {member.name}: {reason}")

    @bot.hybrid_command(name="warnings")
    async def warnings(ctx, member: discord.Member):
        warns = warnings_db.get(member.id, [])
        if not warns:
            await ctx.send(f"No warnings for {member.name}")
        else:
            await ctx.send(f"Warnings for {member.name}: {', '.join(warns)}")

    @bot.hybrid_command(name="clearwarnings")
    @commands.has_permissions(manage_messages=True)
    async def clearwarnings(ctx, member: discord.Member):
        warnings_db.pop(member.id, None)
        await ctx.send(f"Cleared warnings for {member.name}")

    @bot.hybrid_command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Cleared {amount} messages")

    @bot.hybrid_command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx, amount: int):
        """Purges messages in the channel."""
        # Purge the specified number of messages (+1 to include the command message itself)
        deleted_messages = await ctx.channel.purge(limit=amount + 1)
        
        # Send a confirmation message showing how many messages were deleted
        confirmation_msg = await ctx.send(f"{len(deleted_messages) - 1} message(s) purged.", delete_after=5)

    @bot.hybrid_command(name="cleanbot")
    async def cleanbot(ctx):
        def check(m): return m.author == bot.user
        deleted = await ctx.channel.purge(limit=1000, check=check)
        await ctx.send(f"Deleted {len(deleted)} bot messages")

    @bot.hybrid_command(name="snipe")
    async def snipe(ctx):
        if last_deleted_message:
            await ctx.send(f"Sniped message from {last_deleted_message.author}: {last_deleted_message.content}")
        else:
            await ctx.send("No recently deleted message.")

    @bot.event
    async def on_message_delete(message):
        global last_deleted_message
        last_deleted_message = message

    @bot.hybrid_command(name="lock")
    async def lock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("Channel locked")

    @bot.hybrid_command(name="unlock")
    async def unlock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("Channel unlocked")

    @bot.hybrid_command(name="slowmode")
    async def slowmode(ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set slowmode to {seconds} seconds")

    @bot.hybrid_command(name="hide")
    async def hide(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.send("Channel hidden")

    @bot.hybrid_command(name="unhide")
    async def unhide(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
        await ctx.send("Channel visible")

    @bot.hybrid_command(name="nuke")
    async def nuke(ctx):
        new_channel = await ctx.channel.clone()
        await ctx.channel.delete()
        await new_channel.send("Channel nuked")

    @bot.hybrid_command(name="addrole")
    async def addrole(ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"Added {role.name} to {member.name}")

    @bot.hybrid_command(name="removerole")
    async def removerole(ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"Removed {role.name} from {member.name}")

    @bot.hybrid_command(name="createrole")
    async def createrole(ctx, *, name: str):
        await ctx.guild.create_role(name=name)
        await ctx.send(f"Created role {name}")

    @bot.hybrid_command(name="deleterole")
    async def deleterole(ctx, role: discord.Role):
        await role.delete()
        await ctx.send(f"Deleted role {role.name}")

    @bot.hybrid_command(name="addemoji")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(ctx, name: str, link: str):
        """Adds a custom emoji to the server."""
        try:
            # Check if the URL is valid
            emoji_image = await discord.utils.get_link_image(link)
            
            # Add the emoji to the server
            emoji = await ctx.guild.create_custom_emoji(name=name, image=emoji_image)
            
            # Send a confirmation message
            await ctx.send(f"Emoji {emoji.name} added successfully!")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    @bot.hybrid_command(name="editrole")
    async def editrole(ctx, role: discord.Role, new_name: str, color: str = None):
        if color:
            try:
                color = discord.Color(int(color.strip("#"), 16))
            except:
                color = role.color
        else:
            color = role.color
        await role.edit(name=new_name, color=color)
        await ctx.send(f"Updated role to {new_name} with color {color}")