# -*- coding: utf-8 -*-
import scrapy
import re
import json
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from zhihu.items import AnswerItem, CommentItem, SecondCommentItem


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    url_list = []
    id = 0
    comment_url = "https://www.zhihu.com/api/v4/answers/{answer_id}/root_comments?order=normal&limit=20&offset={comment_num}&status=open"

    def __init__(self):
        # 在初始化对象时，创建driver
        super(ZhihuSpiderSpider, self).__init__(name='zhihu_spider')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option)

    def start_requests(self):
        base_url = self.settings.get("INIT_URL")
        for url in base_url:
            yield scrapy.Request(url, self.get_all_answer)

    def get_all_answer(self, response):
        ans_list = []
        answers = response.css('div[itemprop="zhihu:question"]')
        for answer in answers:
            ans_list.append("https://www.zhihu.com"+answer.css('a::attr(href)').extract_first())
        for single_url in ans_list:
            yield scrapy.Request(single_url, self.parse)

    def parse(self, response):
        answer_item = AnswerItem()
        answer_item['id'] = str(ZhihuSpiderSpider.id)
        ZhihuSpiderSpider.id += 1
        answer_item['question'] = response.css('h1[class="QuestionHeader-title"]::text').extract_first()
        answer_item['author'] = response.css('a[class="UserLink-link"]::text').extract_first()
        pattern = re.compile(r'(&lt;/svg>|<)[^>]+>', re.S)
        answer_result = pattern.sub('', response.css('span[class="RichText ztext CopyrightRichText-richText"]').re_first('.*'))
        answer_item['answer'] = answer_result
        yield answer_item
        url_pattern = re.compile(r'answer/(.*)')
        answer_id = url_pattern.findall(response.url)[0]
        for x in range(20, self.settings.get("TOTAL_COMMENT")+1, 20):
            next_comment = ZhihuSpiderSpider.comment_url.format(answer_id=answer_id, comment_num=x)
            yield scrapy.Request(url=next_comment, meta={'answer_id': ZhihuSpiderSpider.id-1}, callback=self.comment_parse)

    def comment_parse(self, response):
        cur_id = response.meta['answer_id']
        comments = json.loads(response.text)
        comments = dict(comments)
        for comment in comments['data']:
            if 'reply_to_author' not in comment:
                comment_item = CommentItem()
                comment_item['id'] = str(cur_id)+"-1"
                comment_item['text'] = comment['content']
                comment_item['author'] = comment['author']['member']['name']
                yield comment_item
            else:
                second_comment_item = SecondCommentItem()
                second_comment_item['id'] = str(cur_id) + "-2"
                second_comment_item['text'] = comment['content']
                second_comment_item['author'] = comment['author']['member']['name']
                yield second_comment_item
