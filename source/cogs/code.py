import discord
from discord.ext import commands
import subprocess
import os
from platform import system
from shutil import which
from io import BytesIO
import pip

def install_command(name: str):
    operating = system()

    if operating == 'Darwin':
        cmd = subprocess.check_call(['brew', 'install', name])
    elif operating == 'Windows':
        print('this bot doesnt really work on windows')
        exit(5)
    elif operating == 'Linux':
        cmd = subprocess.check_call(['sudo', 'apt-get', 'install', name])
    else:
        print(f'{operating} is not a supported OS')
        exit(5)

def ensure_installs():
    if which('clang-format') is None:
        install_command('clang-format')
    else:
        print('clang-format detected')

    if which('yapf') is None:
        pip.main(['install', 'yapf'])
    else:
        print('yapf detected')

    if which('npm') is None:
        install_command('npm')

    if which('js-beautify') is None:
        subprocess.check_call(['npm', 'install', '-g', 'js-beautify'])
    else:
        print('js-beatify detected')

    if which('ktlint') is None:
        subprocess.check_call(['brew', 'install', 'shyiko/ktlint/ktlint'])
    else:
        print('ktlint detected')

class Code:
    def __init__(self, bot):
        self.bot = bot
        ensure_installs()

        if which('rustfmt') is None:
            print('rustfmt not detected, install this manually as it cannot be done in a script')
        else:
            print('rustfmt detected')

        print(f'cog {self.__class__.__name__} loaded')
    
    def trim_code(self, data: str, prefix: str):
        data = data.strip()

        while data.endswith('`'):
            data = data[:-1]

        while data.startswith('`'):
            data = data[1:]

        if data.startswith(prefix):
            data = data[len(prefix):]

        return data

    def dump_file(self, data: str, path: str):
        fd = open(f'cogs/temp/{path}', 'w+')
        fd.write(data)
        fd.close()

    def read_file(self, path: str):
        fd = open(f'cogs/temp/{path}', 'r')
        ret = fd.read()
        fd.close()

        return ret

    @commands.command(name = "kt-format")
    async def _kt_format(self, ctx, *, data: str):
        data = self.trim_code(data, 'kotlin')

        self.dump_file(data, f'{ctx.author.id}.temp.kt')

        try:
            subprocess.check_output(['ktlint', '-F', f'cogs/temp/{ctx.author.id}.temp.kt'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'ktlint failed with error code {e.returncode}')

        await ctx.send(f'```js\n{self.read_file(f"{ctx.author.id}.temp.kt")}```')

    @commands.command(name = "js-format")
    async def _js_beautify(self, ctx, *, data: str):
        data = self.trim_code(data, 'js')

        self.dump_file(data, f'{ctx.author.id}.temp.js')

        try:
            subprocess.check_output(['js-beautify', f'cogs/temp/{ctx.author.id}.temp.js'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'js-beautify failed with error code {e.returncode}')

        await ctx.send(f'```js\n{self.read_file(f"{ctx.author.id}.temp.js")}```')

    @commands.command(name = "rs-format")
    async def _rustfmt(self, ctx, *, data: str):
        data = self.trim_code(data, 'rs')

        self.dump_file(data, f'{ctx.author.id}.temp.rs')

        try:
            subprocess.check_output(['rustfmt', '--emit', 'files', f'cogs/temp/{ctx.author.id}.temp.rs'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'rustfmt failed with error code {e.returncode}')

        await ctx.send(f'```rs\n{self.read_file(f"{ctx.author.id}.temp.rs")}```')

    @commands.command(name = "cpp-format")
    async def _clang_format(self, ctx, *, data: str):
        data = self.trim_code(data, 'cpp')
        
        self.dump_file(data, f'{ctx.author.id}.temp.cpp')
        
        try:
            subprocess.check_output(['clang-format', '-i', '-style=llvm', f'cogs/temp/{ctx.author.id}.temp.cpp'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'clang-format failed with error code {e.returncode}')

        await ctx.send(f'```cpp\n{self.read_file(f"{ctx.author.id}.temp.cpp")}```')

    @commands.command(name = "c-format")
    async def _c_format(self, ctx, *, data: str):
        data = self.trim_code(data, 'c')

        self.dump_file(data, f'{ctx.author.id}.temp.c')

        try:
            subprocess.check_output(['clang-format', '-i', '-style=llvm', f'cogs/temp/{ctx.author.id}.temp.c'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'clang-format failed with error code {e.returncode}')

        await ctx.send(f'```c\n{self.read_file(f"{ctx.author.id}.temp.c")}```')

    @commands.command(name = "py-format")
    async def _yapf(self, ctx, *, data: str):
        data = self.trim_code(data, 'py')

        self.dump_file(data, f'{ctx.author.id}.temp.py')
        
        try:
            subprocess.check_output(['yapf', '-i', f'cogs/temp/{ctx.author.id}.temp.py'])
        except subprocess.CalledProcessError as e:
            return await ctx.send(f'yapf failed with error code {e.returncode}')

        await ctx.send(f'```py\n{self.read_file(f"{ctx.author.id}.temp.py")}```')

def setup(bot):
    bot.add_cog(Code(bot))