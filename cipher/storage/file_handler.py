"""Warstwa storage: trwałe przechowywanie wpisów bufora w plikach JSON."""
import json
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
            dict_entries.append({"text": entry.text, "rot_type": entry.rot_type, "status": entry.status})

        new_list = old + dict_entries

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(new_list, file, ensure_ascii=False)


    def read(self, filename: str) -> list[Text]:
        """Wczytuje wpisy z pliku JSON; rzuca FileHandlerError przy braku lub uszkodzeniu pliku."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                raw_json = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise FileHandlerError(f"Nie znaleziono pliku lub plik jest uszkodzony - '{filename}'") from e

        raw_list = []

        for entry in raw_json:
            raw_list.append(Text(entry["text"], RotType(entry["rot_type"]), Status(entry["status"])))
        return raw_list

