from requests import request
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip
import re

import whisper
# print(f'Loading whisper model "{model}"')

#Absolute to /resources
ABS = os.path.abspath('downloads')
# model = whisper.load_model('medium.en')


def video_download(link, uniq_dir):
    os.mkdir(f'{ABS}/{uniq_dir}')
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path=f'{ABS}/{uniq_dir}', filename='audio.mp3')


def divide_into_parts(uniq_dir):
    try:
        audio = AudioFileClip(f'{ABS}/{uniq_dir}/audio.mp3')
        parts = [audio.subclip(i, i+30) for i in range(0, int(audio.duration), 30)]
        for i, fragment in enumerate(parts):
            fragment.write_audiofile(f'{ABS}/{uniq_dir}/part_{i}.mp3')
    except:
        pass
    os.remove(f'{ABS}/{uniq_dir}/audio.mp3')


def transcribe_all(uniq_dir, model = 'base'):
    #creating expresion for better speed
    p = re.compile(r'\d+')
    whole_transcript = []
    parts = os.listdir(f'{ABS}/{uniq_dir}/')
    #sorting parts list
    parts = sorted(parts, key=lambda s: int(p.search(s).group()))
    for file in parts:
        text = transcribe(file, uniq_dir, model=model)
        whole_transcript.append(text)
        os.remove(f'{ABS}/{uniq_dir}/{file}')
    os.rmdir(f'{ABS}/{uniq_dir}')
    whole_transcript = " ".join(whole_transcript)
    return whole_transcript
    

def transcribe(file, key, LOCAL_MODEL=True, model="base"):
    # for internal model
    if LOCAL_MODEL:
        model = whisper.load_model(model)
        transcript = model.transcribe(f'{ABS}/{key}/{file}')
        return transcript['text']
    # for external model
    else:
        url = "https://whisper.lablab.ai/asr"
        payload={}
        files=[
        ('audio_file',(file ,open(f'{ABS}/{key}/{file}','rb'),'audio/mpeg'))
        ]
        response = request("POST", url, data=payload, files=files)
        transcript = eval(response.text)['text']
        return transcript

# if __name__ == '__main__':
#     file = video_download('https://www.youtube.com/watch?v=n3b9QKo_VpM', 'key')
#     divide_into_parts('key')
#     all = transcribe_all('key')
#     print(all)