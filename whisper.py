from requests import request
from pytube import YouTube
from pydub import AudioSegment
import os

def download(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='./resources')
    base, ext = os.path.splitext(out_file)
    new_file = 'test' + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def cuttin():
    audio = AudioSegment.from_mp3('test.mp3')
    parts = [audio[i:i+30 * 1000] for i in range(0, len(audio), 30*1000)]
    print(parts)
    for i, part in enumerate(parts):
        part.export(f'part_{i}.mp3', format='mp3')
        
def transcribe(file):
    url = "https://whisper.lablab.ai/asr"
    payload={}
    files=[
    ('audio_file',('test.m4a', open(f'{file}','rb'),'audio/mpeg'))
    ]
    response = request("POST", url, data=payload, files=files)
    return response

if __name__ == '__main__':
    # file = download('https://www.youtube.com/watch?v=FCP_KbpA3jI')
    cuttin()
    # res = transcribe('test.m4a')
    # print(res.text)
    # print(res.text[0]['text'])