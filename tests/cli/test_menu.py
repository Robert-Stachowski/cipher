import pytest

from cipher.cli.menu import Menu


@pytest.fixture
def menu():
    return Menu()


@pytest.mark.parametrize("inpt", ["1", " 1", "1\n", " 1 "])
def test_read_choice(mocker, menu, inpt):
    mocker.patch("builtins.input", return_value=inpt)
    choice = menu.read_choice()

    assert choice == "1"


@pytest.mark.parametrize(
    "inpt", ["nazwa.json", " nazwa.json", " nazwa.json ", "nazwa.json "]
)
def test_read_filename(mocker, menu, inpt):
    mocker.patch("builtins.input", return_value=inpt)
    choice = menu.read_filename()

    assert choice == "nazwa.json"


@pytest.mark.parametrize("inpt", ["abc", " abc", " abc ", "abc ", "ab c"])
def test_read_text(mocker, menu, inpt):
    mocker.patch("builtins.input", return_value=inpt)
    choice = menu.read_text()

    assert choice == inpt


@pytest.mark.parametrize("inpt", ["13", " 13", " 13 ", "13 "])
def test_read_rot_type(mocker, menu, inpt):
    mocker.patch("builtins.input", return_value=inpt)
    choice = menu.read_rot_type()

    assert choice == "13"


def test_show_success(menu, capsys):
    menu.show_success("Operacja odczytu udana")
    captured = capsys.readouterr()

    assert captured.out == "✔ Operacja odczytu udana\n"


def test_show_error(menu, capsys):
    menu.show_error("Nazwa pliku nie może być pusta")
    captured = capsys.readouterr()

    assert captured.out == "✖ Nazwa pliku nie może być pusta\n"


def test_show_info(menu, capsys):
    menu.show_info("Pusta pamięć")
    captured = capsys.readouterr()

    assert captured.out == "ℹ Pusta pamięć\n"
