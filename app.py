import PySimpleGUI as sg
import os
from PySimpleGUI.PySimpleGUI import RELIEF_FLAT
import requests
import json
from PIL import Image
import urllib
import threading
from utils.music_utilities import aumentar, diminuir, get_files_inside_directory_not_recursive, play_sound, is_sound_playing, pause_sounds, posicao, stop_sounds, unpause, volume
from ShazamAPI import Shazam
import misc

tocando = False

sg.theme('Reddit')
song_title_column = [
    [sg.Text(text='Press play..', justification='center', background_color='black',
             text_color='white', size=(200, 0), font='Roboto', key='song_name')]
]

currently_playing = [
    [sg.Text(background_color='black', size=(200, 0), text_color='white',
             font=('Tahoma', 10), key='currently_playing')]
]

timer_volume = [
    [sg.Text('0:00/0:00', key='tempo', background_color='black', text_color='white'),
    sg.Text('Volume: 0', key='volume', background_color='black', text_color='white')]
]

GO_BACK_IMAGE_PATH = './Images/back.png'
GO_FORWARD_IMAGE_PATH = './Images/next.png'
PLAY_SONG_IMAGE_PATH = './Images/play_button.png'
PAUSE_SONG_IMAGE_PATH = './Images/pause.png'
ALBUM_COVER_IMAGE_PATH = './Images/pylot.png'
IMAGE_ALBUM = './Images/pylot.png'
AUTO_FALANTE_COM = './Images/altofalantecom.png'
AUTO_FALANTE_SEM = './Images/altofalantesem.png'


main = [
    [
        sg.Canvas(background_color='black', size=(40, 350), pad=None),
        sg.Image(filename=IMAGE_ALBUM, key='image_album', 
                 size=(350, 350), pad=None),
        sg.Canvas(background_color='black', size=(40, 350), pad=None)
    ],
    [sg.Canvas(background_color='black', size=(480, 10), pad=None)],
    [sg.Column(song_title_column, background_color='black',
               justification='c', element_justification='c')],
    [sg.Text('_'*62, background_color='black', text_color='white', key='length')],

    [
        sg.Column(timer_volume, background_color='black',
               justification='c', element_justification='c')
    ],
    [
        sg.Canvas(background_color='black', size=(35, 200), pad=(0, 0)),
        sg.Image(pad=(10, 0), filename=AUTO_FALANTE_SEM, enable_events=True,
                 size=(40, 40), key='diminuir', background_color='black'),
        sg.Image(pad=(10, 0), filename=GO_BACK_IMAGE_PATH, enable_events=True,
                 size=(35, 44), key='previous', background_color='black'),
        sg.Image(filename=PLAY_SONG_IMAGE_PATH,
                 size=(64, 64), pad=(10, 0), enable_events=True, key='play', background_color='black'),
        sg.Image(filename=PAUSE_SONG_IMAGE_PATH,
                 size=(58, 58), pad=(10, 0), enable_events=True, key='pause', background_color='black'),
        sg.Image(filename=GO_FORWARD_IMAGE_PATH, enable_events=True,
                 size=(35, 44), pad=(10, 0), key='next', background_color='black'),
        sg.Image(pad=(10, 0), filename=AUTO_FALANTE_COM, enable_events=True,
                 size=(40, 40), key='aumentar', background_color='black'),
        sg.Canvas(background_color='black', size=(18, 200), pad=(0, 0)),
    ],
    [sg.Column(layout=currently_playing, justification='c',
               element_justification='c', background_color='black', pad=None)]


]
window = sg.Window('mpy3', layout=main, size=(
    480, 730), background_color='black', finalize=True, grab_anywhere=True, resizable=False,)


directory = sg.popup_get_folder('Select Music Directory')

songs_in_directory = get_files_inside_directory_not_recursive(directory)
song_count = len(songs_in_directory)
current_song_index = 0

for musica in songs_in_directory:
    print(musica.split('/')[-1])

window['play'].Widget.config(cursor="hand2")
window['pause'].Widget.config(cursor="hand2")
window['next'].Widget.config(cursor="hand2")
window['previous'].Widget.config(cursor="hand2")
window['aumentar'].Widget.config(cursor="hand2")
window['diminuir'].Widget.config(cursor="hand2")

