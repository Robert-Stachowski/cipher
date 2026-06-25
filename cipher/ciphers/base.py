"""Abstrakcyjny kontrakt szyfru.

Definiuje interfejs `Cipher`, który implementują konkretne
szyfry (ROT13, ROT47). Warstwa odpowiada wyłącznie za
przekształcanie tekstu — nie wie nic o buforze, plikach ani menu.
"""
from abc import ABC, abstractmethod


class Cipher(ABC):
    """Bazowy kontrakt szyfru.

    Wymusza, by każdy szyfr udostępniał metody `encrypt` i `decrypt`
    operujące na tekście. Sama nie zawiera logiki przekształcania —
    realizują ją klasy potomne.
    """

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Szyfruje podany tekst."""
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str:
        """Deszyfruje podany tekst."""
        pass