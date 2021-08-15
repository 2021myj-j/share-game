import requests
import datetime
import time

import confing


class YoutubeLiveChat():
    def __init__(self, youtuber_url, youtuber_api_key, interval=10) -> None:
        """
            Unit of interval: second
        """
        self.youtuber_api_key = youtuber_api_key
        self.chat_id = self._get_chat_id(youtuber_url)
        self.page_token = None
        self.interval = interval
        self.previous_token_time = datetime.datetime.now() - datetime.timedelta(
            seconds=self.interval + 1
        )

    def _get_chat_id(self, yt_url):
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

    def get_chat_message_row_data(self, pageToken=None, part='id,snippet,authorDetails'):
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

        if type(pageToken) == str:
            params['pageToken'] = pageToken

        self.previous_token_time = datetime.datetime.now()
        return requests.get(url, params=params).json()

    def format_row_yotube_data(self, data):
        if not data:
            return None

        comments = []

        try:
            for item in data['items']:
                channelId = item['snippet']['authorChannelId']
                msg = item['snippet']['displayMessage']
                usr = item['authorDetails']['displayName']

                # 要求されたもの
                comment = {
                    "author_channel_id": channelId,
                    "author_name": usr,
                    "display_message": msg,
                }
                comments.append(comment)

        except BaseException:
            return None

        res = {"next_page_token": data['nextPageToken'], "comments": comments}

        return res

    def get_next_chat_message(self, nextPageToken=None, part='id,snippet,authorDetails'):
        if not self.page_token:
            self.page_token = nextPageToken
        row_data = self.get_chat_message_row_data(pageToken=self.page_token, part=part)

        res = self.format_row_yotube_data(row_data)

        if res:
            self.page_token = res["next_page_token"]

        return res


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
    print("\n\n\n\n\n")
    youtube_live_chat = YoutubeLiveChat(confing.YOTUBER_URL, confing.YOTUBER_API_KEY)
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
