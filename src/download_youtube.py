from __future__ import unicode_literals
import youtube_dl

download_dir = "/tmp/"
audio_format = "wav"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': download_dir + "%(title)s.mp4",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
# for high quality audio in exchange for audio stutters
#       'preferredcodec': 'flac',
        'preferredcodec': audio_format,
        'preferredquality': '192',
    }],
}

def download_song(url):

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    info_dict = ydl.extract_info(url)
    return info_dict

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download(['https://www.youtube.com/watch?v=DVHMC2B1WTo'])
