# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class ZhihuPipeline(object):

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)
        if type(item).__name__ == 'AnswerItem':
            f = codecs.open('output/answer.json', 'a', 'utf-8')
            f.write(lines+'\n')
            f.close()
        elif type(item).__name__ == 'CommentItem':
            f = codecs.open('output/firstComment.json', 'a', 'utf-8')
            f.write(lines + '\n')
            f.close()
        else:
            f = codecs.open('output/secondComment.json', 'a', 'utf-8')
            f.write(lines + '\n')
            f.close()
        return item
