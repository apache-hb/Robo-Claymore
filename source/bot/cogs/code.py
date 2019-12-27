from claymore import Wheel
import discord
from discord.ext import commands
import subprocess
from inspect import getsource, getfile
from os.path import relpath
from yapf.yapflib.yapf_api import FormatCode

class Code(Wheel):
    @commands.command(
        name = 'source',
        brief = 'fetch the source code of a function or cog'
    )
    async def _source(self, ctx, *, name: str = None):
        if name is None:
            return await ctx.send('https://github.com/Apache-HB/Robo-Claymore')

        func = ctx.bot.get_command(name)

        if func is None:
            return await ctx.send(f'No command called {name} found')

        ret = getsource(func.callback)
        if len(ret) > 1950:
            return await ctx.send(f'https://github.com/Apache-HB/Robo-Claymore/source/bot/{relpath(getfile(func.callback))}')

        await ctx.send(f'```py\n{ret}```')

    @commands.command(
        name = 'pep8',
        brief = 'format python code with pep8'
    )
    async def _pep8(self, ctx, *, code: str):
        code = code.strip('```').strip('py')
        await ctx.send(f'```py\n{code}```')

    @commands.command(
        name = 'clang-format',
        brief = 'format c/c++ code with clang-format (LLVM style)'
    )
    async def _clang_format(self, ctx, *, code: str):
        code = code.strip('```').strip('c').strip('pp')
        prog = subprocess.Popen(f'echo "{code}" | clang-format --style=LLVM', shell = True, stdout = subprocess.PIPE)
        out, err = prog.communicate()
        await ctx.send(f'```cpp{out.decode("ascii")}```')


def setup(bot):
    bot.add_cog(Code(bot))