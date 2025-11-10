import requests
import pandas
from bs4 import BeautifulSoup

headers = {
	'cookie': '_xsrf=q5ukOEYjTX1rwImMjbIt7DNL9s2eyMzV; _zap=66b4771d-8f59-4a64-8cc1-35ea10f1fa2e; d_c0=ygCUhhqRQhuPTnB5_hxZDx8ZsGOj51qH1TM=|1761103691; captcha_session_v2=2|1:0|10:1761104904|18:captcha_session_v2|88:cHZGUmJVWFpqa0NqdEVLeEFDN3U3dGNuNGk1cm05MU8zSlVwUFc3NkFZWFJWVVFMRzVqRUlzUU0vMUt0K085Mw==|6e3413c4c0d2cd8aedb7256dbc99a2a1b7321b569fe35366f881047c67d6a2c9; __snaker__id=qULvRGaR2TjH3wxr; gdxidpyhxdE=2lt1cUQyfal6tS6m5g88NjxE7oNiKqGmuaa29GTXBhc2UC4cpkxSI%2BCXqO%2FAyQx3YLqfClnsypVBKLjKKBpdXqcWYa44l6u9hUU59KpqNn%2BGJzco1%5CE%2BV2SIWamZZUlXZRtOE9Ev%5C8A991VI5AtsN4HqXwD4YV9iPcPsp4xX%2BfxdhMxk%3A1761105824837; q_c1=c9a11c2c1eb84cdbb44a8d2ca17f2537|1761104940000|1761104940000; z_c0=2|1:0|10:1761109203|4:z_c0|92:Mi4xcmVPTEdnQUFBQURLQUpTR0dwRkNHeGNBQUFCZ0FsVk5MS0xsYVFCRF9HUXlFNDFCYU1nY2xaVmNuVkFXVk53RTNn|262c03b22aa3f13411ca83817850eb7a551a72080bfc4c639f4989a2c293a1e5; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1761902814,1762132704,1762251168,1762748578; HMACCOUNT=8C6808CCC43CD31A; __zse_ck=004_S5mKSOXD/vmw7EgPlhmW7ag7Ujk/qdcIp2vOBFdXXOLqEgcMYUpwfKL84g3/SOdosCZjhz5i2enAnWXNK/D7zc=tR9bHDRqrIlxY2cVLRifR5wTqELaIo13hf1QxzSED-6TPmLfRkatqfu0o1KT2vy82ZmWVtCEyvpRcT3va488fM0B9CIRWs3fmMOhRRqFEx61kKnOpCUP1XLM8GhwHLRtezIIqQu2toxvVD3jSa4lMDA0VmYfFzXr7puJiXltIC; BEC=738c6d0432e7aaf738ea36855cdce904; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1762749141; SESSIONID=ivot7iB1H8g64maKIcABgnk5jjRbhYHuQ1CNxCTcCkq; JOID=U1wQBUoPcgdM_5kkMPGFkMHmD2MvYwVrP8j1ZwJHT2F5zPRAetsaEiL6nSY0FJuSIlq8WSXfrsZfsEgtft1oorc=; osd=U1kXBEMPdwBN9pkhN_CMkMThDmovZgJqNsjwYANOT2R-zf1Af9wbGyL_mic9FJ6VI1O8XCLep8Zat0kkfthvo74=',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}
url = 'https://www.zhihu.com/hot'
resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, 'lxml')
contents = soup.find_all('div', class_='HotItem-content')
id_list, title_list, hot_list, excerpt_list  = [], [], [], []
for content in contents:
	title = content.find('h2').string
	#   <a href="https://www.zhihu.com/question/1971013834941667175" title="放弃体制内稳定工作，去追热爱的事真的值得吗？" target="_blank" rel="noopener noreferrer" data-za-not-track-link="true">
	#                                 <h2 class="HotItem-title">放弃体制内稳定工作，去追热爱的事真的值得吗？</h2>
	#                                 <p class="HotItem-excerpt">30 岁左右纠结要不要裸辞，父母反复强调稳定的重要性，可当前工作完全没热情，每天都在内耗。想知道大家有没有类似经历，或是从过来人的角度，能给点真实建议吗？</p>
	#                             </a>
	# title的上一层级，<a href="https://www.zhihu.com/question/1971013834941667175"，包含了问题id以及url
	url = content.find('h2').parent['href']
	id = url.split('/')[-1]
	hot = content.find('div', class_='HotItem-metrics').get_text()
	try:
		excerpt = content.find('p', class_='HotItem-excerpt').string
	except AttributeError:
		excerpt = ''
	id_list.append(id)
	title_list.append(title)
	hot_list.append(hot.split(' ')[0])
	excerpt_list.append(excerpt)

data = {
	'问题ID': id_list,
	'热度': hot_list,
	'标题': title_list,
	'摘录': excerpt_list,
}
dataframe = pandas.DataFrame(data=data)
dataframe.to_csv('知乎热榜.csv', index=False, encoding='utf_8_sig')

# @time 2021/12/24 2:10
# @author Baneik
# @file 知乎热榜.py