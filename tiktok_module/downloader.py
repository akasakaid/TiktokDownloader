import re
import sys
import random
from base64 import b64decode
try:
	import requests
	import bs4
except ImportError:
	sys.exit('- module not installed !')


class tiktok_downloader:
	def __init__(self):
		pass

	def tik_tok_video(self,url):
		"this function can't be use !"
		ses = requests.Session()
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
			'Accept': 'application/json, text/plain, */*',
			'Accept-Language': 'en-US,en;q=0.5',
			'Content-Type': 'application/json',
			'Content-Length': '46',
			'Origin': 'https://tik-tok-video.com',
			'Referer': 'https://tik-tok-video.com/en/'
		}
		data = {"url":url}
		headers['Content-Length'] = str(len(str(data)))
		req = ses.post('https://tik-tok-video.com/api/convert',json=data)
		print(req.text)

	def musicaldown(self,url,output_name):
		"""url: tiktok video url
		output_name: output video (.mp4). Example : video.mp4
		"""
		ses = requests.Session()
		server_url = 'https://musicaldown.com/'
		headers = {
			"Host": "musicaldown.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"DNT": "1",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "none",
			"Sec-Fetch-User": "?1",
			"TE": "trailers"
		}
		ses.headers.update(headers)
		req = ses.get(server_url)
		data = {}
		parse = bs4.BeautifulSoup(req.text,'html.parser')
		get_all_input = parse.findAll('input')
		for i in get_all_input:
			if i.get("id") == "link_url":
				data[i.get("name")] = url
			else:
				data[i.get("name")] = i.get("value")
		post_url = server_url + "id/download"
		req_post = ses.post(post_url,data=data,allow_redirects=True)
		open('hasil.html','wb').write(req_post.content)
		if req_post.status_code == 302 or 'This video is currently not available' in req_post.text or 'Video is private or removed!' in req_post.text:
			print('- video private or remove')
			return 'private/remove'
		elif 'Submitted Url is Invalid, Try Again' in req_post.text:
			print('- url is invalid')
			return 'url-invalid'
		get_all_blank = bs4.BeautifulSoup(req_post.text,'html.parser').findAll('a',attrs={'target':'_blank'})
		download_link = get_all_blank[len(get_all_blank)-1].get('href')
		get_content = requests.get(download_link).content
		open(output_name,'wb').write(get_content)
