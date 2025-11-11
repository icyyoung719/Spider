import requests
import pandas
from bs4 import BeautifulSoup

# @time 2021/12/24 2:10
# @author Baneik
# @file 知乎热榜.py

headers = {
	'cookie': '_xsrf=q5ukOEYjTX1rwImMjbIt7DNL9s2eyMzV; _zap=66b4771d-8f59-4a64-8cc1-35ea10f1fa2e; d_c0=ygCUhhqRQhuPTnB5_hxZDx8ZsGOj51qH1TM=|1761103691; captcha_session_v2=2|1:0|10:1761104904|18:captcha_session_v2|88:cHZGUmJVWFpqa0NqdEVLeEFDN3U3dGNuNGk1cm05MU8zSlVwUFc3NkFZWFJWVVFMRzVqRUlzUU0vMUt0K085Mw==|6e3413c4c0d2cd8aedb7256dbc99a2a1b7321b569fe35366f881047c67d6a2c9; __snaker__id=qULvRGaR2TjH3wxr; gdxidpyhxdE=2lt1cUQyfal6tS6m5g88NjxE7oNiKqGmuaa29GTXBhc2UC4cpkxSI%2BCXqO%2FAyQx3YLqfClnsypVBKLjKKBpdXqcWYa44l6u9hUU59KpqNn%2BGJzco1%5CE%2BV2SIWamZZUlXZRtOE9Ev%5C8A991VI5AtsN4HqXwD4YV9iPcPsp4xX%2BfxdhMxk%3A1761105824837; q_c1=c9a11c2c1eb84cdbb44a8d2ca17f2537|1761104940000|1761104940000; z_c0=2|1:0|10:1761109203|4:z_c0|92:Mi4xcmVPTEdnQUFBQURLQUpTR0dwRkNHeGNBQUFCZ0FsVk5MS0xsYVFCRF9HUXlFNDFCYU1nY2xaVmNuVkFXVk53RTNn|262c03b22aa3f13411ca83817850eb7a551a72080bfc4c639f4989a2c293a1e5; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1761902814,1762132704,1762251168,1762748578; HMACCOUNT=8C6808CCC43CD31A; __zse_ck=004_S5mKSOXD/vmw7EgPlhmW7ag7Ujk/qdcIp2vOBFdXXOLqEgcMYUpwfKL84g3/SOdosCZjhz5i2enAnWXNK/D7zc=tR9bHDRqrIlxY2cVLRifR5wTqELaIo13hf1QxzSED-6TPmLfRkatqfu0o1KT2vy82ZmWVtCEyvpRcT3va488fM0B9CIRWs3fmMOhRRqFEx61kKnOpCUP1XLM8GhwHLRtezIIqQu2toxvVD3jSa4lMDA0VmYfFzXr7puJiXltIC; BEC=738c6d0432e7aaf738ea36855cdce904; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1762749141; SESSIONID=ivot7iB1H8g64maKIcABgnk5jjRbhYHuQ1CNxCTcCkq; JOID=U1wQBUoPcgdM_5kkMPGFkMHmD2MvYwVrP8j1ZwJHT2F5zPRAetsaEiL6nSY0FJuSIlq8WSXfrsZfsEgtft1oorc=; osd=U1kXBEMPdwBN9pkhN_CMkMThDmovZgJqNsjwYANOT2R-zf1Af9wbGyL_mic9FJ6VI1O8XCLep8Zat0kkfthvo74=',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}
def fetch_hot(output_path='zhihu_hot.csv', headers=headers):
	"""Fetch Zhihu hot list and save to CSV.

	Returns the DataFrame.
	"""
	url = 'https://www.zhihu.com/hot'
	resp = requests.get(url, headers=headers).text
	soup = BeautifulSoup(resp, 'lxml')
	contents = soup.find_all('div', class_='HotItem-content')
	id_list, title_list, hot_list, excerpt_list  = [], [], [], []
	for content in contents:
		title = content.find('h2').string
		# title的上一层级，<a href="https://www.zhihu.com/question/1971013834941667175"，包含了问题id以及url
		url = content.find('h2').parent.get('href', '')
		qid = url.split('/')[-1] if url else ''
		hot = content.find('div', class_='HotItem-metrics').get_text()
		try:
			excerpt = content.find('p', class_='HotItem-excerpt').string
		except AttributeError:
			excerpt = ''
		id_list.append(qid)
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
	dataframe.to_csv(output_path, index=False, encoding='utf_8_sig')
	return dataframe

