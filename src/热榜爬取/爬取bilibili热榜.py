import requests
import pandas
from bs4 import BeautifulSoup

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'cookie':'i-wanna-go-back=-1; buvid4=74D2D138-8FC2-FB57-E036-4E473138603821057-022091817-SV44yNkYjlEb9jZTdZnPlfxy1NoUyiny9wlNK2suQqUsNFMgIDo8gw%3D%3D; buvid_fp_plain=undefined; rpdid=|(umJmYJ)Y)l0J\'uYY)lmR)lY; b_ut=5; LIVE_BUVID=AUTO9316722293666676; CURRENT_PID=76192610-cba7-11ed-9cad-a52f1821f539; CURRENT_BLACKGAP=0; hit-new-style-dyn=1; is-2022-channel=1; FEED_LIVE_VERSION=V_SEO_FIRST_CARD; buvid3=1012DC9B-C26B-A98D-D62A-AD82E974B3D582095infoc; b_nut=1695046282; _uuid=1BE985E10-1013A-6859-34BF-65101ECC5999482020infoc; enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=1883743734; DedeUserID__ckMd5=68822b3f41e5a1bb; fingerprint=dae095ef2b1d07c47e17a079515ca2d1; CURRENT_FNVAL=4048; CURRENT_QUALITY=80; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE4NDAxOTcsImlhdCI6MTcwMTU4MDkzNywicGx0IjotMX0.l6BR-32zRzAmdCJMaFYolMZYlLIgagj97jyXdWIwdns; bili_ticket_expires=1701840137; buvid_fp=dae095ef2b1d07c47e17a079515ca2d1; SESSDATA=976a334e%2C1717132998%2C7b53a%2Ac1CjDef4G7TNNV2HHDTx7EbRAmCpeIkMdfVjJxdLr3DgpmAPjw5EmIi8GgQb6GyDPsGRsSVjJzWkJEelhvZlBPeWxPTXlzUi0ySUpFT3h4aUFQVldUOV9aQ1l2WWZjZDREZm9uRlh5OVFLV185TE5TSE5QU21TV292Wk56Qno4YjFGRGhldFB4T2NBIIEC; bili_jct=f768f9197ac8a0d97344de94412b0470; b_lsid=107CB6E92_18C2F0C6B77; bsource=search_bing; home_feed_column=4; browser_resolution=1396-649; bp_video_offset_1883743734=870747582116134920; sid=7vv1tdjc; innersign=0; PVID=6',
}


titlels,bvidls,authorls,pubdatels,viewls,coinls,likels,dislikels,rankls=[],[],[],[],[],[],[],[],[]


url= 'https://api.bilibili.com/x/web-interface/popular?'

def spider(pn):
    params = {
        'ps': '20',
        'pn': pn,
    }
    i = 0
    resp = requests.get(url, headers = headers, params = params).json()
    for data in resp['data']['list']:
        titlels.append(data['title'])
        bvidls.append(data['bvid'])
        authorls.append(data['owner']['name'])
        pubdatels.append(data['pubdate'])
        viewls.append(data['stat']['view'])
        coinls.append(data['stat']['coin'])
        likels.append(data['stat']['like'])
        dislikels.append(data['stat']['dislike'])
        i = i + 1
        rankls.append(i+(pn-1)*20)

for pn in range(1,6):
    spider(pn)

data = {
    '排名':rankls,
    '标题': titlels,
    'bv号':bvidls ,
    '作者': authorls,
    '日期':pubdatels,
    '观看数':viewls,
    '硬币数':coinls,
    '点赞数':likels,
    '点踩数':dislikels,
}
dataframe = pandas.DataFrame(data=data)
dataframe.to_csv('bilibili热榜.csv', index=False, encoding='utf_8_sig')