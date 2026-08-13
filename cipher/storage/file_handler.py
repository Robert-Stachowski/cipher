"""Warstwa storage: trwałe przechowywanie wpisów bufora w plikach JSON."""
import json
from dataclasses import asdict
from ..models.text import Text, RotType, Status
from ..exceptions import FileHandlerError
from typing import Any


class FileHandler:

    @staticmethod
    def _load_raw_json(filename: str, missing_ok: bool = False) -> list | dict:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            if missing_ok:
                return []
            raise FileHandlerError(f"Nie znaleziono pliku - '{filename}'")
        except (OSError, json.JSONDecodeError) as e:
            raise FileHandlerError(f"Nie udało się odczytać pliku - '{filename}'") from e


    def save(self, filename: str, entries: list[Text]) -> None:
        """Dopisuje wpisy do pliku JSON; tworzy plik, jeśli nie istnieje,
        rzuca FileHandlerError w przypadku uszkodzonego pliku, oraz niepoprawnej struktury danych"""
        old = self._load_raw_json(filename, missing_ok=True)

        if not isinstance(old, list):
            raise FileHandlerError(f"Niepoprawna struktura pliku - '{filename}' - {type(old).__name__}")

        dict_entries = []
        for entry in entries:
            dict_entries.append(asdict(entry))

        new_list = old + dict_entries

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(new_list, file, ensure_ascii=False)


    def read(self, filename: str) -> list[Text]:
        """Wczytuje wpisy z pliku JSON;
        rzuca FileHandlerError przy braku lub uszkodzeniu pliku oraz przy nieznanej wartości / braku klucza"""
        raw_json = self._load_raw_json(filename)

        if not isinstance(raw_json, list):
            raise FileHandlerError(f"Niepoprawna struktura pliku - {filename} - {type(raw_json).__name__}")

        raw_list = []
        try:
            for entry in raw_json:
                text, rot_type, status = entry["text"], entry["rot_type"], entry["status"]
                raw_list.append(Text(text, RotType(rot_type), Status(status)))
        except (ValueError, KeyError, TypeError) as e:
            raise FileHandlerError(f"Nieznana wartość, lub brak klucza: {filename} - {e}") from e
        return raw_list
