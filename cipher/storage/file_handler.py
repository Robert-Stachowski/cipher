"""Warstwa storage: trwałe przechowywanie wpisów bufora w plikach JSON."""
import json
from dataclasses import asdict
from ..models.text import Text, RotType, Status
from ..exceptions import FileHandlerError


class FileHandler:

    def save(self, filename: str, entries: list[Text]) -> None:
        """Dopisuje wpisy do pliku JSON; tworzy plik, jeśli nie istnieje."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                old = json.load(file)
        except FileNotFoundError:
            old = []

        dict_entries = []
        for entry in entries:
            dict_entries.append(asdict(entry))

        new_list = old + dict_entries

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(new_list, file, ensure_ascii=False)


    def read(self, filename: str) -> list[Text]:
        """Wczytuje wpisy z pliku JSON; rzuca FileHandlerError przy braku lub uszkodzeniu pliku oraz przy nieznanej wartości / braku klucza"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                raw_json = json.load(file)
        except (OSError, json.JSONDecodeError) as e:
            raise FileHandlerError(f"Nie udało sie odczytać pliku - '{filename}'") from e

        raw_list = []
        try:
            for entry in raw_json:
                text, rot_type, status = entry["text"], entry["rot_type"], entry["status"]
                raw_list.append(Text(text, RotType(rot_type), Status(status)))
        except (ValueError, KeyError) as e:
            raise FileHandlerError(f"Nieznana wartość, lub brak klucza: {filename} - {e}") from e
        return raw_list
