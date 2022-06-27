from discord.ext import commands
from Utils import  getGeneralDataJSON
from Utils import getGlobalConfig

config = getGlobalConfig()

class GeneralBehaviour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cardinal logged as {self.bot.user}")

    #LOGIN

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == int(getGeneralDataJSON()["LoginMessageId"]):
            if payload.emoji.name == "💚":
                await payload.member.add_roles(payload.member.guild.get_role(config["UserRoleId"]))