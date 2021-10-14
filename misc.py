import librosa
import pydub

def file_duration(fname):
    return librosa.get_duration(filename=fname)

def converter_musica(musica, diretorios, threads):
    musica = pydub.AudioSegment.from_mp3(musica).export(musica.replace('.mp3','.ogg'), format='ogg').name
    achou = False
    for i in range(len(diretorios)):
        if str(diretorios[i]) == str(musica):
            achou = True
    if achou == False:
        diretorios.append(musica)
    threads.pop()