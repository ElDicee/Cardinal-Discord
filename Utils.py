import discord
import json


def getGlobalConfig():
    f = open("config.json", "r")
    j = json.loads(" ".join([line for line in f.readlines()]))
    f.close()
    return j


config = getGlobalConfig()


def getDefaultEmbedWith(args: dict, title, inline=False, color: tuple = (52, 242, 223)):
    embed = discord.Embed(title=title, color=discord.Color.from_rgb(color[0], color[1], color[2]), inline=inline)
    embed.set_footer(text=f"Cardinal by {config['Author']}")
    for name in args.keys():
        embed.add_field(name=name, value=args.get(name))
    return embed


def getProjectsJSON():
    f = open("DB/projects.json", "r")
    j = json.loads(" ".join([line for line in f.readlines()]))
    f.close()
    return j


def writeProjectsJSON(data):
    f = open("DB/projects.json", "w")
    f.write(json.dumps(data))
    f.close()


def getGeneralDataJSON():
    f = open("DB/GeneralData.json", "r")
    j = json.loads(" ".join([line for line in f.readlines()]))
    f.close()
    return j


def writeGeneralDataJSON(data):
    f = open("DB/GeneralData.json", "w")
    f.write(json.dumps(data))
    f.close()
