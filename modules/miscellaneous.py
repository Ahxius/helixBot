from discord.ext import commands
from asyncio import sleep


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
            if category.id == 825932087700881408:  # change this
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
        await sleep(30)
        if not await helix_server.get_channel(voice_channel.id).name:
            return
        if not voice_channel.members:
            await context.send(f'{context.author.mention}, your private VC timed out.')
            await voice_channel.delete()


def setup(client):
    client.add_cog(Miscellaneous(client))
