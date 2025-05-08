import discord
from discord.ext import commands
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
            placeholder="🔽 Choose a category...",
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

            elif value == "utility":
                embed = discord.Embed(
                    title="🛠️ **__Utility Commands__**",
                    color=discord.Color.green()
                )
                embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)

                embed.add_field(name="📊 Bot Info", value=(
                    "**ping** - Show latency\n`Usage:` `-ping`\n"
                    "**uptime** - Show bot uptime\n`Usage:` `-uptime`\n"
                    "**stats** - Show bot stats\n`Usage:` `-stats`\n"
                    "**help** - Open help panel\n`Usage:` `-help`"
                ), inline=False)

                embed.add_field(name="🙋 User Info", value=(
                    "**userinfo** - Show info of user\n`Usage:` `-userinfo @user`\n"
                    "**avatar** - Show avatar\n`Usage:` `-avatar @user`\n"
                    "**roles** - Show user roles\n`Usage:` `-roles @user`\n"
                    "**nickname** - Change nickname\n`Usage:` `-nickname @user NewName`\n"
                    "**resetnick** - Reset nickname\n`Usage:` `-resetnick @user`"
                ), inline=False)

                embed.add_field(name="📌 Server Info", value=(
                    "**serverinfo** - Info about server\n`Usage:` `-serverinfo`\n"
                    "**roleinfo** - Role info\n`Usage:` `-roleinfo @role`\n"
                    "**channels** - List all channels\n`Usage:` `-channels`\n"
                    "**emojis** - Show all emojis\n`Usage:` `-emojis`\n"
                    "**boosts** - Show boosts count\n`Usage:` `-boosts`"
                ), inline=False)

                embed.add_field(name="🎉 Fun & Tools", value=(
                    "**say** - Bot says something\n`Usage:` `-say Hello`\n"
                    "**embed** - Send an embed\n`Usage:` `-embed Hello!`\n"
                    "**poll** - Create yes/no poll\n`Usage:` `-poll Are you happy?`\n"
                    "**quote** - Show a message by ID\n`Usage:` `-quote 12345678`"
                ), inline=False)

            elif value == "ai":
                embed = discord.Embed(
                    title="🧠 **__AI Commands__**",
                    color=discord.Color.purple()
                )
                embed.set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)

                embed.add_field(name="🤖 AI Interaction", value=(
                    "**aichannel** - Set AI chat channel\n`Usage:` `-aichannel #channel`\n"
                    "**ask** - Ask anything to AI\n`Usage:` `-ask What is AI?`"
                ), inline=False)

            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback

        view = View()
        view.add_item(select)
        await ctx.send(embed=embed, view=view)