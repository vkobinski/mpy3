import requests
import json
from PIL import Image
import urllib

def acessa_letra():

    url = "https://shazam.p.rapidapi.com/search"

    querystring = {"term":"PO BOX","locale":"en-US","offset":"0","limit":"5"}

    headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': "aa378c64a6msh6244ac8c2547183p1c403cjsn2b48c94b45e9"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    for musica in response['tracks']['hits']:
        print(musica['track']['title'])
        urllib.request.urlretrieve(musica['track']['share']['image'], "sample.jpg")
        im = Image.open("sample.jpg")
        rgb_im = im.convert('RGB')
        rgb_im.save('sample.png')
        IMAGE_ALBUM = './sample.png'
        img = Image.open(IMAGE_ALBUM)
        img.show()

if __name__ == '__main__':
    acessa_letra()