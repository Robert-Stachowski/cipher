from ..models.text import Text, RotType, Status
import json


class FileHandler:

    def save(self, filename: str, entries: list[Text]) -> None:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                old = json.load(file)
        except FileNotFoundError:
            old = []

        dict_entries = []
        for enter in entries:
            dict_entries.append({"text": enter.text, "rot_type": enter.rot_type, "status": enter.status})

        new_list = old + dict_entries

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(new_list, file, ensure_ascii=False)


    def read(self, filename: str) -> list[Text]:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                raw_json = json.load(file)
        except FileNotFoundError as e:
            raise

        raw_list =[]

        for enter in raw_json:
            raw_list.append(Text(enter["text"], RotType(enter["rot_type"]), Status(enter["status"])))
        return raw_list

