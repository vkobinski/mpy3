import requests
import json
import urllib
from PIL import Image

def cover_spotify():
    ALBUM_COVER_IMAGE_PATH = requests.get("https://api.spotify.com/v1/search?q=let-it-be&type=album&limit=1", headers={'Authorization': 'Bearer BQDmBuyNu-oUXzJ_wtCX3xdLyueV5kMd86g8SYnkN5_vdSxeA3GKgqiTykiC5AUKI4SIJzqeNfzPbh2jXxKxC1jfFvrhVvfBmzKdEQBNYNLAIYsMiWim8MGLPQUuP42Kka8S4d2_YZgy7gfL3908S_qQeS67E_btlO4Sm6hmHHv68_SvWibSiQ22'})
    json_image = json.loads(ALBUM_COVER_IMAGE_PATH.text)
    print(type(json_image))

    IMAGE_PATH = json_image['albums']['items'][0]['images'][1]['url']
    urllib.request.urlretrieve(IMAGE_PATH, "sample.jpg")
    im = Image.open("sample.jpg")
    rgb_im = im.convert('RGB')
    rgb_im.save('sample.png')
    IMAGE_ALBUM = './sample.png'

cover_spotify()