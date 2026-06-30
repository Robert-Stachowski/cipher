"""Wytwarzanie obiektów szyfrów na podstawie typu ROT."""

from ..models.text import RotType
from .rot13 import Rot13Cipher
from .rot47 import Rot47Cipher
from .base import Cipher


class CipherFactory:
    """Mapuje RotType na współdzieloną instancję Cipher."""
    
    _ciphers_map = {
        RotType.ROT13: Rot13Cipher(),
        RotType.ROT47: Rot47Cipher()
    }

    @classmethod
    def create_cipher(cls, rot_type: RotType) -> Cipher:
        """Zwraca szyfr odpowiadający podanemu typowi ROT."""
        return cls._ciphers_map[rot_type]

