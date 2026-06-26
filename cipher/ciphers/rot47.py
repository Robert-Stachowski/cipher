"""Szyfr ROT47 - konkretna implementacja kontraktu Cipher"""
from .base import Cipher


class Rot47Cipher(Cipher):
    """Szyfr ROT47.
       Symetryczny — encrypt i decrypt to ta sama operacja.
       Działa na literach, cyfrach i znakach specjalnych ASCII, resztę zostawia.
    """
    def _cipher(self, text: str) -> str:
        """Przesuwa cały zakres drukowalnego ASCII o 47 (mod 94) """
        rot47_char_list = []
        for char in text:
            if ord("!") <= ord(char) <= ord("~"):
                char_nr = ord(char) - ord("!")
                rot47_char_nr = (char_nr + 47) % 94
                rot47_char = chr(rot47_char_nr + ord("!"))
                rot47_char_list.append(rot47_char)
            else:
                rot47_char_list.append(char)

        return "".join(rot47_char_list)

    def encrypt(self, text: str) -> str:
        """Szyfruje tekst algorytmem ROT47."""
        return self._cipher(text)

    def decrypt(self, text: str) -> str:
        """Deszyfruje tekst algorytmem ROT47 (operacja symetryczna do szyfrowania)."""
        return self._cipher(text)
