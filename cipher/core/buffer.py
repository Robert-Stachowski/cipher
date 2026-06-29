from ..models.text import Text

class Buffer:
    def __init__(self):
        self._buffer_list = []

    def add(self, text_obj: Text) -> None:
        self._buffer_list.append(text_obj)

    @property
    def entries(self) -> list[Text]:
        return self._buffer_list[:]

    def is_empty(self) -> bool:
        return not self._buffer_list
    