# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Title_Cleaner:
    def process_item(self, item, spider):
        if "title" in item.fields and item["title"]:
            item["title"] = item["title"].strip()

        return item


class Audience_Score_Cleaner:
    def process_item(self, item, spider):
        if "audience_rating" in item.fields and not item["audience_rating"]:
            item["audience_rating"] == None
        return item
