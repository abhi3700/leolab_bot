"""
    This file - `db.py` is to check the database data.
"""
import redis
import pandas as pd
import json
from input import REDIS_URL



# ---------------------------------------------------------------
# define Redis database
r = redis.from_url(REDIS_URL)

print(r.keys())

# phoneno1 = '918145634656'
# r.set('918145634656', json.dumps(dict(username= "abhi3701", breed_choice= "labrador")))
# -----------------------------------------------------------------------------
# df = pd.read_csv('../data/breeds.csv')
# breed_list = df['breed'].tolist()
# print(len(breed_list))
# M-1
# """push the item into breeds list from behind"""
# for b in breed_list:
    # print(b)
    # r.rpush('breeds_list', b)    # insert from right side of the list
# print(r.lindex('breeds_list', 0).decode('utf-8'))    # first item
# print(f'first breed: {r.lindex('breeds_list', 0).decode('utf-8')}')    # first item

# M-2
"""push the breeds into a set"""
# print('--------------------------------------------')
# r.sadd('breeds_set', str(breed_list))
# r.sadd('breeds_set',  bytearray(breed_list))
# breed_list_get = r.smembers('breeds_set')
# e = next(iter(breed_list_get)).decode('utf-8')
# print(f'the list: {e}')
# print(type(e))
# b_l_g_list = list(breed_list_get)[0].decode('utf-8')
# print(type(b_l_g_list))
# print(type(breed_list_get))

# keys_list = r.keys()
# del keys_list[0]
# print(keys_list)
# l = [list.index(b'breeds')]
# l = l.remove(b'breeds')
# for i in r.keys():
#     if i.decode('utf-8') != 'breeds':
#         l.append(i)
# print(l)
# for k in r.keys().remove(b'breeds'):
#     print(k)
# -----------------------------------------------------------------------------
"""Finding the phone no. if username exists"""
# key_phone = ""
# for k in keys_list:
#     # print(k.decode('utf-8'))
#     dict_nested2_val2 = json.loads(r.get(k.decode('utf-8')))
#     if dict_nested2_val2['username'] == 'abhi3701':
#         key_phone = k.decode('utf-8')

# print(key_phone)

# -----------------------------------------------------------------------------
"""delete all stored keys"""
# for k in r.keys():
#     r.delete(k)

# -----------------------------------------------------------------------------
"""print all keys"""
for k in r.keys():
    k_decoded = k.decode('utf-8')
    # print(k_decoded)
    print(json.loads(r.get(k_decoded).decode('utf-8')))
    # print(json.loads(r.get(k_decoded).decode('utf-8'))['username'])
    # print(json.loads(r.get(k_decoded).decode('utf-8'))['breed_choice'])
# print(r.keys())