import os
import pytest

from summ3ry import downloader, transcriber, summarizer

TEST_DIR = os.path.join(downloader.ABS, 'test')
TEST_FILE = os.path.join(TEST_DIR, 'audio.mp3')
ABS = os.path.join(os.getcwd(), 'tests')
MP3_FILE = os.path.join(ABS, 'sample.mp3')
TXT_FILE = os.path.join(ABS, 'sample.txt')


@pytest.fixture(scope="function")
def clean_up_directory(request):
    def remove_directory():
        os.remove(TEST_FILE)
        os.rmdir(TEST_DIR)
    request.addfinalizer(remove_directory) 

        
def test_downloader(clean_up_directory):
    downloader.video_download('https://www.youtube.com/watch?v=B_fXSJ97H0E', 'test')
    assert os.path.exists(TEST_FILE)
    
    
def test_transcriber():
    transcript = transcriber.transcribe_audio(MP3_FILE)
    assert transcript


def test_summarizer():
    summary = summarizer.request_summary(TXT_FILE)
    assert summary