import discord
from discord.ext import commands

import openai

openai.api_key = 'API KEY'
role = 'Give role for bot ,exemple : You are a Discord Bot'

bot = commands.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        content = message.content.replace(bot.user.mention, '')
        await message.channel.trigger_typing()
        
        referenced_messages = []
        reply_message_content = ""

        if message.reference is not None:
            referenced_message_id = message.reference.message_id
            referenced_channel = message.channel
            referenced_message = await referenced_channel.fetch_message(referenced_message_id)
            referenced_messages.append(referenced_message)

            while referenced_message.reference is not None:
                referenced_message_id = referenced_message.reference.message_id
                referenced_channel = referenced_message.channel
                referenced_message = await referenced_channel.fetch_message(referenced_message_id)
                referenced_messages.append(referenced_message)

        if referenced_messages:
            referenced_messages.reverse()
            for referenced_message in referenced_messages:
                author_name = referenced_message.author.name
                message_content = referenced_message.content
                reply_message_content += f"{author_name}: {message_content} ; "

            reply_message_content = reply_message_content.rstrip(" ; ")
            

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=str(role) + reply_message_content + "\n\n" + content,
            max_tokens=3000,
        )

        text = response.choices[0].text.strip()
        lentext = len(text)
        
        print(text)
        
        previous_length = 0
        
        if lentext >= 1999:
            while lentext >= 1950:
                
                words = text.split()
                x = []
                
                for index, word in enumerate(words):
                    word_length = len(word)
                    x.append(previous_length + word_length)
                    previous_length += word_length
                    if previous_length >= 1900:
                        await message.reply(text[:previous_length])
                        lentext = 0
                        break 

            await message.channel.send(text[previous_length:])
        else:
            if text:
                await message.reply(text)

bot.run('TOKEN')
