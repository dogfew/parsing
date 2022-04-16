def get_comments(video_id: str) -> list:
	from googleapiclient.discovery import build
	api_key = 'AIzaSyCieUf1tBKe7gmSiGignYT7PC4MJPGP6gE' # API KEY
	youtube = build('youtube', 'v3',
					developerKey=api_key)
	video_response = youtube.commentThreads().list(
		part='snippet,replies',
		videoId=video_id
	).execute()
	comments = []
	while video_response:
		for item in video_response['items']:
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			comments.append(comment)

		if 'nextPageToken' in video_response:
			video_response = youtube.commentThreads().list(
				part='snippet,replies',
				videoId=video_id
			).execute()
		else:
			break
	return comments



