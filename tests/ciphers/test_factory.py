import pytest
from cipher.ciphers.factory import CipherFactory
from cipher.ciphers.rot13 import Rot13Cipher
from cipher.ciphers.rot47 import Rot47Cipher
from cipher.models.text import RotType


def test_cipher13_created():
    assert isinstance(CipherFactory.create_cipher(RotType.ROT13), Rot13Cipher)

def test_cipher47_created():
    assert isinstance(CipherFactory.create_cipher(RotType.ROT47), Rot47Cipher)

