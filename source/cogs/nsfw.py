import discord
from discord.ext import commands
from .store import style_embed, is_embedable, shorten_url, pyout

import xml.etree.ElementTree as ET
import json
import aiohttp

class Nsfw:
	def __init__(self, bot):
		self.danbooru_thumbnail = 'https://tinyurl.com/ya9ug3la'
		self.bot = bot
		self.a = 0
		pyout('Cog {} loaded'.format(self.__class__.__name__))

	
	@commands.command(name="danbooru")
	async def _danbooru(self, ctx, *, tags: str=None):
		if tags is None:
			url = 'https://danbooru.donmai.us/posts.json?random=true'
		else:
			url = 'https://danbooru.donmai.us/posts.json?limit=50?tags=\"{tags}\"'.format(
				tags=tags.split(' ')
			)
			
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				j = json.loads(await resp.text())
					
				if not j:
					return await ctx.send('Nothing found')
				
				#todo there has to be a nicer way of doing this
				while True:
					try:
						post = j[self.a]
						self.a+=1
						break
					except IndexError:
						self.a = 0
								
				embed=style_embed(ctx, title='A post from danbooru',
				description='Posted by {}'.format(
					post['uploader_name']
				))
					
				tags = post['tag_string'].split(' ')
					
				embed.set_footer(text='With tags {}'.format(
				', '.join(tags[:5])),
				url=self.danbooru_thumbnail)
					
				if is_embedable(post['large_file_url']):
					embed.set_image(post['large_file_url'])
					
				embed.add_field(name='Image source',
				value=shorten_url(post['large_file_url']))
				
				await ctx.send(embed=embed)
	
	@commands.command(name='rule34')
	async def _rule34(self, ctx, *, tags: str=None):
		if tags is None:
			return await ctx.send('Due to current api limitations, you must request tags')
			
			url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags={tags}'.format(
				tags=tags.replace(' ', '%20')
			)
			
			async with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					tree = ET.parse(await resp.text())
					#todo find a way to get the image url from a json return to eliminate xml dependancy
					root = tree.getroot()
					
					if root.posts == 0:
						return await ctx.send('Nothing with tags {} found'.format(tags))

					while True:
						try:
							post = root[self.a]
							self.a+=1
							break
						except IndexError:
							self.a = 0

					#todo alot of testing
					tags = post.find('tags').text
					file_url = post.find('file_url').text

					#todo the rest of this
	
	@commands.command(name='gelbooru')
	async def _gelbooru(self, ctx, *, tags: str=None):
		if tags is None:
			return await ctx.send('Due to current api limitations, you must request tags')
		
		url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={tags}'.format(
			tags=tags.replace(' ', '%20')
		)
		
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				try:
					j = json.loads(await resp.text())
				except ValueError:
					return await ctx.send('Nothing with tags {} found'.format(tags))
				
				while True:
					try:
						post = j[self.a]
						self.a+=1
						break
					except IndexError:
						self.a = 0
						
				embed=style_embed(ctx, title='A post from gelbooru',
				description='Posted by {}'.format(post['owner']))
				
				tags = post['tags'].split(' ')
				
				#todo find gelbooru thumbnail
				embed.set_footer(text='With tags {}'.format(', '.join(tags[:5])))
					
				if is_embedable(post['file_url']):
					embed.set_image(post['file_url'])
				
				embed.add_field(name='Image source',
				value=shorten_url(post['file_url']))
				
				await ctx.send(embed=embed)
	
def setup(bot):
	bot.add_cog(Nsfw(bot))