import os
from pygame import mixer
import misc
mixer.init()

def get_files_inside_directory_not_recursive(directory):
    directories = []
    for (root, dirs, files) in os.walk(directory):
        for file in files:
            if str(file).find('.wav') != -1:
                directories.append(root + os.sep + file)
            elif str(file).find('.mp3') != -1:
                file = misc.converter_musica(root + '/' + file)
                directories.append(file)

    return directories


def play_sound(sound_path):
    mixer.music.load(sound_path)
    mixer.music.play()


def stop_sounds():
    mixer.music.stop()

def aumentar():
    if mixer.music.get_volume() + 0.1> 1:
        mixer.music.set_volume(1)
    if mixer.music.get_volume() + 0.1<= 1:
        mixer.music.set_volume(mixer.music.get_volume()+0.1)

def diminuir():
    if mixer.music.get_volume() - 0.1 < 0:
        mixer.music.set_volume(0)
    if mixer.music.get_volume() -0.1 >= 0:
        mixer.music.set_volume(mixer.music.get_volume()-0.1)

def volume():
    return '{}'.format(int(float(mixer.music.get_volume())*10))

def pause_sounds():
    mixer.music.pause()

def unpause_sounds():
    mixer.music.unpause()


def unpause():
    mixer.music.unpause()

def posicao():
    return mixer.music.get_pos()


def is_sound_playing():
    if mixer.music.get_busy() == True:
        return True
    return False



