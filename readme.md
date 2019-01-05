# npr agent

习惯使用播客听TED，之前使用的是iOS自带的播客听的Ted Radio Hour，去年发现好像不好使用了速度慢了很多

后来下载官方的npr one改用app收听

然而大概一个月前又听不了，很多链接都被墙了

实在忍不了，看下之前的梯子用的那小鸡，居然是1g RAM，有点闲置，于是利用起来

用python3写了个脚本，把npr上的Ted Radio Hour订阅源关注了，定时把资源下载下来然后用nginx服务跑起来

然后更新下RSS的资源链接

这样访问这个代理的RSS就流畅多了，自己使用也不用担心流量问题

理论上扩展为其他的订阅也是👌的

使用办法：

修改npr_agent.py的host为你最终提供服务的域名或者IP
比如
new_media_base_url = "http://yourdomain:8001/media/"
NEW_FEED_URL = "http://yourdomain:8001/ted.xml"

然后
```bash
docker-compose build
docker-compose up -d 
```

稍等一下，取决于你的vps速度，
然后在播客上添加新的订阅源http://yourdomain:8001/ted.xml 即可