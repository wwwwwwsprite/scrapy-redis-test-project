# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/图书/b/ref=sa_menu_top_books_l1?ie=UTF8&node=658390051']
    redis_key = 'amazon'

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='a-row a-expander-container a-expander-extend-container']/li",)), follow=True),
        # 匹配一个li标签
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']//a[@class='a-link-normal a-text-normal']",)), callback="parse_book_detail"),
        # 匹配列表页翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)), follow=True),
    )

    def parse_book_detail(self, response):
        item = {}
        item["book_title"] = response.xpath("//span[@id='productTitle']/text()").extract_first()
        item["book_publish_date"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first().strip()
        item["book_author"] = response.xpath("//div[@id='bylineInfo']/span/a/text()").extract()
        item["book_author"] = [i.strip() for i in item['book_author'] if len(i.strip())>0]
        # item["book_img"] = response.xpath("//div[@id='img-canvas']/img/@src").extract_first()
        item["book_price"] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()").extract_first()
        item["book_cate"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//ul/li[not(@class)]/span/a/text()").extract()
        item["book_cate"] = [i.strip() for i in item['book_cate'] if len(i.strip())>0]
        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
        print(item)

