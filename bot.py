import botogram
from input import *
import requests
import json
from bs4 import BeautifulSoup


bot = botogram.create(API_key)
bot.about = "This is a Dog Bot.\nThis gives random images of Dog."
bot.owner = "@abhi3700"


def readstream(r):
    rsvp_list = []
    for raw_rsvp in r.iter_lines():
        if raw_rsvp:
            rsvp = json.loads(raw_rsvp)
            rsvp_list.append(rsvp)
    return rsvp_list

@bot.command("show")
def show_command(chat, message, args):
    """Show random images of Dogs"""
    response = requests.get("https://random.dog/woof.json?filter=mp4,webm", verify=False)
    html_page = readstream(response)
    chat.send(html_page[0]['url'])
    # chat.send("https://random.dog/woof.json?filter=mp4,webm")
    
if __name__ == "__main__":
    bot.run()