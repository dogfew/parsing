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
    with open('data.json') as f:
        dictionary = json.load(f)
    date = datetime.now()
    name = '{}-{:0>2}-{:0>2}_{:0>2}:{:0>2}'.format(date.year, date.month, date.day, date.hour, date.minute)
    dictionary[name] = dict()
    with open('channels.csv', 'r') as f:
        users = [user for user in f.read().split(';')]
        print('Users:', *users)
    for user in users:
        try:
            print(f'Getting information for {user}', end='...\n')
            dictionary[name][user] = create_portfolio(user)
            print(f'        Got information for {user}!')
        except Exception as e:
            dictionary[user] = None
            print(f"        Couldn't get information for {user}:\n      {e}", end='\n')
        # comments
        try:
            print(f"    Trying to get comments... for {user}")
            for video in dictionary[name][user]:
                video_id = dictionary[name][user][video]['id']
                dictionary[name][user][video]['comments'] = get_comments(video_id)
            print(f"        We've got comments for {user}")
        except Exception as e:
            print(f"        Couldn't get comments for {user}:\n     {e}")
    json.dump(dictionary, open('data.json', "w+"))

