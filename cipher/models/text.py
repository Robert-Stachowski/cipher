"""Model domeny aplikacji Cipher: obiekt-wartość Text oraz jego enumy."""
from dataclasses import dataclass
from enum import StrEnum

class RotType(StrEnum):
    ROT13 = "rot13"
    ROT47 = "rot47"

class Status(StrEnum):
    ENCRYPTED = "encrypted"
    DECRYPTED = "decrypted"


@dataclass(frozen=True)
class Text:
    """Niezmienny obiekt-wartość: tekst wraz z jego typem ROT i statusem.""
    text: str
    rot_type: RotType
    status: Status