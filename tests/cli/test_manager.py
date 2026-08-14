import pytest
from cipher.cli.manager import Manager
from cipher.models.text import RotType, Status, Text



class FakeMenu:
    def __init__(self, choices: list[str]):
        self._choices = choices or []
        self.infos = []
        self.shown_buffer = None

    def show_main_menu(self):
        pass

    def read_choice(self):
        return self._choices.pop(0)

    def show_info(self, message: str):
        self.infos.append(message)

    def show_buffer(self, entries: list[Text]):
        self.shown_buffer = entries


class FakeFacade:
    def __init__(self, buffer_entries):
        self.buffer_entries = buffer_entries or []


def test_show_buffer_when_empty():
    menu = FakeMenu(["5", "0"])
    manager = Manager(menu, FakeFacade([]))
    manager.run()

    assert menu.infos == ["Pusta pamięć"]

def test_show_buffer_eq_entries():
    entries = [
        Text("test_text", RotType.ROT13, Status.ENCRYPTED),
        Text("test", RotType.ROT47, Status.ENCRYPTED),
    ]
    facade = FakeFacade(entries)
    menu = FakeMenu(["5", "0"])
    manager = Manager(menu, facade)
    manager.run()

    assert menu.shown_buffer == entries
    assert menu.infos == []