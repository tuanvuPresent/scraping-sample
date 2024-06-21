from datetime import datetime
from typing import Any

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response


class SampleSpider(scrapy.Spider):
    name = 'sample'
    start_urls = ['https://www.python.org']

    def parse(self, response: Response, **kwargs: Any) -> Any:
        href = ''
        yield response.follow(href, callback=self.parse_item, meta={})

    def parse_item(self, response: Response):
        try:
            for item in range(10):
                yield {
                    'data': 'data',
                }
        except Exception as e:
            self.logger.error(f'{response.url}: {e}')


if __name__ == '__main__':
    output_path = f'output_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    custom_settings = {
        "FEEDS": {
            output_path: {"format": "csv"},
        },
        'LOG_LEVEL': 'INFO',
    }
    sample_process = CrawlerProcess(settings=custom_settings)
    sample_process.crawl(SampleSpider)
    sample_process.start()
