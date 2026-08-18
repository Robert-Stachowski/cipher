from unittest.mock import create_autospec

import pytest

from cipher.cli.manager import Manager
from cipher.cli.menu import Menu
from cipher.exceptions import FileHandlerError
from cipher.facade import Facade
from cipher.models.text import RotType, Status, Text


@pytest.fixture
def menu():
    return create_autospec(Menu, instance=True)


@pytest.fixture
def facade():
    return create_autospec(Facade, instance=True)


def test_encrypt_happy_path(menu, facade):
    menu.read_choice.side_effect = ["1", "0"]
    menu.read_text.return_value = "test_text"
    menu.read_rot_type.return_value = "13"
    entry = Text("grfg_grkg", RotType.ROT13, Status.ENCRYPTED)
    facade.encrypt.return_value = entry
    manager = Manager(menu, facade)
    manager.run()

    facade.encrypt.assert_called_once_with("test_text", RotType.ROT13)
    menu.show_success.assert_called_once_with(
        f"Operacja udana: {entry.text}  {entry.status}"
    )


@pytest.mark.parametrize("text", ["", " "])
def test_encrypt_with_empty_text(menu, facade, text):
    menu.read_choice.side_effect = ["1", "0"]
    menu.read_text.return_value = text
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with("Tekst nie może być pusty")
    facade.encrypt.assert_not_called()
    menu.read_rot_type.assert_not_called()


def test_encrypt_with_invalid_rot_type(menu, facade):
    menu.read_choice.side_effect = ["1", "0"]
    menu.read_text.return_value = "trlalala"
    menu.read_rot_type.return_value = "invalid_rot_type"
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with("Nieprawidłowy wybór szyfru")
    facade.encrypt.assert_not_called()
    menu.show_success.assert_not_called()


def test_decrypt_happy_path(menu, facade):
    menu.read_choice.side_effect = ["2", "0"]
    menu.read_text.return_value = "grfg_grkg"
    menu.read_rot_type.return_value = "13"
    entry = Text("test_text", RotType.ROT13, Status.DECRYPTED)
    facade.decrypt.return_value = entry
    manager = Manager(menu, facade)
    manager.run()

    facade.decrypt.assert_called_once_with("grfg_grkg", RotType.ROT13)
    menu.show_success.assert_called_once_with(
        f"Operacja udana: {entry.text}  {entry.status}"
    )


def test_save_happy_path(menu, facade):
    menu.read_choice.side_effect = ["3", "0"]
    menu.read_filename.return_value = "fake_json.json"
    manager = Manager(menu, facade)
    manager.run()

    facade.save.assert_called_once_with("fake_json.json")
    menu.show_success.assert_called_once_with("Operacja zapisu udana")


@pytest.mark.parametrize("filename", ["", " "])
def test_save_with_empty_filename_shows_error(menu, facade, filename):
    menu.read_choice.side_effect = ["3", "0"]
    menu.read_filename.return_value = filename
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with("Nazwa pliku nie może być pusta")
    facade.save.assert_not_called()


def test_load_happy_path(menu, facade):
    menu.read_choice.side_effect = ["4", "0"]
    menu.read_filename.return_value = "fake_json.json"
    manager = Manager(menu, facade)
    manager.run()

    facade.load.assert_called_once_with("fake_json.json")
    menu.show_success.assert_called_once_with("Operacja odczytu udana")


@pytest.mark.parametrize("filename", ["", " "])
def test_load_with_empty_filename_shows_error(menu, facade, filename):
    menu.read_choice.side_effect = ["4", "0"]
    menu.read_filename.return_value = filename
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with("Nazwa pliku nie może być pusta")
    facade.load.assert_not_called()


def test_show_buffer_when_empty(menu, facade):
    menu.read_choice.side_effect = ["5", "0"]
    facade.buffer_entries = []
    manager = Manager(menu, facade)
    manager.run()

    menu.show_info.assert_called_once_with("Pusta pamięć")
    menu.show_buffer.assert_not_called()


def test_show_buffer_passes_entries(menu, facade):
    menu.read_choice.side_effect = ["5", "0"]
    entries = [
        Text("test_text", RotType.ROT13, Status.ENCRYPTED),
        Text("test", RotType.ROT47, Status.ENCRYPTED),
    ]
    facade.buffer_entries = entries
    manager = Manager(menu, facade)
    manager.run()

    menu.show_buffer.assert_called_once_with(entries)
    menu.show_info.assert_not_called()


def test_invalid_menu_choice_shows_error(menu, facade):
    menu.read_choice.side_effect = ["9", "0"]
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with("Niepoprawny wybór")
    assert facade.mock_calls == []


def test_file_handler_error_is_shown_as_message(menu, facade):
    menu.read_choice.side_effect = ["4", "0"]
    filename = menu.read_filename.return_value = "przykladowy.json"
    facade.load.side_effect = FileHandlerError(f"Nie znaleziono pliku - '{filename}'")
    manager = Manager(menu, facade)
    manager.run()

    menu.show_error.assert_called_once_with(f"Nie znaleziono pliku - '{filename}'")
    menu.show_success.assert_not_called()


@pytest.mark.parametrize("type_of_error", [EOFError, KeyboardInterrupt])
def test_interrupt_ends_session(menu, facade, type_of_error):
    menu.read_choice.side_effect = type_of_error
    manager = Manager(menu, facade)
    manager.run()

    assert menu.read_choice.call_count == 1
    menu.show_info.assert_called_once_with("Przerwane przez użytkownika")
