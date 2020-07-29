# -*- coding: utf-8 -*-
from gerapy_pyppeteer import PyppeteerRequest
from scrapy import Request, Spider


class BookSpider(Spider):
    name = 'book'
    allowed_domains = ['dynamic5.scrape.center']
    
    base_url = 'https://dynamic5.scrape.center/page/{page}'
    max_page = 10
    
    def start_requests(self):
        for page in range(1, self.max_page + 1):
            url = self.base_url.format(page=page)
            yield PyppeteerRequest(url, callback=self.parse_index, wait_for='.item .name')
    
    def parse_index(self, response):
        for item in response.css('.item'):
            name = item.css('.name::text').extract_first()
            authors = item.css('.authors::text').extract_first()
            name = name.strip() if name else None
            authors = authors.strip() if authors else None
            yield {
                'name': name,
                'authors': authors
            }
