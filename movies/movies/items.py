# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    audience_rating = scrapy.Field()
    critic_rating = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    release_date = scrapy.Field()
