import requests
import datetime

import confing


class YoutubeLiveChat():
    def __init__(self, youtuber_url, youtuber_api_key, interval=10) -> None:
        """
            Unit of interval: second
        """
        self.youtuber_api_key = youtuber_api_key
        self.chat_id = self.get_chat_id(youtuber_url)
        if not self.chat_id:

            class NoneError(Exception):
                def __str__(self) -> str:
                    return "This value can NOT be None!"

            raise NoneError
        self.interval = interval
        self.previous_token_time = datetime.datetime.now() - datetime.timedelta(seconds=self.interval + 1)  # yapf: disable
        self.page_token = self.get_chat_message_next_page_token()

    def get_chat_id(self, yt_url: str):
        '''
        from qiita @iroiro_bot
        https://qiita.com/iroiro_bot/items/ad0f3901a2336fe48e8f

        https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
        '''
        video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
        print('video_id : ', video_id)

        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': self.youtuber_api_key,
            'id': video_id,
            'part': 'liveStreamingDetails'
        }
        data = requests.get(url, params=params).json()

        try:
            liveStreamingDetails = data['items'][0]['liveStreamingDetails']
        except BaseException:
            print('NO live')
            return None

        if 'activeLiveChatId' in liveStreamingDetails.keys():
            chat_id = liveStreamingDetails['activeLiveChatId']
            print('get_chat_id done!')
        else:
            chat_id = None
            print('NOT live')

        return chat_id

    def get_chat_message_row_data(self, page_token=None, part='id,snippet,authorDetails'):
        # inputの方がサガサイでやりやすそう
        interval = datetime.datetime.now() - self.previous_token_time
        if interval.seconds < self.interval:
            return None

        url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
        params = {
            'key': self.youtuber_api_key,
            'liveChatId': self.chat_id,
            'part': 'id,snippet,authorDetails',
        }

        if page_token:
            params['pageToken'] = page_token

        self.previous_token_time = datetime.datetime.now()
        res = requests.get(url, params=params).json()

        if "error" in res:
            return None

        return res

    def get_chat_message_next_page_token(self):
        chat_message_row_data = self.get_chat_message_row_data()

        if not chat_message_row_data:
            return None

        return chat_message_row_data["nextPageToken"]

    def format_chat_message_row_data(self, data):
        if not data:
            return None

        comments = []

        try:
            for item in data['items']:
                channelId = item['snippet']['authorChannelId']
                msg = item['snippet']['displayMessage']
                published_at = item['snippet']["publishedAt"]
                usr = item['authorDetails']['displayName']

                # 要求されたもの
                comment = {
                    "author_channel_id": channelId,
                    "author_name": usr,
                    "display_message": msg,
                    "published_at": published_at
                }
                comments.append(comment)

        except BaseException:
            return None

        res = {"next_page_token": data['nextPageToken'], "comments": comments}

        return res

    # yapf: disable
    def get_formatted_chat_message_data(self, page_token=None, part='id,snippet,authorDetails'):
        chat_message_row_data = self.get_chat_message_row_data(page_token=page_token, part=part)
        formatted_chat_message_data = self.format_chat_message_row_data(chat_message_row_data)
        return formatted_chat_message_data
    # yapf: enable

    def get_next_chat_message(self, part='id,snippet,authorDetails'):

        if not self.page_token:
            self.page_token = self.get_chat_message_next_page_token()

        next_chat_message = self.get_formatted_chat_message_data(page_token=self.page_token, part=part)  # yapf: disable
        if not next_chat_message:
            return

        self.page_token = next_chat_message["next_page_token"]
        return next_chat_message


if __name__ == '__main__':
    # yt_url = input('Input YouTube URL > ')
    # chat_id = get_chat_id(yt_url)
    # chat_id = get_chat_id(confing.YOTUBER_URL)

    # url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    # params = {
    #     'key': confing.YOTUBER_API_KEY,
    #     'liveChatId': chat_id,
    #     'part': 'id,snippet,authorDetails'
    # }
    # pageToken = None

    # if type(pageToken) == str:
    #     params['pageToken'] = pageToken

    # data = requests.get(url, params=params).json()
    # print(data)
    import time

    print("\n\n\n\n\n")
    youtube_live_chat = YoutubeLiveChat(confing.YOTUBER_URL, confing.YOTUBER_API_KEY)
    # print(youtube_live_chat.get_chat_id(confing.YOTUBER_URL))
    print(youtube_live_chat.get_next_chat_message())
    time.sleep(5)
    print(youtube_live_chat.get_next_chat_message())
    time.sleep(6)
    print(youtube_live_chat.get_next_chat_message())
    """
    chat_id = get_chat_id(confing.YOTUBER_URL)
    data = get_chat_message(confing.YOTUBER_API_KEY, chat_id)
    format_data = format_row_yotube_data(data)
    print(format_data)
    """
    # data = [
    #     {
    #         "author_channel_id": "5555",
    #         "author_name": "sei",
    #         "display_message": "楽しい！！！！！"
    #     },
    #     {
    #         "author_channel_id": "5555",
    #         "author_name": "sei",
    #         "display_message": "楽しい！！！！！"
    #     },
    #     {
    #         "author_channel_id": "5555",
    #         "author_name": "sei",
    #         "display_message": "楽しい！！！！！"
    #     }
    # ]
