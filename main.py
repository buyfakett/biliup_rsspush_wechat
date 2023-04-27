#coding=utf-8
import random, datetime, time, os, sys, json, requests, feedparser


# 检测的主播
uid = "11073"

# 检测的时间(分钟）
detection_time = 1

# 模板id
template_id = "fE51ho"

# rsshub服务的ip
ip = ""

# appId
app_id = "wxd4072"
# appSecret
app_secret = "64ff49a3631c"

# 发送的用户的id
to_user_ids = ["oSZLh7E"]

# 公众号的跳转链接
jump_url = "https://space.bilibili.com/" + uid + "/dynamic"

bili_url = "http://" + ip + ":1200/bilibili/user/dynamic/" + uid


def write():
    f = open("database.txt", "w", encoding="utf-8")
    f.write(feedparser.parse(bili_url)['entries'][0]['title'])
    f.close()


def get_rss():
    d = feedparser.parse(bili_url)
    post_data_detail = d['entries'][0]['summary']
    post_data_title = d['entries'][0]['title']
    post_data = {
        "title": post_data_title,
        "detail": post_data_detail
    }
    return json.dumps(post_data, ensure_ascii=False)

def get_access_token(app_id, app_secret):
    # appId
    app_id = app_id
    # appSecret
    app_secret = app_secret
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = requests.get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token

def get_color():
    # 往list中填喜欢的颜色即可
    color_list = ['#6495ED', '#3CB371', "#3B99D4", "#8ED14B", "#F06B49", "#ECC2F1", "#82C7C3", "#E3698A", "#1776EB", "#F5B2AC", "#533085", "#89363A", "#19413E", "#D92B45", "#60C9FF", "#1B9F2E", "#BA217D", "#076B82"]
    return random.choice(color_list)


def send_message(to_user, now_time, title, detail, url, wx_post_url):
    data = {
        "touser": to_user,
        "template_id": template_id,
        "url": url,
        "topcolor": "#FF0000",
        "data": {
            "title_title": {
                "value": "通知内容：  ",
                "color": "#a9a9a9"
            },
            "title": {
                "value": title,
                "color": get_color()
            },
            "now_time_title": {
                "value": "\n通知时间：  ",
                "color": "#a9a9a9"
            },
            "now_time": {
                "value": now_time,
                "color": get_color()
            },
            "detail_title": {
                "value": "\n通知内容：  ",
                "color": "#a9a9a9"
            },
            "detail": {
                "value": detail,
                "color": get_color()
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = requests.post(wx_post_url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


def main():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ACCESS_TOKEN = get_access_token(app_id, app_secret)
    wx_post_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + ACCESS_TOKEN
    rss_data = json.loads(get_rss())

    f = open("database.txt", "r", encoding="utf-8")
    data = f.read()
    f.close()
    if feedparser.parse(bili_url)['entries'][0]['title'] == data:
        print(now_time + "主播没有发新动态")
    else:
        write()
        for i in to_user_ids:
            send_message(i, now_time, rss_data['title'], rss_data['detail'], jump_url, wx_post_url)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(detection_time * 60)