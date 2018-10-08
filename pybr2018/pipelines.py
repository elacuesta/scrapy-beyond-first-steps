from scrapy.exceptions import DropItem
import jsonschema


class ValidateBookPipeline:
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': 'http://example.com/product.schema.json',
        'title': 'Book',
        'type': 'object',
        'properties': {
            'url': {
                'type': 'string',
            },
            'title': {
                'type': 'string',
                'maxLength': 80,
            },
            'price': {
                'type': 'number',
                'minimum': 20,
                'maximum': 50,
            },
        },
        'additionalProperties': True,
        'required': ['url', 'title', 'price'],
    }

    def process_item(self, item, spider):
        try:
            jsonschema.validate(dict(item), self.schema)
        except jsonschema.ValidationError as ex:
            raise DropItem(ex.message)
        else:
            return item
