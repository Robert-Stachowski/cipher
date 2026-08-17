from unittest.mock import create_autospec

import pytest

from cipher.core.buffer import Buffer
from cipher.facade import Facade
from cipher.models.text import RotType, Status, Text
from cipher.storage.file_handler import FileHandler


@pytest.fixture
def file_handler():
    return create_autospec(FileHandler, instance=True)


@pytest.fixture
def buffer():
    return Buffer()


@pytest.fixture
def facade(buffer, file_handler):
    return Facade(buffer=buffer, file_handler=file_handler)


@pytest.mark.parametrize(
    "rot_type, plain_text, expected",
    [
        (RotType.ROT13, "test_text", "grfg_grkg"),
        (RotType.ROT47, "test_text", "E6DE0E6IE"),
    ],
)
def test_encrypt(facade, rot_type, plain_text, expected):
    result = facade.encrypt(plain_text, rot_type)

    assert result.text == expected
    assert result.rot_type is rot_type
    assert result.status is Status.ENCRYPTED
    assert facade.buffer_entries == [result]


@pytest.mark.parametrize(
    "rot_type, encrypted_text, expected",
    [
        (RotType.ROT13, "grfg_grkg", "test_text"),
        (RotType.ROT47, "E6DE0E6IE", "test_text"),
    ],
)
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


def test_save(file_handler, facade, buffer):
    first = Text("fake_text", RotType.ROT13, Status.ENCRYPTED)
    second = Text("fake_text_2", RotType.ROT47, Status.ENCRYPTED)
    buffer.add(first)
    buffer.add(second)
    facade.save("fake_json.json")

    file_handler.save.assert_called_once_with(
        filename="fake_json.json", entries=[first, second]
    )


def test_load(file_handler, facade):
    first = Text("fake_text_3", RotType.ROT47, Status.ENCRYPTED)
    second = Text("fake_text_4", RotType.ROT13, Status.ENCRYPTED)
    file_handler.read.return_value = [first, second]
    facade.load("fake_json_1.json")

    assert len(facade.buffer_entries) == 2
    assert facade.buffer_entries == [first, second]


def test_load_appends_to_existing_buffer(file_handler, facade, buffer):
    old = Text("fake_text_5", RotType.ROT47, Status.ENCRYPTED)
    buffer.add(old)
    first = Text("fake_text_6", RotType.ROT13, Status.DECRYPTED)
    second = Text("balabla_test", RotType.ROT47, Status.ENCRYPTED)
    file_handler.read.return_value = [first, second]
    facade.load("fake_json_2.json")

    assert len(facade.buffer_entries) == 3
    assert facade.buffer_entries == [old, first, second]
