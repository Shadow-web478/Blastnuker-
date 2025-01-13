import discord
from discord.ext import commands
import asyncio
import logging

# Configure logging for better output management
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to securely load the token and prefix
def get_token_and_prefix():
    token = input("Enter your bot token: ")
    prefix = input("Enter your bot prefix: ")
    return token, prefix

# Display banner function
def display_banner():
    banner_text = """
  ____  _           _     _   _       _             
 |  _ \\| |         | |   | \\ | |     | |            
 | |_) | | __ _ ___| |_  |  \\| |_   _| | _____ _ __ 
 |  _ <| |/ _` / __| __| | . ` | | | | |/ / _ \\ '__|
 | |_) | | (_| \\__ \\ |_  | |\\  | |_| |   <  __/ |   
 |____/|_|\\__,_|___/\\__| |_| \\_|\\__,_|_|\_\\___|_|   
                                                    
                                                    
"""
    logger.info(banner_text)

# Bot setup
def main():
    # Securely load token and prefix
    token, prefix = get_token_and_prefix()

    # Set up intents
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    # Initialize bot
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    bot.remove_command("help")

    # Event for when the bot is ready
    @bot.event
    async def on_ready():
        logger.info(f'Logged in as {bot.user.name}')
        logger.info(f'Bot ID: {bot.user.id}')
        display_banner()

        # Display the list of commands in a predefined channel
        channel = bot.get_channel(123456789012345678)  # Replace with your actual channel ID
        if channel:
            await display_command_list(channel)

    # Display command list in the channel
    async def display_command_list(channel):
        command_list = """
        Here are the available commands:
        [1] - Ban all members
        [2] - Delete Channels
        [3] - Delete Roles
        [4] - Kick Members
        [5] - Prune Members
        [6] - Create Channels
        [7] - Spam All Channels
        [8] - Create Roles
        [9] - Delete Roles
        [10] - Rename Channels
        [11] - Rename Guild
        [12] - Rename Roles
        [13] - Credits
        [14] - Exit
        """
        
        # Create embed with green color
        embed = discord.Embed(title="Command List", description=command_list, color=discord.Color.green())
        embed.set_footer(text="Use with caution! Commands are powerful.")
        
        # Send the embed to the desired channel
        await channel.send(embed=embed)

    # Command to check bot permissions
    def check_permissions(ctx, perm):
        if not getattr(ctx.author.guild_permissions, perm):
            raise commands.MissingPermissions([perm])

    # Command to ban all members concurrently
    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban_all(ctx):
        try:
            check_permissions(ctx, "ban_members")
            success_msgs = []
            failure_msgs = []
            tasks = [ban_member(ctx, member, success_msgs, failure_msgs) for member in ctx.guild.members if not member.bot]
            await asyncio.gather(*tasks)
            
            # Send success and failure summaries
            success_embed = discord.Embed(description=f"Successfully banned {len(success_msgs)} members.", color=discord.Color.green())
            failure_embed = discord.Embed(description=f"Failed to ban {len(failure_msgs)} members.", color=discord.Color.red())
            
            await ctx.send(embed=success_embed)
            await ctx.send(embed=failure_embed)
        
        except Exception as e:
            logger.error(f"Error banning members: {e}")
            await ctx.send("An error occurred while trying to ban members.")
        
    # Placeholder function for banning a member
    async def ban_member(ctx, member, success_msgs, failure_msgs):
        try:
            await member.ban()
            success_msgs.append(member.name)
        except Exception as e:
            failure_msgs.append(member.name)
            logger.error(f"Failed to ban {member.name}: {e}")

    # Run the bot
    bot.run(token)

# Run the bot setup
if __name__ == "__main__":
    main()