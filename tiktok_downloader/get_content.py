import httpx
import aiofiles


async def get_content(
    url: str, output: str = "video.mp4", cookies: httpx.Cookies = None
):
    client = httpx.AsyncClient()
    result = await client.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        },
        cookies=cookies,
    )
    async with aiofiles.open(output, "wb") as w:
        async for content in result.aiter_bytes(chunk_size=1024):
            await w.write(content)
