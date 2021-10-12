import librosa
import pydub

def file_duration(fname):
    return librosa.get_duration(filename=fname)

def converter_musica(musica):
    musica = pydub.AudioSegment.from_mp3(musica).export(musica.replace('.mp3','.wav'), format='wav').name
    return musica