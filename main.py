import json
from typing import Dict

import aiohttp
import asyncio
import os

UID = '401746666'
URL = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={UID}&need_top=1'
CookieFilePath = ""
CookieFileName = "cookies.json"
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Cookie": ""}
Continue = True
Offset = 0
Count = -1
SaveFilePath = ""
SaveFileName = "save.json"


def Debug(Function):
    async def run():
        global Count
        global Offset
        Offset = 724914703621423139
        Count = 1
        await Function()
    return run


def LoadCookie():
    global Headers
    global CookieFilePath
    with open(f"{CookieFilePath}{CookieFileName}", "r", encoding="utf-8") as f:
        cookies = json.load(f)
        for cookie in cookies:
            Headers["Cookie"] += f"{cookie['Name raw']}={cookie['Content raw']};"


def SaveToFile(Data: Dict):
    global SaveFilePath
    with open(f"{SaveFilePath}{SaveFileName}", "a", encoding="utf-16") as f:
        Json = json.dumps(Data, indent=4, ensure_ascii=True).encode().decode("unicode_escape").encode('utf-8', 'replace').decode('utf-8')
        try:
            f.write(Json)
        except UnicodeEncodeError as e:
            pass


def PrepareSaveFile():
    if os.path.exists(f"{SaveFilePath}{SaveFileName}"):
        os.remove(f"{SaveFilePath}{SaveFileName}")


# @Debug
async def main():
    LoadCookie()
    PrepareSaveFile()
    global Offset
    global Continue
    global Count
    while Continue:
        if Count == 0:
            break
        async with aiohttp.ClientSession() as session:
            async with session.get(URL + f"&offset_dynamic_id={Offset}", headers=Headers) as response:
                Data = await response.json()
                if Data["data"]["has_more"] == 1:
                    Offset = Data["data"]["next_offset"]
                    if Count > 0:
                        Count -= 1
                else:
                    Continue = False
                print(Data)
                SaveToFile(Data)


if __name__ == '__main__':
    asyncio.run(main())