# -------------------------------------
# 爬取制定问题id下的回答
test_id = '1970998781324529762'


def fetch_answers(question_id, limit=20, max_answers=None, headers=headers):
	"""Fetch answers for a Zhihu question using the v4 API and return a pandas DataFrame.

	Args:
		question_id (str): Zhihu question id
		limit (int): number of answers to fetch per request (max allowed by API)
		max_answers (int|None): optional cap on total answers to fetch
		headers (dict): request headers (should include cookie for auth if needed)

	Returns:
		pandas.DataFrame: columns: ['answer_id', 'author', 'voteup_count', 'comment_count', 'created_time', 'content']
	"""
	import time
	import json
	from bs4 import BeautifulSoup as BS

	base = f'https://www.zhihu.com/api/v4/questions/{question_id}/answers'
	offset = 0
	rows = []
	fetched = 0

	include = (
		'data[*].is_normal,content,author,created_time,voteup_count,comment_count'
	)

	while True:
		params = {
			'include': include,
			'limit': str(limit),
			'offset': str(offset),
		}
		try:
			resp = requests.get(base, params=params, headers=headers, timeout=10)
			data = resp.json()
		except Exception as e:
			print(f'Error fetching answers: {e}')
			break

		if 'data' not in data:
			print('Unexpected response structure, stopping.')
			break

		for item in data.get('data', []):
			# answer id
			ans_id = item.get('id')
			author = ''
			a = item.get('author')
			if isinstance(a, dict):
				author = a.get('name') or a.get('id') or ''
			# vote and comment counts
			vote = item.get('voteup_count', 0)
			comment = item.get('comment_count', 0)
			created = item.get('created_time')
			# content html -> text
			content_html = item.get('content') or ''
			try:
				content_text = BS(content_html, 'lxml').get_text(separator='\n').strip()
			except Exception:
				content_text = content_html

			rows.append({
				'answer_id': ans_id,
				'author': author,
				'voteup_count': vote,
				'comment_count': comment,
				'created_time': created,
				'content': content_text,
			})
			fetched += 1
			if max_answers and fetched >= max_answers:
				break

		# paging: if less than limit returned, we're done
		length = len(data.get('data', []))
		if max_answers and fetched >= max_answers:
			break
		if length < limit:
			break
		offset += length
		# be polite
		time.sleep(0.5)

	df = pandas.DataFrame(rows)
	return df


