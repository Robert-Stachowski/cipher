import pytest
from cipher.ciphers.rot47 import Rot47Cipher


@pytest.mark.parametrize("text, expected", [
    ("Hello", "w6==@"),
    ("World", "(@C=5")
])
def test_cipher_rot47(text, expected):
    assert Rot47Cipher()._cipher(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("Hello", "w6==@"),
    ("World", "(@C=5")
])
def test_encrypt(text, expected):
    assert Rot47Cipher().encrypt(text) == expected

@pytest.mark.parametrize("text, expected", [
    ("w6==@", "Hello"),
    ("(@C=5", "World"),
    ("","")
])
def test_decrypt(text, expected):
    assert Rot47Cipher().decrypt(text) == expected