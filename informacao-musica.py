import requests
import json
import urllib
from PIL import Image

url = "https://shazam.p.rapidapi.com/search"

musica = input('Insira a musica a buscar: ')

querystring = {"term":musica,"locale":"en-US","offset":"0","limit":"5"}

headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': "aa378c64a6msh6244ac8c2547183p1c403cjsn2b48c94b45e9"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

response = json.loads(response.text)
key = response['tracks']['hits'][0]['track']['key']
print(key)

url = "https://shazam.p.rapidapi.com/songs/get-details"

querystring = {"key": key,"locale":"en-US"}

headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': "aa378c64a6msh6244ac8c2547183p1c403cjsn2b48c94b45e9"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_obj = json.loads(response.text)
json_obj['images']['background']

urllib.request.urlretrieve(json_obj['images']['background'], "sample.jpg")
im = Image.open("sample.jpg")
rgb_im = im.convert('RGB')
rgb_im.save('sample.png')
IMAGE_ALBUM = './sample.png'
img = Image.open(IMAGE_ALBUM)
img.show()