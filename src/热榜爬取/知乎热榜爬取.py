import requests
import pandas
from bs4 import BeautifulSoup

headers = {
    'cookie': '_xsrf=Siipge1cNfNIWMiOl6bhAMONtAxuuiyQ; _zap=fbb0e699-dc53-4c23-ab40-f35851aa90ca; d_c0=AICTnlrHmRePTjRuy5614d_8N8b2A2ftdZE=|1698236906; q_c1=d107dc499f3a4ca4a849a2f5447b2bdd|1698300872000|1698300872000; __snaker__id=tJr13QslRmq90BIg; YD00517437729195%3AWM_TID=Mjp4MuhbuehEEURFBBeRm9DCOi1bWEyq; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1701521781,1701580274,1701582567,1701585237; gdxidpyhxdE=xxzjwr27GbCR6ox7MEmif9YLsaG4OYm5%2Fc%2FETthjXtlvx3d8Yn%5CyNs%2BZ6u%2BrUHwRiKQRp4eXvtTmuyhl7JffzQvp%5CmuevtdmfI8QjaXKMy6VICEno%2FbyAEOe6DO8oEeN6vRIcy%5C8NK0l8%5CboC2bBpInwU%2FebV%5CU%2FyEJEQgze2hTqE9AH%3A1701586147047; YD00517437729195%3AWM_NI=q65pbEQ4PfpVAK816xbvQnRTvCbCpzevgPnXrLc9Lo37FMb31itulxoEL9MdPwEK0n5QoXyyK07ZoL1i8ZI1vNhZsJ59xAnm%2BJery2G9bvqsgzHpAz8o6BpNNQRDs8yjeXQ%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee93c268a2efbf98c6348cb48bb6d85b938a8aacc86582b2f883d86daee88aa9e52af0fea7c3b92ab3eafb91e14f93eca087f35e8395f8d2b574a2aa9f8fd160b69daea4f372a7aaa9b1ed54b294addacf65f1e98aaee139f3b7bc96ef74ad9b84dad07094a98bacb366f78fa1b9fc7389f0f9bbee48f3b7f8bbcc3bb692a8bbf242f7e7b8a2ed67e996ab93fc3a85e7ae97f479a5a68891c472fcb1faa3f3468e8f9ea5f234bbb6abb9d437e2a3; SESSIONID=nH0hlbbl2AeN4yDY7ytq38n5t8yTIWpKsMyONjR3keQ; captcha_session_v2=2|1:0|10:1701585255|18:captcha_session_v2|88:MFBNSk5xbGlBOTRtN1pCT3NTc1QrWXNtRVpBYWl4UE8vMHZQTHVpT0tvSEJGM3ZtR05QMEl6QzA4YUFLSWVWMA==|167c50be84dc31c1a1438f7251cddb59222422d5690d5ff6ba7039a5d3b1a382; JOID=W14dB01LuUn4E8lUFEaZEtL8zm0CKv91knCkOHR29yK6Jb8fQyKaK5ATyFYaUeNyQ4KyV1A57i-EyT7sileCuio=; osd=Wl8SBklKuEb5F8hVG0edE9Pzz2kDK_B0lnGlN3Vy9iO1JLseQi2bL5ESx1ceUOJ9QoazVl846i6Fxj_oi1aNuy4=; o_act=login; ref_source=other_https://www.zhihu.com/signin?next=/; expire_in=15552000; tst=h; z_c0=2|1:0|10:1701585422|4:z_c0|92:Mi4xcmVPTEdnQUFBQUFBZ0pPZVdzZVpGeGNBQUFCZ0FsVk5EWEJaWmdDQkNwb1h3bURUTDhHR29qZkk3WEZyMjVoQjJR|94e45915f5e55f56fafa18a5698550081fce9b4bfe040d231a18ab8a7b416c1b; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1701586050; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1701586050|1701585235',
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36',
}
url = 'https://www.zhihu.com/hot'
resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, 'lxml')
contents = soup.find_all('div', class_='HotItem-content')
title_list, hot_list, excerpt_list = [], [], []
for content in contents:
    title = content.find('h2').string
    hot = content.find('div', class_='HotItem-metrics').get_text()
    try:
        excerpt = content.find('p').string
    except AttributeError:
        excerpt = ''
    title_list.append(title)
    hot_list.append(hot.split(' ')[0])
    excerpt_list.append(excerpt)

data = {
    '热度': hot_list,
    '标题': title_list,
    '摘录': excerpt_list,
}
dataframe = pandas.DataFrame(data=data)
dataframe.to_csv('知乎热榜.csv', index=False, encoding='utf_8_sig')

# @time 2021/12/24 2:10
# @author Baneik
# @file 知乎热榜.py