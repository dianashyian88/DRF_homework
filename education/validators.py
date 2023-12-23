from rest_framework.serializers import ValidationError
from re import findall


class DescriptionValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        # urls = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        result = [url for url in findall(urls, tmp_val)]
        if len(result) != 0:
            for item in result:
                if 'youtube.com' not in item:
                    raise ValidationError('Материалы содержат недопустимые ссылки')
