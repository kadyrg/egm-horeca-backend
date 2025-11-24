from rest_framework.renderers import JSONRenderer


def camelize(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def camelize_dict(data):
    if isinstance(data, list):
        return [camelize_dict(item) for item in data]
    elif isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = camelize(key)
            new_dict[new_key] = camelize_dict(value)
        return new_dict
    else:
        return data

class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        camelized_data = camelize_dict(data)
        return super().render(camelized_data, accepted_media_type, renderer_context)
