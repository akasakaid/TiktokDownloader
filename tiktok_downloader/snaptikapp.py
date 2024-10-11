import httpx
import re
import js2py


async def snaptikapp(url: str):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://snaptik.app",
        "priority": "u=1, i",
        "referer": "https://snaptik.app/en1",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }
    ses = httpx.AsyncClient(headers=headers)
    result = await ses.get("https://snaptik.app/")
    token = re.search(
        r'<input name="token" value="(.*?)" type="hidden">', result.text
    ).group(1)
    data = {"token": token, "url": url, "lang": "en1"}
    result = await ses.post("https://snaptik.app/abc2.php", data=data)
    result = result.text.replace("eval", "let result = ")
    result += ";return result;"
    open("hasiljs.js", "w").write(result)
    jsresult = js2py.eval_js(result)
    print(jsresult)
