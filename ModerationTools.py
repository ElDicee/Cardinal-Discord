import discord
from discord.ext import commands
from Utils import getGeneralDataJSON
from Utils import writeGeneralDataJSON
from Utils import getDefaultEmbedWith
from asyncio import sleep


class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, context, limit: int):
        if context.author.guild_permissions.manage_messages:
            await context.channel.purge(limit=limit)

    @commands.command()
    async def setLoginMessageId(self, context, id):
        if context.author.guild_permissions.administrator:
            current = getGeneralDataJSON()
            current["LoginMessageId"] = int(id)
            writeGeneralDataJSON(current)
            txt = await context.channel.send(embed=getDefaultEmbedWith(title="Info", inline=False, args={
                "Éxito": "La id se ha establecido correctamente."}))
            await sleep(2)
            await context.channel.delete_messages([txt, context.message])
            msg = await context.channel.fetch_message(id)
            await msg.add_reaction("💚")
