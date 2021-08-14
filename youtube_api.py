import time
import requests
# import json
import confing


def get_chat_id(yt_url):
    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
    print('video_id : ', video_id)

    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': confing.YOTUBER_API_KEY, 'id': video_id, 'part': 'liveStreamingDetails'}
    data = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id






def get_chat_message(key, chat_id, pageToken=None, part='id,snippet,authorDetails'):
    # inputの方がサガサイでやりやすそう

    url = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {
        'key': key,
        'liveChatId': chat_id,
        'part': 'id,snippet,authorDetails',
    }

    if type(pageToken) == str:
        params['pageToken'] = pageToken

    return requests.get(url, params=params).json()



def format_row_yotube_data(data):
    comments = []

    try:
        for item in data['items']:
            channelId = item['snippet']['authorChannelId']
            msg       = item['snippet']['displayMessage']
            usr       = item['authorDetails']['displayName']

            # 要求されたもの
            comment = {
             "author_channel_id": channelId,
             "author_name": usr,
             "display_message": msg,
            }
            comments.append(comment)

    except:
        pass
    res = {
        "next_page_token": data['nextPageToken'],
        "comments": comments
    }

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
    chat_id = get_chat_id(confing.YOTUBER_URL)
    data = get_chat_message(confing.YOTUBER_API_KEY, chat_id)
    format_data = format_row_yotube_data(data)
    print(format_data)
    

    

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
