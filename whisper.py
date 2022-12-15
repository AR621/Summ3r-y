from requests import request
from pytube import YouTube
import os
from moviepy.editor import AudioFileClip
import re

#Absolute to /resources
ABS = os.path.abspath('resources')

def video_download(link, key):
    os.mkdir(f'{ABS}/{key}')
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=f'{ABS}/{key}', filename='audio.mp3')

def divide_into_parts(key):
    try:
        audio = AudioFileClip(f'{ABS}/{key}/audio.mp3')
        parts = [audio.subclip(i, i+30) for i in range(0, int(audio.duration), 30)]
        for i, fragment in enumerate(parts):
            fragment.write_audiofile(f'{ABS}/{key}/part_{i}.mp3')
    except:
        pass
    os.remove(f'{ABS}/{key}/audio.mp3')

def transcribe_all(key):
    #creating expresion for better speed
    p = re.compile(r'\d+')
    whole_transcript = []
    parts = os.listdir(f'{ABS}/{key}/')
    #sorting parts list
    parts = sorted(parts, key=lambda s: int(p.search(s).group()))
    for file in parts:
        text = transcribe(file, key)
        whole_transcript.append(text)
        os.remove(f'{ABS}/{key}/{file}')
    os.rmdir(f'{ABS}/{key}')
    return whole_transcript
    

def transcribe(file, key):
    url = "https://whisper.lablab.ai/asr"
    payload={}
    files=[
    ('audio_file',(file ,open(f'{ABS}/{key}/{file}','rb'),'audio/mpeg'))
    ]
    response = request("POST", url, data=payload, files=files)
    transcript = eval(response.text)['text']
    return transcript

if __name__ == '__main__':
    file = video_download('https://www.youtube.com/watch?v=5Dq1oQkwhUw', 'key')
    divide_into_parts('key')
    all = transcribe_all('key')
    print(all)
