import asyncio
import json
from datetime import datetime
from typing import Dict

import aiohttp

UID = '401746666'
URL = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={UID}&need_top=1'
CookieFilePath = ""
CookieFileName = "cookies.json"
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Cookie": "",
    "Referer":f"https://space.bilibili.com/{UID}/dynamic"}
Continue = True
Offset = 0
Count = -1
SaveFilePath = ""
SaveFileName = "save"
ExtensionFilename = ".json"
TimeNow = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
SaveFileFullName = f"{SaveFilePath}{SaveFileName} - {TimeNow}{ExtensionFilename}"
RequestRate = 1


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
    with open(SaveFileFullName, "a", encoding="utf-16") as f:
        # Json = json.dumps(Data, indent=4, ensure_ascii=True).encode().decode("unicode_escape").encode('utf-8', 'replace').decode('utf-8')
        Json = json.dumps(Data, indent=4, ensure_ascii=False)
        try:
            f.write(Json)
        except UnicodeEncodeError as e:
            pass


# @Debug
async def main():
    LoadCookie()
    global Offset
    global Continue
    global Count
    while Continue:
        if Count == 0:
            break
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(RequestRate)
            async with session.get(URL + f"&offset_dynamic_id={Offset}", headers=Headers) as response:
                if response.status == 412:
                    raise RuntimeError(f"触发风控\n{await response.text()}")
                Data = await response.json()
                if Data["data"]["has_more"] == 0 and Data["data"]["cards"] is None:
                    raise RuntimeError("请传递Cookie")
                for c in Data["data"]["cards"]:
                    c["card"] = json.loads(c["card"])
                    c["extend_json"] = json.loads(c["extend_json"])
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
