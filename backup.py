import os, json, requests, html2text
from bs4 import BeautifulSoup

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'
}

path     = 'result/{user}/list/'
manifest = 'result/{user}/manifest.json'
filename = 'result/{user}/list/[{id}] {date} {time}.json'

# userlist = [26673, 51815, 26166, 30903, 41918, 25902, 25715, 32831, 23243]
userlist = [36361, 36362, 36363, 62869, 26199, 28216]

def makedir(path):
	try:
		os.makedirs(path)
	except:
		pass

def solve(user):
	page, counter = 0, 0
	makedir(path.format(user=user))
	base = open(manifest.format(user=user), 'w+')
	while True:
		page += 1
		url  = 'https://www.luogu.org/feed/user/{user}?page={page}'.format(user=user, page=page)
		html = requests.get(url, headers=headers).text
		if '$("#feed-more").hide()' in html:
			break
		print('at page', page)
		soup = BeautifulSoup(html, features="html.parser")
		benb = soup.find_all(class_='am-comment-main')
		for it in benb:
			this = {}
			counter += 1
			_tmp, this['date'], this['time'] = it.header.div.text.split()
			this['html'] = str(it.find_all(class_="am-comment-bd")[0].span)[27:-7]
			this['markdown'] = html2text.html2text(this['html'])[:-2]
			with open(filename.format(
					id    = '%05d' % counter,
					user  = user,
					date  = this['date'],
					time  = this['time'],
					short = this['markdown'][0:30]), 'w+') as file:
				file.write(json.dumps(this, ensure_ascii=False))
				file.close()
			status = ['%05d' % counter, this['date'], this['time'], this['markdown'].replace('\n', '')]
			base.write(' '.join(status) + '\n')
			status[-1] = this['markdown'][0:30].replace('\n', '')
			print(' '.join(status))
	base.close()

if __name__ == '__main__':
	for user in userlist:
		solve(user)