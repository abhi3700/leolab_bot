import botogram
import redis
import requests
import json
from spellchecker import SpellChecker
from input import *


bot = botogram.create(API_key)
bot.about = "This is a Dog Bot.\nIt gives random images of Dog based on preferred breed by user."
bot.owner = "@abhi3700"
# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

# -------------------------------------------------------Spell------------------------------------------------------------------------
spell = SpellChecker()

# Python3 program to Check if given words appear together in a list of sentence 
def check(sentence, words): 
    res = [all([k in s for k in words]) for s in sentence] 
    return [sentence[i] for i in range(0, len(res)) if res[i]]

# =======================================================Share phone via keyboard===========================================================================
@bot.command("sharephone")
def sharephone_command(chat, message, args):
    """Share your phone no. via clicking the keyboard below."""    
    bot.api.call('sendMessage', {
        'chat_id': chat.id,
        'text': 'Please click on \'Phone no.\' button below to share your phone no.',
        'reply_markup': json.dumps({
            'keyboard': [
                [
                    {
                        'text': 'Phone no.',
                        'request_contact': True,
                    },
                ],
            ],
            # These 3 parameters below are optional
            # See https://core.telegram.org/bots/api#replykeyboardmarkup
            'resize_keyboard': True,
            'one_time_keyboard': True,
            'selective': True,
        }),
    })

# # =======================================================Set Breed via keyboard===========================================================================
@bot.command("setbreed")
def setbreed_command(chat, message, args):
    """Set your preferred breed via clicking the keyboard below."""
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    for k in r.keys():
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
        if dict_nested2_val2['username'] == message.sender.username:
            key_phone = k.decode('utf-8')

    # chat.send('phone no. {phone}'.format(phone=key_phone))  # for DEBUG
    if key_phone != "":
        chat.send('Please type your breed below:')
    else:
        chat.send("Please, share the phone no. first via /sharephone")

# =======================================================Process messages===========================================================================
@bot.process_message
def button_messages_are_like_normal_messages(chat, message):
    if message.text:
        text_in = message.text.lower()
        chat.send("'You wrote \'{text}\'".format(text= text_in))

        # find the root phoneno. if username is available in REDIS DB
        key_phone = ""
        for k in r.keys():
            # chat.send(k.decode('utf-8'))
            dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
            if dict_nested2_val2['username'] == message.sender.username:
                key_phone = k.decode('utf-8')

        if key_phone != "":
            # chat.send('The selected breed is: \'{breed}\''.format(breed=json.loads(r.get(key_phone).decode('utf-8'))['breed_choice']))
            sentence = []   # initialize
            response = requests.get(Dog_API_URL_breedslist, verify= False)
            response_json = response.json()

            if response_json['status'] == 'success':
                sentence = list(response_json['message'].keys())

                words = []  # intialize

                words = text_in.split()    # if contains space or not, it will split the words into an array
                sugg_list = check(sentence, words)
                # chat.send("suggestion list: {sugg_list}".format(sugg_list= sugg_list))    # for DEBUG

                # # find those words (in list) that may be misspelled based on English dictionary
                misspelled = spell.unknown(words)
                # chat.send("misspelled: {misspelled}".format(misspelled= misspelled))    # for DEBUG

                if len(misspelled):                 # based on dictionary
                    chat.send("Please check the spelling...")
                    for word in misspelled:
                        # Get the one `most likely` answer
                        chat.send("Did you mean \'{word}\' ?".format(word= spell.correction(word)))

                        # Get a list of `likely` options
                        chat.send('Probable words: {word}'.format(word= spell.candidates(word)))
                        chat.send("SORRY! Please, try again via /setbreed command.")

                else:          # based on the custom list
                    r.set(key_phone, json.dumps(dict(username= message.sender.username, breed_choice= text_in)))
                    chat.send("Okay! the breed is saved now.")
                    # chat.send(sugg_list)
            else:
                chat.send('Server Error')
        else:
            chat.send("Please, share the phone no. first via /sharephone.")

    elif message.contact:
        phoneno = message.contact.phone_number
        phoneno = phoneno.replace("+", "")      # '+91343242343' --> '91343242343'Unlike phone app, in Telegram desktop app, it's '+' sign in phone no.

        # Create a node - `phone` and store `username` in REDIS DB. This is bcoz in botogram, can't set global_variable.
        r.set(phoneno, json.dumps(dict(username= message.sender.username)))

        # find the root phoneno. if username is available in REDIS DB
        key_phone = ""
        for k in r.keys():
            # chat.send(k.decode('utf-8'))
            dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
            if dict_nested2_val2['username'] == message.sender.username:
                key_phone = k.decode('utf-8')

        chat.send('You choose to send your contact no.: \'{phone}\''.format(phone= key_phone))
        chat.send("Now, you can set your preferred breed via /setbreed command.")
        chat.send('Press /removekeyboard to remove the annoying keyboard')


# ===================================================remove keyboard(s)=================================================================
@bot.command("removekeyboard")
def removekeyboard_command(chat, message):
    """removes the keyboard appearing below"""
    bot.api.call('sendMessage', {
        'chat_id': chat.id,
        'reply_to_message': message.id,
        'text': 'keyboards removed.',
        'reply_markup': json.dumps({
            'remove_keyboard': True,
            # This 1 parameter below is optional
            # See https://core.telegram.org/bots/api#replykeyboardremove
            'selective': True,
        })
    })

# ===============================================Show images=================================================
@bot.command("show")
def show_command(chat, message, args):
    """Show random images of Dogs"""
    # find the root phoneno. if username is available in REDIS DB
    key_phone = ""
    for k in r.keys():
        # chat.send(k.decode('utf-8'))
        dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
        if dict_nested2_val2['username'] == message.sender.username:
            key_phone = k.decode('utf-8')

    # chat.send('phone no. {phone}'.format(phone=key_phone))  # for DEBUG
    if key_phone != "":
        breed = json.loads(r.get(key_phone).decode('utf-8'))['breed_choice']
        # chat.send("breed: {breed}".format(breed=breed))     # for DEBUG

        response = requests.get(Dog_API_URL_image.format(breed= breed), verify=False)
        response_json = response.json()
        # chat.send('response: {response}'.format(response=response_json))    # for DEBUG
        if response_json['status'] == 'success':
            chat.send(response_json['message'])
            # chat.send("https://random.dog/woof.json?filter=mp4,webm")
        else:
            chat.send('SORRY! Server problem. Please raise the query at @abhi3700.')
    else:
        chat.send("Please, share the phone no. first via /sharephone")

# ================================================MAIN===========================================================================    
if __name__ == "__main__":
    bot.run()