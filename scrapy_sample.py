import os
from datetime import datetime
from typing import Any

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter
from scrapy.http import Response


class ItemPipeline(object):
    files = {}
    exporters = {}
    csv_item_types = []

    def open_spider(self, spider):
        feeds = spider.custom_settings.get('MULTI_CSV_FEEDS', {})
        self.csv_item_types = feeds.keys()
        for output_path, feed_config in feeds.items():
            file_path = os.path.join(spider.custom_settings.get('FILES_STORE', ''), output_path)
            file_exists = os.path.exists(file_path)
            self.files[output_path] = open(file_path, 'ab')
            if file_exists:
                include_headers_line = True
            else:
                include_headers_line = False
            self.exporters[output_path] = CsvItemExporter(self.files[output_path],
                                                          include_headers_line=include_headers_line)

        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        output_path_name = item.pop('output_path_name', None)
        if output_path_name in set(self.csv_item_types):
            self.exporters[output_path_name].export_item(item)
        return item


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
