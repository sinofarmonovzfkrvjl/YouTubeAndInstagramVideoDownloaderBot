import yt_dlp
import instaloader
import os
import glob

def YouTubeDownloader(url, output_path='.'):
    ydl_opts = {
        'outtmpl': f'{output_path}/video.mp4',
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
        #     'preferredcodec': 'mp3',  # Convert audio to mp3
        #     'preferredquality': '192',  # Set the preferred quality (bitrate)
        # }],
        'format': 'best'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=True)
    video_title = info_dict.get('title')
    video_id = info_dict.get('id')
    video_url = info_dict.get('webpage_url')
    uploader = info_dict.get('uploader')
    upload_date = info_dict.get('upload_date')
    duration = info_dict.get('duration')
    view_count = info_dict.get('view_count')
    like_count = info_dict.get('like_count')
    description = info_dict.get('description')
    tags = info_dict.get('tags')
    return {"title": video_title, "id": video_id, "url": video_url, "uploader": uploader, "upload_date": upload_date, "duration": duration, "view_count": view_count, "like_count": like_count, "description": description, "tags": tags}

def InstagramDownloader(url):
    L = instaloader.Instaloader()
    post_url = url
    shortcode = post_url.split('/')[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=post.owner_username)
    pattern = os.path.join(post.owner_username, '*.txt')
    video = os.path.join(post.owner_username, '*mp4')
    txt_file = glob.glob(pattern)
    video_file = glob.glob(video)
    return [txt_file[0], video_file, post.owner_username]