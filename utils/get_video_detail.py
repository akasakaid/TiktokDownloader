import httpx
import json
from bs4 import BeautifulSoup as bs


async def get_video_detail(url: str):
    """
    url: str -> tiktok video url

    return video_id / None
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    ses = httpx.AsyncClient(headers=headers)
    result = await ses.get(url, follow_redirects=True)
    parser = bs(result.text, "html.parser")
    infotag = parser.find("script", attrs={"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    if infotag is None:
        return None
    infoload = json.loads(infotag.text)
    video_detail = infoload.get("__DEFAULT_SCOPE__", {}).get("webapp.video-detail", {})
    video_id = video_detail.get("itemInfo", {}).get("itemStruct", {}).get("id")
    return video_id
