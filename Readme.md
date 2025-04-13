# BiliBili用户动态下载器

## 介绍
就是下载用户动态内容用的。  
我需要，而我没看到有其他人做，所以自己搓了一个。  

**目前只做了最最基本的东西，从服务器拿到的数据不管是什么全部保存。**  
**没有分类，没有图片下载**  
**什么时候更新，取决于我什么时候想弄**

## 注意事项
获取动态内容的接口URL是`https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={用户UID}`  
这个接口好像要求登录，不然从服务器返回来的只有一条无意义数据。  
如果做登录的话太麻烦，而且我大概率搞不定。  
所以我用的是传递Cookie的方式，适配的Cookie文件格式是Firefox插件Cookie Quick Manager导出的json文件。  

## 使用方法
克隆本仓库  
```shell
git clone https://github.com/TheWhiteDog9487/bilibili-user-dynamic-download-script
```
本项目使用uv管理Python环境，请确保你的设备上已经安装，具体请参考[uv的官方文档](https://docs.astral.sh/uv/getting-started/installation/)  
然后，在仓库文件夹下打开终端.
```shell
# 安装项目依赖项
uv sync

# 运行程序
uv run main.py --uid <你的用户UID>

# 例子：
uv run main.py --uid 1709916540
```
记得把你导出的Cookie放在脚本旁边。  
程序会在抓取完成之后自动退出，运行输出在output文件夹里。  

如果觉得运行太慢，并且不想要动态底下评论区的数据，那你可以让程序不要抓取评论区，这会让程序完成所需时间极为显著地减少。  
```shell
uv run main.py --uid <你的用户UID> --no_comment
```