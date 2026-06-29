from ..models.text import RotType
from .rot13 import Rot13Cipher
from .rot47 import Rot47Cipher
from .base import Cipher


class CipherFactory:
    _ciphers_map = {
        RotType.ROT13: Rot13Cipher(),
        RotType.ROT47: Rot47Cipher()
    }

    @classmethod
    def create_cipher(cls, rot_type: RotType) -> Cipher:
        return cls._ciphers_map[rot_type]

