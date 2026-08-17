"""Wytwarzanie obiektów szyfrów na podstawie typu ROT."""

from typing import ClassVar

from ..models.text import RotType
from .base import Cipher
from .rot13 import Rot13Cipher
from .rot47 import Rot47Cipher


class CipherFactory:
    """Mapuje RotType na klasę Cipher."""

    _CIPHERS_MAP: ClassVar[dict] = {
        RotType.ROT13: Rot13Cipher,
        RotType.ROT47: Rot47Cipher,
    }

    @classmethod
    def create_cipher(cls, rot_type: RotType) -> Cipher:
        """Tworzy szyfr (Cipher) właściwy dla podanego typu ROT."""
        return cls._CIPHERS_MAP[rot_type]()
