# 知乎自定义精华文章及其评论爬取

**环境配置**

* pip3 install scrapy
* pip3 install selenium
* 使用火狐浏览器的webdriver，请下载后放在系统路径

**爬虫配置**

> ***编辑zhihu/zhihu/settings.py***

> > 修改第27行 SCROLL_LEN 以确定爬取文章数

> >修改第29行 TOTAL_COMMENT 以确定单篇文章评论数

> > 修改第18行 INIT_URL以确定主题

> > > 如下图金融话题的精华文章url为https://www.zhihu.com/topic/19609455/top-answers，
> > >
> > > 加入到INIT_URL中

> > ![image](https://github.com/heard1/ZhihuJinhua/blob/master/picture/1.png)

**爬取命令**

* cd scrapy
* scrapy crawl zhihu_spider

**爬取结果**

​	结果储存在zhihu/output中，
answer.json为文章，firstComment.json为一级评论，secondComment.json为二级评论

