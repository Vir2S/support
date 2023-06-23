from rest_framework.serializers import Serializer


class SerializerError(Exception):
    def __init__(self, serializer: Serializer) -> None:
        self._serializer = serializer
        super().__init__()
