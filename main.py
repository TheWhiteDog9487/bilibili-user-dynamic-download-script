import asyncio
import json
from collections.abc import Callable
from datetime import datetime
from os import makedirs
from typing import Dict

import aiohttp

from wbi import get_wbi_params

UID = '401746666'
Dynamic_URL = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={UID}&need_top=1'
Comment_URL = "https://api.bilibili.com/x/v2/reply/wbi/main?"
CookieFilePath = ""
CookieFileName = "cookies.json"
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Cookie": "",}
Continue = True
Offset = 0
Count = -1
TimeNow = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
RequestRate = 0
Universal_SaveFilePath = f"output/{TimeNow}/"
Dynamic_SaveFileName = "dynamic"
Universal_ExtensionFilename = ".json"
Dynamic_SaveFileFullName = f"{Universal_SaveFilePath}{Dynamic_SaveFileName}{Universal_ExtensionFilename}"
Comment_SaveFileName = "comment"
Comment_SaveFileFullName = f"{Universal_SaveFilePath}{Comment_SaveFileName}{Universal_ExtensionFilename}"
Dynamic_List = []
Comment_List = []


async def Get_Comment(Data: Dict):
    Inner_Comment_List = []
    async with aiohttp.ClientSession(headers=Headers) as session:
        for dynamic in Data["data"]["cards"]:
            type: int = 0
            match dynamic["desc"]["type"]:
                case 4:
                    # 纯文字动态 投票
                    type = 17
                case 2:
                    # 带图动态
                    type = 11
                case 1:
                    # 转发动态 转发直播间
                    type = 17
                case 8:
                    # 投稿视频
                    type = 1
                case 64:
                    # 专栏
                    type = 12
            wbi_params = get_wbi_params({
                "oid" : dynamic["desc"]["rid"],
                "type" : type})
            # 是rid不是dynamic_id
            # dynamic_id会有其中一部分评论区抓过来是404啥都木有
            # 别问我为什么rid就行，我也不知道，Copilot自动补全跟我说用这个的
            async with session.get(Comment_URL + wbi_params) as response:
                Comment = await response.json()
                # 这返回的数据里怎么还有广告啊？
                Inner_Comment_List.append({dynamic["desc"]["rid"]: Comment})
    Comment_List.append(Inner_Comment_List)
    print(Inner_Comment_List)

def Debug(Function: Callable):
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


def SaveToFile():
    # if isinstance(Data, list):
    #     for data in Data:
    #         SaveToFile(data, SaveFileFullName)
    makedirs(Universal_SaveFilePath, exist_ok=True)
    with open(Dynamic_SaveFileFullName, "a", encoding="utf-16") as f:
        # Json = json.dumps(Data, indent=4, ensure_ascii=True).encode().decode("unicode_escape").encode('utf-8', 'replace').decode('utf-8')
        Json = json.dumps(Dynamic_List, indent=4, ensure_ascii=False)
        f.write(Json)
    with open(Comment_SaveFileFullName, "a", encoding="utf-16") as f:
        Json = json.dumps(Comment_List, indent=4, ensure_ascii=False)
        f.write(Json)


# @Debug
async def main():
    LoadCookie()
    global Offset
    global Continue
    global Count
    async with aiohttp.ClientSession() as session:
        while Continue:
            if Count == 0:
                break
            await asyncio.sleep(RequestRate)
            async with session.get(Dynamic_URL + f"&offset_dynamic_id={Offset}", headers=Headers) as response:
                if response.status == 412:
                    raise RuntimeError(f"触发风控\n{await response.text()}")
                Dynamic = await response.json()
                if Dynamic["data"]["has_more"] == 0 and Dynamic["data"]["cards"] is None:
                    raise RuntimeError("请传递Cookie")
                for Card in Dynamic["data"]["cards"]:
                    Card["card"] = json.loads(Card["card"])
                    Card["extend_json"] = json.loads(Card["extend_json"])
                if Dynamic["data"]["has_more"] == 1:
                    Offset = Dynamic["data"]["next_offset"]
                    if Count > 0:
                        Count -= 1
                else:
                    Continue = False
                await Get_Comment(Dynamic)
                print(Dynamic)
                Dynamic_List.append(Dynamic)

if __name__ == '__main__':
    asyncio.run(main())
    SaveToFile()
