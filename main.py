import sys
import traceback
from datetime import datetime

from cipher.cli.manager import Manager
from cipher.cli.menu import Menu
from cipher.core.buffer import Buffer
from cipher.facade import Facade
from cipher.storage.file_handler import FileHandler


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        buffer = Buffer()
        filehandler = FileHandler()
        facade = Facade(buffer, filehandler)
        menu = Menu()
        manager = Manager(menu, facade)
        manager.run()
    # ostatnia bariera procesu: traceback do pliku, kod wyjścia 1
    except Exception:  # noqa: BLE001
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now().astimezone().isoformat()} ---\n")
            traceback.print_exc(file=f)
        sys.exit(1)


if __name__ == "__main__":
    main()
