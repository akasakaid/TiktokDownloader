from ast import literal_eval
import re
import sys
import random
from base64 import b64decode
try:
    import requests
    import bs4
except ImportError:
    sys.exit('- module not installed !')

"""
function (h, u, n, t, e, r) {
    r = "";
    for (var i = 0, len = h.length;
        i < len;
        i++) {
        var s = "";
        while (h[i] !== n[e]) {
            s += h[i];
            i++
        } for (var j = 0;
            j < n.length;
            j++)s = s.replace(new RegExp(n[j], "g"), j);
        r += String.fromCharCode(_0xe45c(s, e, 10) - t)
    }
    var hasil = decodeURIComponent(escape(r));
    return hasil;
}
"""


class tiktok_downloader:
    def __init__(self):
        pass

    def ttscraper(self, url, output_name):
        ses = requests.Session()
        req = ses.post('https://ytpp3.com/ttscraper/parse', data={"url": url})
        if '"message":"success"' in req.text:
            load = req.json()
            url_download = load['data']['nwm_video_url']
            get_content = requests.get(url_download)
            with open(output_name, 'wb') as fd:
                fd.write(get_content.content)
            return True
        else:
            return False

    def musicaldown(self, url, output_name):
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
        parse = bs4.BeautifulSoup(req.text, 'html.parser')
        get_all_input = parse.findAll('input')
        for i in get_all_input:
            if i.get("id") == "link_url":
                data[i.get("name")] = url
            else:
                data[i.get("name")] = i.get("value")
        post_url = server_url + "id/download"
        req_post = ses.post(post_url, data=data, allow_redirects=True)
        if req_post.status_code == 302 or 'This video is currently not available' in req_post.text or 'Video is private or removed!' in req_post.text:
            print('- video private or remove')
            return 'private/remove'
        elif 'Submitted Url is Invalid, Try Again' in req_post.text:
            print('- url is invalid')
            return 'url-invalid'
        get_all_blank = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll(
            'a', attrs={'target': '_blank'})

        download_link = get_all_blank[0].get('href')
        get_content = requests.get(download_link)

        with open(output_name, 'wb') as fd:
            fd.write(get_content.content)
        return True
