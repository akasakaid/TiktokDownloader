import re
import httpx
from fake_useragent import UserAgent

# from utils import tikmate_decode


async def tikmate(url: str, output):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "PHPSESSID=mtoghi4e6hifojr6q58d61vs62",
        "priority": "u=0, i",
        "referer": "https://www.google.com/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }
    ses = httpx.AsyncClient(headers=headers, timeout=1000)
    result = await ses.get("https://tikmate.io")
    print(result.cookies)
    open("hasil.html", "w", encoding="utf-8").write(result.text)
    token = re.search(r'<input name="token" value="(.*?)"', result.text).group(1)
    data = {"url": url, "token": token}
    ses.headers.update({"content-type": "application/x-www-form-urlencoded"})
    result = await ses.post("https://tikmate.io/abc.php", data=data)
    print(result.text)
    open("hasil.html", "w", encoding="utf-8").write(result.text)
    params = re.search(r'\("(.*?)", (.*?), "(.*?)", (.*?), (.*?)\)', result.text)
    print(params)
