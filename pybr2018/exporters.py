from ruamel.yaml import YAML
from scrapy.exporters import BaseItemExporter


class YAMLItemExporter(BaseItemExporter):

    def __init__(self, file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = file
        self.yaml = YAML()
        self.yaml.encoding = self.encoding

    def export_item(self, item):
        self.yaml.dump([dict(item)], self.file)
