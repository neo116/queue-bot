import re
from dataclasses import dataclass
from datetime import datetime, timezone

import discord
from discord.ext import commands


QUEUE_MESSAGE_PATTERN = re.compile(r"^(\d+)?q(\d+)$", re.IGNORECASE)
LEAVE_MESSAGE_PATTERN = re.compile(r"^(\d+)?l$", re.IGNORECASE)


@dataclass
class QueueEntry:
    user: discord.Member | discord.User
    alt_number: int
    queue_number: int
    updated_at: datetime


class QueueCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue_channels: dict[int, dict[tuple[int, int], QueueEntry]] = {}
        self.queue_messages: dict[int, discord.Message] = {}

    @commands.command(name="queuer")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def queuer(self, ctx: commands.Context, channel: discord.TextChannel):
        """Start or reset queue tracking in a text channel."""
        self.queue_channels[channel.id] = {}
        embed = self._build_embed(channel.id)
        message = await channel.send(embed=embed)
        self.queue_messages[channel.id] = message
        await ctx.send(f"Queue tracking started in {channel.mention}.", delete_after=5)

    @queuer.error
    async def queuer_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need Manage Messages to use this command.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !queuer {channel}", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid text channel.", delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id not in self.queue_channels:
            return

        content = message.content.strip()
        queue_match = QUEUE_MESSAGE_PATTERN.fullmatch(content)
        if queue_match:
            alt_number = int(queue_match.group(1) or 1)
            self.queue_channels[message.channel.id][(message.author.id, alt_number)] = QueueEntry(
                user=message.author,
                alt_number=alt_number,
                queue_number=int(queue_match.group(2)),
                updated_at=datetime.now(timezone.utc),
            )
        else:
            leave_match = LEAVE_MESSAGE_PATTERN.fullmatch(content)
            if leave_match:
                alt_number = int(leave_match.group(1) or 1)
                self.queue_channels[message.channel.id].pop((message.author.id, alt_number), None)

        await message.delete()
        await self._update_embed(message.channel.id)

    def _build_embed(self, channel_id: int) -> discord.Embed:
        embed = discord.Embed(description="currents queues:", color=discord.Color.blurple())
        entries = self.queue_channels.get(channel_id, {})

        if entries:
            lines = [
                f"{entry.user.mention} | alt {entry.alt_number} | q{entry.queue_number} | {discord.utils.format_dt(entry.updated_at, style='R')}"
                for entry in sorted(entries.values(), key=lambda item: (item.queue_number, item.updated_at))
            ]
            embed.add_field(name="", value="\n".join(lines), inline=False)

        return embed

    async def _update_embed(self, channel_id: int):
        queue_message = self.queue_messages.get(channel_id)
        if queue_message is None:
            return

        try:
            await queue_message.edit(embed=self._build_embed(channel_id))
        except discord.NotFound:
            self.queue_messages.pop(channel_id, None)


async def setup(bot: commands.Bot):
    await bot.add_cog(QueueCog(bot))