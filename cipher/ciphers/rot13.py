"""Implementacja szyfru ROT13.

Konkretna realizacja kontraktu `Cipher` dla wariantu ROT13 —
przesuwa litery alfabetu łacińskiego o 13 pozycji, pozostawiając
pozostałe znaki bez zmian.
"""
from .base import Cipher


class Rot13Cipher(Cipher):
    """Szyfr ROT13.

    Przesuwa każdą literę ASCII (`a-z`, `A-Z`) o 13 pozycji w obrębie
    jej zakresu, z zawijaniem (modulo 26). Znaki spoza alfabetu
    łacińskiego (cyfry, spacje, interpunkcja) pozostają nietknięte.
    ROT13 jest symetryczny — ponowne zaszyfrowanie odtwarza oryginał.
    """
    def encrypt(self, text: str) -> str:
        """Szyfruje tekst algorytmem ROT13.

        :param text: tekst wejściowy do zaszyfrowania.
        :return: tekst z literami przesuniętymi o 13 pozycji.
        """
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

    def decrypt(self, text: str) -> str:
        """Deszyfruje tekst ROT13.

        Dzięki symetrii ROT13 (przesunięcie o 13 w 26-literowym
        alfabecie) deszyfrowanie jest tożsame z szyfrowaniem, więc
        deleguje do :meth:`encrypt`.

        :param text: tekst wejściowy do odszyfrowania.
        :return: tekst odszyfrowany (oryginał).
        """
        return self.encrypt(text)

#x = Rot13Cipher()
#x.encrypt("a b")

