import httpx
import re
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from .get_content import get_content


async def musicaldown(url: str, output: str):
    """
    url: tiktok video url
    output: output file name
    """
    try:
        headers = {"User-Agent": UserAgent().random}
        ses = httpx.AsyncClient(headers=headers)
        res = await ses.get("https://musicaldown.com/en")
        parsing = bs(res.text, "html.parser")
        allInput = parsing.findAll("input")
        data = {}
        for i in allInput:
            if i.get("id") == "link_url":
                data[i.get("name")] = url
                continue

            data[i.get("name")] = i.get("value")

        res = await ses.post(
            "https://musicaldown.com/download", data=data, follow_redirects=True
        )
        if res.text.find("Convert Video Now") >= 0:
            data = re.search(r"data: '(.*?)'", res.text).group(1)
            urlSlider = re.search(r"url: '(.*?)'", res.text).group(1)
            res = await ses.post(urlSlider, data={"data": data})
            if res.text.find('"success":true') >= 0:
                urlVideo = res.json()["url"]
                res = await get_content(urlVideo, output)
                return True

            return False

        parsing = bs(res.text, "html.parser")
        urls = parsing.findAll(
            "a", attrs={"class": "btn waves-effect waves-light orange download"}
        )
        if len(urls) <= 0:
            return False

        i = random.randint(0, 1)
        urlVideo = urls[i].get("href")
        res = await get_content(urlVideo, output)
        return True

    except Exception as e:
        print(f"musicaldown error : {e}")
        return False
