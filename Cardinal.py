import discord
from discord.ext import commands
import ProjectManagementSystem
from GeneralBehaviour import GeneralBehaviour
from ModerationTools import ModerationTools
from Utils import getGlobalConfig

def setupConfig():
     global config
     config = getGlobalConfig()

def main():
    client = commands.Bot(command_prefix="$")
    client.add_cog(GeneralBehaviour(client))
    client.add_cog(ModerationTools(client))
    client.add_cog(ProjectManagementSystem.PMS(client))
    print("Initializing...")
    client.run(config["Token"])

if __name__ == "__main__":
    setupConfig()
    main()