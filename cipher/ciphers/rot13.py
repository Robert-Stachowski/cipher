"""Szyfr ROT13 — konkretna implementacja kontraktu Cipher."""
from .base import Cipher


class Rot13Cipher(Cipher):
    """Szyfr ROT13.
    Symetryczny — encrypt i decrypt to ta sama operacja. Działa na literach ASCII, resztę zostawia.
    """
    def _cipher(self, text: str) -> str:
        """Przesuwa litery ASCII o 13 (mod 26); nie-litery zostawia bez zmian."""
        rot13_char_list = []
        for char in text:
            if ord('a') <= ord(char) <= ord('z'):
                base = ord('a')
            elif ord('A') <= ord(char) <= ord('Z'):
                base = ord('A')
            else:
                rot13_char_list.append(char)
                continue

            char_nr = ord(char) - base
            rot13_char_nr = (char_nr + 13) % 26
            rot13_char = chr(rot13_char_nr + base)
            rot13_char_list.append(rot13_char)

        return "".join(rot13_char_list)

    def encrypt(self, text: str) -> str:
        """Szyfruje tekst algorytmem ROT13."""
        return self._cipher(text)

    def decrypt(self, text: str) -> str:
        """Deszyfruje tekst ROT13 (operacja symetryczna do szyfrowania)."""
        return self._cipher(text)

