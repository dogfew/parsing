import json
from youtube_dl import YoutubeDL
from datetime import datetime
from comments import get_comments
youtube_dl_opts = {
    'ignorerrors': True,
    'quiet': True
}


def get_videos_from_channel(channel_id: str) -> list:
    with YoutubeDL(youtube_dl_opts) as ydl:
        try:
            videos = ydl.extract_info(f'https://www.youtube.com/channel/{channel_id}/videos', download=False)
        except Exception:
            try:
                videos = ydl.extract_info(f'https://www.youtube.com/c/{channel_id}/videos', download=False)
            except Exception:
                return []
    return [f"https://www.youtube.com/watch?v={i['id']}" for i in videos['entries']]


def get_info_from_video(video: str) -> dict:
    with YoutubeDL(youtube_dl_opts) as ydl:
        info_dict = ydl.extract_info(video, download=False)
        video_title = info_dict.get('title', None)
        video_id = info_dict.get('id', None)
        video_views = info_dict.get('view_count', None)
        video_likes = info_dict.get('like_count', None)
        video_description = info_dict.get('description', None)
    return {'title': video_title, 'views': video_views,
            'likes': video_likes, 'id': video_id,
            'description': video_description}


def create_portfolio(user_id: str) -> dict:
    return {video: get_info_from_video(video) for video in get_videos_from_channel(user_id)}


if __name__ == '__main__':
    dictionary = dict()
    # users = []
    with open('channels.csv', 'r') as f:
        users = [user for user in f.read().split(';')]
        print('Users:', users)
    for user in users:
        try:
            dictionary[user] = create_portfolio(user)
        except Exception:
            dictionary[user] = None
    date = datetime.now()
    file_name = 'data_{}-{}-{}_{}:{}.json'.format(date.year, date.month, date.day, date.hour, date.minute)
    json.dump(dictionary, open(file_name, "w+"))
    # add comments
    # with open(file_name) as f:
    #     data = json.load(f)
    # for channel in data:
    #     for video in data[channel]:
    #         video_id = data[channel][video]['id']
    #         try: data[channel][video]['comments'] = get_comments(video_id)
    #         except Exception: pass
    # with open(f"{file_name}_comments", 'w+') as f:
    #     json.dump(data, f)

