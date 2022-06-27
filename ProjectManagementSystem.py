import discord
from discord.ext import commands
from Utils import getGlobalConfig
from Utils import getDefaultEmbedWith
from Utils import getProjectsJSON
from Utils import writeProjectsJSON
import random


class PMS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global config
        config = getGlobalConfig()

    @commands.command()
    async def project(self, context, *args):
        if context.channel.id == int(config["TerminalChannelId"]):
            if len(args) > 0:
                if str(args[0]).lower() == "create":
                    if len(args) > 1:
                        try:
                            b = len(list(getProjectsJSON()["authorsInfo"][str(context.author.id)])) < int(
                                config["MaxOwnProjects"])
                        except:
                            b = True
                        if b:
                            if not alreadyExists(args[1], context.author.id):
                                role = None

                                for r in context.guild.roles:
                                    if r.id == int(config["UserRoleId"]):
                                        role = r
                                        break

                                cat = await context.guild.create_category(f"ρяσנє¢т: {args[1]}")
                                await cat.create_text_channel("ιηƒσ")
                                await cat.create_text_channel("∂євαтє")
                                await cat.create_text_channel("αναη¢єѕ")

                                await cat.create_voice_channel("∂ιѕ¢υѕιóη")

                                await cat.set_permissions(role, view_channel=False)
                                await cat.set_permissions(context.guild.default_role, view_channel=False)

                                role = await context.guild.create_role(name=args[1],
                                                                       colour=discord.colour.Colour.from_rgb(
                                                                           random.randint(0, 255),
                                                                           random.randint(0, 255),
                                                                           random.randint(0, 255)))
                                await context.author.add_roles(role)
                                await cat.set_permissions(role, view_channel=True)

                                p = Project(args[1], context=context, json=False)
                                p.setup(authname=context.author.name, authid=context.author.id, contrib=[],
                                        assignedCategoryId=cat.id, RoleId=role.id)
                                p.addContrib(context.author.id)

                                p.saveToFile()
                                await context.channel.send(
                                    embed=getDefaultEmbedWith(title="Operación realizada con éxito",
                                                              color=(30, 220, 30), args={
                                            "Info": f":white_check_mark: Se ha creado el proyecto: {p.name}",
                                            "Dueño": p.authorName}))
                            else:
                                await context.channel.send(embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30),
                                                                                     args={
                                                                                         "Oups!": "Parece que ya te pertenece un proyecto con el mismo nombre."}))
                        else:
                            await context.channel.send(embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30),
                                                                                 args={
                                                                                     "Oups!": "Has alcanzado el máximo número de proyectos en tu propiedad."}))
                    else:
                        await context.channel.send(embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                            "Oups!": "Debes especificar el nombre del proyecto.",
                            "Ejemplo": "$project create miproyecto"}))
                elif str(args[0]).lower() == "remove":
                    if len(args) > 1:
                        if alreadyExists(args[1], context.author.id):
                            p = Project(args[1], context=context)
                            await p.destroyProject()
                            await context.channel.send(
                                embed=getDefaultEmbedWith(title="Operación realizada con éxito", color=(30, 220, 30),
                                                          args={
                                                              "Info": f":white_check_mark: Se ha eliminado el proyecto: {p.name}",
                                                              "Dueño": p.authorName}))
                        else:
                            await context.channel.send(
                                embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                                    "Oups!": "No se ha encontrado el proyecto."}))
                    else:
                        await context.channel.send(embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                            "Oups!": "Debes especificar el nombre del proyecto.",
                            "Ejemplo": "$project remove miproyecto"}))
                elif str(args[0]).lower() == "manage":
                    if len(args) > 1:
                        project = args[1]
                        if len(args) > 2:
                            if alreadyExists(project, context.author.id):
                                if args[2].lower() == "contributor":
                                    if len(args) > 3:
                                        if args[3].lower() == "add":
                                            if len(args) > 4:
                                                p = Project(name=project, context=context)
                                                for m in context.message.mentions:
                                                    p.addContrib(m.id)
                                                    await m.add_roles(m.guild.get_role(p.RoleId))
                                            else:
                                                await context.channel.send(
                                                    embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                                                        "Oups!": "Debes mencionar al usuario que quieres añadir como contribuidor."}))
                                        elif args[3].lower() == "remove":
                                            if len(args) > 4:
                                                p = Project(name=project, context=context)
                                                for m in context.message.mentions:
                                                    p.removeContrib(m.id)
                                                    await m.remove_roles(m.guild.get_role(p.RoleId))
                                            else:
                                                await context.channel.send(
                                                    embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                                                        "Oups!": "Debes mencionar al usuario que quieres añadir como contribuidor."}))
                                        else:
                                            await context.channel.send(
                                                embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                                                    "Oups!": "Orden desconocida",
                                                "Ordenes disponibles:": "add/remove"}))
                                    else:
                                        await context.channel.send(
                                            embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                                                "Oups!": "Se requiere una orden.",
                                                "Ordenes disponibles:": "add/remove"}))
                        else:
                            await context.channel.send(
                                embed=getDefaultEmbedWith(title="**Lista de argumentos**",
                                                          args={
                                                              "contributor": "Gestiona los colaboradores del proyecto.",
                                                              "migrate": "Transfiere la propiedad del proyecto a otra persona.",
                                                              "ping": "Llama a los colaboradores.",
                                                              "customize": "Personaliza el proyecto."}))
                    else:
                        await context.channel.send(embed=getDefaultEmbedWith(title="Error", color=(220, 30, 30), args={
                            "Oups!": "Debes especificar el nombre del proyecto.",
                            "Ejemplo": "$project manage miproyecto"}))
            else:
                await context.channel.send(embed=getDefaultEmbedWith(args={"create": "Crea un nuevo proyecto.",
                                                                           "remove": "Elimina un proyecto existente.",
                                                                           "manage": "Gestiona alguno de tus proyectos."},
                                                                     title="**Lista de argumentos**"))
        else:
            await context.message.delete()
            await context.channel.send("Los comandos se deben ejecutar en #тєямιηαℓ")


