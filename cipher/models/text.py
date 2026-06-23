"""Domain model for the Cipher app: the Text value object and its enums."""
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
    """Immutable value object: a piece of text with its rot type and status."""
    text: str
    rot_type: RotType
    status: Status