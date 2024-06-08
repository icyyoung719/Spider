import requests
import pandas
from bs4 import BeautifulSoup

headers = {
    'cookie':'SUB=_2AkMTxRtMf8NxqwJRmfkWymvrZYpwzgnEieKlmeqXJRMxHRl-yT9vqmwGtRB6OEU1o0XHA1oelIk8yihKQUtI4PpbJiDN; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFfhoRyDQqxppb5s-ZKTSrm; SINAGLOBAL=275051762866.5894.1687786635502; ULV=1687786635528:1:1:1:275051762866.5894.1687786635502:; XSRF-TOKEN=rluiT7u8NL9c-jdCp9GJuqMp; WBPSESS=rcUsgxdBPA3YG5ZaoysyzO3wF5zGoF4aIJWkaQeL2KkjOOFvGau2c7U8EytAPgiiD9CkM1CPFDM5EHc2ofjVBm9IDDSfD8BSI0FrUowKeP7tuAzYwJiRVyTupAGG9hRG',
    #'reference':'https://weibo.com/newlogin?tabtype=search&gid=&openLoginLayer=0&url=https%3A%2F%2Fwww.weibo.com%2F',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
}

url='https://weibo.com/ajax/side/hotSearch'
resp = requests.get(url, headers=headers).json()
titlelist,ranklist,hotlist,categorylist=[],[],[],[]
titlelist.append(resp['data']['hotgov']['name'])
ranklist.append("置顶")
hotlist.append(0)
categorylist.append("置顶榜单")
# i=0
for data in resp['data']['realtime']:
    # print(i)
    # i+=1
    if 'ad_type' in data:
        if(data['ad_type'] == "商业投放" or data['ad_type'] == "资源投放"):
            continue
    title=data['note']
    rank=data['rank']
    hot=data['raw_hot']
    category=data['category']
    titlelist.append(title)
    ranklist.append(rank+1)
    hotlist.append(hot)
    categorylist.append(category)
data = {
    '标题': titlelist,
    '排名': ranklist,
    '热度': hotlist,
    '类别':categorylist,
}
dataframe = pandas.DataFrame(data=data)
dataframe.to_csv('微博热榜.csv', index=False, encoding='utf_8_sig')
