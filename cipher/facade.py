"""Facade — wysokopoziomowe API aplikacji: encrypt, decrypt, save, load."""
from .ciphers.factory import CipherFactory
from .core.buffer import Buffer
from .models.text import RotType, Status, Text
from .storage.file_handler import FileHandler


class Facade:
    def __init__(self, buffer: Buffer, file_handler: FileHandler) -> None:
        self._buffer = buffer
        self._file_handler = file_handler

    def encrypt(self, text: str, rot_type: RotType) -> Text:
        """Szyfruje tekst wybranym ROT-em, zapisuje wynik w buforze i go zwraca."""
        cipher = CipherFactory.create_cipher(rot_type)
        encrypted_text = cipher.encrypt(text)

        entry = Text(
            text=encrypted_text,
            rot_type=rot_type,
            status=Status.ENCRYPTED
        )
        self._buffer.add(entry)
        return entry

    def decrypt(self, text: str, rot_type: RotType) -> Text:
        """Odszyfrowuje tekst wybranym ROT-em, zapisuje wynik w buforze i go zwraca."""
        cipher = CipherFactory.create_cipher(rot_type)
        decrypted_text = cipher.decrypt(text)

        entry = Text(
            text=decrypted_text,
            rot_type=rot_type,
            status=Status.DECRYPTED
        )
        self._buffer.add(entry)
        return entry

    def save(self, filename: str) -> None:
        """Zapisuje całą zawartość bufora do pliku."""
        self._file_handler.save(filename=filename, entries=self._buffer.entries)

    def load(self, filename: str) -> None:
        """Wczytuje wpisy z pliku i dodaje je do bufora."""
        entries = self._file_handler.read(filename=filename)
        for entry in entries:
            self._buffer.add(entry)

    @property
    def buffer_entries(self) -> list[Text]:
        return self._buffer.entries
