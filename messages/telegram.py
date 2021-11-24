import requests

token = ""


def telegram(id, msg):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': id,
               'text': msg,
               }
    requests.post(url, params=payload)


telegram('11111', '봇 방')
telegram('@xxxx_ch', '채널 방')

'''
https://tech.lonpeach.com/2021/02/13/python-telegram-restock-bot/
1. 봇을 만들고 토큰이 포함된 주소를 봇 방에 타이핑하고 클릭
https://api.telegram.org/bot토큰/getUpdates
웹에 보이는 json의 id 값이 봇방의 chat_id이다.

2. 여럿이 사용할려면 채널을 만들고 채널안에 봇을 추가
chat_id는 @채널방명 을 사용한다.
'''
