import botogram
from input import *
import requests


bot = botogram.create(API_key)
bot.about = "This is a Dog Bot.\nThis gives random images of Dog."
bot.owner = "@abhi3700"

response = requests.get("https://dog.ceo/api/breed/<breed_name>/images/random")

@bot.command("show")
def show_command(chat, message, args):
    """Show random images of Dogs"""
    if response.status
    chat.send("https://dog.ceo/api/breed/labrador/images/random")

if __name__ == "__main__":
    bot.run()