def atualizar_length(duracao, percorrido):
    tamanho_dividido = duracao/62
    percorrido = percorrido/1000
    partes = percorrido/tamanho_dividido
    partes = '_'*int(partes)
    window['length'].update(partes)

def atualizar_tempo():
    tempo_atual = posicao()
    tamanho = misc.file_duration(songs_in_directory[current_song_index])
    atualizar_length(tamanho, tempo_atual)
    minutos = int((tempo_atual/60000)%60)
    segundos = int((tempo_atual/1000)%60)
    minutos_totais = int((tamanho/60))
    segundos_totais = int((tamanho%60))
    string_tempo = "%02d:%02d/%02d:%02d" % (minutos, segundos,minutos_totais,segundos_totais)
    window['tempo'].update(string_tempo)
    return

def update_cover():
    mp3_file_content_to_recognize = open(songs_in_directory[current_song_index], 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    json_obj = json.loads(json.dumps((next(recognize_generator))))
    del json_obj[0]
    json_obj = json_obj[0]
    try:
        show_lyrics(json_obj)
    except:
        os.system('clear')
        print('No lyric found')
    json_music_name = json_obj['track']['title']
    json_music_artist = json_obj['track']['subtitle']
    window['song_name'].update(f'{json_music_name} - {json_music_artist}')
    window['currently_playing'].update(
        f'Playing: {json_music_name} - {json_music_artist}')
    cover_image = json_obj['track']['images']['coverart']
    urllib.request.urlretrieve(cover_image, "sample.jpg")
    im = Image.open("sample.jpg")
    rgb_im = im.convert('RGB')
    rgb_im = rgb_im.resize((350,350))
    rgb_im.save('sample.png')
    IMAGE_ALBUM = './sample.png'
    window['image_album'].update(IMAGE_ALBUM)
    return

def update_volume():
    volume_str = volume()
    volume_str = 'Volume: %s' % volume_str
    window['volume'].update(volume_str)

def show_lyrics(json_obj):
    keys = json_obj['track']['sections'][1]['text']
    keys = str(keys)
    versos = keys.split(',')
    os.system('clear')
    for verso in versos:
        if str(verso).find('[') != -1:
            verso = str(verso).replace('[', '')
        if str(verso).find(']') != -1:
            verso = str(verso).replace(']', '')
        print(verso)

while True:
    if is_sound_playing():
        atualizar_tempo()
        event, values = window.read(timeout=100)
    elif is_sound_playing() == False and tocando and event == '__TIMEOUT__':
        if current_song_index < song_count-1:
            stop_sounds()
            current_song_index += 1
            play_sound(songs_in_directory[current_song_index])
            x = threading.Thread(target=update_cover, args=())
            x.run()
        else:
            print('Reached last song')
        event, values = window.read(timeout=1)   
    else:
        event, values = window.read()
    if event == sg.WIN_CLOSED:
        directories = []
        for (root, dirs, files) in os.walk(directory):
            for file in files:
                if str(file).find('.ogg') != -1:
                    os.remove(root +'/'+ file)
        break
    elif event == 'play':
        atualizar_tempo()
        if is_sound_playing() == False and tocando:
            unpause()
        elif is_sound_playing() == False:
            update_volume()
            tocando = True
            play_sound(songs_in_directory[current_song_index])
            x = threading.Thread(target=update_cover, args=())
            x.start()
        else:
            pass
    
    elif event == 'pause':
        if is_sound_playing():
            pause_sounds()
        else:
            unpause()
        continue

    elif event == 'diminuir':
        diminuir()
        update_volume()
    
    elif event == 'aumentar':
        aumentar()
        update_volume()

    elif event == 'next':
        atualizar_tempo()
        if current_song_index + 1 < song_count:
            stop_sounds()
            current_song_index += 1
            play_sound(songs_in_directory[current_song_index])
            x = threading.Thread(target=update_cover, args=())
            x.start()
        else:
            print('Reached last song')
        continue

    elif event == 'previous':
        atualizar_tempo()
        if current_song_index + 1 <= song_count and current_song_index > 0:
            stop_sounds()
            current_song_index -= 1
            play_sound(songs_in_directory[current_song_index])
            x = threading.Thread(target=update_cover, args=())
            x.start()
        else:
            print('Reached first song')
    else:
        atualizar_tempo()