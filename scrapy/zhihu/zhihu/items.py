# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnswerItem(scrapy.Item):
    # id = 1
    id = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    author = scrapy.Field()


class CommentItem(scrapy.Item):
    # id = 1-234
    id = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()


class SecondCommentItem(scrapy.Item):
    # id = 1-234-56
    id = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
