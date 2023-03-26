from pytube import YouTube
import os


#Absolute to /downloads
ABS = os.path.abspath(os.path.join(os.getcwd(), 'summ3ry'))
ABS = os.path.join(ABS, 'downloads')


def video_download(link: str, uniq_dir: str):
    ''' Downloads audio from provided yt url
        link: link to a YT video
        uniq_dir: name of audio file created in /downloads
    '''
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path=ABS, filename=f'{uniq_dir}')