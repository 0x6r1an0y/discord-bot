
import json
import yt_dlp
URL = "https://www.youtube.com/playlist?list=PL5CCDFBBE2143D7CB"
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=True)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    print(json.dumps(ydl.sanitize_info(info)))