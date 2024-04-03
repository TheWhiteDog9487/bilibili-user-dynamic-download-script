# BiliBili用户动态下载器

## 介绍
就是下载用户动态内容用的。  
我需要，而我没看到有其他人做，所以自己搓了一个。  

**目前只做了最最基本的东西，从服务器拿到的数据不管是什么全部保存。**  
**没有分类，没有图片下载**  
**什么时候更新，取决于我什么时候想弄**  

## 依赖项
```python
import json
from typing import Dict

import aiohttp
import asyncio
import os
```
aiohttp需要单独安装，其他的全是内置的标准库。  
```shell
pip install aiohttp
apt install python3-aiohttp
```

## 注意事项
获取动态内容的接口URL是`https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={用户UID}&need_top=1`  
这个接口好像要求登录，不然从服务器返回来的只有一条无意义数据。  
如果做登录的话太麻烦，而且我大概率搞不定。  
所以我用的是传递Cookie的方式，适配的Cookie文件格式是Firefox插件Cookie Quick Manager导出的json文件。  

## 使用方法
下载仓库中的main.py，用记事本或其他文本编辑软件打开，翻到文件的最上面。  
```python
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
```
这一堆配置项，需要修改的只有第一个。  
把UID后面的数字换成你要下载的用户的UID。  
然后直接运行脚本。  
记得把你导出的Cookie放在脚本旁边。