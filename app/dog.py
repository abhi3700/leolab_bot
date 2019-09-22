import requests
from input import Dog_API_URL_image, Dog_API_URL_breedslist

response1 = requests.get(Dog_API_URL_image.format(breed= 'wolfhound'), verify= False)
response_json1 = response1.json()

print(response_json1['message'])
print(response_json1['status'])

response2 = requests.get(Dog_API_URL_breedslist, verify= False)
response_json2 = response2.json()

# print(response_json2['message'].keys())

# convert `dict_keys` to `list`
breedslist = list(response_json2['message'].keys())
print(len(breedslist))
# print(type(list(response_json['message'].keys())))
print(breedslist)
print(response_json2['status'] == 'success')