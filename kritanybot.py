import discord
import os
import random
from discord import app_commands
from discord.ext import commands
import string
import sys

# You define the necessary intents
intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='?', intents=intents)

# Global variable to store the invoice count
invoice_count = 0

# File path for the invoice count file
INVOICE_COUNT_FILE = 'invoice_count.txt'

# Load invoice count from a file on bot startup
def load_invoice_count():
    global invoice_count
    try:
        with open(INVOICE_COUNT_FILE, 'r') as file:
            data = file.read().strip()
            print(f"Data read from file: {data}")  # Add this line
            if data:
                invoice_count = int(data)
                print(f"Loaded invoice count: {invoice_count}")
    except FileNotFoundError:
        print("Invoice count file not found. Creating a new one.")
        save_invoice_count()
    except ValueError:
        print("Error: Unable to load invoice count. File contains invalid data.")

# Save invoice count to a file on bot shutdown
def save_invoice_count():
    global invoice_count
    with open(INVOICE_COUNT_FILE, 'w') as file:
        file.write(str(invoice_count))
    print(f"Invoices Saving: {invoice_count}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="Virtual Life"))
    print('Bot is ready')
    load_invoice_count()

@bot.event
async def on_disconnect():
    print('Bot is disconnecting')
    save_invoice_count()

@bot.command()
async def invoice(ctx, user: discord.Member, payment_method: str, price: float, promo_percentage: float = 0):
    global invoice_count

    # Increment invoice count
    invoice_count += 1

    # Format invoice number
    invoice_number = str(invoice_count).zfill(3)

    # Calculate the promotional price
    promo_discount = price * (promo_percentage / 100)
    promo_price = price - promo_discount

    # Create embed
    embed = discord.Embed(
        title=f"Invoice #{invoice_number}",
        description="ᴹᴬᴰᴱ ᶠᴼᴿ ᴬ ⱽᴵᴿᵀᵁᴬᴸ ᴸᴵᶠᴱ ᴼᴿᴰᴱᴿ",
        color=0xFF5733
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1223622352953151660/1225141710359625798/Composition_1.gif?ex=663676a1&is=66352521&hm=642c6c4cfdbc73748b47369a86f75c2e0a908ad0bd35d41b6a0108fe15e8b1f6&")
    embed.add_field(name="Method of Payment", value=payment_method, inline=False)
    embed.add_field(name="Price", value=f"{price:.2f} (After {promo_percentage}% discount: {promo_price:.2f})", inline=False)
    embed.add_field(name="Promotional Discount", value=f"{promo_percentage}%", inline=False)
    embed.add_field(name="Status", value="UNPAID", inline=False)
    
    # Set image in the embed
    embed.set_image(url="https://cdn.discordapp.com/attachments/1213995896296177676/1225589808781328526/invoice.png?ex=66361db4&is=6634cc34&hm=95797c790f4742c5eea8ff2baff2bd3e9a2cfe53d8603a59a8fe87c2c8902bb6&")


    # Send the embed
    message = await ctx.send(embed=embed)

    # Pin the message
    await message.pin()

    # Save invoice count to file
    save_invoice_count()

@bot.command()
async def invoice_paid(ctx, invoice_id: int):
    try:
        # Fetch the original message by its ID
        message = await ctx.channel.fetch_message(invoice_id)

        # Check if the message contains an embed
        if message.embeds:
            # Get the first embed
            embed = message.embeds[0]

            # Find the index of the "Status" field
            status_index = None
            for index, field in enumerate(embed.fields):
                if field.name == "Status":
                    status_index = index
                    break

            # If "Status" field is found, update its value
            if status_index is not None:
                embed.set_field_at(index=status_index, name="Status", value="PAID", inline=False)
                await message.edit(embed=embed)
                await ctx.send("Invoice status updated to PAID.")
            else:
                await ctx.send("No 'Status' field found in the specified message.")
        else:
            await ctx.send("No embed found in the specified message. Please provide a valid invoice ID.")
    except discord.NotFound:
        await ctx.send("Invoice not found. Please provide a valid invoice ID.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def set_invoice_count(ctx, count: int):
    global invoice_count
    if count < 0:
        await ctx.send("Invoice count cannot be negative.")
        return

    invoice_count = count
    save_invoice_count()
    await ctx.send(f"Invoice count has been set to {count}.")

# Command to reload the bot
@bot.command()
async def reload(ctx):
    """Reload the entire bot."""
    await ctx.send("Reloading bot...")

    # Unload all extensions
    for extension in list(bot.extensions):
        bot.unload_extension(extension)

    # Reload the Python script
    python = sys.executable
    os.execl(python, python, *sys.argv)

bot.run('MTIzNjA0OTE5MzMwNzczNDEyOA.GbXAye.ZVK0bT-q-0gBAnapSNZ0NQPfZSrsvZpn2D1HV0')
