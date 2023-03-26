import whisper


model = whisper.load_model('base')

def transcribe_audio(path_to_audio_file: str):
    ''' Transcribes given audio file '''
    transcript = model.transcribe(path_to_audio_file)
    return transcript['text']