if __name__ == '__main__':
	# interactive CLI: choose fetching hot list or fetching answers
	import os
	from datetime import datetime

	# script directory and output folder
	script_dir = os.path.dirname(os.path.abspath(__file__))
	out_root = os.path.join(script_dir, 'out')
	os.makedirs(out_root, exist_ok=True)

	def prompt_menu():
		print('\n请选择功能：')
		print('1. 爬取知乎热榜并保存为 CSV (保存到 out/)')
		print('2. 爬取单个问题的回答（输入单个 question id，CSV 保存到 out/）')
		print('3. 从 CSV 文件读取问题列表并爬取（CSV 包含 question_id 列或第一列为 id，批量结果保存到 out/时间戳子目录）')
		print('4. 将热榜问题列表作为待爬取问题（可选择先更新热榜，批量结果保存到 out/时间戳子目录）')
		print('q. 退出')
		return input('输入选项 (1/2/3/4/q): ').strip()

	while True:
		choice = prompt_menu()
		if choice == '1':
			out_name = input('输入保存文件名（回车使用默认 zhihu_hot.csv）: ').strip() or 'zhihu_hot.csv'
			out_path = os.path.join(out_root, out_name)
			print('正在爬取热榜...')
			df_hot = fetch_hot(out_path, headers=headers)
			print(f'已保存 {len(df_hot)} 条热榜到 "{out_path}"')
		elif choice == '2':
			# 单个问题 ID
			qid = input('输入问题 ID: ').strip()
			if not qid:
				print('未输入问题ID，返回菜单。')
				continue
			ma = input('可选：输入最大回答数（留空表示不限制）: ').strip()
			max_answers = int(ma) if ma.isdigit() else None
			print(f'Fetching answers for question id: {qid} ...')
			try:
				df_answers = fetch_answers(qid, limit=20, max_answers=max_answers, headers=headers)
			except Exception as e:
				print(f'问题 {qid} 爬取出错: {e}')
				continue
			# save single CSV directly to out_root
			out_file = os.path.join(out_root, f'zhihu_answers_{qid}.csv')
			df_answers.to_csv(out_file, index=False, encoding='utf_8_sig')
			print(f'Wrote {len(df_answers)} answers to "{out_file}"')
			# show a small sample for validation
			print('示例：')
			print(df_answers.head(2).to_dict(orient='records'))
		elif choice == '3':
			# 从指定 CSV 文件中读取 question_id 列
			src = input('输入 CSV 文件路径（包含 question_id 列，回车使用默认 list.csv）: ').strip() or 'list.csv'
			ma = input('可选：输入每个问题的最大回答数（留空表示不限制）: ').strip()
			max_answers = int(ma) if ma.isdigit() else None

			qids = []
			if os.path.exists(src) and src.lower().endswith('.csv'):
				try:
					df_in = pandas.read_csv(src)
					if 'question_id' in df_in.columns:
						qids = df_in['question_id'].astype(str).tolist()
					else:
						qids = df_in.iloc[:, 0].astype(str).tolist()
				except Exception as e:
					print(f'读取 CSV 出错: {e}')
					continue
			else:
				print('CSV 文件不存在或不是以 .csv 结尾，返回菜单。')
				continue

			if not qids:
				print('没有发现任何问题ID，返回菜单。')
				continue

			# batch: create timestamped subfolder under out_root
			timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
			batch_dir = os.path.join(out_root, timestamp)
			os.makedirs(batch_dir, exist_ok=True)
			for q in qids:
				print(f'Fetching answers for question id: {q} ...')
				try:
					df_answers = fetch_answers(q, limit=20, max_answers=max_answers, headers=headers)
				except Exception as e:
					print(f'问题 {q} 爬取出错: {e}')
					continue
				out_file = os.path.join(batch_dir, f'zhihu_answers_{q}.csv')
				df_answers.to_csv(out_file, index=False, encoding='utf_8_sig')
				print(f'Wrote {len(df_answers)} answers to "{out_file}"')
		elif choice == '4':
			# 将热榜问题列表作为待爬取问题
			use_hot = input('是否先更新热榜并保存为 out/zhihu_hot.csv？(y/n，默认 y): ').strip().lower() or 'y'
			if use_hot == 'y':
				print('正在更新热榜...')
				# save hot to out_root
				df_hot = fetch_hot(os.path.join(out_root, 'zhihu_hot.csv'), headers=headers)
			else:
				# try to read existing out/zhihu_hot.csv
				hot_path = os.path.join(out_root, 'zhihu_hot.csv')
				if os.path.exists(hot_path):
					df_hot = pandas.read_csv(hot_path)
				else:
					print('未找到 out/zhihu_hot.csv，先更新热榜。')
					df_hot = fetch_hot(os.path.join(out_root, 'zhihu_hot.csv'), headers=headers)

			# extract question ids column '问题ID'
			if '问题ID' in df_hot.columns:
				qids = df_hot['问题ID'].astype(str).tolist()
			else:
				qids = df_hot.iloc[:, 0].astype(str).tolist()

			# optional max answers
			ma = input('可选：输入每个问题的最大回答数（留空表示不限制）: ').strip()
			max_answers = int(ma) if ma.isdigit() else None

			# batch: create timestamped subfolder under out_root
			timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
			batch_dir = os.path.join(out_root, timestamp)
			os.makedirs(batch_dir, exist_ok=True)

			for q in qids:
				if not q:
					continue
				print(f'Fetching answers for question id: {q} ...')
				try:
					df_answers = fetch_answers(q, limit=20, max_answers=max_answers, headers=headers)
				except Exception as e:
					print(f'问题 {q} 爬取出错: {e}')
					continue
				out_file = os.path.join(batch_dir, f'zhihu_answers_{q}.csv')
				df_answers.to_csv(out_file, index=False, encoding='utf_8_sig')
				print(f'Wrote {len(df_answers)} answers to "{out_file}"')
		elif choice.lower() in ('q', 'quit', 'exit'):
			print('退出。')
			break
		else:
			print('未知选项，请重试。')

# 爬取热榜、问题的基础功能已经实现了，修改脚本的整体框架如下：
# 启动后，询问用户需要什么功能：1. 爬取热榜 2. 爬取指定问题的回答 3. 爬取代码中指定路径csv列表中的回答 4. 将热榜问题列表作为待爬取问题
# 根据用户选择，执行相应的功能模块


# 爬取爬取指定问题的回答，允许用户输入问题ID，以及可选的最大回答数​（默认不限制）
# 用户也可以输入csv，表示爬取csv_path中含有的问题ID列表​
# csv_path格式如下：
# question_id
# 1970998781324529762
# 1971013834941667175
# 等等