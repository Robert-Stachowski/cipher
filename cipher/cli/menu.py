"""Menu — warstwa prezentacji i wejścia (CLI).

Moduł odpowiada *wyłącznie* za wyświetlanie interfejsu w terminalu oraz
czytanie surowego wejścia od użytkownika. Nie zna szyfrów, bufora ani
plików — zgodnie ze złotą zasadą architektury zależności wskazują tylko
w jedną stronę, a `Menu` jest jej najniższą niezależną warstwą.

Walidacja danych i routing komend należą do `Manager` / `CipherFacade`.
Tutaj zwracamy surowe stringi i drukujemy gotowe komunikaty.
"""
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..models.text import Text


class Menu:
    """Renderuje opcje i czyta input z terminala.

    Klasa jest bezstanowa — wszystkie metody operują na standardowym
    wejściu/wyjściu. Trzymanie jej jako instancji (a nie zbioru funkcji
    statycznych) pozwala `Manager`-owi wstrzyknąć ją jako zależność i
    łatwo podmienić/zamockować w testach.
    """

    # Pozycje menu jako pary (klawisz, etykieta) w kolejności wyświetlania.
    _OPTIONS: tuple[tuple[str, str], ...] = (
        ("1", "Szyfruj"),
        ("2", "Odszyfruj"),
        ("3", "Zapisz bufor do pliku"),
        ("4", "Wczytaj plik do bufora"),
        ("5", "Pokaż bufor"),
        ("0", "Wyjście"),
    )

    # ── Renderowanie ─────────────────────────────────────────────────────

    def show_main_menu(self) -> None:
        print("\n======== CIPHER =========\n")
        for key, label in self._OPTIONS:
            print(key, label)

    def show_buffer(self, entries: list["Text"]) -> None:
        """Wyświetla zawartość bufora"""
        print(f"\n── Bufor ({len(entries)}) ─────────────────")
        for index, entry in enumerate(entries, start=1):
            print(f"  {index}. {entry.text}  {entry.rot_type}  {entry.status}")
        print()

    # ── Komunikaty ───────────────────────────────────────────────────────

    def show_success(self, message: str) -> None:
        print(f"✔ {message}")

    def show_error(self, message: str) -> None:
        print(f"✖ {message}")

    def show_info(self, message: str) -> None:
        print(f"ℹ {message}")

    # ── Wejście ──────────────────────────────────────────────────────────

    def read_choice(self) -> str:
        """Czyta wybór z menu (surowy, bez walidacji)."""
        return input("> ").strip()

    def read_rot_type(self) -> str:
        """Pyta o wariant ROT. Zwraca surowy string (np. ``"13"``)."""
        return input("Wybierz ROT [13 / 47]: ").strip()

    def read_text(self) -> str:
        return input("Podaj tekst: ")

    def read_filename(self) -> str:
        """Pyta o nazwę pliku (bez rozszerzenia)."""
        return input("Nazwa pliku: ").strip()
