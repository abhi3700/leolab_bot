# import pandas as pd
import redis
import json
import requests
from spellchecker import SpellChecker
from input import *



# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)



spell = SpellChecker()

# # Python3 program to Check if given words 
# # appear together in a list of sentence 

def check(sentence, words): 
    res = [all([k in s for k in words]) for s in sentence] 
    return [sentence[i] for i in range(0, len(res)) if res[i]] 
    
# parse breeds list from REDIS DB to a var
sentence = []   # initialize
response = requests.get(Dog_API_URL_breedslist, verify= False)
response_json = response.json()

if response_json['status'] == 'success':
    sentence = list(response_json['message'].keys())
    text_input = 'road'    # input
    words = text_input.split()  # if contains space or not, it will split the words into an array

    sugg_list = check(sentence, words)

    # # find those words (in list) that may be misspelled based on English dictionary
    misspelled = spell.unknown(words)
    print(misspelled)

    if len(misspelled):                 # based on dictionary
        print("Please check the spelling...")
        for word in misspelled:
            # Get the one `most likely` answer
            print(f'Correct word may be: {spell.correction(word)}')

            # Get a list of `likely` options
            print(f'Probable words: {spell.candidates(word)}')

    elif len(sugg_list):          # based on the custom list
        print("Correct! the word is found.")
        # print(sugg_list)
    else:
        print('The word doesn\'t exist in our database.')
else:
    print('Server Error')

