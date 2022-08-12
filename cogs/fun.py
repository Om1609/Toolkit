from asyncio import sleep
from random import choice

import discord
from discord import ApplicationContext

from core import Cog


class Fun(Cog):
    """Fun commands."""

    magic_8ball = discord.SlashCommandGroup(
        "8ball", "Commands to ask a question to the magic 8 ball."
    )

    @magic_8ball.command(name="ask")
    @discord.option(
        "question",
        description="The question to ask to the magic 8 ball.",
    )
    async def magic_8ball_ask(self, ctx: ApplicationContext, question: str):
        """Ask a yes-or-no question to the magic 8 ball and get an answer."""
        await ctx.defer()
        answer = choice(
            (
                "Definitely.",
                "Most probably.",
                "I'm not sure.",
                "Perhaps.",
                "I don't think so.",
                "There's a chance!",
                "Under no circumstances.",
            )
        )
        await sleep(2)
        await ctx.respond(f"> {question}\n{answer}")

    @magic_8ball.command(name="yes_or_no")
    @discord.option(
        "question",
        description="The question to ask to the magic 8 ball.",
    )
    async def magic_8ball_yes_or_no(self, ctx: ApplicationContext, question: str):
        """Ask a yes-or-no question to the magic 8 ball and get an answer (either yes or no)."""
        await ctx.defer()
        answer = choice(("Yes.", "No."))
        await sleep(2)
        await ctx.respond(f"> {question}\n{answer}")

    @discord.slash_command()
    @discord.guild_only()
    @discord.option("text", description="The text to check for in display names.")
    async def how_many(self, ctx: ApplicationContext, *, text: str):
        """Shows the amount of members that have the supplied text in their display name."""
        text = text.strip().lower()
        count = sum(text in member.display_name.lower() for member in ctx.guild.members)
        await ctx.respond(
            f"{count} members have `{text}` (any case) in their display name."
        )

    @discord.slash_command()
    @discord.option("question", description="The question of the poll.")
    @discord.option("choice1", description="The first choice.")
    @discord.option("choice2", description="The second choice.")
    async def poll(
        self, ctx: ApplicationContext, question: str, choice1: str, choice2: str
    ):
        """Create a poll."""
        interaction = await ctx.respond(
            embed=discord.Embed(
                title=f"Poll: {question}",
                description=f":a: {choice1}\n:b: {choice2}",
                color=discord.Color.brand_red(),
            ).set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar
            )
        )
        message = await interaction.original_message()
        await message.add_reaction("🅰")
        await message.add_reaction("🅱")

    @discord.slash_command()
    @discord.option("question", description="The question of the poll.")
    async def poll_yesno(self, ctx: ApplicationContext, *, question: str):
        """Create a poll with the options being yes or no."""
        interaction = await ctx.respond(
            embed=discord.Embed(
                title="Yes/No Poll",
                description=question,
                color=discord.Color.brand_green(),
            ).set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar
            )
        )
        message = await interaction.original_message()
        await message.add_reaction("✅")
        await message.add_reaction("❎")


def setup(bot):
    bot.add_cog(Fun(bot))
