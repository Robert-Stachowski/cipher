from cipher.models.text import RotType, Status, Text
from cipher.storage.file_handler import FileHandler
from cipher.core.buffer import Buffer
from cipher.facade import Facade
import pytest


class FakeFileHandler:
    def __init__(self, read_entries: list[Text] | None = None):
        self.saved_filename = None
        self.saved_entries = None
        self.read_entries = read_entries or []

    def save(self, filename: str, entries: list[Text]) -> None:
        self.saved_filename = filename
        self.saved_entries = entries

    def read(self, filename: str) -> list[Text]:
        return self.read_entries


@pytest.fixture
def facade():
    return Facade(buffer=Buffer(), file_handler=FileHandler())


@pytest.mark.parametrize("rot_type, plain_text, expected", [
    (RotType.ROT13, "test_text", "grfg_grkg"),
    (RotType.ROT47, "test_text", "E6DE0E6IE")
])
def test_encrypt(facade, rot_type, plain_text, expected):
    result = facade.encrypt(plain_text, rot_type)

    assert result.text == expected
    assert result.rot_type is rot_type
    assert result.status is Status.ENCRYPTED
    assert facade.buffer_entries == [result]


@pytest.mark.parametrize("rot_type, encrypted_text, expected", [
    (RotType.ROT13, "grfg_grkg", "test_text"),
    (RotType.ROT47, "E6DE0E6IE", "test_text")
])
def test_decrypt(facade, rot_type, encrypted_text, expected):
    result = facade.decrypt(encrypted_text, rot_type)

    assert result.text == expected
    assert result.rot_type is rot_type
    assert result.status is Status.DECRYPTED
    assert facade.buffer_entries == [result]


def test_buffer_keeps_entries_in_order(facade):
    first = facade.encrypt("test_text", RotType.ROT13)
    second = facade.encrypt("test_text_2", RotType.ROT47)

    assert len(facade.buffer_entries) == 2
    assert facade.buffer_entries[0] == first
    assert facade.buffer_entries[1] == second


def test_save():
    fake_handler = FakeFileHandler()
    buffer = Buffer()
    first = Text("fake_text", RotType.ROT13, Status.ENCRYPTED)
    second = Text("fake_text_2", RotType.ROT47, Status.ENCRYPTED)
    buffer.add(first)
    buffer.add(second)
    facade = Facade(buffer=buffer, file_handler=fake_handler)
    facade.save("fake_json.json")

    assert len(fake_handler.saved_entries) == 2
    assert fake_handler.saved_entries[0] == first
    assert fake_handler.saved_entries[1] == second
    assert fake_handler.saved_filename == "fake_json.json"


def test_load():
    buffer = Buffer()
    first = Text("fake_text_3", RotType.ROT47, Status.ENCRYPTED)
    second = Text("fake_text_4", RotType.ROT13, Status.ENCRYPTED)
    fake_handler = FakeFileHandler([first, second])
    facade = Facade(buffer=buffer, file_handler=fake_handler)
    facade.load("fake_json_1.json")

    assert facade.buffer_entries == [first, second]


def test_load_appends_to_existing_buffer():
    buffer = Buffer()
    old = Text("fake_text_5", RotType.ROT47, Status.ENCRYPTED)
    buffer.add(old)
    first = Text("fake_text_6", RotType.ROT13, Status.DECRYPTED)
    second = Text("balabla_test", RotType.ROT47, Status.ENCRYPTED)
    fake_handler = FakeFileHandler([first, second])
    facade = Facade(buffer=buffer, file_handler=fake_handler)
    facade.load("fake_json_2.json")

    assert facade.buffer_entries == [old, first, second]
