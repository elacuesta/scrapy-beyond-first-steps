from scrapy.exceptions import DropItem
import jsonschema


class ValidateQuotesPipeline:
    """
    Validate each item with JSON Schema
    """
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': 'http://example.com/product.schema.json',
        'title': 'Quote',
        'type': 'object',
        'properties': {
            'url': {
                'type': 'string',
            },
            'author': {
                'type': 'string',
            },
            'text': {
                'type': 'string',
                'maxLength': 200,
            },
            'tags': {
                'type': 'array',
                'items': {
                    'type': 'string',
                },
                'minItems': 2,
                'maxItems': 5,
            }
        },
        'additionalProperties': True,
        'required': ['url', 'author', 'text', 'tags'],
    }

    def process_item(self, item, spider):
        try:
            jsonschema.validate(dict(item), self.schema)
        except jsonschema.ValidationError as ex:
            raise DropItem(ex.message)
        else:
            return item
