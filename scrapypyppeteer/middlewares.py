# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from pyppeteer import launch
from scrapy import signals
from scrapy.http import HtmlResponse
import asyncio
import logging

logging.getLogger('websockets').setLevel(logging.WARNING)
logging.getLogger('pyppeteer').setLevel(logging.WARNING)


class PyppeteerDownloaderMiddleware:
    
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    
    async def _process_request(self, request, spider):
        options = {
            'headless': False,
        }
        browser = await launch(options)
        page = await browser.newPage()
        response = await page.goto(
            request.url,
            options={
                'timeout': 3000,
            }
        )
        
        content = await page.content()
        body = str.encode(content)
        await page.close()
        await browser.close()
        
        return HtmlResponse(
            page.url,
            status=response.status,
            headers=response.headers,
            body=body,
            encoding='utf-8',
            request=request
        )
    
    def process_request(self, request, spider):
        result = self.loop.run_until_complete(self._process_request(request, spider))
        return result
