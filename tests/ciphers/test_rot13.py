import pytest
from cipher.ciphers.rot13 import Rot13Cipher

@pytest.mark.parametrize("text, expected", [
    ("Hello", "Uryyb"),
    ("World", "Jbeyq")
])
def test_cipher_rot_13(text, expected):
    assert Rot13Cipher()._cipher(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello", "Uryyb"),
    ("World", "Jbeyq")
])
def test_encrypt(text, expected):
    assert Rot13Cipher().encrypt(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("Uryyb", "Hello"),
    ("Jbeyq", "World"),
    ("", "")
])
def test_decrypt(text, expected):
    assert Rot13Cipher().decrypt(text) == expected

