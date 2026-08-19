"""Manager — pętla główna CLI: routing wyboru z menu na operacje Facade."""

from collections.abc import Callable
from typing import ClassVar

from ..exceptions import FileHandlerError
from ..facade import Facade
from ..models.text import RotType, Text
from .menu import Menu


class Manager:
    _ROT_MAP: ClassVar[dict[str, RotType]] = {"13": RotType.ROT13, "47": RotType.ROT47}

    def __init__(self, menu: Menu, facade: Facade) -> None:
        self._menu = menu
        self._facade = facade
        self._running = True

    def _handle_cipher(self, operation: Callable[[str, RotType], Text]) -> None:
        """Wspólny przepływ encrypt/decrypt; ``operation`` to metoda Facade wołana na (tekst, ROT)."""
        text = self._menu.read_text()
        if not text.strip():
            self._menu.show_error("Tekst nie może być pusty")
            return
        raw_rot_type = self._menu.read_rot_type()
        rot_type = self._ROT_MAP.get(raw_rot_type)
        if rot_type is None:
            self._menu.show_error("Nieprawidłowy wybór szyfru")
            return
        entry = operation(text, rot_type)
        self._menu.show_success(f"Operacja udana: {entry.text}  {entry.status}")

    def _handle_encrypt(self) -> None:
        self._handle_cipher(self._facade.encrypt)

    def _handle_decrypt(self) -> None:
        self._handle_cipher(self._facade.decrypt)

    def _handle_save(self) -> None:
        filename = self._menu.read_filename()
        if not filename.strip():
            self._menu.show_error("Nazwa pliku nie może być pusta")
            return
        self._facade.save(filename)
        self._menu.show_success("Operacja zapisu udana")

    def _handle_load(self) -> None:
        filename = self._menu.read_filename()
        if not filename.strip():
            self._menu.show_error("Nazwa pliku nie może być pusta")
            return
        self._facade.load(filename)
        self._menu.show_success("Operacja odczytu udana")

    def _handle_show_buffer(self) -> None:
        entries = self._facade.buffer_entries
        if not entries:
            self._menu.show_info("Pusta pamięć")
            return
        self._menu.show_buffer(entries)

    def _handle_exit(self) -> None:
        self._running = False

    def run(self) -> None:
        """Pętla główna: renderuje menu, czyta wybór i uruchamia właściwy handler aż do wyjścia."""
        oper_map = {
            "1": self._handle_encrypt,
            "2": self._handle_decrypt,
            "3": self._handle_save,
            "4": self._handle_load,
            "5": self._handle_show_buffer,
            "0": self._handle_exit,
        }
        try:
            while self._running:
                self._menu.show_main_menu()
                choice = self._menu.read_choice()
                try:
                    handler = oper_map.get(choice)
                    if handler is None:
                        self._menu.show_error("Niepoprawny wybór")
                        continue
                    handler()
                except FileHandlerError as e:
                    self._menu.show_error(str(e))
        except (KeyboardInterrupt, EOFError):
            self._menu.show_info("Przerwane przez użytkownika")
        # dodatkowe zabezpieczenie: nieprzewidziany błąd kończy sesję —
        # użytkownik dostaje komunikat, traceback trafia do error.log w main()
        except Exception as e:
            self._menu.show_error(f"Nieoczekiwany błąd: {e!r}")
            raise
