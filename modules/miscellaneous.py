from discord.ext import commands
from asyncio import sleep
import sys
from discord import PermissionOverwrite


class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='channel', aliases=['private', 'vc', 'temp'])
    async def channel(self, context, quantity: int = None):
        if not quantity:
            await context.send("``h?channel <max amt of people>``")
            return
        helix_server = self.client.get_guild(824783141855166514)
        for category in helix_server.categories:
            if category.id == 836394405274976258:
                private_category = category
                break
        x = 1
        for channel in helix_server.voice_channels:
            if 'Private VC' in channel.name:
                x += 1
        # noinspection PyUnboundLocalVariable
        voice_channel = await helix_server.create_voice_channel(name=f'Private VC #{x}', user_limit=quantity,
                                                                reason=f'Requested by {context.author.nick}',
                                                                category=private_category)
        visitor_role = helix_server.get_role(824792388013785169)
        helix_role = helix_server.get_role(824791320446238740)
        officer_role = helix_server.get_role(824791253995487282)
        default_overwrite = voice_channel.overwrites_for(visitor_role)
        default_overwrite.view_channel = True
        default_overwrite.connect = True
        default_overwrite.speak = True
        default_overwrite.use_voice_activation = True
        await voice_channel.set_permissions(visitor_role, overwrite=default_overwrite)
        await voice_channel.set_permissions(helix_role, overwrite=default_overwrite)
        default_overwrite.mute_members = True
        default_overwrite.deafen_members = True
        await voice_channel.set_permissions(officer_role, overwrite=default_overwrite)
        await sleep(30)
        if not helix_server.get_channel(voice_channel.id).name:
            return
        if not voice_channel.members:
            await context.send(f'{context.author.mention}, your private VC timed out.')
            await voice_channel.delete()

    @commands.command(name='clean')
    async def clean(self, context):
        member_roles = context.author.roles
        helix_server = self.client.get_guild(824783141855166514)
        hicom_role = helix_server.get_role(824791164019802112)
        if hicom_role not in member_roles and context.author.id != 193051160616239104:
            await context.send(f'You do not have proper permissions to use this command.')
            return
        voice_channels = helix_server.voice_channels
        for channel in voice_channels:
            if 'Private VC' in channel.name:
                await channel.delete()

    @commands.command(name='shutdown', hidden=True)
    @commands.is_owner()
    async def shutdown(self, context):
        await context.send(f'Shutting down...')
        sys.exit()


def setup(client):
    client.add_cog(Miscellaneous(client))
