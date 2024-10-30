import httpx
import json
from bs4 import BeautifulSoup as bs
from pathlib import Path
from tiktok_downloader.get_content import get_content


async def get_video_detail(url: str):
    """
    url: str -> tiktok video url

    return video_id / None
    """
    path = Path(url)
    post_id = path.stem
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }
    ses = httpx.AsyncClient(headers=headers)
    if not post_id.isdigit():
        result = await ses.get(url, follow_redirects=False)
        if result.text.startswith('<a href="'):
            post_url = result.text.split('<a href="')[1].split("?")[0]
            post_id = Path(post_url).stem
    result = await ses.get(
        f"https://tiktok.com/@i/video/{post_id}", follow_redirects=True
    )
    cookies = result.cookies
    # print(cookie)
    open("tiktok_get_result.html", "w", encoding="utf-8").write(result.text)
    parser = bs(result.text, "html.parser")
    infotag = parser.find("script", attrs={"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    if infotag is None:
        return None
    infoload = json.loads(infotag.text)
    video_detail = infoload.get("__DEFAULT_SCOPE__", {}).get("webapp.video-detail", {})
    video_id = video_detail.get("itemInfo", {}).get("itemStruct", {}).get("id")
    author = video_detail.get("itemInfo", {}).get("itemStruct", {}).get("author", {})
    video = video_detail.get("itemInfo", {}).get("itemStruct", {}).get("video", {})
    image_post = (
        video_detail.get("itemInfo", {}).get("itemStruct", {}).get("imagePost", {})
    )
    images = image_post.get("images")
    author_id = author.get("id")
    author_username = author.get("uniqueId")
    video_url = video.get("playAddr")
    return video_id, author_id, author_username, video_url, images, cookies
