import json


class JSONSerializer(object):
    """Serializer to be used in session storage."""

    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))
