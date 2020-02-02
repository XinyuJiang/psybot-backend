import requests

from psybot.config import APPID, SECRET


class OpenidUtils(object):

    def __init__(self, code):
        self.url = "https://api.weixin.qq.com/sns/jscode2session"
        self.appid = APPID
        self.secret = SECRET
        self.code = code    # 前端传回的动态jscode

    def get_openid(self):
        # url一定要拼接，不可用传参方式
        url = self.url + "?appid=" + self.appid + "&secret=" + self.secret + "&js_code=" + self.code + "&grant_type=authorization_code"
        r = requests.get(url)
        print(r.json())
        openid = r.json()['openid']
        session_key = r.json()['session_key']

        return openid,session_key
