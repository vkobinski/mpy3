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


def pause_sounds():
    mixer.music.pause()


def unpause():
    mixer.music.unpause()

def posicao():
    return mixer.music.get_pos()


def is_sound_playing():
    if mixer.music.get_busy() == True:
        return True
    return False



