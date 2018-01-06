from __future__ import unicode_literals
import youtube_dl

DOWNLOAD_DIR = "/tmp/"
AUDIO_FORMAT = "wav"

ydl_pretend_opts = { 'simulate': True }

ydl_download_opts = {
    'format': 'bestaudio/best',
    'outtmpl': DOWNLOAD_DIR + "%(title)s.mp4",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
# for high quality audio in exchange for audio stutters
#       'preferredcodec': 'flac',
        'preferredcodec': AUDIO_FORMAT,
        'preferredquality': '192',
    }],
}

def get_song_info(url : str):
    ''' '''
    info_dict = None
    if (url is not None):
        ydl = youtube_dl.YoutubeDL(ydl_pretend_opts)
        info_dict = ydl.extract_info(url)
    return info_dict

def download_song(url : str):
    ''' '''
    info_dict = None
    if (url is not None):
        ydl = youtube_dl.YoutubeDL(ydl_download_opts)
        info_dict = ydl.extract_info(url)
    return info_dict


def get_download_dir():
    return DOWNLOAD_DIR

def get_audio_format():
    return AUDIO_FORMAT

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download(['https://www.youtube.com/watch?v=DVHMC2B1WTo'])