class Project():
    def __init__(self, name, context, json: bool = True):
        self.name = name
        self.context = context
        self.currentPhysicalData = getProjectsJSON()
        if json:
            mainJson = getProjectsJSON()["projects"]
            self.authorName = mainJson[self.name]["Author"][0]
            self.authorId = int(mainJson[self.name]["Author"][1])
            self.contributors = list(mainJson[self.name]["Contributors"])
            self.assignedCategoryId = int(mainJson[self.name]["Category"])
            self.RoleId = int(mainJson[self.name]["RoleId"])

    def setup(self, authname: str, authid: int, contrib: list, assignedCategoryId: int, RoleId: int):
        self.authorName = authname
        self.authorId = authid
        self.contributors = contrib
        self.assignedCategoryId = assignedCategoryId
        self.RoleId = RoleId
        try:
            self.currentPhysicalData["authorsInfo"][str(authid)].append(self.name)
        except:
            self.currentPhysicalData["authorsInfo"][str(authid)] = [self.name]

    def addContrib(self, id):
        if not id in self.contributors:
            self.contributors.append(id)

    def removeContrib(self, id):
        if id in self.contributors:
            self.contributors.pop(id)

    def migrateAuthor(self, name, id):
        self.authorName = name
        self.authorId = id

    def saveToFile(self):
        try:
            self.currentPhysicalData["projects"][self.name]["Author"] = [self.authorName, self.authorId]
            self.currentPhysicalData["projects"][self.name]["Contributors"] = self.contributors
            self.currentPhysicalData["projects"][self.name]["Category"] = self.assignedCategoryId
            self.currentPhysicalData["projects"][self.name]["RoleId"] = self.RoleId
        except:
            self.currentPhysicalData["projects"][self.name] = {}
            self.saveToFile()
        writeProjectsJSON(self.currentPhysicalData)

    async def destroyProject(self):
        c = None
        for cat in self.context.guild.categories:
            if cat.id == self.assignedCategoryId:
                c = cat
                break
        for text in c.text_channels:
            await text.delete()
        for voice in c.voice_channels:
            await voice.delete()
        await c.delete()
        await self.context.guild.get_role(self.RoleId).delete()
        del self.currentPhysicalData["projects"][self.name]
        self.currentPhysicalData["authorsInfo"][str(self.authorId)].remove(self.name)
        writeProjectsJSON(self.currentPhysicalData)

def alreadyExists(name: str, authid: int):
    try:
        b = name in list(getProjectsJSON()["authorsInfo"][str(authid)])
    except:
        b = False
    return b