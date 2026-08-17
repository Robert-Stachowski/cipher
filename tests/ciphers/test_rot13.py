import pytest

from cipher.ciphers.rot13 import Rot13Cipher


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello", "Uryyb"),
        ("World", "Jbeyq"),
        ("12345", "12345"),
        ("a1b2c3", "n1o2p3"),
        ("[]^_, ", "[]^_, "),
        ("ąĄżŻ", "ąĄżŻ"),
        ("", ""),
    ],
)
def test_encrypt(text, expected):
    assert Rot13Cipher().encrypt(text) == expected


@pytest.mark.parametrize(
    "text, expected", [("Uryyb, Jbeyq!", "Hello, World!"), ("", "")]
)
def test_decrypt(text, expected):
    assert Rot13Cipher().decrypt(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "Dzień dobry, to zestaw testujący różne znaki",
        "Tu zestaw numer 2, a może 3, lub 4",
        "Lista: [], to coś innego niż słownik: {}, lub krotka: ()",
    ],
)
def test_decrypt_reverses_encrypt(text):
    rot13 = Rot13Cipher()
    assert rot13.decrypt(rot13.encrypt(text)) == text
