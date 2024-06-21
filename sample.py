import csv
import io


class Exporter:
    def open(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def close(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def process_item(self, item):
        raise NotImplementedError("Subclasses should implement this method.")


class CsvExporter(Exporter):
    def __init__(self, filename, encoding='utf-8', newline=''):
        self.filename = filename
        self.encoding = encoding
        self.newline = newline
        self.stream = None
        self.csv_writer = None
        self._headers_not_written = True

    def open(self):
        file = open(self.filename, 'ab')
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline=self.newline,
        )
        self.csv_writer = csv.writer(self.stream)

    def process_item(self, item: dict):
        if self._headers_not_written:
            self._headers_not_written = False
            self.csv_writer.writerow(item.keys())
        self.csv_writer.writerow(item.values())

    def close(self):
        if self.stream:
            self.stream.close()
            self.stream = None
            self.csv_writer = None


class Scraper:
    def __init__(self, exporter):
        self.exporter = exporter

    def parse(self):
        yield from self.parse_detail()

    def parse_detail(self):
        for i in range(10):
            yield {
                'age': 'age',
                'name': i,
            }

    def start(self):
        try:
            self.exporter.open()
            for item in self.parse():
                print(item)
                self.exporter.process_item(item)
        finally:
            self.exporter.close()


if __name__ == "__main__":
    exporter = CsvExporter('items.csv')
    scraper = Scraper(exporter)
    scraper.start()
