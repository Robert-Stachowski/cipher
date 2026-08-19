from ..models.text import Text


class Buffer:
    def __init__(self) -> None:
        self._buffer_list: list[Text] = []

    def add(self, text_obj: Text) -> None:
        self._buffer_list.append(text_obj)

    @property
    def entries(self) -> list[Text]:
        # kopia: getter nie może być furtką do mutacji stanu
        return self._buffer_list[:]
