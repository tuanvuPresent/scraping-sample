class SeleniumRequest:
    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        opts = ChromeOptions()
        opts.add_argument("--disable-dev-shm-usage")
        # opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=service, options=opts)
        self.driver = driver

    def get(self, url):
        self.driver.get(url)
        page_source = self.driver.page_source
        self.driver.close()
        return page_source


class ScrapSelenium:

    def __init__(self, exporter):
        self.exporter = exporter

    def parse(self):
        page_source = SeleniumRequest().get('https://www.python.org/')
        for i in range(10):
            yield {
                'index': i,
            }

    def start(self):
        try:
            self.exporter.open()
            for item in self.parse():
                self.exporter.process_item(item)
        finally:
            self.exporter.close()


if __name__ == '__main__':
    ScrapSelenium(CsvExporter('sample.csv')).start()
