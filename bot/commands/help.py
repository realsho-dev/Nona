from discord.ext import commands
import discord
from discord.ui import Select, View

def setup_help(bot):
    bot.remove_command("help")

    @bot.command(name="help")
    async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 **__Bot Help Panel__**",
        description=(
            "**Welcome to the Help Menu!**\n\n"
            "Select a category from the dropdown below to see commands.\n\n"
            "**👨‍💻 Developer:** `Ayanokouji`"
        ),
        color=discord.Color.blurple()
    )
    embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
    embed.set_footer(text="Use the dropdown below to select a command category.")

    select = Select(
        placeholder="🔽️ Choose a category...",
        options=[
            discord.SelectOption(label="Moderation", value="moderation", emoji="🛡️"),
            discord.SelectOption(label="Utility", value="utility", emoji="🛠️"),
            discord.SelectOption(label="AI", value="ai", emoji="🧠"),
        ]
    )

    async def select_callback(interaction: discord.Interaction):
        value = select.values[0]

        if value == "moderation":
            embed = discord.Embed(
                title="🛡️ **__Moderation Commands__**",
                color=discord.Color.red()
            )
            embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)

            embed.add_field(name="👥 Member Moderation", value=(
                "**kick** - Kick a user\n`Usage:` `-kick @user [reason]`\n"
                "**ban** - Ban a user\n`Usage:` `-ban @user [reason]`\n"
                "**unban** - Unban a user\n`Usage:` `-unban user_id`\n"
                "**mute** - Temporarily mute a user\n`Usage:` `-mute @user 10m`\n"
                "**unmute** - Unmute a user\n`Usage:` `-unmute @user`\n"
                "**timeout** - Timeout a user\n`Usage:` `-timeout @user 10m`\n"
                "**untimeout** - Remove timeout\n`Usage:` `-untimeout @user`"
            ), inline=False)

            embed.add_field(name="⚠️ Warnings & Logs", value=(
                "**warn** - Warn a user\n`Usage:` `-warn @user [reason]`\n"
                "**warnings** - Check user warnings\n`Usage:` `-warnings @user`\n"
                "**clearwarnings** - Clear all warnings\n`Usage:` `-clearwarnings @user`"
            ), inline=False)

            embed.add_field(name="🧹 Message Management", value=(
                "**clear** - Delete messages\n`Usage:` `-clear 50`\n"
                "**purge** - Purge messages from user\n`Usage:` `-purge @user`\n"
                "**cleanbot** - Remove bot messages\n`Usage:` `-cleanbot`\n"
                "**snipe** - Show last deleted message\n`Usage:` `-snipe`"
            ), inline=False)

            embed.add_field(name="🔒 Channel Management", value=(
                "**lock** - Lock a channel\n`Usage:` `-lock #channel`\n"
                "**unlock** - Unlock a channel\n`Usage:` `-unlock #channel`\n"
                "**slowmode** - Set slowmode\n`Usage:` `-slowmode #channel 10`\n"
                "**hide** - Hide a channel\n`Usage:` `-hide #channel`\n"
                "**unhide** - Unhide a channel\n`Usage:` `-unhide #channel`\n"
                "**nuke** - Nuke a channel\n`Usage:` `-nuke #channel`"
            ), inline=False)

            embed.add_field(name="🎭 Role Management", value=(
                "**addrole** - Add role\n`Usage:` `-addrole @user @role`\n"
                "**removerole** - Remove role\n`Usage:` `-removerole @user @role`\n"
                "**createrole** - Create a role\n`Usage:` `-createrole NewRole`\n"
                "**deleterole** - Delete a role\n`Usage:` `-deleterole @role`\n"
                "**editrole** - Edit a role\n`Usage:` `-editrole @role [setting]`"
            ), inline=False)

            embed.add_field(name="😀 Emoji Management", value=(
                "**addemoji** - Add emoji\n`Usage:` `-addemoji :emoji:`"
            ), inline=False)

        elif value == "utility":
            embed = discord.Embed(
                title="🛠️ **__Utility Commands__**",
                color=discord.Color.green()
            )
            embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)

            embed.add_field(name="📊 Bot Info", value=(
                "**ping** - Show latency\n`Usage:` `-ping`\n"
                "**uptime** - Show uptime\n`Usage:` `-uptime`\n"
                "**stats** - Bot stats\n`Usage:` `-stats`\n"
                "**help** - Help menu\n`Usage:` `-help`"
            ), inline=False)

            embed.add_field(name="🙋 User Info", value=(
                "**userinfo** - User info\n`Usage:` `-userinfo @user`\n"
                "**avatar** - Show avatar\n`Usage:` `-avatar @user`\n"
                "**roles** - Show roles\n`Usage:` `-roles @user`\n"
                "**nickname** - Change nickname\n`Usage:` `-nickname @user NewName`\n"
                "**resetnick** - Reset nickname\n`Usage:` `-resetnick @user`"
            ), inline=False)

            embed.add_field(name="📌 Server Info", value=(
                "**serverinfo** - Server info\n`Usage:` `-serverinfo`\n"
                "**roleinfo** - Role info\n`Usage:` `-roleinfo @role`\n"
                "**channels** - List channels\n`Usage:` `-channels`\n"
                "**emojis** - Show emojis\n`Usage:` `-emojis`\n"
                "**boosts** - Server boosts\n`Usage:` `-boosts`"
            ), inline=False)

            embed.add_field(name="🎉 Fun & Tools", value=(
                "**say** - Repeat text\n`Usage:` `-say Hello`\n"
                "**embed** - Send embed\n`Usage:` `-embed Hello!`\n"
                "**poll** - Yes/No poll\n`Usage:` `-poll Are you happy?`\n"
                "**quote** - Show message by ID\n`Usage:` `-quote 12345678`\n"
                "**echo** - Echo message\n`Usage:` `-echo Hello`\n"
                "**reverse** - Reverse message\n`Usage:` `-reverse Hello`\n"
                "**remindme** - Set reminder\n`Usage:` `-remindme 10m Take a break`\n"
                "**timer** - Start timer\n`Usage:` `-timer 10m`\n"
                "**invite** - Bot invite\n`Usage:` `-invite`\n"
                "**support** - Support server\n`Usage:` `-support`"
            ), inline=False)

        elif value == "ai":
            embed = discord.Embed(
                title="🧠 **__AI Commands__**",
                color=discord.Color.purple()
            )
            embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)

            embed.add_field(name="🤖 AI Interaction", value=(
                "**aichannel** - Set AI channel\n`Usage:` `-aichannel #channel`\n"
                "**ask** - Ask AI\n`Usage:` `-ask What is AI?`\n"
                "**clearhistory** - Clear AI chat\n`Usage:` `-clearhistory`"
            ), inline=False)

        await interaction.response.edit_message(embed=embed, view=view)

    select.callback = select_callback

    view = View()
    view.add_item(select)
    await ctx.send(embed=embed, view=view)

